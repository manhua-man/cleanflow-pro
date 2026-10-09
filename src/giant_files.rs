use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use std::time::SystemTime;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GiantFileItem {
    pub path: String,
    pub name: String,
    pub size_bytes: u64,
    pub extension: String,
    pub category: String,
    pub modified_timestamp: u64,
}

pub fn scan_giant_files(min_size_bytes: u64, max_results: usize) -> Vec<GiantFileItem> {
    let mut root_dirs = Vec::new();

    // Prioritize user profile directories where giant files accumulate
    if let Ok(user_profile) = std::env::var("USERPROFILE") {
        let p = PathBuf::from(user_profile);
        root_dirs.push(p);
    }

    let mut giant_files: Vec<GiantFileItem> = Vec::new();

    for root in root_dirs {
        if !root.exists() {
            continue;
        }

        // Parallel or fast walkdir, skip AppData\Local\Packages or Windows temp system locks if needed
        for entry in jwalk::WalkDir::new(&root)
            .skip_hidden(false)
            .max_depth(6)
        {
            if let Ok(entry) = entry {
                if entry.file_type.is_file() {
                    if let Ok(meta) = entry.metadata() {
                        let len = meta.len();
                        if len >= min_size_bytes {
                            let path = entry.path();
                            let ext = path
                                .extension()
                                .and_then(|s| s.to_str())
                                .unwrap_or("")
                                .to_lowercase();
                            let category = categorize_extension(&ext);
                            let file_name = entry.file_name().to_string_lossy().to_string();

                            let modified_ts = meta
                                .modified()
                                .unwrap_or(SystemTime::UNIX_EPOCH)
                                .duration_since(SystemTime::UNIX_EPOCH)
                                .map(|d| d.as_secs())
                                .unwrap_or(0);

                            giant_files.push(GiantFileItem {
                                path: path.to_string_lossy().to_string(),
                                name: file_name,
                                size_bytes: len,
                                extension: ext,
                                category,
                                modified_timestamp: modified_ts,
                            });
                        }
                    }
                }
            }
        }
    }

    // Sort descending by size
    giant_files.sort_by(|a, b| b.size_bytes.cmp(&a.size_bytes));

    if giant_files.len() > max_results {
        giant_files.truncate(max_results);
    }

    giant_files
}

pub fn categorize_extension(ext: &str) -> String {
    match ext {
        "vmdk" | "vhdx" | "vdi" | "qcow2" | "img" | "iso" => "VirtualDisk".to_string(),
        "db" | "vscdb" | "sqlite" | "sqlite3" | "mdf" | "ldf" => "Database".to_string(),
        "zip" | "rar" | "7z" | "tar" | "gz" | "tgz" | "unitypackage" => "Archive".to_string(),
        "bin" | "safetensors" | "gguf" | "onnx" | "pt" | "pth" | "ckpt" => "AIModel".to_string(),
        "hprof" | "dmp" | "dump" | "log" | "crash" => "DumpLog".to_string(),
        "mp4" | "mkv" | "mov" | "avi" | "flac" | "wav" => "Media".to_string(),
        "exe" | "msi" => "Executable".to_string(),
        _ => "Other".to_string(),
    }
}
