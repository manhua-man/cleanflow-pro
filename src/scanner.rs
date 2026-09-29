use crate::rules::{resolve_path_patterns, CleanRule, RuleCategory, RuleConfig};
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScanReport {
    pub total_size_bytes: u64,
    pub total_files: u64,
    pub categories: Vec<CategoryScanResult>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CategoryScanResult {
    pub id: String,
    pub name: String,
    pub description: String,
    pub risk_level: String,
    pub total_size_bytes: u64,
    pub total_files: u64,
    pub rules: Vec<RuleScanResult>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RuleScanResult {
    pub id: String,
    pub name: String,
    pub action: String,
    pub default_checked: bool,
    pub total_size_bytes: u64,
    pub total_files: u64,
    pub matched_paths: Vec<MatchedPathItem>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MatchedPathItem {
    pub path: String,
    pub size_bytes: u64,
    pub file_count: u64,
    pub is_dir: bool,
}

pub fn calculate_path_stats(path: &Path) -> (u64, u64) {
    if !path.exists() {
        return (0, 0);
    }

    if path.is_file() {
        let sz = path.metadata().map(|m| m.len()).unwrap_or(0);
        return (sz, 1);
    }

    let mut total_size = 0u64;
    let mut file_count = 0u64;

    for entry in jwalk::WalkDir::new(path).skip_hidden(false) {
        if let Ok(entry) = entry {
            if entry.file_type.is_file() {
                file_count += 1;
                if let Ok(meta) = entry.metadata() {
                    total_size += meta.len();
                }
            }
        }
    }

    (total_size, file_count)
}

pub fn scan_rule(rule: &CleanRule) -> RuleScanResult {
    let paths = resolve_path_patterns(&rule.path_pattern);
    let mut total_size = 0u64;
    let mut total_files = 0u64;
    let mut items = Vec::new();

    for p in paths {
        let (sz, count) = calculate_path_stats(&p);
        if sz > 0 || p.exists() {
            total_size += sz;
            total_files += count;
            items.push(MatchedPathItem {
                path: p.to_string_lossy().to_string(),
                size_bytes: sz,
                file_count: count,
                is_dir: p.is_dir(),
            });
        }
    }

    RuleScanResult {
        id: rule.id.clone(),
        name: rule.name.clone(),
        action: rule.action.clone(),
        default_checked: rule.default_checked,
        total_size_bytes: total_size,
        total_files,
        matched_paths: items,
    }
}

pub fn scan_category(category: &RuleCategory) -> CategoryScanResult {
    let rule_results: Vec<RuleScanResult> = category
        .rules
        .par_iter()
        .map(|r| scan_rule(r))
        .collect();

    let total_size = rule_results.iter().map(|r| r.total_size_bytes).sum();
    let total_files = rule_results.iter().map(|r| r.total_files).sum();

    CategoryScanResult {
        id: category.id.clone(),
        name: category.name.clone(),
        description: category.description.clone(),
        risk_level: category.risk_level.clone(),
        total_size_bytes: total_size,
        total_files,
        rules: rule_results,
    }
}

pub fn scan_all(config: &RuleConfig) -> ScanReport {
    let categories: Vec<CategoryScanResult> = config
        .categories
        .par_iter()
        .map(|cat| scan_category(cat))
        .collect();

    let total_size = categories.iter().map(|c| c.total_size_bytes).sum();
    let total_files = categories.iter().map(|c| c.total_files).sum();

    ScanReport {
        total_size_bytes: total_size,
        total_files,
        categories,
    }
}
