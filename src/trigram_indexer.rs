use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader, Read};
use std::path::Path;
use std::time::Instant;

pub const MAX_INDEXABLE_FILE_SIZE: u64 = 10 * 1024 * 1024; // 10 MB per text file
pub const TEXT_EXTENSIONS: &[&str] = &[
    "rs", "toml", "json", "py", "js", "ts", "tsx", "jsx", "html", "css",
    "md", "txt", "yaml", "yml", "ini", "c", "cpp", "h", "hpp", "cs", "sql"
];

#[inline(always)]
pub fn make_trigram(b0: u8, b1: u8, b2: u8) -> u32 {
    ((b0.to_ascii_lowercase() as u32) << 16)
        | ((b1.to_ascii_lowercase() as u32) << 8)
        | (b2.to_ascii_lowercase() as u32)
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GrepHit {
    pub file_path: String,
    pub file_name: String,
    pub line_number: usize,
    pub line_text: String,
    pub match_start: usize,
    pub match_len: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrigramIndexedFile {
    pub id: u32,
    pub path: String,
    pub size_bytes: u64,
}

#[derive(Default, Serialize, Deserialize)]
pub struct TrigramIndex {
    pub files: Vec<TrigramIndexedFile>,
    // Map trigram (24-bit u32) -> sorted list of file IDs
    pub postings: HashMap<u32, Vec<u32>>,
    pub total_trigrams: usize,
}

impl TrigramIndex {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn is_text_file(path: &Path) -> bool {
        if let Some(ext) = path.extension().and_then(|s| s.to_str()) {
            let lower = ext.to_lowercase();
            TEXT_EXTENSIONS.contains(&lower.as_str())
        } else {
            false
        }
    }

    pub fn extract_file_trigrams(content: &[u8]) -> Vec<u32> {
        if content.len() < 3 {
            return Vec::new();
        }

        let mut set = std::collections::HashSet::with_capacity(content.len() / 2);
        for window in content.windows(3) {
            let tg = make_trigram(window[0], window[1], window[2]);
            set.insert(tg);
        }

        let mut result: Vec<u32> = set.into_iter().collect();
        result.sort_unstable();
        result
    }

    pub fn build_from_directory(root_dir: &Path, max_files: usize) -> Self {
        let mut index = TrigramIndex::new();
        if !root_dir.exists() {
            return index;
        }

        // Collect all eligible text files
        let mut file_paths = Vec::new();
        for entry in jwalk::WalkDir::new(root_dir)
            .parallelism(jwalk::Parallelism::Serial)
            .skip_hidden(true)
            .max_depth(8)
        {
            if let Ok(entry) = entry {
                if entry.file_type.is_file() {
                    let path = entry.path();
                    if Self::is_text_file(&path) {
                        if let Ok(meta) = entry.metadata() {
                            if meta.len() > 0 && meta.len() <= MAX_INDEXABLE_FILE_SIZE {
                                file_paths.push((path, meta.len()));
                                if file_paths.len() >= max_files {
                                    break;
                                }
                            }
                        }
                    }
                }
            }
        }

        // Parallel extract trigrams
        let indexed_data: Vec<(u32, String, u64, Vec<u32>)> = file_paths
            .into_par_iter()
            .enumerate()
            .filter_map(|(id, (p, size))| {
                if let Ok(mut f) = File::open(&p) {
                    let mut buf = Vec::with_capacity(size as usize);
                    if f.read_to_end(&mut buf).is_ok() {
                        let trigrams = Self::extract_file_trigrams(&buf);
                        return Some((id as u32, p.to_string_lossy().to_string(), size, trigrams));
                    }
                }
                None
            })
            .collect();

        // Assemble into inverted index
        let mut postings: HashMap<u32, Vec<u32>> = HashMap::new();
        let mut files = Vec::with_capacity(indexed_data.len());

        for (file_id, path, size, trigrams) in indexed_data {
            files.push(TrigramIndexedFile {
                id: file_id,
                path,
                size_bytes: size,
            });

            for tg in trigrams {
                postings.entry(tg).or_default().push(file_id);
            }
        }

        index.total_trigrams = postings.len();
        index.files = files;
        index.postings = postings;
        index
    }

    pub fn search_grep(
        &self,
        query: &str,
        max_hits: usize,
    ) -> (Vec<GrepHit>, u64) {
        let start_time = Instant::now();
        let trimmed = query.trim();
        if trimmed.len() < 2 {
            return (Vec::new(), 0);
        }

        let query_bytes = trimmed.as_bytes();
        let mut candidate_file_ids: Option<Vec<u32>> = None;

        // If query >= 3 bytes, use trigram intersection
        if query_bytes.len() >= 3 {
            let mut query_trigrams = Vec::new();
            for window in query_bytes.windows(3) {
                query_trigrams.push(make_trigram(window[0], window[1], window[2]));
            }

            // Sort trigrams by posting list size ascending (most selective first)
            query_trigrams.sort_by_key(|tg| self.postings.get(tg).map(|l| l.len()).unwrap_or(0));

            for tg in query_trigrams {
                if let Some(list) = self.postings.get(&tg) {
                    if let Some(ref current) = candidate_file_ids {
                        // Intersect current with list
                        let mut intersected = Vec::new();
                        let mut i = 0;
                        let mut j = 0;
                        while i < current.len() && j < list.len() {
                            if current[i] == list[j] {
                                intersected.push(current[i]);
                                i += 1;
                                j += 1;
                            } else if current[i] < list[j] {
                                i += 1;
                            } else {
                                j += 1;
                            }
                        }
                        candidate_file_ids = Some(intersected);
                    } else {
                        candidate_file_ids = Some(list.clone());
                    }

                    if candidate_file_ids.as_ref().map(|c| c.is_empty()).unwrap_or(false) {
                        break;
                    }
                } else {
                    // Trigram not in index at all -> 0 candidates!
                    return (Vec::new(), start_time.elapsed().as_millis() as u64);
                }
            }
        } else {
            // Short query (<3 chars): consider all files as candidates
            candidate_file_ids = Some((0..self.files.len() as u32).collect());
        }

        let candidates = candidate_file_ids.unwrap_or_default();
        let query_lower = trimmed.to_lowercase();
        let mut hits = Vec::new();

        // Scan candidate files from disk fresh
        for fid in candidates {
            if let Some(file_info) = self.files.get(fid as usize) {
                if let Ok(file) = File::open(&file_info.path) {
                    let reader = BufReader::new(file);
                    let file_name = Path::new(&file_info.path)
                        .file_name()
                        .and_then(|s| s.to_str())
                        .unwrap_or("")
                        .to_string();

                    for (line_idx, line_res) in reader.lines().enumerate() {
                        if let Ok(line) = line_res {
                            if let Some(pos) = line.to_lowercase().find(&query_lower) {
                                hits.push(GrepHit {
                                    file_path: file_info.path.clone(),
                                    file_name: file_name.clone(),
                                    line_number: line_idx + 1,
                                    line_text: line.trim().to_string(),
                                    match_start: pos,
                                    match_len: trimmed.len(),
                                });

                                if hits.len() >= max_hits {
                                    break;
                                }
                            }
                        }
                    }

                    if hits.len() >= max_hits {
                        break;
                    }
                }
            }
        }

        let duration_ms = start_time.elapsed().as_millis() as u64;
        (hits, duration_ms)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_trigram_generation_and_search() {
        let sample = b"fn apply_dir() { println!(\"hello\"); }";
        let trigrams = TrigramIndex::extract_file_trigrams(sample);
        assert!(!trigrams.is_empty());

        let tg_app = make_trigram(b'a', b'p', b'p');
        assert!(trigrams.contains(&tg_app));
    }

    #[test]
    fn test_trigram_in_memory_grep() {
        let unique_name = format!(
            "cleanflow_trigram_test_{}_{}",
            std::process::id(),
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_nanos()
        );
        let temp_dir = std::env::temp_dir().join(unique_name);
        let _ = std::fs::remove_dir_all(&temp_dir);
        let _ = std::fs::create_dir_all(&temp_dir);

        let f1 = temp_dir.join("main.rs");
        let f2 = temp_dir.join("config.toml");
        std::fs::write(&f1, "fn execute_search() -> bool {\n    true\n}\n").unwrap();
        std::fs::write(&f2, "[settings]\nname = \"cleanflow\"\n").unwrap();

        let index = TrigramIndex::build_from_directory(&temp_dir, 50);
        assert_eq!(index.files.len(), 2);
        assert!(index.total_trigrams > 0);

        // Search for "execute_search"
        let (hits, _ms) = index.search_grep("execute_search", 10);
        assert_eq!(hits.len(), 1);
        assert_eq!(hits[0].file_name, "main.rs");
        assert_eq!(hits[0].line_number, 1);
        assert!(hits[0].line_text.contains("execute_search"));

        // Search for "cleanflow"
        let (hits_cfg, _) = index.search_grep("cleanflow", 10);
        assert_eq!(hits_cfg.len(), 1);
        assert_eq!(hits_cfg[0].file_name, "config.toml");

        // Search for nonexistent string
        let (hits_none, _) = index.search_grep("nonexistent_symbol_12345", 10);
        assert!(hits_none.is_empty());

        let _ = std::fs::remove_dir_all(&temp_dir);
    }
}
