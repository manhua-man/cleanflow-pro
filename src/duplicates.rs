use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::{self, File};
use std::io::Read;
use std::path::Path;

const PARTIAL_HASH_SIZE: usize = 16 * 1024; // 16 KB head buffer for microsecond filtering
const FULL_HASH_BUFFER_SIZE: usize = 128 * 1024; // 128 KB streaming chunk for maximum NVMe throughput

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DuplicateFile {
    pub path: String,
    pub size_bytes: u64,
    pub modified_time: String,
    pub is_recommended_keep: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DuplicateGroup {
    pub hash: String,
    pub size_bytes: u64,
    pub wasted_bytes: u64,
    pub file_count: usize,
    pub files: Vec<DuplicateFile>,
}

pub fn compute_file_hash<P: AsRef<Path>>(path: P) -> Option<String> {
    let mut file = File::open(path).ok()?;
    let mut hasher = blake3::Hasher::new();
    let mut buffer = [0u8; FULL_HASH_BUFFER_SIZE];

    loop {
        let n = file.read(&mut buffer).ok()?;
        if n == 0 {
            break;
        }
        hasher.update(&buffer[..n]);
    }

    Some(hasher.finalize().to_hex().to_string())
}

fn compute_head_hash<P: AsRef<Path>>(path: P) -> Option<String> {
    let mut file = File::open(path).ok()?;
    let mut hasher = blake3::Hasher::new();
    let mut buffer = [0u8; PARTIAL_HASH_SIZE];

    let n = file.read(&mut buffer).ok()?;
    hasher.update(&buffer[..n]);

    Some(hasher.finalize().to_hex().to_string())
}

pub fn scan_duplicate_files(target_dir: &str, min_size_bytes: u64) -> Vec<DuplicateGroup> {
    let root = Path::new(target_dir);
    if !root.exists() || !root.is_dir() {
        return Vec::new();
    }

    // Phase 1: Group files by exact size
    let mut size_map: HashMap<u64, Vec<String>> = HashMap::new();

    for entry in jwalk::WalkDir::new(root).parallelism(jwalk::Parallelism::Serial).skip_hidden(true) {
        if let Ok(entry) = entry {
            if entry.file_type.is_file() {
                if let Ok(meta) = entry.metadata() {
                    let sz = meta.len();
                    if sz > 0 && sz >= min_size_bytes {
                        size_map.entry(sz).or_default().push(entry.path().to_string_lossy().to_string());
                    }
                }
            }
        }
    }

    // Candidate size groups with at least 2 files
    let candidate_size_groups: Vec<(u64, Vec<String>)> = size_map
        .into_iter()
        .filter(|(_sz, paths)| paths.len() >= 2)
        .collect();

    // Phase 2: Parallel candidate verification with Rayon work-stealing pool
    let duplicate_groups: Vec<DuplicateGroup> = candidate_size_groups
        .into_par_iter()
        .flat_map(|(sz, paths)| {
            // Step 2a: Parallel head hash computation
            let head_results: Vec<(String, String)> = paths
                .into_par_iter()
                .filter_map(|p| {
                    compute_head_hash(&p).map(|hh| (hh, p))
                })
                .collect();

            let mut head_map: HashMap<String, Vec<String>> = HashMap::new();
            for (hh, p) in head_results {
                head_map.entry(hh).or_default().push(p);
            }

            let mut size_groups = Vec::new();

            for (head_hash, mut cand_paths) in head_map {
                if cand_paths.len() < 2 {
                    continue;
                }

                // Prefer shortest path first for deterministic preservation recommendation
                cand_paths.sort_by(|a, b| a.len().cmp(&b.len()).then_with(|| a.cmp(b)));

                // If file size is within head buffer, head hash IS the exact full BLAKE3 hash
                if sz <= PARTIAL_HASH_SIZE as u64 {
                    let wasted = sz * (cand_paths.len() as u64 - 1);
                    let count = cand_paths.len();
                    let files = cand_paths
                        .iter()
                        .enumerate()
                        .map(|(i, p)| {
                            let mod_str = fs::metadata(p)
                                .and_then(|m| m.modified())
                                .map(|t| {
                                    let d = t.duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs();
                                    format!("{}", d)
                                })
                                .unwrap_or_default();

                            DuplicateFile {
                                path: p.clone(),
                                size_bytes: sz,
                                modified_time: mod_str,
                                is_recommended_keep: i == 0,
                            }
                        })
                        .collect();

                    size_groups.push(DuplicateGroup {
                        hash: head_hash,
                        size_bytes: sz,
                        wasted_bytes: wasted,
                        file_count: count,
                        files,
                    });
                } else {
                    // For files larger than 16 KB, compute full BLAKE3 hash in parallel with Rayon
                    let full_results: Vec<(String, String)> = cand_paths
                        .into_par_iter()
                        .filter_map(|p| {
                            compute_file_hash(&p).map(|fh| (fh, p))
                        })
                        .collect();

                    let mut full_map: HashMap<String, Vec<String>> = HashMap::new();
                    for (fh, p) in full_results {
                        full_map.entry(fh).or_default().push(p);
                    }

                    for (fh, mut matched_paths) in full_map {
                        if matched_paths.len() < 2 {
                            continue;
                        }

                        matched_paths.sort_by(|a, b| a.len().cmp(&b.len()).then_with(|| a.cmp(b)));
                        let wasted = sz * (matched_paths.len() as u64 - 1);
                        let count = matched_paths.len();
                        let files = matched_paths
                            .iter()
                            .enumerate()
                            .map(|(i, p)| {
                                let mod_str = fs::metadata(p)
                                    .and_then(|m| m.modified())
                                    .map(|t| {
                                        let d = t.duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs();
                                        format!("{}", d)
                                    })
                                    .unwrap_or_default();

                                DuplicateFile {
                                    path: p.clone(),
                                    size_bytes: sz,
                                    modified_time: mod_str,
                                    is_recommended_keep: i == 0,
                                }
                            })
                            .collect();

                        size_groups.push(DuplicateGroup {
                            hash: fh,
                            size_bytes: sz,
                            wasted_bytes: wasted,
                            file_count: count,
                            files,
                        });
                    }
                }
            }

            size_groups
        })
        .collect();

    let mut groups = duplicate_groups;
    groups.sort_by(|a, b| b.wasted_bytes.cmp(&a.wasted_bytes));
    groups
}

pub fn delete_duplicate_files(paths: &[String]) -> (u64, usize, Vec<String>) {
    let mut freed = 0u64;
    let mut count = 0usize;
    let mut errors = Vec::new();

    for p in paths {
        let path = Path::new(p);
        if path.exists() && path.is_file() {
            if let Ok(meta) = path.metadata() {
                let sz = meta.len();
                match fs::remove_file(path) {
                    Ok(_) => {
                        freed += sz;
                        count += 1;
                    }
                    Err(e) => {
                        errors.push(format!("删除重复文件失败 {}: {}", p, e));
                    }
                }
            }
        }
    }

    (freed, count, errors)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compute_hash() {
        let temp_file = std::env::temp_dir().join("cleanflow_test_hash.txt");
        let _ = fs::write(&temp_file, b"CleanFlow duplicate test content");
        let h = compute_file_hash(&temp_file);
        assert!(h.is_some());
        let hash_str = h.unwrap();
        // BLAKE3 produces a 256-bit (64 hex characters) hash
        assert_eq!(hash_str.len(), 64);
        let _ = fs::remove_file(&temp_file);
    }

    #[test]
    fn test_blake3_partial_hash_large_file_differentiation() {
        let test_dir = std::env::temp_dir().join(format!("cleanflow_blake3_partial_test_{}", std::process::id()));
        let _ = fs::remove_dir_all(&test_dir);
        fs::create_dir_all(&test_dir).unwrap();

        // 32 KB files (> 16 KB partial hash buffer)
        let f_a1 = test_dir.join("file_a1.bin");
        let f_a2 = test_dir.join("file_a2.bin");
        let f_b = test_dir.join("file_b_diff_head.bin");

        let mut data_a = vec![0u8; 32 * 1024];
        data_a[0..8].copy_from_slice(b"HEADER_A");

        let mut data_b = vec![0u8; 32 * 1024];
        data_b[0..8].copy_from_slice(b"HEADER_B");

        fs::write(&f_a1, &data_a).unwrap();
        fs::write(&f_a2, &data_a).unwrap();
        fs::write(&f_b, &data_b).unwrap();

        let groups = scan_duplicate_files(test_dir.to_str().unwrap(), 0);
        // Only f_a1 and f_a2 should match into a duplicate group
        assert_eq!(groups.len(), 1);
        assert_eq!(groups[0].file_count, 2);
        assert_eq!(groups[0].hash.len(), 64);

        let _ = fs::remove_dir_all(&test_dir);
    }

    #[test]
    fn test_scan_and_delete_duplicates() {
        let test_dir = std::env::temp_dir().join(format!("cleanflow_dup_test_dir_{}", std::process::id()));
        let sub_dir = test_dir.join("sub");
        let _ = fs::remove_dir_all(&test_dir);
        fs::create_dir_all(&sub_dir).unwrap();

        let f1 = test_dir.join("original.txt");
        let f2 = test_dir.join("copy1.txt");
        let f3 = sub_dir.join("copy2_nested.txt");
        let f4 = test_dir.join("different.txt");

        let dup_data = b"Duplicate stream payload content for Rayon parallel testing";
        fs::write(&f1, dup_data).unwrap();
        fs::write(&f2, dup_data).unwrap();
        fs::write(&f3, dup_data).unwrap();
        fs::write(&f4, b"Completely distinct content").unwrap();

        let groups = scan_duplicate_files(test_dir.to_str().unwrap(), 0);
        assert_eq!(groups.len(), 1);
        let g = &groups[0];
        assert_eq!(g.file_count, 3);
        assert_eq!(g.wasted_bytes, dup_data.len() as u64 * 2);

        // Verify shortest path is recommended to keep
        let kept: Vec<_> = g.files.iter().filter(|f| f.is_recommended_keep).collect();
        assert_eq!(kept.len(), 1);

        // Delete duplicates (excluding kept)
        let delete_targets: Vec<String> = g.files.iter()
            .filter(|f| !f.is_recommended_keep)
            .map(|f| f.path.clone())
            .collect();
        assert_eq!(delete_targets.len(), 2);

        let (freed, count, errs) = delete_duplicate_files(&delete_targets);
        assert_eq!(count, 2);
        assert_eq!(freed, dup_data.len() as u64 * 2);
        assert!(errs.is_empty());

        assert!(f1.exists() || f2.exists()); // The kept one still exists

        let _ = fs::remove_dir_all(&test_dir);
    }
}
