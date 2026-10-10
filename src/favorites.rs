// CleanFlow Pro - Favorite Folders & Short Aliases Manager
// Strictly Zero Emoji in all comments, logs and code.

use serde::{Deserialize, Serialize};
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::{OnceLock, RwLock};
use std::time::SystemTime;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct FavoriteFolder {
    pub id: String,
    pub path: String,
    pub name: String,
    pub alias: Option<String>,
    pub created_at: String,
    pub pinned: bool,
}

#[derive(Debug)]
pub struct FavoriteManager {
    favorites: Vec<FavoriteFolder>,
    storage_path: PathBuf,
}

impl FavoriteManager {
    pub fn new(storage_path: PathBuf) -> Self {
        let mut mgr = Self {
            favorites: Vec::new(),
            storage_path,
        };
        mgr.load();
        mgr
    }

    fn current_timestamp_str() -> String {
        let now = SystemTime::now();
        let dur = now.duration_since(SystemTime::UNIX_EPOCH).unwrap_or_default();
        let secs = dur.as_secs();
        let days = secs / 86400;
        let rem_secs = secs % 86400;
        let hours = rem_secs / 3600;
        let mins = (rem_secs % 3600) / 60;
        let s = rem_secs % 60;
        format!("{:04}d {:02}:{:02}:{:02}", days, hours, mins, s)
    }

    pub fn load(&mut self) {
        if !self.storage_path.exists() {
            return;
        }
        if let Ok(content) = fs::read_to_string(&self.storage_path) {
            if let Ok(list) = serde_json::from_str::<Vec<FavoriteFolder>>(&content) {
                self.favorites = list;
            }
        }
    }

    pub fn save(&self) {
        if let Ok(json_str) = serde_json::to_string_pretty(&self.favorites) {
            let tmp_path = self.storage_path.with_extension("tmp");
            if fs::write(&tmp_path, json_str).is_ok() {
                let _ = fs::rename(&tmp_path, &self.storage_path);
            }
        }
    }

    pub fn list_all(&self) -> Vec<FavoriteFolder> {
        self.favorites.clone()
    }

    pub fn is_favorite(&self, path: &str) -> bool {
        let norm_path = path.trim_end_matches(['\\', '/']).to_lowercase();
        self.favorites.iter().any(|f| f.path.trim_end_matches(['\\', '/']).to_lowercase() == norm_path)
    }

    pub fn get_by_alias(&self, alias: &str) -> Option<FavoriteFolder> {
        let clean = alias.trim().to_lowercase();
        if clean.is_empty() {
            return None;
        }
        self.favorites.iter().find(|f| {
            f.alias.as_deref().map(|a| a.trim().to_lowercase()) == Some(clean.clone())
        }).cloned()
    }

    pub fn find_by_query(&self, q: &str) -> Vec<FavoriteFolder> {
        let q_clean = q.trim().to_lowercase();
        if q_clean.is_empty() {
            return self.favorites.clone();
        }
        self.favorites.iter().filter(|f| {
            let name_match = f.name.to_lowercase().contains(&q_clean);
            let path_match = f.path.to_lowercase().contains(&q_clean);
            let alias_match = f.alias.as_deref().map(|a| a.to_lowercase().contains(&q_clean)).unwrap_or(false);
            name_match || path_match || alias_match
        }).cloned().collect()
    }

    pub fn add(&mut self, path: &str, custom_name: Option<&str>, alias: Option<&str>) -> FavoriteFolder {
        let clean_path = path.trim_end_matches(['\\', '/']).to_string();
        let norm_path = clean_path.to_lowercase();

        // Check if already exists
        if let Some(pos) = self.favorites.iter().position(|f| f.path.trim_end_matches(['\\', '/']).to_lowercase() == norm_path) {
            let item = &mut self.favorites[pos];
            if let Some(n) = custom_name {
                if !n.trim().is_empty() {
                    item.name = n.trim().to_string();
                }
            }
            if let Some(a) = alias {
                let clean_a = a.trim();
                item.alias = if clean_a.is_empty() { None } else { Some(clean_a.to_lowercase()) };
            }
            let res = item.clone();
            self.save();
            return res;
        }

        let default_name = Path::new(&clean_path)
            .file_name()
            .and_then(|n| n.to_str())
            .unwrap_or(&clean_path)
            .to_string();

        let final_name = match custom_name {
            Some(n) if !n.trim().is_empty() => n.trim().to_string(),
            _ => default_name,
        };

        let final_alias = alias.and_then(|a| {
            let clean = a.trim();
            if clean.is_empty() { None } else { Some(clean.to_lowercase()) }
        });

        let id = format!("{:x}", md5_hash(&format!("{}:{}", clean_path, Self::current_timestamp_str())));

        let entry = FavoriteFolder {
            id,
            path: clean_path,
            name: final_name,
            alias: final_alias,
            created_at: Self::current_timestamp_str(),
            pinned: false,
        };

        self.favorites.push(entry.clone());
        self.save();
        entry
    }

    pub fn remove(&mut self, path_or_id: &str) -> bool {
        let clean = path_or_id.trim_end_matches(['\\', '/']).to_lowercase();
        let prev_len = self.favorites.len();
        self.favorites.retain(|f| {
            f.id != path_or_id && f.path.trim_end_matches(['\\', '/']).to_lowercase() != clean
        });
        let removed = self.favorites.len() < prev_len;
        if removed {
            self.save();
        }
        removed
    }

    pub fn update_alias(&mut self, path_or_id: &str, alias: Option<&str>) -> bool {
        let clean = path_or_id.trim_end_matches(['\\', '/']).to_lowercase();
        let clean_alias = alias.and_then(|a| {
            let s = a.trim();
            if s.is_empty() { None } else { Some(s.to_lowercase()) }
        });

        for item in &mut self.favorites {
            if item.id == path_or_id || item.path.trim_end_matches(['\\', '/']).to_lowercase() == clean {
                item.alias = clean_alias;
                self.save();
                return true;
            }
        }
        false
    }
}

fn md5_hash(data: &str) -> u64 {
    // Lightweight 64-bit FNV-1a hash for ID generation
    let mut hash: u64 = 0xcbf29ce484222325;
    for byte in data.as_bytes() {
        hash ^= *byte as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    hash
}

static GLOBAL_FAVORITES: OnceLock<RwLock<FavoriteManager>> = OnceLock::new();

pub fn get_global_favorites() -> &'static RwLock<FavoriteManager> {
    GLOBAL_FAVORITES.get_or_init(|| {
        let path = PathBuf::from("cleanflow_favorites.json");
        RwLock::new(FavoriteManager::new(path))
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_favorite_manager_lifecycle() {
        let temp_dir = std::env::temp_dir().join(format!("cleanflow_fav_test_{}", std::process::id()));
        let _ = fs::remove_dir_all(&temp_dir);
        let _ = fs::create_dir_all(&temp_dir);
        let store_file = temp_dir.join("favorites.json");

        let mut mgr = FavoriteManager::new(store_file.clone());
        assert_eq!(mgr.list_all().len(), 0);

        // Add favorite with alias
        let item1 = mgr.add("C:\\Users\\Default\\Downloads", Some("我的下载"), Some("dl"));
        assert_eq!(item1.name, "我的下载");
        assert_eq!(item1.alias.as_deref(), Some("dl"));
        assert!(mgr.is_favorite("C:\\Users\\Default\\Downloads"));

        // Match by alias
        let found = mgr.get_by_alias("dl");
        assert!(found.is_some());
        assert_eq!(found.unwrap().path, "C:\\Users\\Default\\Downloads");

        // Add second favorite
        mgr.add("D:\\Projects", None, Some("proj"));
        assert_eq!(mgr.list_all().len(), 2);

        // Search by query
        let query_res = mgr.find_by_query("下载");
        assert_eq!(query_res.len(), 1);

        // Update alias
        assert!(mgr.update_alias("D:\\Projects", Some("p")));
        assert_eq!(mgr.get_by_alias("p").map(|f| f.path), Some("D:\\Projects".to_string()));

        // Remove favorite
        assert!(mgr.remove("C:\\Users\\Default\\Downloads"));
        assert_eq!(mgr.list_all().len(), 1);
        assert!(!mgr.is_favorite("C:\\Users\\Default\\Downloads"));

        // Test persistence reload
        let mgr2 = FavoriteManager::new(store_file);
        assert_eq!(mgr2.list_all().len(), 1);
        assert_eq!(mgr2.list_all()[0].path, "D:\\Projects");

        let _ = fs::remove_dir_all(&temp_dir);
    }
}
