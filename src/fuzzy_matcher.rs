use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum MatchQuality {
    Exact,
    Prefix,
    Suffix,
    FuzzySubsequence,
    TypoTolerant, // 1-edit typo
    None,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MatchScoreResult {
    pub quality: MatchQuality,
    pub score: i32,
    pub matched_ranges: Vec<(usize, usize)>,
}

pub fn is_one_edit_away(s1: &str, s2: &str) -> bool {
    let len1 = s1.chars().count();
    let len2 = s2.chars().count();

    if (len1 as isize - len2 as isize).abs() > 1 {
        return false;
    }

    let c1: Vec<char> = s1.chars().collect();
    let c2: Vec<char> = s2.chars().collect();

    let mut i = 0;
    let mut j = 0;
    let mut edits = 0;

    while i < len1 && j < len2 {
        if c1[i] != c2[j] {
            edits += 1;
            if edits > 1 {
                return false;
            }

            if len1 > len2 {
                i += 1;
            } else if len2 > len1 {
                j += 1;
            } else {
                // Check adjacent transposition (e.g. "mian" vs "main")
                if i + 1 < len1 && j + 1 < len2 && c1[i] == c2[j + 1] && c1[i + 1] == c2[j] {
                    i += 2;
                    j += 2;
                    continue;
                }
                i += 1;
                j += 1;
            }
        } else {
            i += 1;
            j += 1;
        }
    }

    if i < len1 || j < len2 {
        edits += 1;
    }

    edits <= 1
}

pub fn score_fuzzy_match(target: &str, query: &str) -> MatchScoreResult {
    if query.is_empty() {
        return MatchScoreResult {
            quality: MatchQuality::Exact,
            score: 100,
            matched_ranges: Vec::new(),
        };
    }

    let is_smart_case = query.chars().all(|c| !c.is_alphabetic() || c.is_lowercase());

    let (norm_target, norm_query) = if is_smart_case {
        (target.to_lowercase(), query.to_lowercase())
    } else {
        (target.to_string(), query.to_string())
    };

    // 1. Exact Match
    if norm_target == norm_query {
        return MatchScoreResult {
            quality: MatchQuality::Exact,
            score: 1000,
            matched_ranges: vec![(0, target.len())],
        };
    }

    // 2. Prefix Match
    if norm_target.starts_with(&norm_query) {
        return MatchScoreResult {
            quality: MatchQuality::Prefix,
            score: 800 + (norm_query.len() * 10) as i32,
            matched_ranges: vec![(0, query.len())],
        };
    }

    // 3. Suffix Match
    if norm_target.ends_with(&norm_query) {
        let start = norm_target.len() - norm_query.len();
        return MatchScoreResult {
            quality: MatchQuality::Suffix,
            score: 600 + (norm_query.len() * 10) as i32,
            matched_ranges: vec![(start, target.len())],
        };
    }

    // 4. Substring Match
    if let Some(idx) = norm_target.find(&norm_query) {
        let mut score = 500;
        // Word boundary bonus
        if idx > 0 {
            let prev_char = norm_target.chars().nth(idx - 1).unwrap_or(' ');
            if prev_char == '_' || prev_char == '-' || prev_char == '.' || prev_char == ' ' || prev_char == '\\' {
                score += 150; // boundary bonus
            }
        }
        return MatchScoreResult {
            quality: MatchQuality::FuzzySubsequence,
            score: score + (norm_query.len() * 8) as i32,
            matched_ranges: vec![(idx, idx + norm_query.len())],
        };
    }

    // 5. Fuzzy Subsequence Match
    let target_chars: Vec<char> = norm_target.chars().collect();
    let query_chars: Vec<char> = norm_query.chars().collect();

    let mut q_idx = 0;
    let mut score = 0;
    let mut consecutive = 0;
    let mut matched_indices = Vec::new();

    for (t_idx, &tc) in target_chars.iter().enumerate() {
        if q_idx < query_chars.len() && tc == query_chars[q_idx] {
            matched_indices.push(t_idx);
            score += 10;
            consecutive += 1;
            score += consecutive * 5; // consecutive match bonus

            // Boundary bonus
            if t_idx == 0 || ['_', '-', '.', ' ', '\\'].contains(&target_chars[t_idx - 1]) {
                score += 30;
            }

            q_idx += 1;
        } else {
            consecutive = 0;
        }
    }

    if q_idx == query_chars.len() {
        return MatchScoreResult {
            quality: MatchQuality::FuzzySubsequence,
            score,
            matched_ranges: matched_indices.iter().map(|&i| (i, i + 1)).collect(),
        };
    }

    // 6. Typo Tolerance (fsearch inspired: for queries with >= 4 characters, forgive 1 edit)
    if query_chars.len() >= 4 {
        // Compare target base name against query
        let base_name = Path::new(target)
            .file_name()
            .and_then(|n| n.to_str())
            .unwrap_or(target);
        let norm_base = if is_smart_case {
            base_name.to_lowercase()
        } else {
            base_name.to_string()
        };

        if is_one_edit_away(&norm_base, &norm_query) {
            return MatchScoreResult {
                quality: MatchQuality::TypoTolerant,
                score: 250,
                matched_ranges: Vec::new(),
            };
        }

        // Also check if any dot/dash segment has 1-edit distance
        for token in norm_target.split(|c| c == '.' || c == '_' || c == '-' || c == ' ') {
            if token.len() >= 4 && is_one_edit_away(token, &norm_query) {
                return MatchScoreResult {
                    quality: MatchQuality::TypoTolerant,
                    score: 200,
                    matched_ranges: Vec::new(),
                };
            }
        }
    }

    MatchScoreResult {
        quality: MatchQuality::None,
        score: 0,
        matched_ranges: Vec::new(),
    }
}

use std::path::Path;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_exact_and_prefix_match() {
        let res_exact = score_fuzzy_match("Cargo.toml", "Cargo.toml");
        assert_eq!(res_exact.quality, MatchQuality::Exact);
        assert!(res_exact.score >= 1000);

        let res_prefix = score_fuzzy_match("cleanflow.exe", "clean");
        assert_eq!(res_prefix.quality, MatchQuality::Prefix);
        assert!(res_prefix.score >= 800);
    }

    #[test]
    fn test_fuzzy_subsequence_match() {
        let res_sub = score_fuzzy_match("src/mft_scanner.rs", "mftscan");
        assert_eq!(res_sub.quality, MatchQuality::FuzzySubsequence);
        assert!(res_sub.score > 0);
    }

    #[test]
    fn test_typo_tolerance_fsearch_parity() {
        // "mian.rs" should match "main.rs"
        let res_typo = score_fuzzy_match("main.rs", "mian.rs");
        assert_eq!(res_typo.quality, MatchQuality::TypoTolerant);
        assert!(res_typo.score > 0);

        // "cagro.toml" should match "cargo.toml"
        let res_cargo = score_fuzzy_match("cargo.toml", "cagro.toml");
        assert_eq!(res_cargo.quality, MatchQuality::TypoTolerant);

        // completely different string should NOT match
        let res_none = score_fuzzy_match("rustdesk.exe", "firefox.exe");
        assert_eq!(res_none.quality, MatchQuality::None);
    }
}
