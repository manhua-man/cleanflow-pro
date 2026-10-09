use crate::rules::resolve_path_patterns;
use crate::winapp2_parser::WinApp2Rule;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::ffi::OsStr;
use std::fs;
use std::os::windows::ffi::OsStrExt;
use std::path::Path;

const HKEY_CLASSES_ROOT: isize = -2147483648; // 0x80000000
const HKEY_CURRENT_USER: isize = -2147483647; // 0x80000001
const HKEY_LOCAL_MACHINE: isize = -2147483646; // 0x80000002
const KEY_READ: u32 = 0x20019;

#[link(name = "advapi32")]
extern "system" {
    fn RegOpenKeyExW(
        hKey: isize,
        lpSubKey: *const u16,
        ulOptions: u32,
        samDesired: u32,
        phkResult: *mut isize,
    ) -> i32;

    fn RegCloseKey(hKey: isize) -> i32;
}

fn to_wide_null(s: &str) -> Vec<u16> {
    OsStr::new(s).encode_wide().chain(std::iter::once(0)).collect()
}

/// Checks if a Windows Registry key exists using high-speed RegOpenKeyExW (~0.001ms)
pub fn check_reg_key_exists(reg_path: &str) -> bool {
    let clean = reg_path.trim().replace('/', "\\");
    let (root_str, subkey) = match clean.split_once('\\') {
        Some((r, s)) => (r.to_uppercase(), s),
        None => (clean.to_uppercase(), ""),
    };

    let h_root = match root_str.as_str() {
        "HKCU" | "HKEY_CURRENT_USER" => HKEY_CURRENT_USER,
        "HKLM" | "HKEY_LOCAL_MACHINE" => HKEY_LOCAL_MACHINE,
        "HKCR" | "HKEY_CLASSES_ROOT" => HKEY_CLASSES_ROOT,
        _ => return false,
    };

    let wide_sub = to_wide_null(subkey);
    let mut h_result: isize = 0;

    let res = unsafe {
        RegOpenKeyExW(
            h_root,
            wide_sub.as_ptr(),
            0,
            KEY_READ,
            &mut h_result,
        )
    };

    if res == 0 {
        unsafe { RegCloseKey(h_result) };
        true
    } else {
        false
    }
}

/// Checks whether an application is installed and detected on this PC
pub fn is_rule_detected(rule: &WinApp2Rule) -> bool {
    if rule.detect_file.is_empty() && rule.detect_reg.is_empty() {
        return true;
    }

    // 1. Check file system markers
    for df in &rule.detect_file {
        if Path::new(df).exists() {
            return true;
        }
    }

    // 2. Check registry markers
    for dr in &rule.detect_reg {
        if check_reg_key_exists(dr) {
            return true;
        }
    }

    false
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WinApp2CategoryResult {
    pub section_name: String,
    pub total_size_bytes: u64,
    pub file_count: usize,
    pub target_paths: Vec<String>,
    pub default_enabled: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WinApp2ScanReport {
    pub total_rules_loaded: usize,
    pub active_apps_detected: usize,
    pub total_reclaimable_bytes: u64,
    pub categories: Vec<WinApp2CategoryResult>,
}

fn file_matches_mask(filename: &str, mask: &str) -> bool {
    if mask == "*.*" || mask == "*" || mask.is_empty() {
        return true;
    }

    let regex_pattern = format!(
        "(?i)^{}$",
        regex::escape(mask)
            .replace("\\*", ".*")
            .replace("\\?", ".")
    );

    if let Ok(re) = regex::Regex::new(&regex_pattern) {
        re.is_match(filename)
    } else {
        true
    }
}

pub fn scan_winapp2_rules(rules: &[WinApp2Rule]) -> WinApp2ScanReport {
    let active_rules: Vec<&WinApp2Rule> = rules
        .iter()
        .filter(|r| is_rule_detected(r))
        .collect();

    let active_count = active_rules.len();

    let categories: Vec<WinApp2CategoryResult> = active_rules
        .into_par_iter()
        .filter_map(|rule| {
            let mut total_bytes = 0u64;
            let mut file_count = 0usize;
            let mut matched_paths = Vec::new();

            for fk in &rule.file_keys {
                let resolved_roots = resolve_path_patterns(&fk.resolved_dir);

                for root in resolved_roots {
                    if !root.exists() {
                        continue;
                    }

                    if root.is_file() {
                        if let Ok(meta) = root.metadata() {
                            total_bytes += meta.len();
                            file_count += 1;
                            matched_paths.push(root.to_string_lossy().to_string());
                        }
                    } else if root.is_dir() {
                        let walk = if fk.recurse {
                            jwalk::WalkDir::new(&root).max_depth(8)
                        } else {
                            jwalk::WalkDir::new(&root).max_depth(1)
                        };

                        for entry in walk.skip_hidden(false) {
                            if let Ok(entry) = entry {
                                if entry.file_type.is_file() {
                                    let fname = entry.file_name().to_string_lossy();
                                    if file_matches_mask(&fname, &fk.file_mask) {
                                        let p = entry.path();
                                        let p_str = p.to_string_lossy().to_string();

                                        let is_excluded = rule.exclude_keys.iter().any(|ex| {
                                            p_str.starts_with(ex) || p_str.eq_ignore_ascii_case(ex)
                                        });

                                        if !is_excluded {
                                            if let Ok(meta) = entry.metadata() {
                                                total_bytes += meta.len();
                                                file_count += 1;
                                                matched_paths.push(p_str);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            if file_count > 0 && total_bytes > 0 {
                Some(WinApp2CategoryResult {
                    section_name: rule.section_name.clone(),
                    total_size_bytes: total_bytes,
                    file_count,
                    target_paths: matched_paths,
                    default_enabled: rule.default_enabled,
                })
            } else {
                None
            }
        })
        .collect();

    let mut sorted_cats = categories;
    sorted_cats.sort_by(|a, b| b.total_size_bytes.cmp(&a.total_size_bytes));

    let total_reclaimable: u64 = sorted_cats.iter().map(|c| c.total_size_bytes).sum();

    WinApp2ScanReport {
        total_rules_loaded: rules.len(),
        active_apps_detected: active_count,
        total_reclaimable_bytes: total_reclaimable,
        categories: sorted_cats,
    }
}

pub fn clean_winapp2_categories(
    rules: &[WinApp2Rule],
    selected_sections: &[String],
) -> (u64, usize, Vec<String>) {
    let mut bytes_freed = 0u64;
    let mut files_deleted = 0usize;
    let mut errors = Vec::new();

    let selected_rules: Vec<&WinApp2Rule> = rules
        .iter()
        .filter(|r| selected_sections.contains(&r.section_name))
        .collect();

    for rule in selected_rules {
        for fk in &rule.file_keys {
            let resolved_roots = resolve_path_patterns(&fk.resolved_dir);
            for root in resolved_roots {
                if !root.exists() {
                    continue;
                }

                if root.is_file() {
                    if let Ok(meta) = root.metadata() {
                        let sz = meta.len();
                        if let Err(e) = fs::remove_file(&root) {
                            errors.push(format!("删除文件失败 {}: {}", root.display(), e));
                        } else {
                            bytes_freed += sz;
                            files_deleted += 1;
                        }
                    }
                } else if root.is_dir() {
                    if fk.remove_self {
                        let _ = fs::remove_dir_all(&root);
                    } else {
                        let walk = if fk.recurse {
                            jwalk::WalkDir::new(&root).max_depth(8)
                        } else {
                            jwalk::WalkDir::new(&root).max_depth(1)
                        };

                        for entry in walk.skip_hidden(false) {
                            if let Ok(entry) = entry {
                                if entry.file_type.is_file() {
                                    let fname = entry.file_name().to_string_lossy();
                                    if file_matches_mask(&fname, &fk.file_mask) {
                                        let p = entry.path();
                                        if let Ok(meta) = entry.metadata() {
                                            let sz = meta.len();
                                            if let Err(e) = fs::remove_file(&p) {
                                                errors.push(format!("删除失败 {}: {}", p.display(), e));
                                            } else {
                                                bytes_freed += sz;
                                                files_deleted += 1;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    (bytes_freed, files_deleted, errors)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_check_reg_key_exists() {
        // Standard Windows registry key that always exists
        assert!(check_reg_key_exists("HKLM\\Software\\Microsoft"));
        // Bogus non-existent key
        assert!(!check_reg_key_exists("HKLM\\Software\\NonExistent_FakeKey_9999"));
    }

    #[test]
    fn test_rule_detection_and_scan() {
        let temp_dir = std::env::temp_dir().join("cleanflow_winapp2_engine_test");
        let cache_dir = temp_dir.join("Cache");
        let _ = fs::remove_dir_all(&temp_dir);
        fs::create_dir_all(&cache_dir).unwrap();

        let f1 = cache_dir.join("file1.tmp");
        let f2 = cache_dir.join("file2.log");
        fs::write(&f1, b"Temp data 1").unwrap();
        fs::write(&f2, b"Log data 2").unwrap();

        let rule = WinApp2Rule {
            section_name: "Mock App Cache*".to_string(),
            detect_reg: Vec::new(),
            detect_file: vec![temp_dir.to_string_lossy().to_string()],
            file_keys: vec![crate::winapp2_parser::WinApp2FileKey {
                raw_path: cache_dir.to_string_lossy().to_string(),
                resolved_dir: cache_dir.to_string_lossy().to_string(),
                file_mask: "*.*".to_string(),
                recurse: true,
                remove_self: false,
            }],
            exclude_keys: Vec::new(),
            default_enabled: true,
        };

        assert!(is_rule_detected(&rule));

        let report = scan_winapp2_rules(&[rule.clone()]);
        assert_eq!(report.active_apps_detected, 1);
        assert_eq!(report.categories.len(), 1);
        assert_eq!(report.categories[0].file_count, 2);

        let (freed, count, errs) = clean_winapp2_categories(&[rule], &["Mock App Cache*".to_string()]);
        assert_eq!(count, 2);
        assert!(freed > 0);
        assert!(errs.is_empty());

        let _ = fs::remove_dir_all(&temp_dir);
    }
}
