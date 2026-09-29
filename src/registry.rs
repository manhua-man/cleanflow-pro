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
                        category: "失效应用缓存 (MUICache)".to_string(),
                        description: format!("历史程序已删除或临时安装包已清理，残留注册表图标及名称映射"),
                        invalid_path: file_path_str.to_string(),
                        is_safe: true,
                    });
                }
            }
        }
    }

    // 2. Scan Uninstall entries in HKCU for deleted installations
    let uninst_key = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall";
    let output_uninst = Command::new("reg")
        .args(["query", uninst_key])
        .output();

    if let Ok(out) = output_uninst {
        let text = String::from_utf8_lossy(&out.stdout);
        for subkey_line in text.lines() {
            let subkey = subkey_line.trim();
            if subkey.is_empty() || !subkey.starts_with(r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall") {
                continue;
            }

            // Query InstallLocation
            let query_loc = Command::new("reg")
                .args(["query", subkey, "/v", "InstallLocation"])
                .output();

            if let Ok(loc_out) = query_loc {
                let loc_text = String::from_utf8_lossy(&loc_out.stdout);
                for l in loc_text.lines() {
                    if let Some(pos) = l.find("REG_SZ") {
                        let path_str = l[pos + 6..].trim();
                        if path_str.len() > 3 && &path_str[1..3] == ":\\" {
                            let p = Path::new(path_str);
                            if !p.exists() {
                                let id = format!("reg_uninst_{}", COUNTER.fetch_add(1, Ordering::Relaxed));
                                issues.push(RegistryIssue {
                                    id,
                                    root_key: subkey.to_string(),
                                    value_name: None,
                                    category: "失效软件卸载项 (Uninstall)".to_string(),
                                    description: "软件安装目录已不存在，控制面板添加/删除程序中残留无效条目".to_string(),
                                    invalid_path: path_str.to_string(),
                                    is_safe: true,
                                });
                            }
                        }
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
    let backup_path = backup_dir.join(format!("backup_{}.reg", timestamp));

    // Write .reg backup header
    let mut backup_content = String::from("Windows Registry Editor Version 5.00\r\n\r\n");

    for issue in targets {
        if let Some(ref val) = issue.value_name {
            // Backup single value removal command
            backup_content.push_str(&format!("[{}]\r\n", issue.root_key));
            backup_content.push_str(&format!("; CleanFlow Auto-Backup: {}\r\n", issue.invalid_path));
            backup_content.push_str(&format!("\"{}\"=\"-\"\r\n\r\n", val.replace("\\", "\\\\")));

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
            // Backup entire key
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
