use std::fs;
use std::path::Path;

#[derive(Debug, Default)]
pub struct CleanResult {
    pub bytes_freed: u64,
    pub files_deleted: u64,
    pub errors: Vec<String>,
}

pub fn clear_directory_contents<P: AsRef<Path>>(path: P) -> CleanResult {
    let mut result = CleanResult::default();
    let p = path.as_ref();
    if !p.exists() || !p.is_dir() {
        return result;
    }

    if let Ok(entries) = fs::read_dir(p) {
        for entry in entries.flatten() {
            let item_path = entry.path();
            if item_path.is_file() || item_path.is_symlink() {
                if let Ok(meta) = item_path.metadata() {
                    let len = meta.len();
                    match fs::remove_file(&item_path) {
                        Ok(_) => {
                            result.bytes_freed += len;
                            result.files_deleted += 1;
                        }
                        Err(e) => {
                            result.errors.push(format!("无法删除文件 {}: {}", item_path.display(), e));
                        }
                    }
                }
            } else if item_path.is_dir() {
                // Measure size before removal
                let (dir_size, dir_files) = crate::scanner::calculate_path_stats(&item_path);
                match fs::remove_dir_all(&item_path) {
                    Ok(_) => {
                        result.bytes_freed += dir_size;
                        result.files_deleted += dir_files;
                    }
                    Err(e) => {
                        result.errors.push(format!("无法删除目录 {}: {}", item_path.display(), e));
                    }
                }
            }
        }
    }

    result
}

pub fn remove_directory<P: AsRef<Path>>(path: P) -> CleanResult {
    let mut result = CleanResult::default();
    let p = path.as_ref();
    if !p.exists() {
        return result;
    }

    let (dir_size, dir_files) = crate::scanner::calculate_path_stats(p);
    match fs::remove_dir_all(p) {
        Ok(_) => {
            result.bytes_freed = dir_size;
            result.files_deleted = dir_files;
        }
        Err(e) => {
            result.errors.push(format!("删除目录失败 {}: {}", p.display(), e));
        }
    }

    result
}

pub fn delete_single_file<P: AsRef<Path>>(path: P) -> CleanResult {
    let mut result = CleanResult::default();
    let p = path.as_ref();
    if !p.exists() || !p.is_file() {
        return result;
    }

    if let Ok(meta) = p.metadata() {
        let len = meta.len();
        match fs::remove_file(p) {
            Ok(_) => {
                result.bytes_freed = len;
                result.files_deleted = 1;
            }
            Err(e) => {
                result.errors.push(format!("删除文件失败 {}: {}", p.display(), e));
            }
        }
    }

    result
}
