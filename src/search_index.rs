use crate::mft_scanner::{list_available_volumes, read_volume_mft_stream, reconstruct_paths, VolumeInfo};
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::path::{Path, PathBuf};
use std::time::{Instant, SystemTime};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CompactFileEntry {
    pub id: u64,
    pub name: String,
    pub path: String,
    pub size_bytes: u64,
    pub is_dir: bool,
    pub modified_timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VolumeIndex {
    pub drive_letter: char,
    pub label: String,
    pub fs_type: String,
    pub is_mft_accelerated: bool,
    pub last_indexed_epoch: u64,
    pub duration_ms: u64,
    pub entries: Vec<CompactFileEntry>,
}

fn get_index_storage_dir() -> PathBuf {
    let base = if let Ok(local_app_data) = std::env::var("LOCALAPPDATA") {
        PathBuf::from(local_app_data).join("CleanFlow").join("indexes")
    } else {
        std::env::temp_dir().join("cleanflow_indexes")
    };
    let _ = std::fs::create_dir_all(&base);
    base
}

fn get_index_file_path(drive_letter: char) -> PathBuf {
    get_index_storage_dir().join(format!("index_{}.json", drive_letter))
}

impl VolumeIndex {
    pub fn build_for_volume(vol: &VolumeInfo, fallback_crawl_depth: Option<usize>) -> Self {
        let start_time = Instant::now();

        // 1. Try MFT direct stream reading first
        if vol.is_ntfs {
            if let Ok(raw_entries) = read_volume_mft_stream(vol.drive_letter) {
                let resolved = reconstruct_paths(vol.drive_letter, &raw_entries);
                let entries: Vec<CompactFileEntry> = resolved
                    .into_iter()
                    .map(|(path, is_dir, frn, ts)| {
                        let name = Path::new(&path)
                            .file_name()
                            .and_then(|n| n.to_str())
                            .unwrap_or("")
                            .to_string();
                        CompactFileEntry {
                            id: frn,
                            name,
                            path,
                            size_bytes: 0,
                            is_dir,
                            modified_timestamp: ts,
                        }
                    })
                    .collect();

                let duration_ms = start_time.elapsed().as_millis() as u64;
                let epoch = SystemTime::now()
                    .duration_since(SystemTime::UNIX_EPOCH)
                    .unwrap_or_default()
                    .as_secs();

                return VolumeIndex {
                    drive_letter: vol.drive_letter,
                    label: vol.label.clone(),
                    fs_type: vol.fs_type.clone(),
                    is_mft_accelerated: true,
                    last_indexed_epoch: epoch,
                    duration_ms,
                    entries,
                };
            }
        }

        // 2. Fallback: Fast multi-threaded parallel directory crawl
        let mut entries = Vec::new();
        let mut seen_paths = std::collections::HashSet::new();
        let root_path = PathBuf::from(&vol.root_path);
        let max_depth = fallback_crawl_depth.unwrap_or(6);

        let mut crawl_roots = vec![(root_path, max_depth)];
        if vol.drive_letter == 'C' {
            if let Ok(user_profile) = std::env::var("USERPROFILE") {
                let up_path = PathBuf::from(user_profile);
                if up_path.exists() {
                    crawl_roots.push((up_path, 9));
                }
            }
        }

        let mut id_counter = 1u64;
        for (dir_root, depth) in crawl_roots {
            if dir_root.exists() {
                for entry in jwalk::WalkDir::new(&dir_root)
                    .skip_hidden(false)
                    .max_depth(depth)
                {
                    if let Ok(entry) = entry {
                        let path_str = entry.path().to_string_lossy().to_string();
                        if !seen_paths.insert(path_str.clone()) {
                            continue;
                        }

                        let is_dir = entry.file_type.is_dir();
                        let name = entry.file_name().to_string_lossy().to_string();
                        let meta = entry.metadata().ok();
                        let size_bytes = meta.as_ref().map(|m| m.len()).unwrap_or(0);
                        let modified_ts = meta
                            .and_then(|m| m.modified().ok())
                            .and_then(|t| t.duration_since(SystemTime::UNIX_EPOCH).ok())
                            .map(|d| d.as_secs())
                            .unwrap_or(0);

                        entries.push(CompactFileEntry {
                            id: id_counter,
                            name,
                            path: path_str,
                            size_bytes,
                            is_dir,
                            modified_timestamp: modified_ts,
                        });
                        id_counter += 1;
                    }
                }
            }
        }

        let duration_ms = start_time.elapsed().as_millis() as u64;
        let epoch = SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();

        VolumeIndex {
            drive_letter: vol.drive_letter,
            label: vol.label.clone(),
            fs_type: vol.fs_type.clone(),
            is_mft_accelerated: false,
            last_indexed_epoch: epoch,
            duration_ms,
            entries,
        }
    }

    pub fn save_to_disk(&self) -> Result<PathBuf, String> {
        let path = get_index_file_path(self.drive_letter);
        let file = File::create(&path).map_err(|e| format!("无法创建索引缓存文件: {}", e))?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, self)
            .map_err(|e| format!("序列化索引失败: {}", e))?;
        Ok(path)
    }

    pub fn load_from_disk(drive_letter: char) -> Option<Self> {
        let path = get_index_file_path(drive_letter);
        if !path.exists() {
            return None;
        }
        let file = File::open(&path).ok()?;
        let reader = BufReader::new(file);
        serde_json::from_reader(reader).ok()
    }
}

pub fn get_or_build_all_indexes(fallback_depth: Option<usize>) -> Vec<VolumeIndex> {
    let volumes = list_available_volumes();
    volumes
        .into_iter()
        .map(|vol| {
            if let Some(cached) = VolumeIndex::load_from_disk(vol.drive_letter) {
                // If cached within 24 hours, reuse cache
                let now = SystemTime::now()
                    .duration_since(SystemTime::UNIX_EPOCH)
                    .unwrap_or_default()
                    .as_secs();
                if now.saturating_sub(cached.last_indexed_epoch) < 86400 && !cached.entries.is_empty() {
                    return cached;
                }
            }
            let fresh = VolumeIndex::build_for_volume(&vol, fallback_depth);
            let _ = fresh.save_to_disk();
            fresh
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_volume_index_lifecycle() {
        let vol = VolumeInfo {
            drive_letter: 'C',
            root_path: "C:\\".to_string(),
            label: "Test".to_string(),
            fs_type: "NTFS".to_string(),
            serial_number: 1234,
            is_ntfs: true,
        };

        // Shallow crawl for fast unit testing
        let idx = VolumeIndex::build_for_volume(&vol, Some(1));
        assert_eq!(idx.drive_letter, 'C');
        assert!(!idx.entries.is_empty(), "C: root shallow crawl should have entries");

        let save_res = idx.save_to_disk();
        assert!(save_res.is_ok());

        let loaded = VolumeIndex::load_from_disk('C');
        assert!(loaded.is_some());
        let l = loaded.unwrap();
        assert_eq!(l.entries.len(), idx.entries.len());
    }
}
