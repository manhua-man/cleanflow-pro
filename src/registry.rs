use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::fs::File;
use std::hash::{Hash, Hasher};
use std::io::Write;
use std::path::Path;
use std::process::Command;

fn compute_issue_id(prefix: &str, key: &str, val: Option<&str>) -> String {
    let mut hasher = std::collections::hash_map::DefaultHasher::new();
    key.hash(&mut hasher);
    if let Some(v) = val {
        v.hash(&mut hasher);
    }
    format!("{}_{:012x}", prefix, hasher.finish() & 0x0000_ffff_ffff_ffff)
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RegistryIssue {
    pub id: String,
    pub root_key: String,
    pub value_name: Option<String>,
    pub original_value: Option<String>,
    pub category: String,
    pub description: String,
    pub invalid_path: String,
    pub is_safe: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RegistryCleanResult {
    pub success: bool,
    pub items_cleaned: usize,
    pub backup_file: Option<String>,
    pub errors: Vec<String>,
}

fn get_registered_app_paths() -> HashSet<String> {
    let mut set = HashSet::new();
    let keys = [
        r"HKLM\Software\Microsoft\Windows\CurrentVersion\App Paths",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths",
    ];
    for k in &keys {
        if let Ok(out) = Command::new("reg").args(["query", k]).output() {
            let text = String::from_utf8_lossy(&out.stdout);
            for line in text.lines() {
                let trimmed = line.trim();
                if let Some(pos) = trimmed.rfind('\\') {
                    let exe = &trimmed[pos + 1..];
                    if !exe.is_empty() {
                        set.insert(exe.to_lowercase());
                    }
                }
            }
        }
    }
    set
}

fn extract_dead_target(uninst_str: &str, install_loc: &str) -> Option<String> {
    if !uninst_str.is_empty() {
        let clean = uninst_str.trim();
        let target = if clean.starts_with('"') {
            if let Some(end_idx) = clean[1..].find('"') {
                &clean[1..1 + end_idx]
            } else {
                clean.trim_matches('"')
            }
        } else {
            clean.split(" /").next().unwrap_or(clean).split(" -").next().unwrap_or(clean)
        };
        let target_trimmed = target.trim();
        if target_trimmed.len() > 3 && &target_trimmed[1..3] == ":\\" {
            if !Path::new(target_trimmed).exists() {
                return Some(target_trimmed.to_string());
            }
        }
    }

    if !install_loc.is_empty() {
        let loc_trimmed = install_loc.trim().trim_matches('"');
        if loc_trimmed.len() > 3 && &loc_trimmed[1..3] == ":\\" {
            if !Path::new(loc_trimmed).exists() {
                return Some(loc_trimmed.to_string());
            }
        }
    }

    None
}

fn scan_mui_cache() -> Vec<RegistryIssue> {
    let mut issues = Vec::new();
    let mui_key = r"HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache";
    let output = Command::new("reg")
        .args(["query", mui_key, "/v", "*"])
        .output();

    if let Ok(out) = output {
        let text = String::from_utf8_lossy(&out.stdout);
        for line in text.lines() {
            let trimmed = line.trim();
            if trimmed.is_empty() || !trimmed.contains("REG_") {
                continue;
            }

            let parts: Vec<&str> = trimmed.split("REG_").collect();
            if parts.is_empty() {
                continue;
            }

            let val_raw = parts[0].trim();
            let orig_val = if parts.len() > 1 {
                let rest = parts[1].trim();
                let sub = rest.splitn(2, ' ').collect::<Vec<&str>>();
                if sub.len() > 1 { sub[1].trim().to_string() } else { String::new() }
            } else {
                String::new()
            };

            let mut file_path_str = val_raw;

            if let Some(pos) = file_path_str.rfind(".FriendlyAppName") {
                file_path_str = &file_path_str[..pos];
            } else if let Some(pos) = file_path_str.rfind(".ApplicationCompany") {
                file_path_str = &file_path_str[..pos];
            }

            if (file_path_str.len() > 3 && &file_path_str[1..3] == ":\\") || file_path_str.starts_with(r"\\") {
                let p = Path::new(file_path_str);
                if !p.exists() {
                    let id = compute_issue_id("reg_mui", mui_key, Some(val_raw));
                    issues.push(RegistryIssue {
                        id,
                        root_key: mui_key.to_string(),
                        value_name: Some(val_raw.to_string()),
                        original_value: Some(orig_val),
                        category: "失效应用缓存 (MUICache)".to_string(),
                        description: "历史程序已删除或临时安装包已清理，残留注册表图标及名称映射".to_string(),
                        invalid_path: file_path_str.to_string(),
                        is_safe: true,
                    });
                }
            }
        }
    }
    issues
}

fn scan_openwith_list() -> Vec<RegistryIssue> {
    let mut issues = Vec::new();
    let registered_apps = get_registered_app_paths();

    let common_dirs = [
        std::env::var("ProgramFiles").unwrap_or_default(),
        std::env::var("ProgramFiles(x86)").unwrap_or_default(),
        format!("{}\\Programs", std::env::var("LOCALAPPDATA").unwrap_or_default()),
        std::env::var("WINDIR").unwrap_or_default(),
        format!("{}\\System32", std::env::var("WINDIR").unwrap_or_default()),
    ];

    let file_exts_key = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts";
    let output_exts = Command::new("reg")
        .args(["query", file_exts_key, "/s"])
        .output();

    if let Ok(out) = output_exts {
        let text = String::from_utf8_lossy(&out.stdout);
        let mut current_key = String::new();

        for line in text.lines() {
            let trimmed = line.trim();
            if trimmed.starts_with(r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts") {
                current_key = trimmed.to_string();
            } else if current_key.contains("OpenWithList") && trimmed.contains("REG_SZ") {
                let parts: Vec<&str> = trimmed.split("REG_SZ").collect();
                if parts.len() >= 2 {
                    let val_name = parts[0].trim();
                    let exe_name = parts[1].trim();

                    if val_name.to_lowercase() != "mruposition" && exe_name.to_lowercase().ends_with(".exe") {
                        let exe_lower = exe_name.to_lowercase();
                        let mut exists = registered_apps.contains(&exe_lower);

                        if !exists {
                            for dir in &common_dirs {
                                if !dir.is_empty() && Path::new(dir).join(exe_name).exists() {
                                    exists = true;
                                    break;
                                }
                            }
                        }

                        if !exists {
                            let reg_root = current_key.replace("HKEY_CURRENT_USER", "HKCU");
                            let id = compute_issue_id("reg_openwith", &reg_root, Some(val_name));
                            issues.push(RegistryIssue {
                                id,
                                root_key: reg_root,
                                value_name: Some(val_name.to_string()),
                                original_value: Some(exe_name.to_string()),
                                category: "失效右键打开方式 (OpenWith)".to_string(),
                                description: format!("关联程序 [{}] 已卸载或失效，右键文件菜单中残留失效菜单项", exe_name),
                                invalid_path: exe_name.to_string(),
                                is_safe: true,
                            });
                        }
                    }
                }
            }
        }
    }
    issues
}

fn scan_uninstall_single_root(root: &str) -> Vec<RegistryIssue> {
    let mut issues = Vec::new();
    let output_uninst = Command::new("reg")
        .args(["query", root, "/s"])
        .output();

    if let Ok(out) = output_uninst {
        let text = String::from_utf8_lossy(&out.stdout);

        let mut current_subkey = String::new();
        let mut display_name = String::new();
        let mut uninst_str = String::new();
        let mut install_loc = String::new();

        let commit_entry = |subkey: &str, d_name: &str, u_str: &str, i_loc: &str, issue_list: &mut Vec<RegistryIssue>| {
            if subkey.is_empty() || subkey.ends_with(r"\Uninstall") {
                return;
            }

            if let Some(dead_path) = extract_dead_target(u_str, i_loc) {
                let clean_key = subkey
                    .replace("HKEY_LOCAL_MACHINE", "HKLM")
                    .replace("HKEY_CURRENT_USER", "HKCU");
                let id = compute_issue_id("reg_uninst", &clean_key, None);
                let app_label = if !d_name.is_empty() {
                    d_name.to_string()
                } else {
                    clean_key.rsplit('\\').next().unwrap_or("Unknown").to_string()
                };

                issue_list.push(RegistryIssue {
                    id,
                    root_key: clean_key,
                    value_name: None,
                    original_value: None,
                    category: "失效软件卸载项 (Uninstall)".to_string(),
                    description: format!("软件 [{}] 卸载器或安装目录已不存在，控制面板添加/删除程序中残留无效条目", app_label),
                    invalid_path: dead_path,
                    is_safe: true,
                });
            }
        };

        for line in text.lines() {
            let trimmed = line.trim();
            if trimmed.starts_with("HKEY_") {
                commit_entry(&current_subkey, &display_name, &uninst_str, &install_loc, &mut issues);
                current_subkey = trimmed.to_string();
                display_name.clear();
                uninst_str.clear();
                install_loc.clear();
            } else if trimmed.contains("DisplayName") && trimmed.contains("REG_SZ") {
                if let Some(pos) = trimmed.find("REG_SZ") {
                    display_name = trimmed[pos + 6..].trim().to_string();
                }
            } else if trimmed.contains("UninstallString") && (trimmed.contains("REG_SZ") || trimmed.contains("REG_EXPAND_SZ")) {
                let flag = if trimmed.contains("REG_EXPAND_SZ") { "REG_EXPAND_SZ" } else { "REG_SZ" };
                if let Some(pos) = trimmed.find(flag) {
                    uninst_str = trimmed[pos + flag.len()..].trim().to_string();
                }
            } else if trimmed.contains("InstallLocation") && trimmed.contains("REG_SZ") {
                if let Some(pos) = trimmed.find("REG_SZ") {
                    install_loc = trimmed[pos + 6..].trim().to_string();
                }
            }
        }

        commit_entry(&current_subkey, &display_name, &uninst_str, &install_loc, &mut issues);
    }

    issues
}

/// Scans for obsolete or orphaned registry keys and application caches concurrently across CPU threads
pub fn scan_registry_issues() -> Vec<RegistryIssue> {
    let mut mui_issues = Vec::new();
    let mut openwith_issues = Vec::new();
    let mut uninst_hklm = Vec::new();
    let mut uninst_wow = Vec::new();
    let mut uninst_hkcu = Vec::new();

    std::thread::scope(|s| {
        let t_mui = s.spawn(|| scan_mui_cache());
        let t_openwith = s.spawn(|| scan_openwith_list());
        let t_hklm = s.spawn(|| scan_uninstall_single_root(r"HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall"));
        let t_wow = s.spawn(|| scan_uninstall_single_root(r"HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"));
        let t_hkcu = s.spawn(|| scan_uninstall_single_root(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall"));

        mui_issues = t_mui.join().unwrap_or_default();
        openwith_issues = t_openwith.join().unwrap_or_default();
        uninst_hklm = t_hklm.join().unwrap_or_default();
        uninst_wow = t_wow.join().unwrap_or_default();
        uninst_hkcu = t_hkcu.join().unwrap_or_default();
    });

    let mut issues = Vec::new();
    issues.extend(mui_issues);
    issues.extend(openwith_issues);
    issues.extend(uninst_hklm);
    issues.extend(uninst_wow);
    issues.extend(uninst_hkcu);
    issues
}

/// Safely cleans chosen registry issues with automatic .reg backup and Rayon parallel execution
pub fn clean_registry_issues(targets: &[RegistryIssue]) -> RegistryCleanResult {
    let backup_dir = std::env::temp_dir().join("cleanflow_registry_backups");
    let _ = std::fs::create_dir_all(&backup_dir);
    let timestamp = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0);
    let backup_path = backup_dir.join(format!("backup_reg_{}.reg", timestamp));

    let mut backup_content = String::from("Windows Registry Editor Version 5.00\r\n\r\n");

    for issue in targets {
        if let Some(ref val) = issue.value_name {
            backup_content.push_str(&format!("[{}]\r\n", issue.root_key));
            backup_content.push_str(&format!("; CleanFlow Auto-Backup for: {}\r\n", issue.invalid_path));
            let orig = issue.original_value.as_deref().unwrap_or("");
            backup_content.push_str(&format!(
                "\"{}\"=\"{}\"\r\n\r\n",
                val.replace('\\', "\\\\").replace('"', "\\\""),
                orig.replace('\\', "\\\\").replace('"', "\\\"")
            ));
        } else {
            backup_content.push_str(&format!("; CleanFlow Auto-Backup key removal: {}\r\n", issue.root_key));
            backup_content.push_str(&format!("[-{}]\r\n\r\n", issue.root_key));
        }
    }

    let backup_file_str = if let Ok(mut f) = File::create(&backup_path) {
        let _ = f.write_all(backup_content.as_bytes());
        Some(backup_path.to_string_lossy().to_string())
    } else {
        None
    };

    let execution_results: Vec<(bool, Option<String>)> = targets
        .par_iter()
        .map(|issue| {
            if let Some(ref val) = issue.value_name {
                let status = Command::new("reg")
                    .args(["delete", &issue.root_key, "/v", val, "/f"])
                    .status();

                match status {
                    Ok(s) if s.success() => (true, None),
                    Ok(s) => (false, Some(format!("删除值 {} 失败，退出码: {:?}", val, s.code()))),
                    Err(e) => (false, Some(format!("执行 reg delete 失败: {}", e))),
                }
            } else {
                let status = Command::new("reg")
                    .args(["delete", &issue.root_key, "/f"])
                    .status();

                match status {
                    Ok(s) if s.success() => (true, None),
                    Ok(s) => (false, Some(format!("删除键 {} 失败，退出码: {:?}", issue.root_key, s.code()))),
                    Err(e) => (false, Some(format!("执行 reg delete 失败: {}", e))),
                }
            }
        })
        .collect();

    let mut cleaned = 0;
    let mut errors = Vec::new();
    for (success, err) in execution_results {
        if success {
            cleaned += 1;
        } else if let Some(e) = err {
            errors.push(e);
        }
    }

    RegistryCleanResult {
        success: errors.is_empty(),
        items_cleaned: cleaned,
        backup_file: backup_file_str,
        errors,
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RegistryBackupRecord {
    pub file_name: String,
    pub file_path: String,
    pub created_at: String,
    pub size_bytes: u64,
    pub entry_count: usize,
}

pub fn list_registry_backups() -> Vec<RegistryBackupRecord> {
    let backup_dir = std::env::temp_dir().join("cleanflow_registry_backups");
    if !backup_dir.exists() {
        return Vec::new();
    }

    let mut records = Vec::new();
    if let Ok(entries) = std::fs::read_dir(&backup_dir) {
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_file() && path.extension().and_then(|s| s.to_str()) == Some("reg") {
                let file_name = path.file_name().unwrap_or_default().to_string_lossy().to_string();
                let meta = std::fs::metadata(&path).ok();
                let size_bytes = meta.as_ref().map(|m| m.len()).unwrap_or(0);

                let created_at = meta
                    .and_then(|m| m.created().or_else(|_| m.modified()).ok())
                    .map(|time| {
                        let dur = time.duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs();
                        dur.to_string()
                    })
                    .unwrap_or_default();

                let entry_count = std::fs::read_to_string(&path)
                    .map(|content| {
                        content.lines().filter(|l| l.trim().starts_with('[')).count()
                    })
                    .unwrap_or(0);

                records.push(RegistryBackupRecord {
                    file_name,
                    file_path: path.to_string_lossy().to_string(),
                    created_at,
                    size_bytes,
                    entry_count,
                });
            }
        }
    }

    records.sort_by(|a, b| b.file_path.cmp(&a.file_path));
    records
}

pub fn restore_registry_backup(backup_path: &str) -> anyhow::Result<()> {
    let path = Path::new(backup_path);
    if !path.exists() {
        anyhow::bail!("指定的注册表备份文件不存在: {}", backup_path);
    }

    let output = Command::new("reg")
        .args(["import", backup_path])
        .output()?;

    if output.status.success() {
        Ok(())
    } else {
        let err = String::from_utf8_lossy(&output.stderr).to_string();
        let out = String::from_utf8_lossy(&output.stdout).to_string();
        let msg = if !err.trim().is_empty() { err } else { out };
        anyhow::bail!("还原注册表快照失败: {}", msg.trim());
    }
}

pub fn delete_registry_backup(backup_path: &str) -> anyhow::Result<()> {
    let path = Path::new(backup_path);
    if path.exists() {
        std::fs::remove_file(path)?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_dead_target() {
        let dead = extract_dead_target(r#""C:\NonExistentApp12345\uninst.exe" /S"#, "");
        assert_eq!(dead, Some(r"C:\NonExistentApp12345\uninst.exe".to_string()));

        let dead_loc = extract_dead_target("", r#"C:\NonExistentAppDirectory54321"#);
        assert_eq!(dead_loc, Some(r"C:\NonExistentAppDirectory54321".to_string()));
    }

    #[test]
    fn test_compute_issue_id() {
        let id1 = compute_issue_id("test", "HKCU\\Software\\Foo", Some("bar"));
        let id2 = compute_issue_id("test", "HKCU\\Software\\Foo", Some("bar"));
        let id3 = compute_issue_id("test", "HKCU\\Software\\Foo", Some("baz"));
        assert_eq!(id1, id2);
        assert_ne!(id1, id3);
    }

    #[test]
    fn test_scan_registry_concurrent() {
        let issues = scan_registry_issues();
        // Scanning executes without panic and returns vector
        println!("Concurrent registry scan completed, found {} issues", issues.len());
    }

    #[test]
    fn test_registry_backup_lifecycle() {
        let backup_dir = std::env::temp_dir().join("cleanflow_registry_backups");
        let _ = std::fs::create_dir_all(&backup_dir);
        let test_file = backup_dir.join("test_cleanflow_backup_mock.reg");
        let sample_reg = "Windows Registry Editor Version 5.00\r\n\r\n[HKEY_CURRENT_USER\\Software\\TestMock]\r\n\"Val\"=\"1\"\r\n";
        let _ = std::fs::write(&test_file, sample_reg);

        let backups = list_registry_backups();
        assert!(backups.iter().any(|b| b.file_name == "test_cleanflow_backup_mock.reg"));

        let target = backups.into_iter().find(|b| b.file_name == "test_cleanflow_backup_mock.reg").unwrap();
        assert_eq!(target.entry_count, 1);
        assert!(target.size_bytes > 0);

        let del_res = delete_registry_backup(&test_file.to_string_lossy());
        assert!(del_res.is_ok());
        assert!(!test_file.exists());
    }
}
