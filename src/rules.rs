use serde::{Deserialize, Serialize};
use std::env;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RuleConfig {
    pub version: String,
    pub categories: Vec<RuleCategory>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RuleCategory {
    pub id: String,
    pub name: String,
    pub description: String,
    pub risk_level: String,
    pub rules: Vec<CleanRule>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CleanRule {
    pub id: String,
    pub name: String,
    pub path_pattern: String,
    pub action: String,
    #[serde(default = "default_true")]
    pub default_checked: bool,
}

fn default_true() -> bool {
    true
}

impl RuleConfig {
    pub fn load_from_str(json_str: &str) -> anyhow::Result<Self> {
        let config: RuleConfig = serde_json::from_str(json_str)?;
        Ok(config)
    }

    pub fn load_from_file<P: AsRef<Path>>(path: P) -> anyhow::Result<Self> {
        let content = std::fs::read_to_string(path)?;
        Self::load_from_str(&content)
    }
}

pub fn expand_env_vars(raw_pattern: &str) -> String {
    let mut result = raw_pattern.to_string();
    for (k, v) in env::vars() {
        let placeholder = format!("%{}%", k);
        if result.contains(&placeholder) {
            result = result.replace(&placeholder, &v);
        }
    }
    result
}

pub fn resolve_path_patterns(pattern: &str) -> Vec<PathBuf> {
    let expanded = expand_env_vars(pattern);

    // If no wildcards, return directly
    if !expanded.contains('*') && !expanded.contains('?') {
        let p = PathBuf::from(expanded);
        if p.exists() {
            return vec![p];
        } else {
            return Vec::new();
        }
    }

    // Normalize slashes for Windows
    let normalized = expanded.replace('/', "\\");
    let segments: Vec<&str> = normalized.split('\\').filter(|s| !s.is_empty()).collect();
    if segments.is_empty() {
        return Vec::new();
    }

    let mut current_paths: Vec<PathBuf> = Vec::new();
    let mut start_idx = 0;

    if segments[0].ends_with(':') {
        current_paths.push(PathBuf::from(format!("{}\\", segments[0])));
        start_idx = 1;
    } else if normalized.starts_with("\\\\") {
        if segments.len() >= 2 {
            current_paths.push(PathBuf::from(format!("\\\\{}\\{}", segments[0], segments[1])));
            start_idx = 2;
        } else {
            return Vec::new();
        }
    } else {
        current_paths.push(PathBuf::from("."));
    }

    for &seg in &segments[start_idx..] {
        let mut next_paths = Vec::new();

        if !seg.contains('*') && !seg.contains('?') {
            for cp in current_paths {
                let candidate = cp.join(seg);
                if candidate.exists() {
                    next_paths.push(candidate);
                }
            }
        } else {
            let regex_pattern = format!(
                "(?i)^{}$",
                regex::escape(seg)
                    .replace("\\*", ".*")
                    .replace("\\?", ".")
            );
            if let Ok(re) = regex::Regex::new(&regex_pattern) {
                for cp in current_paths {
                    if let Ok(entries) = std::fs::read_dir(&cp) {
                        for entry in entries.flatten() {
                            if let Ok(name) = entry.file_name().into_string() {
                                if re.is_match(&name) {
                                    next_paths.push(entry.path());
                                }
                            }
                        }
                    }
                }
            }
        }

        current_paths = next_paths;
        if current_paths.is_empty() {
            break;
        }
    }

    current_paths
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_resolve_temp_path() {
        let paths = resolve_path_patterns("%LOCALAPPDATA%\\Temp");
        assert!(!paths.is_empty(), "Temp directory should resolve");
    }

    #[test]
    fn test_resolve_wildcard_segments() {
        let paths = resolve_path_patterns("%LOCALAPPDATA%\\*");
        assert!(!paths.is_empty(), "Local appdata wildcard should resolve multiple folders");
    }
}
