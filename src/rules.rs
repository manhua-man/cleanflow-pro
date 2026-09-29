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

    // Split parent directory and glob pattern
    let path = Path::new(&expanded);
    let parent = match path.parent() {
        Some(p) if p.exists() => p,
        _ => return Vec::new(),
    };

    let file_pattern = match path.file_name().and_then(|n| n.to_str()) {
        Some(f) => f,
        None => return Vec::new(),
    };

    let regex_pattern = format!(
        "^{}$",
        regex::escape(file_pattern)
            .replace("\\*", ".*")
            .replace("\\?", ".")
    );

    let re = match regex::Regex::new(&regex_pattern) {
        Ok(r) => r,
        Err(_) => return Vec::new(),
    };

    let mut matches = Vec::new();
    if let Ok(entries) = std::fs::read_dir(parent) {
        for entry in entries.flatten() {
            if let Ok(name) = entry.file_name().into_string() {
                if re.is_match(&name) {
                    matches.push(entry.path());
                }
            }
        }
    }

    matches
}
