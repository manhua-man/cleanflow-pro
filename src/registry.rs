use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Write;
use std::path::Path;
use std::process::Command;
use std::sync::atomic::{AtomicU64, Ordering};

static COUNTER: AtomicU64 = AtomicU64::new(1);

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

/// Scans for obsolete or orphaned registry keys and application caches
pub fn scan_registry_issues() -> Vec<RegistryIssue> {
    let mut issues = Vec::new();

    // 1. Scan MuiCache for deleted executables
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

            // Line format: <Path>.FriendlyAppName    REG_SZ    <FriendlyName>
            // or:          <Path>.ApplicationCompany REG_SZ    <Company>
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

            // Validate if it is a file path
            if (file_path_str.len() > 3 && &file_path_str[1..3] == ":\\") || file_path_str.starts_with(r"\\") {
                let p = Path::new(file_path_str);
                if !p.exists() {
                    let id = format!("reg_mui_{}", COUNTER.fetch_add(1, Ordering::Relaxed));
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

    // 2. Scan OpenWithList in FileExts for uninstalled application right-click associations
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
                        // Check if exe is registered or exists in common app directories
                        let mut exists = false;

                        // Check App Paths in registry
                        let app_path_key = format!(r"HKLM\Software\Microsoft\Windows\CurrentVersion\App Paths\{}", exe_name);
                        let check_reg = Command::new("reg")
                            .args(["query", &app_path_key])
                            .output();
                        if let Ok(c) = check_reg {
                            if c.status.success() {
                                exists = true;
                            }
                        }

                        if !exists {
                            let common_dirs = [
                                std::env::var("ProgramFiles").unwrap_or_default(),
                                std::env::var("ProgramFiles(x86)").unwrap_or_default(),
                                format!("{}\\Programs", std::env::var("LOCALAPPDATA").unwrap_or_default()),
                                std::env::var("WINDIR").unwrap_or_default(),
                                format!("{}\\System32", std::env::var("WINDIR").unwrap_or_default()),
                            ];

                            for dir in &common_dirs {
                                if !dir.is_empty() && Path::new(dir).join(exe_name).exists() {
                                    exists = true;
                                    break;
                                }
                            }
                        }

                        if !exists {
                            let id = format!("reg_openwith_{}", COUNTER.fetch_add(1, Ordering::Relaxed));
                            let reg_root = current_key.replace("HKEY_CURRENT_USER", "HKCU");
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

    // 3. Scan Uninstall entries across HKLM, WOW6432Node, and HKCU for deleted installations
    let uninst_keys = [
        r"HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall",
        r"HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall",
    ];

    for root in &uninst_keys {
        let output_uninst = Command::new("reg")
            .args(["query", root])
            .output();

        if let Ok(out) = output_uninst {
            let text = String::from_utf8_lossy(&out.stdout);
            for subkey_line in text.lines() {
                let subkey = subkey_line.trim();
                if subkey.is_empty() || !subkey.contains(r"Software\Microsoft\Windows\CurrentVersion\Uninstall") {
                    continue;
                }

                let query_details = Command::new("reg")
                    .args(["query", subkey])
                    .output();

                if let Ok(det_out) = query_details {
                    let det_text = String::from_utf8_lossy(&det_out.stdout);
                    let mut display_name = String::new();
                    let mut uninst_str = String::new();
                    let mut install_loc = String::new();

                    for l in det_text.lines() {
                        let line_trimmed = l.trim();
                        if line_trimmed.contains("DisplayName") && line_trimmed.contains("REG_SZ") {
                            if let Some(pos) = line_trimmed.find("REG_SZ") {
                                display_name = line_trimmed[pos + 6..].trim().to_string();
                            }
                        } else if line_trimmed.contains("UninstallString") && (line_trimmed.contains("REG_SZ") || line_trimmed.contains("REG_EXPAND_SZ")) {
                            let flag = if line_trimmed.contains("REG_EXPAND_SZ") { "REG_EXPAND_SZ" } else { "REG_SZ" };
                            if let Some(pos) = line_trimmed.find(flag) {
                                uninst_str = line_trimmed[pos + flag.len()..].trim().to_string();
                            }
                        } else if line_trimmed.contains("InstallLocation") && line_trimmed.contains("REG_SZ") {
                            if let Some(pos) = line_trimmed.find("REG_SZ") {
                                install_loc = line_trimmed[pos + 6..].trim().to_string();
                            }
                        }
                    }

                    // Validate target executable or directory existence
                    let mut dead_target = None;
                    if !uninst_str.is_empty() {
                        let clean_uninst = uninst_str.trim_matches('"');
                        let exe_target = if let Some(idx) = clean_uninst.find('"') {
                            &clean_uninst[..idx]
                        } else {
                            clean_uninst.split(" /").next().unwrap_or(clean_uninst).split(" -").next().unwrap_or(clean_uninst)
                        };

                        if exe_target.len() > 3 && &exe_target[1..3] == ":\\" {
                            if !Path::new(exe_target).exists() {
                                dead_target = Some(exe_target.to_string());
                            }
                        }
                    } else if !install_loc.is_empty() && install_loc.len() > 3 && &install_loc[1..3] == ":\\" {
                        if !Path::new(&install_loc).exists() {
                            dead_target = Some(install_loc.to_string());
                        }
                    }

                    if let Some(dead_path) = dead_target {
                        let id = format!("reg_uninst_{}", COUNTER.fetch_add(1, Ordering::Relaxed));
                        let app_label = if !display_name.is_empty() {
                            display_name
                        } else {
                            subkey.rsplit('\\').next().unwrap_or("Unknown").to_string()
                        };

                        // Convert HKEY_LOCAL_MACHINE to HKLM, etc.
                        let clean_key = subkey
                            .replace("HKEY_LOCAL_MACHINE", "HKLM")
                            .replace("HKEY_CURRENT_USER", "HKCU");

                        issues.push(RegistryIssue {
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
                }
            }
        }
    }

    issues
}

/// Safely cleans chosen registry issues with automatic .reg backup
pub fn clean_registry_issues(targets: &[RegistryIssue]) -> RegistryCleanResult {
    let mut cleaned = 0;
    let mut errors = Vec::new();

    // Prepare backup directory in Temp
    let backup_dir = std::env::temp_dir().join("cleanflow_registry_backups");
    let _ = std::fs::create_dir_all(&backup_dir);
    let timestamp = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0);
    let backup_path = backup_dir.join(format!("backup_reg_{}.reg", timestamp));

    // Write .reg backup header
    let mut backup_content = String::from("Windows Registry Editor Version 5.00\r\n\r\n");

    for issue in targets {
        if let Some(ref val) = issue.value_name {
            // Backup single value restoration entry
            backup_content.push_str(&format!("[{}]\r\n", issue.root_key));
            backup_content.push_str(&format!("; CleanFlow Auto-Backup for: {}\r\n", issue.invalid_path));
            let orig = issue.original_value.as_deref().unwrap_or("");
            backup_content.push_str(&format!(
                "\"{}\"=\"{}\"\r\n\r\n",
                val.replace('\\', "\\\\").replace('"', "\\\""),
                orig.replace('\\', "\\\\").replace('"', "\\\"")
            ));

            // Execute delete
            let status = Command::new("reg")
                .args(["delete", &issue.root_key, "/v", val, "/f"])
                .status();

            match status {
                Ok(s) if s.success() => cleaned += 1,
                Ok(s) => errors.push(format!("删除值 {} 失败，退出码: {:?}", val, s.code())),
                Err(e) => errors.push(format!("执行 reg delete 失败: {}", e)),
            }
        } else {
            // Backup entire key removal
            backup_content.push_str(&format!("; CleanFlow Auto-Backup key removal: {}\r\n", issue.root_key));
            backup_content.push_str(&format!("[-{}]\r\n\r\n", issue.root_key));

            let status = Command::new("reg")
                .args(["delete", &issue.root_key, "/f"])
                .status();

            match status {
                Ok(s) if s.success() => cleaned += 1,
                Ok(s) => errors.push(format!("删除键 {} 失败，退出码: {:?}", issue.root_key, s.code())),
                Err(e) => errors.push(format!("执行 reg delete 失败: {}", e)),
            }
        }
    }

    // Save backup file
    let backup_file_str = if let Ok(mut f) = File::create(&backup_path) {
        let _ = f.write_all(backup_content.as_bytes());
        Some(backup_path.to_string_lossy().to_string())
    } else {
        None
    };

    RegistryCleanResult {
        success: errors.is_empty(),
        items_cleaned: cleaned,
        backup_file: backup_file_str,
        errors,
    }
}
