use serde::{Deserialize, Serialize};
use std::fs;
use std::hash::{Hash, Hasher};
use std::path::{Path, PathBuf};
use std::process::Command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StartupItem {
    pub id: String,
    pub name: String,
    pub command: String,
    pub source: String,
    pub location: String,
    pub target_path: String,
    pub exists: bool,
    pub impact: String,
    pub enabled: bool,
}

fn compute_id(source: &str, name: &str) -> String {
    let mut hasher = std::collections::hash_map::DefaultHasher::new();
    source.hash(&mut hasher);
    name.hash(&mut hasher);
    format!("startup_{:012x}", hasher.finish() & 0x0000_ffff_ffff_ffff)
}

fn extract_executable_path(cmd: &str) -> String {
    let trimmed = cmd.trim();
    if trimmed.is_empty() {
        return String::new();
    }

    if trimmed.starts_with('"') {
        if let Some(end_quote) = trimmed[1..].find('"') {
            return trimmed[1..=end_quote].to_string();
        }
    }

    let first_token = trimmed.split_whitespace().next().unwrap_or(trimmed);
    first_token.to_string()
}

fn expand_env(path: &str) -> String {
    let mut result = path.to_string();
    let vars = ["WINDIR", "SYSTEMROOT", "USERPROFILE", "LOCALAPPDATA", "APPDATA", "PROGRAMFILES", "PROGRAMFILES(X86)"];
    for var in vars {
        if let Ok(val) = std::env::var(var) {
            let placeholder = format!("%{}%", var);
            result = result.replace(&placeholder, &val);
            let lower_placeholder = format!("%{}%", var.to_lowercase());
            result = result.replace(&lower_placeholder, &val);
        }
    }
    result
}

fn evaluate_impact(name: &str, cmd: &str) -> String {
    let lower_name = name.to_lowercase();
    let lower_cmd = cmd.to_lowercase();

    if lower_name.contains("edge")
        || lower_name.contains("chrome")
        || lower_name.contains("baidu")
        || lower_name.contains("steam")
        || lower_name.contains("docker")
        || lower_name.contains("mumu")
        || lower_name.contains("gameviewer")
        || lower_name.contains("dingtalk")
        || lower_cmd.contains("electron")
        || lower_name.contains("onedrive")
    {
        return "高影响".to_string();
    }

    if lower_name.contains("listary")
        || lower_name.contains("proxifier")
        || lower_name.contains("rtkaud")
        || lower_name.contains("awesun")
    {
        return "中等影响".to_string();
    }

    "轻量启动".to_string()
}

pub fn get_startup_items() -> Vec<StartupItem> {
    let mut items = Vec::new();

    // 1. Registry Keys via reg query
    let reg_targets = [
        (r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run", "HKCU"),
        (r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run", "HKLM"),
        (r"HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run", "HKLM_WOW64"),
    ];

    for (reg_path, source_code) in reg_targets {
        let output = Command::new("reg")
            .args(["query", reg_path])
            .output();

        if let Ok(out) = output {
            let text = String::from_utf8_lossy(&out.stdout);
            for line in text.lines() {
                let trimmed = line.trim();
                if trimmed.is_empty() || trimmed.starts_with("HKEY_") {
                    continue;
                }

                let (name, cmd) = if let Some(idx) = trimmed.find("REG_SZ") {
                    let n = trimmed[..idx].trim();
                    let c = trimmed[idx + "REG_SZ".len()..].trim();
                    (n, c)
                } else if let Some(idx) = trimmed.find("REG_EXPAND_SZ") {
                    let n = trimmed[..idx].trim();
                    let c = trimmed[idx + "REG_EXPAND_SZ".len()..].trim();
                    (n, c)
                } else {
                    continue;
                };

                if name.is_empty() || cmd.is_empty() {
                    continue;
                }

                let target_raw = extract_executable_path(cmd);
                let target_expanded = expand_env(&target_raw);
                let exists = if target_expanded.is_empty() {
                    false
                } else {
                    Path::new(&target_expanded).exists()
                };

                let impact = if !exists {
                    "失效残留".to_string()
                } else {
                    evaluate_impact(name, cmd)
                };

                let id = compute_id(source_code, name);

                items.push(StartupItem {
                    id,
                    name: name.to_string(),
                    command: cmd.to_string(),
                    source: source_code.to_string(),
                    location: reg_path.to_string(),
                    target_path: target_expanded,
                    exists,
                    impact,
                    enabled: true,
                });
            }
        }
    }

    // 2. Startup Folders
    let folder_targets = [
        ("APPDATA", r"Microsoft\Windows\Start Menu\Programs\Startup", "UserStartupFolder"),
        ("ALLUSERSPROFILE", r"Microsoft\Windows\Start Menu\Programs\Startup", "CommonStartupFolder"),
    ];

    for (base_var, sub_path, label) in folder_targets {
        if let Ok(base_val) = std::env::var(base_var) {
            let startup_dir = PathBuf::from(base_val).join(sub_path);
            if startup_dir.exists() && startup_dir.is_dir() {
                if let Ok(entries) = fs::read_dir(&startup_dir) {
                    for entry in entries.flatten() {
                        let path = entry.path();
                        if let Some(file_name) = path.file_name().and_then(|n| n.to_str()) {
                            if file_name.eq_ignore_ascii_case("desktop.ini") {
                                continue;
                            }
                            let id = compute_id(label, file_name);
                            let target_path = path.to_string_lossy().to_string();
                            let exists = path.exists();
                            let impact = evaluate_impact(file_name, &target_path);

                            items.push(StartupItem {
                                id,
                                name: file_name.to_string(),
                                command: target_path.clone(),
                                source: label.to_string(),
                                location: startup_dir.to_string_lossy().to_string(),
                                target_path,
                                exists,
                                impact,
                                enabled: true,
                            });
                        }
                    }
                }
            }
        }
    }

    items
}

pub fn remove_startup_item(source: &str, name: &str, location: &str) -> Result<(), String> {
    if source.starts_with("HKCU") || source.starts_with("HKLM") {
        let output = Command::new("reg")
            .args(["delete", location, "/v", name, "/f"])
            .output()
            .map_err(|e| format!("执行注册表删除失败: {}", e))?;

        if !output.status.success() {
            let err = String::from_utf8_lossy(&output.stderr);
            return Err(format!("删除自启动项失败: {}", err));
        }

        Ok(())
    } else {
        let path = Path::new(location).join(name);
        if path.exists() {
            fs::remove_file(&path).map_err(|e| format!("删除启动快捷方式失败: {}", e))?;
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_startup_items() {
        let items = get_startup_items();
        assert!(!items.is_empty(), "Should discover startup items on Windows");
        let item = &items[0];
        assert!(!item.id.is_empty());
        assert!(!item.name.is_empty());
    }
}
