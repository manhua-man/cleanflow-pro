use md5::{Digest, Md5};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::{self, File};
use std::io::Read;
use std::path::Path;

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

fn compute_file_hash<P: AsRef<Path>>(path: P) -> Option<String> {
    let mut file = File::open(path).ok()?;
    let mut hasher = Md5::new();
    let mut buffer = [0u8; 8192];

    loop {
        let n = file.read(&mut buffer).ok()?;
        if n == 0 {
            break;
        }
        hasher.update(&buffer[..n]);
    }

    Some(hex::encode(hasher.finalize()))
}

fn compute_head_hash<P: AsRef<Path>>(path: P) -> Option<String> {
    let mut file = File::open(path).ok()?;
    let mut hasher = Md5::new();
    let mut buffer = [0u8; 4096];

    let n = file.read(&mut buffer).ok()?;
    if n == 0 {
        return None;
    }
    hasher.update(&buffer[..n]);

    Some(hex::encode(hasher.finalize()))
}

pub fn scan_duplicate_files(target_dir: &str, min_size_bytes: u64) -> Vec<DuplicateGroup> {
    let root = Path::new(target_dir);
    if !root.exists() || !root.is_dir() {
        return Vec::new();
    }

    // Phase 1: Group files by exact size
    let mut size_map: HashMap<u64, Vec<String>> = HashMap::new();

    for entry in jwalk::WalkDir::new(root).skip_hidden(true) {
        if let Ok(entry) = entry {
            if entry.file_type.is_file() {
                if let Ok(meta) = entry.metadata() {
                    let sz = meta.len();
                    if sz >= min_size_bytes {
                        size_map.entry(sz).or_default().push(entry.path().to_string_lossy().to_string());
                    }
                }
            }
        }
    }

    // Phase 2: For candidates with identical size, compute head hash then full hash
    let mut full_hash_map: HashMap<(u64, String), Vec<String>> = HashMap::new();

    for (sz, paths) in size_map {
        if paths.len() < 2 {
            continue;
        }

        // Head hash check
        let mut head_map: HashMap<String, Vec<String>> = HashMap::new();
        for p in paths {
            if let Some(hh) = compute_head_head_opt(&p) {
                head_map.entry(hh).or_default().push(p);
            }
        }

        for (_hh, cand_paths) in head_map {
            if cand_paths.len() < 2 {
                continue;
            }

            for p in cand_paths {
                if let Some(fh) = compute_file_hash(&p) {
                    full_hash_map.entry((sz, fh)).or_default().push(p);
                }
            }
        }
    }

    // Phase 3: Construct DuplicateGroup results
    let mut groups = Vec::new();

    for ((sz, hash), paths) in full_hash_map {
        if paths.len() < 2 {
            continue;
        }

        let mut files = Vec::new();
        for (i, p) in paths.iter().enumerate() {
            let mod_str = fs::metadata(p)
                .and_then(|m| m.modified())
                .map(|t| {
                    let d = t.duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs();
                    format!("{}", d)
                })
                .unwrap_or_default();

            // Recommend keeping the first one (or shortest path)
            files.push(DuplicateFile {
                path: p.clone(),
                size_bytes: sz,
                modified_time: mod_str,
                is_recommended_keep: i == 0,
            });
        }

        let wasted = sz * (paths.len() as u64 - 1);
        let count = files.len();

        groups.push(DuplicateGroup {
            hash,
            size_bytes: sz,
            wasted_bytes: wasted,
            file_count: count,
            files,
        });
    }

    groups.sort_by(|a, b| b.wasted_bytes.cmp(&a.wasted_bytes));
    groups
}

fn compute_head_head_opt(path: &str) -> Option<String> {
    compute_head_hash(path)
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
        let _ = fs::remove_file(&temp_file);
    }
}
