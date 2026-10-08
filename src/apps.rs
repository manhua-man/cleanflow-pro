use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::hash::{Hash, Hasher};
use std::path::Path;
use std::process::Command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InstalledApp {
    pub id: String,
    pub name: String,
    pub version: String,
    pub publisher: String,
    pub install_date: String,
    pub size_bytes: u64,
    pub install_location: String,
    pub uninstall_string: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppLeftover {
    pub id: String,
    pub folder_name: String,
    pub path: String,
    pub size_bytes: u64,
    pub file_count: u64,
    pub category: String,
    pub reason: String,
}

#[derive(Deserialize)]
struct RawAppItem {
    #[serde(rename = "DisplayName")]
    display_name: Option<String>,
    #[serde(rename = "DisplayVersion")]
    display_version: Option<String>,
    #[serde(rename = "Publisher")]
    publisher: Option<String>,
    #[serde(rename = "InstallDate")]
    install_date: Option<serde_json::Value>,
    #[serde(rename = "EstimatedSize")]
    estimated_size: Option<serde_json::Value>,
    #[serde(rename = "InstallLocation")]
    install_location: Option<String>,
    #[serde(rename = "UninstallString")]
    uninstall_string: Option<String>,
}

fn compute_app_id(name: &str) -> String {
    let mut hasher = std::collections::hash_map::DefaultHasher::new();
    name.hash(&mut hasher);
    format!("app_{:012x}", hasher.finish() & 0x0000_ffff_ffff_ffff)
}

pub fn get_installed_apps() -> Vec<InstalledApp> {
    let script = r#"
        $ErrorActionPreference = 'SilentlyContinue'
        $keys = @(
            'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
            'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
            'HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*'
        )
        $items = Get-ItemProperty $keys | Where-Object { $_.DisplayName } | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate, EstimatedSize, InstallLocation, UninstallString
        $items | ConvertTo-Json -Compress
    "#;

    let output = Command::new("powershell")
        .args(["-NoProfile", "-Command", script])
        .output();

    let mut apps = Vec::new();
    let mut seen: HashSet<String> = HashSet::new();

    if let Ok(out) = output {
        let stdout = String::from_utf8_lossy(&out.stdout);
        if let Ok(raw_list) = serde_json::from_str::<Vec<RawAppItem>>(&stdout) {
            for raw in raw_list {
                let name = match raw.display_name {
                    Some(n) if !n.trim().is_empty() => n.trim().to_string(),
                    _ => continue,
                };

                if name.starts_with('{') && name.ends_with('}') {
                    continue;
                }

                if seen.contains(&name) {
                    continue;
                }
                seen.insert(name.clone());

                let version = raw.display_version.unwrap_or_default();
                let publisher = raw.publisher.unwrap_or_default();
                let install_date = match raw.install_date {
                    Some(serde_json::Value::String(s)) => s,
                    Some(serde_json::Value::Number(n)) => n.to_string(),
                    _ => String::new(),
                };
                let install_location = raw.install_location.unwrap_or_default();
                let uninstall_string = raw.uninstall_string.unwrap_or_default();

                let size_kb: u64 = match raw.estimated_size {
                    Some(serde_json::Value::Number(n)) => n.as_u64().unwrap_or(0),
                    _ => 0,
                };
                let mut size_bytes = size_kb * 1024;

                if size_bytes == 0 && !install_location.is_empty() {
                    let loc_path = Path::new(install_location.trim_matches('"'));
                    if loc_path.exists() && loc_path.is_dir() {
                        let (dir_sz, _) = crate::scanner::calculate_path_stats(loc_path);
                        size_bytes = dir_sz;
                    }
                }

                let id = compute_app_id(&name);

                apps.push(InstalledApp {
                    id,
                    name,
                    version,
                    publisher,
                    install_date,
                    size_bytes,
                    install_location,
                    uninstall_string,
                });
            }
        }
    }

    apps.sort_by(|a, b| b.size_bytes.cmp(&a.size_bytes));
    apps
}

pub fn scan_app_leftovers() -> Vec<AppLeftover> {
    let apps = get_installed_apps();
    let mut installed_words: HashSet<String> = HashSet::new();

    for app in &apps {
        for w in app.name.split_whitespace() {
            let clean = w.to_lowercase().chars().filter(|c| c.is_alphanumeric()).collect::<String>();
            if clean.len() >= 3 {
                installed_words.insert(clean);
            }
        }
    }

    let mut leftovers = Vec::new();
    let scan_roots = [
        ("LOCALAPPDATA", "AppData\\Local 孤立残留"),
        ("APPDATA", "AppData\\Roaming 孤立残留"),
    ];

    let system_ignore = [
        "microsoft", "temp", "packages", "assembly", "connecteddevicesplatform",
        "d3dscache", "fontcache", "pip", "pnpm", "npm-cache", "google", "docker",
        "tencent", "larkshell", "cursor", "unity", "adobe", "mozilla", "git",
    ];

    for (var_name, cat_label) in scan_roots {
        if let Ok(base_path) = std::env::var(var_name) {
            let p = Path::new(&base_path);
            if let Ok(entries) = std::fs::read_dir(p) {
                for entry in entries.flatten() {
                    let item_path = entry.path();
                    if !item_path.is_dir() {
                        continue;
                    }

                    let folder_name = match item_path.file_name().and_then(|n| n.to_str()) {
                        Some(name) => name,
                        None => continue,
                    };

                    let lower = folder_name.to_lowercase();
                    if system_ignore.contains(&lower.as_str()) {
                        continue;
                    }

                    let mut matched = false;
                    for word in &installed_words {
                        if lower.contains(word) || word.contains(&lower) {
                            matched = true;
                            break;
                        }
                    }

                    if !matched {
                        let (sz, count) = crate::scanner::calculate_path_stats(&item_path);
                        if sz > 1024 * 1024 { // > 1 MB
                            let mut hasher = std::collections::hash_map::DefaultHasher::new();
                            item_path.hash(&mut hasher);
                            let id = format!("leftover_{:012x}", hasher.finish() & 0x0000_ffff_ffff_ffff);

                            leftovers.push(AppLeftover {
                                id,
                                folder_name: folder_name.to_string(),
                                path: item_path.to_string_lossy().to_string(),
                                size_bytes: sz,
                                file_count: count,
                                category: cat_label.to_string(),
                                reason: "未检索到匹配的已安装程序，疑似卸载后残留数据".to_string(),
                            });
                        }
                    }
                }
            }
        }
    }

    leftovers.sort_by(|a, b| b.size_bytes.cmp(&a.size_bytes));
    leftovers
}

pub fn launch_uninstaller(cmd: &str) -> Result<(), String> {
    let trimmed = cmd.trim();
    if trimmed.is_empty() {
        return Err("卸载命令为空".to_string());
    }

    Command::new("cmd")
        .args(["/C", trimmed])
        .spawn()
        .map_err(|e| format!("启动卸载向导失败: {}", e))?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_installed_apps() {
        let apps = get_installed_apps();
        assert!(!apps.is_empty(), "Should discover installed apps");
        assert!(!apps[0].name.is_empty());
    }
}
