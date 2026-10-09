use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct WinApp2FileKey {
    pub raw_path: String,
    pub resolved_dir: String,
    pub file_mask: String,
    pub recurse: bool,
    pub remove_self: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct WinApp2Rule {
    pub section_name: String,
    pub detect_reg: Vec<String>,
    pub detect_file: Vec<String>,
    pub file_keys: Vec<WinApp2FileKey>,
    pub exclude_keys: Vec<String>,
    pub default_enabled: bool,
}

/// Expands standard Windows environment variables in paths, case-insensitively
pub fn expand_winapp2_env_vars(raw: &str) -> String {
    let mut result = raw.to_string();

    let env_map: [(&str, &str); 7] = [
        ("%LOCALAPPDATA%", "LOCALAPPDATA"),
        ("%APPDATA%", "APPDATA"),
        ("%PROGRAMDATA%", "ProgramData"),
        ("%USERPROFILE%", "USERPROFILE"),
        ("%WINDIR%", "windir"),
        ("%SYSTEMDRIVE%", "SystemDrive"),
        ("%TEMP%", "TEMP"),
    ];

    for (token, env_key) in env_map {
        let mut start_idx = 0;
        while let Some(rel_pos) = result[start_idx..].to_uppercase().find(token) {
            let actual_pos = start_idx + rel_pos;
            let val = std::env::var(env_key).unwrap_or_else(|_| {
                // Sane Windows defaults if missing
                match env_key {
                    "ProgramData" => "C:\\ProgramData".to_string(),
                    "windir" => "C:\\Windows".to_string(),
                    "SystemDrive" => "C:".to_string(),
                    _ => "".to_string(),
                }
            });

            result.replace_range(actual_pos..actual_pos + token.len(), &val);
            start_idx = actual_pos + val.len();
        }
    }

    result
}

/// Parses a pipe-delimited FileKey entry: Path|Mask|Flags
pub fn parse_file_key(raw_val: &str) -> WinApp2FileKey {
    let parts: Vec<&str> = raw_val.split('|').map(|s| s.trim()).collect();

    let raw_path = parts.first().copied().unwrap_or("").to_string();
    let resolved_dir = expand_winapp2_env_vars(&raw_path);
    let file_mask = parts.get(1).copied().unwrap_or("*.*").to_string();

    let mut recurse = false;
    let mut remove_self = false;

    for flag in parts.iter().skip(2) {
        let f_upper = flag.to_uppercase();
        if f_upper.contains("RECURSE") {
            recurse = true;
        }
        if f_upper.contains("REMOVESELF") {
            remove_self = true;
        }
    }

    WinApp2FileKey {
        raw_path,
        resolved_dir,
        file_mask,
        recurse,
        remove_self,
    }
}

/// Parses full WinApp2 INI content into structured rules
pub fn parse_winapp2_ini(ini_content: &str) -> Vec<WinApp2Rule> {
    let mut rules = Vec::new();
    let mut current_rule: Option<WinApp2Rule> = None;

    for line in ini_content.lines() {
        let trimmed = line.trim();

        // Skip comments and blank lines
        if trimmed.is_empty() || trimmed.starts_with(';') || trimmed.starts_with('#') {
            continue;
        }

        // Section header
        if trimmed.starts_with('[') && trimmed.ends_with(']') {
            if let Some(r) = current_rule.take() {
                if !r.file_keys.is_empty() {
                    rules.push(r);
                }
            }

            let section_name = trimmed[1..trimmed.len() - 1].trim().to_string();
            current_rule = Some(WinApp2Rule {
                section_name,
                detect_reg: Vec::new(),
                detect_file: Vec::new(),
                file_keys: Vec::new(),
                exclude_keys: Vec::new(),
                default_enabled: true,
            });
            continue;
        }

        // Key = Value
        if let Some(rule) = current_rule.as_mut() {
            if let Some((key, val)) = trimmed.split_once('=') {
                let k = key.trim();
                let v = val.trim();
                let k_upper = k.to_uppercase();

                if k_upper.starts_with("DETECTFILE") {
                    rule.detect_file.push(expand_winapp2_env_vars(v));
                } else if k_upper.starts_with("DETECT") {
                    rule.detect_reg.push(v.to_string());
                } else if k_upper.starts_with("FILEKEY") {
                    let fk = parse_file_key(v);
                    rule.file_keys.push(fk);
                } else if k_upper.starts_with("EXCLUDEKEY") {
                    rule.exclude_keys.push(expand_winapp2_env_vars(v));
                } else if k_upper == "DEFAULT" {
                    rule.default_enabled = !v.eq_ignore_ascii_case("false");
                }
            }
        }
    }

    if let Some(r) = current_rule {
        if !r.file_keys.is_empty() {
            rules.push(r);
        }
    }

    rules
}

/// Reads and parses an external winapp2.ini file from disk
pub fn load_winapp2_file<P: AsRef<Path>>(path: P) -> Result<Vec<WinApp2Rule>, std::io::Error> {
    let content = fs::read_to_string(path)?;
    Ok(parse_winapp2_ini(&content))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_expand_env_vars() {
        let raw = "%LOCALAPPDATA%\\Google\\Chrome\\User Data";
        let expanded = expand_winapp2_env_vars(raw);
        assert!(!expanded.contains("%LOCALAPPDATA%"));
        assert!(expanded.contains("Google\\Chrome"));
    }

    #[test]
    fn test_parse_file_key() {
        let raw = "%APPDATA%\\Code\\Cache|*.*|RECURSE";
        let fk = parse_file_key(raw);
        assert!(fk.recurse);
        assert!(!fk.remove_self);
        assert_eq!(fk.file_mask, "*.*");
        assert!(fk.resolved_dir.contains("Code\\Cache"));
    }

    #[test]
    fn test_parse_winapp2_snippet() {
        let snippet = r#"
        ; CleanFlow WinApp2 Test Sample
        [Visual Studio Code Cache*]
        LangSecRef=3021
        Detect=HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\{Code}
        DetectFile=%APPDATA%\Code
        Default=False
        FileKey1=%APPDATA%\Code\Cache|*.*|RECURSE
        FileKey2=%APPDATA%\Code\CachedData|*.*
        ExcludeKey1=%APPDATA%\Code\Cache\index

        [Google Chrome Cache*]
        DetectFile=%LOCALAPPDATA%\Google\Chrome
        FileKey1=%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache|*.*|RECURSE|REMOVESELF
        "#;

        let rules = parse_winapp2_ini(snippet);
        assert_eq!(rules.len(), 2);

        let vscode = &rules[0];
        assert_eq!(vscode.section_name, "Visual Studio Code Cache*");
        assert_eq!(vscode.detect_reg.len(), 1);
        assert_eq!(vscode.detect_file.len(), 1);
        assert_eq!(vscode.file_keys.len(), 2);
        assert!(!vscode.default_enabled);
        assert_eq!(vscode.exclude_keys.len(), 1);

        let chrome = &rules[1];
        assert_eq!(chrome.section_name, "Google Chrome Cache*");
        assert!(chrome.file_keys[0].recurse);
        assert!(chrome.file_keys[0].remove_self);
    }

    #[test]
    fn test_load_winapp2_default_file() {
        let path = Path::new("winapp2_default.ini");
        if path.exists() {
            let res = load_winapp2_file(path);
            assert!(res.is_ok());
            let rules = res.unwrap();
            assert_eq!(rules.len(), 15);
            // Verify WeChat and Cursor rules exist
            assert!(rules.iter().any(|r| r.section_name.contains("Cursor")));
            assert!(rules.iter().any(|r| r.section_name.contains("WeChat")));
        }
    }
}

