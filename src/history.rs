use serde::{Deserialize, Serialize};
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::{OnceLock, RwLock};
use std::time::{SystemTime, UNIX_EPOCH};

const MAX_RECENT_FILES: usize = 50;
const MAX_QUERY_HISTORY: usize = 30;
const HISTORY_FILE_NAME: &str = "cleanflow_history.json";

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RecentFileItem {
    pub path: String,
    pub name: String,
    pub is_dir: bool,
    pub timestamp: u64,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct PersistentHistoryData {
    pub recent_files: Vec<RecentFileItem>,
    pub recent_queries: Vec<String>,
}

pub struct HistoryManager {
    storage_path: PathBuf,
    data: RwLock<PersistentHistoryData>,
}

impl HistoryManager {
    pub fn new() -> Self {
        let storage_path = PathBuf::from(HISTORY_FILE_NAME);
        let data = if storage_path.exists() {
            match fs::read_to_string(&storage_path) {
                Ok(content) => serde_json::from_str(&content).unwrap_or_default(),
                Err(_) => PersistentHistoryData::default(),
            }
        } else {
            PersistentHistoryData::default()
        };

        Self {
            storage_path,
            data: RwLock::new(data),
        }
    }

    pub fn record_file(&self, path_str: &str) {
        if path_str.trim().is_empty() {
            return;
        }

        let p = Path::new(path_str);
        let name = p
            .file_name()
            .and_then(|n| n.to_str())
            .unwrap_or(path_str)
            .to_string();
        let is_dir = p.is_dir();
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_secs())
            .unwrap_or(0);

        let mut lock = match self.data.write() {
            Ok(g) => g,
            Err(p) => p.into_inner(),
        };

        // Deduplicate
        lock.recent_files.retain(|f| !f.path.eq_ignore_ascii_case(path_str));

        // Insert at beginning
        lock.recent_files.insert(
            0,
            RecentFileItem {
                path: path_str.to_string(),
                name,
                is_dir,
                timestamp: now,
            },
        );

        if lock.recent_files.len() > MAX_RECENT_FILES {
            lock.recent_files.truncate(MAX_RECENT_FILES);
        }

        self.save_locked(&lock);
    }

    pub fn get_recent_files(&self, limit: usize) -> Vec<RecentFileItem> {
        let lock = match self.data.read() {
            Ok(g) => g,
            Err(p) => p.into_inner(),
        };

        lock.recent_files.iter().take(limit).cloned().collect()
    }

    pub fn record_query(&self, query: &str) {
        let trimmed = query.trim();
        if trimmed.is_empty() {
            return;
        }

        let mut lock = match self.data.write() {
            Ok(g) => g,
            Err(p) => p.into_inner(),
        };

        lock.recent_queries.retain(|q| !q.eq_ignore_ascii_case(trimmed));
        lock.recent_queries.insert(0, trimmed.to_string());

        if lock.recent_queries.len() > MAX_QUERY_HISTORY {
            lock.recent_queries.truncate(MAX_QUERY_HISTORY);
        }

        self.save_locked(&lock);
    }

    pub fn get_recent_queries(&self, limit: usize) -> Vec<String> {
        let lock = match self.data.read() {
            Ok(g) => g,
            Err(p) => p.into_inner(),
        };

        lock.recent_queries.iter().take(limit).cloned().collect()
    }

    fn save_locked(&self, data: &PersistentHistoryData) {
        if let Ok(json) = serde_json::to_string_pretty(data) {
            let _ = fs::write(&self.storage_path, json);
        }
    }
}

static GLOBAL_HISTORY: OnceLock<HistoryManager> = OnceLock::new();

pub fn get_global_history() -> &'static HistoryManager {
    GLOBAL_HISTORY.get_or_init(HistoryManager::new)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_record_file_and_query() {
        let mgr = HistoryManager::new();
        mgr.record_query("calc");
        mgr.record_query("cargo");
        let q = mgr.get_recent_queries(5);
        assert_eq!(q[0], "cargo");
        assert_eq!(q[1], "calc");

        mgr.record_file("C:\\Windows\\notepad.exe");
        let f = mgr.get_recent_files(5);
        assert!(!f.is_empty());
        assert_eq!(f[0].name, "notepad.exe");
    }
}
