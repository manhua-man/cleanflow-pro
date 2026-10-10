use crate::fuzzy_matcher::MatchQuality;
use crate::search_index::VolumeIndex;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ParsedSearchQuery {
    pub raw_query: String,
    pub terms: Vec<String>,
    pub in_directory: Option<String>,
    pub extension: Option<String>,
    pub min_size: Option<u64>,
    pub max_size: Option<u64>,
    pub only_dirs: bool,
    pub only_files: bool,
    pub limit: usize,
    // Pro Features: RegEx and Noise Shielding
    pub regex_pattern: Option<String>,
    pub shield_noise: bool,
    pub category: Option<String>,
}

pub fn tokenize_query_string(input: &str) -> Vec<String> {
    let mut tokens = Vec::new();
    let mut current = String::new();
    let mut in_quotes = false;

    for c in input.chars() {
        if c == '"' {
            in_quotes = !in_quotes;
            current.push(c);
        } else if c.is_whitespace() && !in_quotes {
            if !current.is_empty() {
                tokens.push(current);
                current = String::new();
            }
        } else {
            current.push(c);
        }
    }
    if !current.is_empty() {
        tokens.push(current);
    }
    tokens
}

impl ParsedSearchQuery {
    pub fn parse(input: &str) -> Self {
        let trimmed = input.trim();
        let mut terms = Vec::new();
        let mut in_dir = None;
        let mut ext = None;
        let mut min_size = None;
        let mut max_size = None;
        let mut only_dirs = false;
        let mut only_files = false;
        let mut regex_pattern = None;
        let mut shield_noise = true; // Enabled by default
        let mut category = None;
        let mut limit = 200;

        for part in tokenize_query_string(trimmed) {
            let lower = part.to_lowercase();
            if lower.starts_with("in:") {
                let path = part[3..].trim_matches('"').to_string();
                in_dir = Some(path);
            } else if lower.starts_with("ext:") {
                let extension = part[4..].trim_start_matches('.').to_lowercase();
                ext = Some(extension);
            } else if lower.starts_with("regex:") {
                regex_pattern = Some(part[6..].to_string());
            } else if lower == "noise:all" || lower == "shield:off" || lower == "noise:show" {
                shield_noise = false;
            } else if lower.starts_with("size:>=") {
                min_size = parse_size_str(&part[7..]);
            } else if lower.starts_with("size:<=") {
                max_size = parse_size_str(&part[7..]);
            } else if lower.starts_with("size:>") {
                min_size = parse_size_str(&part[6..]);
            } else if lower.starts_with("size:<") {
                max_size = parse_size_str(&part[6..]);
            } else if lower.starts_with("size:") {
                let range_val = &part[5..];
                if let Some((low_s, high_s)) = range_val.split_once("..").or_else(|| range_val.split_once('-')) {
                    min_size = parse_size_str(low_s);
                    max_size = parse_size_str(high_s);
                } else {
                    min_size = parse_size_str(range_val);
                }
            } else if (lower.starts_with('>') || lower.starts_with('<'))
                && lower.chars().skip(1).any(|c| c.is_ascii_digit())
                && (lower.ends_with('b') || lower.ends_with('k') || lower.ends_with("kb") || lower.ends_with('m') || lower.ends_with("mb") || lower.ends_with('g') || lower.ends_with("gb"))
            {
                if lower.starts_with('>') {
                    min_size = parse_size_str(&part[1..]);
                } else {
                    max_size = parse_size_str(&part[1..]);
                }
            } else if lower.starts_with("category:") || lower.starts_with("cat:") {
                let cat = if lower.starts_with("category:") { &lower[9..] } else { &lower[4..] };
                category = Some(cat.to_string());
            } else if lower.starts_with("pic:") || lower.starts_with("picture:") {
                category = Some("pic".to_string());
                let rest = if lower.starts_with("pic:") { &part[4..] } else { &part[8..] };
                if !rest.is_empty() { terms.push(rest.to_string()); }
            } else if lower.starts_with("doc:") || lower.starts_with("document:") {
                category = Some("doc".to_string());
                let rest = if lower.starts_with("doc:") { &part[4..] } else { &part[9..] };
                if !rest.is_empty() { terms.push(rest.to_string()); }
            } else if lower.starts_with("video:") {
                category = Some("video".to_string());
                let rest = &part[6..];
                if !rest.is_empty() { terms.push(rest.to_string()); }
            } else if lower.starts_with("audio:") || lower.starts_with("music:") {
                category = Some("audio".to_string());
                let rest = if lower.starts_with("audio:") { &part[6..] } else { &part[6..] };
                if !rest.is_empty() { terms.push(rest.to_string()); }
            } else if lower.starts_with("folder:") || lower.starts_with("dir:") {
                category = Some("folder".to_string());
                only_dirs = true;
                let rest = if lower.starts_with("folder:") { &part[7..] } else { &part[4..] };
                if !rest.is_empty() { terms.push(rest.to_string()); }
            } else if lower.starts_with("archive:") || lower.starts_with("zip:") {
                category = Some("archive".to_string());
                let rest = if lower.starts_with("archive:") { &part[8..] } else { &part[4..] };
                if !rest.is_empty() { terms.push(rest.to_string()); }
            } else if lower.starts_with("app:") || lower.starts_with("exe:") {
                category = Some("app".to_string());
                let rest = if lower.starts_with("app:") { &part[4..] } else { &part[4..] };
                if !rest.is_empty() { terms.push(rest.to_string()); }
            } else if lower == "type:dir" || lower == "kind:dir" || lower == "kind:folder" {
                only_dirs = true;
                category = Some("folder".to_string());
            } else if lower == "type:file" || lower == "kind:file" {
                only_files = true;
            } else if lower.starts_with("limit:") || lower.starts_with("count:") {
                let num_str = if lower.starts_with("limit:") { &part[6..] } else { &part[6..] };
                if let Ok(n) = num_str.parse::<usize>() {
                    limit = n.clamp(1, 10000);
                }
            } else {
                let clean_term = part.trim_matches('"').to_string();
                if !clean_term.is_empty() {
                    terms.push(clean_term);
                }
            }
        }

        ParsedSearchQuery {
            raw_query: trimmed.to_string(),
            terms,
            in_directory: in_dir,
            extension: ext,
            min_size,
            max_size,
            only_dirs,
            only_files,
            limit,
            regex_pattern,
            shield_noise,
            category,
        }
    }
}

pub fn matches_category(name: &str, is_dir: bool, category: &str) -> bool {
    let lower_cat = category.to_lowercase();
    match lower_cat.as_str() {
        "all" => true,
        "folder" | "dir" => is_dir,
        "doc" | "document" => {
            if is_dir { return false; }
            let lower = name.to_lowercase();
            const DOC_EXTS: &[&str] = &["doc", "docx", "pdf", "txt", "xlsx", "xls", "pptx", "ppt", "md", "csv", "rtf", "epub"];
            DOC_EXTS.iter().any(|ext| lower.ends_with(&format!(".{}", ext)))
        }
        "pic" | "picture" | "image" => {
            if is_dir { return false; }
            let lower = name.to_lowercase();
            const PIC_EXTS: &[&str] = &["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg", "ico", "psd", "ai", "tiff", "raw"];
            PIC_EXTS.iter().any(|ext| lower.ends_with(&format!(".{}", ext)))
        }
        "video" => {
            if is_dir { return false; }
            let lower = name.to_lowercase();
            const VIDEO_EXTS: &[&str] = &["mp4", "mkv", "avi", "mov", "wmv", "flv", "rmvb", "webm", "m4v"];
            VIDEO_EXTS.iter().any(|ext| lower.ends_with(&format!(".{}", ext)))
        }
        "audio" | "music" => {
            if is_dir { return false; }
            let lower = name.to_lowercase();
            const AUDIO_EXTS: &[&str] = &["mp3", "wav", "flac", "aac", "m4a", "ogg", "wma"];
            AUDIO_EXTS.iter().any(|ext| lower.ends_with(&format!(".{}", ext)))
        }
        "archive" | "zip" => {
            if is_dir { return false; }
            let lower = name.to_lowercase();
            const ARCHIVE_EXTS: &[&str] = &["zip", "rar", "7z", "tar", "gz", "bz2", "iso"];
            ARCHIVE_EXTS.iter().any(|ext| lower.ends_with(&format!(".{}", ext)))
        }
        "app" | "exe" => {
            if is_dir { return false; }
            let lower = name.to_lowercase();
            const APP_EXTS: &[&str] = &["exe", "lnk", "bat", "cmd", "msi"];
            APP_EXTS.iter().any(|ext| lower.ends_with(&format!(".{}", ext)))
        }
        _ => true,
    }
}

pub fn is_dev_noise_path(path: &str) -> bool {
    let lower = path.to_lowercase();
    lower.contains("\\node_modules\\")
        || lower.contains("\\.git\\")
        || lower.contains("\\target\\debug\\")
        || lower.contains("\\target\\release\\")
        || lower.contains("\\.venv\\")
        || lower.contains("\\venv\\")
        || lower.contains("\\__pycache__\\")
        || lower.contains("\\vendor\\bundle\\")
        || lower.contains("\\appdata\\local\\temp\\")
}

pub fn is_high_priority_path(path: &str) -> bool {
    let lower = path.to_lowercase();
    lower.contains("\\projects\\")
        || lower.contains("\\src\\")
        || lower.contains("\\documents\\")
        || lower.contains("\\desktop\\")
        || lower.contains("\\repos\\")
        || lower.contains("\\workspace\\")
}

fn parse_size_str(s: &str) -> Option<u64> {
    let lower = s.trim().replace(' ', "").to_lowercase();
    let num_str: String = lower.chars().take_while(|c| c.is_ascii_digit() || *c == '.').collect();
    let val: f64 = num_str.parse().ok()?;

    if lower.ends_with("gb") || lower.ends_with("g") {
        Some((val * 1024.0 * 1024.0 * 1024.0) as u64)
    } else if lower.ends_with("mb") || lower.ends_with("m") {
        Some((val * 1024.0 * 1024.0) as u64)
    } else if lower.ends_with("kb") || lower.ends_with("k") {
        Some((val * 1024.0) as u64)
    } else {
        Some(val as u64)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SearchResultHit {
    pub name: String,
    pub path: String,
    pub size_bytes: u64,
    pub is_dir: bool,
    pub modified_timestamp: u64,
    pub score: i32,
    pub match_quality: MatchQuality,
    // CleanFlow Action Bridge Capabilities
    pub can_junction_migrate: bool,
    pub can_block_clone: bool,
    pub can_check_lock: bool,
    // Favorite & Alias Metadata
    pub is_favorite: bool,
    pub favorite_alias: Option<String>,
}

pub fn execute_search(
    indexes: &[VolumeIndex],
    query: &ParsedSearchQuery,
) -> Vec<SearchResultHit> {
    let compiled_regex = query
        .regex_pattern
        .as_ref()
        .and_then(|p| regex::RegexBuilder::new(p).case_insensitive(true).build().ok());

    let excl_rules = crate::exclusions::get_global_exclusion_manager()
        .read()
        .ok()
        .map(|guard| guard.clone());

    let (fav_map, all_favs) = if let Ok(fav_guard) = crate::favorites::get_global_favorites().read() {
        let all = fav_guard.list_all();
        let mut map = std::collections::HashMap::new();
        for f in &all {
            let norm = f.path.trim_end_matches(['\\', '/']).to_lowercase();
            map.insert(norm, f.alias.clone());
        }
        (map, all)
    } else {
        (std::collections::HashMap::new(), Vec::new())
    };

    let mut all_hits: Vec<SearchResultHit> = indexes
        .par_iter()
        .flat_map(|vol_idx| {
            let is_refs = vol_idx.fs_type.eq_ignore_ascii_case("ReFS");

            vol_idx
                .entries
                .par_iter()
                .filter_map(|entry| {
                    // 1. Noise shield filter (Listary Pro & fsearch alignment)
                    if query.shield_noise && is_dev_noise_path(&entry.path) {
                        let explicitly_searched = query.terms.iter().any(|t| {
                            t.contains("node_modules")
                                || t.contains(".git")
                                || t.contains("target")
                                || t.contains("venv")
                        });
                        if !explicitly_searched {
                            return None;
                        }
                    }

                    // 1.5 Custom user exclusions filter (fsearch 5.1 & 5.2 parity)
                    if let Some(ref excl) = excl_rules {
                        if excl.matches_path(&entry.path) {
                            return None;
                        }
                    }

                    // 2. Directory constraint
                    if let Some(ref req_dir) = query.in_directory {
                        if !entry.path.to_lowercase().starts_with(&req_dir.to_lowercase()) {
                            return None;
                        }
                    }

                    // 3. Type constraints
                    if query.only_dirs && !entry.is_dir {
                        return None;
                    }
                    if query.only_files && entry.is_dir {
                        return None;
                    }

                    // 3.5. Category macro constraints (Filter Chips)
                    if let Some(ref cat) = query.category {
                        if !matches_category(&entry.name, entry.is_dir, cat) {
                            return None;
                        }
                    }

                    // 4. Size constraints
                    if let Some(min_s) = query.min_size {
                        if entry.size_bytes < min_s {
                            return None;
                        }
                    }
                    if let Some(max_s) = query.max_size {
                        if entry.size_bytes > max_s {
                            return None;
                        }
                    }

                    // 5. Extension constraint
                    if let Some(ref req_ext) = query.extension {
                        if !entry.name.to_lowercase().ends_with(&format!(".{}", req_ext)) {
                            return None;
                        }
                    }

                    // 6. RegEx filter (fsearch Pro parity)
                    if let Some(ref re) = compiled_regex {
                        if !re.is_match(&entry.name) && !re.is_match(&entry.path) {
                            return None;
                        }
                    }

                    // 7. Query term matching & Priority Boost (Pinyin Aware)
                    let (best_quality, mut total_score) = if query.terms.is_empty() {
                        if compiled_regex.is_some() {
                            (MatchQuality::Exact, 120)
                        } else {
                            (MatchQuality::Exact, 100)
                        }
                    } else {
                        let mut quality = MatchQuality::None;
                        let mut sum_score = 0;

                        for term in &query.terms {
                            let match_res = crate::pinyin_matcher::score_pinyin_aware_match(&entry.name, term);
                            if match_res.quality == MatchQuality::None {
                                // If base name doesn't match, check full path
                                let path_match = crate::pinyin_matcher::score_pinyin_aware_match(&entry.path, term);
                                if path_match.quality == MatchQuality::None {
                                    return None;
                                }
                                sum_score += path_match.score / 2;
                                quality = path_match.quality;
                            } else {
                                sum_score += match_res.score;
                                quality = match_res.quality;
                            }
                        }

                        (quality, sum_score)
                    };

                    if total_score <= 0 {
                        return None;
                    }

                    // Priority Boost: grant +25 score bonus to user projects and work documents
                    if is_high_priority_path(&entry.path) {
                        total_score += 25;
                    }

                    // Favorite Folder Enrichment & Priority Boost
                    let norm = entry.path.trim_end_matches(['\\', '/']).to_lowercase();
                    let (is_fav, fav_alias) = if let Some(alias_opt) = fav_map.get(&norm) {
                        (true, alias_opt.clone())
                    } else {
                        (false, None)
                    };

                    if is_fav {
                        total_score += 40;
                    }

                    // Action Bridge Enrichment
                    let can_junction_migrate = entry.is_dir || entry.size_bytes > 50 * 1024 * 1024;
                    let can_block_clone = is_refs && !entry.is_dir;
                    let can_check_lock = !entry.is_dir;

                    Some(SearchResultHit {
                        name: entry.name.clone(),
                        path: entry.path.clone(),
                        size_bytes: entry.size_bytes,
                        is_dir: entry.is_dir,
                        modified_timestamp: entry.modified_timestamp,
                        score: total_score,
                        match_quality: best_quality,
                        can_junction_migrate,
                        can_block_clone,
                        can_check_lock,
                        is_favorite: is_fav,
                        favorite_alias: fav_alias,
                    })
                })
                .collect::<Vec<_>>()
        })
        .collect();

    // Direct Favorite Alias Injection: If user typed an alias, guarantee favorite appears at top
    for term in &query.terms {
        let clean_t = if term.starts_with("fav:") { &term[4..] } else { term.as_str() };
        if let Some(fav) = all_favs.iter().find(|f| f.alias.as_deref().map(|a| a.eq_ignore_ascii_case(clean_t)).unwrap_or(false)) {
            if !all_hits.iter().any(|h| h.path.eq_ignore_ascii_case(&fav.path)) {
                all_hits.push(SearchResultHit {
                    name: fav.name.clone(),
                    path: fav.path.clone(),
                    size_bytes: 0,
                    is_dir: true,
                    modified_timestamp: 0,
                    score: 350,
                    match_quality: MatchQuality::Exact,
                    can_junction_migrate: true,
                    can_block_clone: false,
                    can_check_lock: false,
                    is_favorite: true,
                    favorite_alias: fav.alias.clone(),
                });
            }
        }
    }

    // Sort by score descending, then by path
    all_hits.sort_by(|a, b| b.score.cmp(&a.score));

    if all_hits.len() > query.limit {
        all_hits.truncate(query.limit);
    }

    all_hits
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::search_index::CompactFileEntry;

    #[test]
    fn test_parse_search_query() {
        let q = ParsedSearchQuery::parse("cagro.toml in:C:\\Users\\ ext:toml size:>1mb regex:^c.*");
        assert_eq!(q.terms, vec!["cagro.toml".to_string()]);
        assert_eq!(q.in_directory, Some("C:\\Users\\".to_string()));
        assert_eq!(q.extension, Some("toml".to_string()));
        assert_eq!(q.min_size, Some(1024 * 1024));
        assert_eq!(q.regex_pattern, Some("^c.*".to_string()));
        assert!(q.shield_noise);
    }

    #[test]
    fn test_execute_search_fuzzy_and_actions() {
        let vol_idx = VolumeIndex {
            drive_letter: 'C',
            label: "System".to_string(),
            fs_type: "NTFS".to_string(),
            is_mft_accelerated: true,
            last_indexed_epoch: 1000,
            duration_ms: 10,
            entries: vec![
                CompactFileEntry {
                    id: 1,
                    name: "cargo.toml".to_string(),
                    path: "C:\\Projects\\cargo.toml".to_string(),
                    size_bytes: 2048,
                    is_dir: false,
                    modified_timestamp: 100,
                },
                CompactFileEntry {
                    id: 2,
                    name: "main.rs".to_string(),
                    path: "C:\\Projects\\src\\main.rs".to_string(),
                    size_bytes: 4096,
                    is_dir: false,
                    modified_timestamp: 100,
                },
            ],
        };

        // Query with typo: "cagro.toml" should find "cargo.toml"
        let q_typo = ParsedSearchQuery::parse("cagro.toml");
        let hits = execute_search(&[vol_idx], &q_typo);
        assert!(!hits.is_empty(), "Typo query cagro.toml must find cargo.toml");
        assert_eq!(hits[0].name, "cargo.toml");
        assert_eq!(hits[0].match_quality, MatchQuality::TypoTolerant);
        assert!(hits[0].can_check_lock);
    }

    #[test]
    fn test_regex_search_and_noise_shield() {
        let vol_idx = VolumeIndex {
            drive_letter: 'C',
            label: "System".to_string(),
            fs_type: "NTFS".to_string(),
            is_mft_accelerated: true,
            last_indexed_epoch: 1000,
            duration_ms: 10,
            entries: vec![
                CompactFileEntry {
                    id: 1,
                    name: "package.json".to_string(),
                    path: "C:\\Projects\\app\\node_modules\\lodash\\package.json".to_string(),
                    size_bytes: 1024,
                    is_dir: false,
                    modified_timestamp: 100,
                },
                CompactFileEntry {
                    id: 2,
                    name: "package.json".to_string(),
                    path: "C:\\Projects\\app\\package.json".to_string(),
                    size_bytes: 2048,
                    is_dir: false,
                    modified_timestamp: 100,
                },
            ],
        };

        // Query with noise shield: node_modules file should be excluded
        let q_shield = ParsedSearchQuery::parse("package.json");
        let hits_shield = execute_search(&[vol_idx.clone()], &q_shield);
        assert_eq!(hits_shield.len(), 1);
        assert_eq!(hits_shield[0].path, "C:\\Projects\\app\\package.json");

        // RegEx search
        let q_regex = ParsedSearchQuery::parse("regex:^package\\..*");
        let hits_regex = execute_search(&[vol_idx], &q_regex);
        assert_eq!(hits_regex.len(), 1);
    }

    #[test]
    fn test_advanced_size_query_parsing() {
        let q1 = ParsedSearchQuery::parse("video size:>100mb");
        assert_eq!(q1.min_size, Some(100 * 1024 * 1024));

        let q2 = ParsedSearchQuery::parse("doc size:<=500kb");
        assert_eq!(q2.max_size, Some(500 * 1024));

        let q3 = ParsedSearchQuery::parse("archive size:10mb..50mb");
        assert_eq!(q3.min_size, Some(10 * 1024 * 1024));
        assert_eq!(q3.max_size, Some(50 * 1024 * 1024));

        let q4 = ParsedSearchQuery::parse(">1gb");
        assert_eq!(q4.min_size, Some(1024 * 1024 * 1024));

        let q5 = ParsedSearchQuery::parse("test limit:500");
        assert_eq!(q5.limit, 500);

        let q6 = ParsedSearchQuery::parse("music count:1000");
        assert_eq!(q6.limit, 1000);
    }

    #[test]
    fn test_quote_aware_query_parsing() {
        let q = ParsedSearchQuery::parse("in:\"C:\\Program Files\" \"visual studio code\" ext:exe");
        assert_eq!(q.in_directory, Some("C:\\Program Files".to_string()));
        assert_eq!(q.terms, vec!["visual studio code".to_string()]);
        assert_eq!(q.extension, Some("exe".to_string()));
    }
}
