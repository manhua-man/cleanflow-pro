use crate::fuzzy_matcher::{score_fuzzy_match, MatchQuality, MatchScoreResult};
use pinyin::ToPinyinMulti;

#[derive(Debug, Clone)]
pub struct PinyinShadow {
    pub initials: String,
    pub full: String,
    pub alt_initials: Vec<String>,
    pub alt_full: Vec<String>,
}

/// Normalizes compound initials (zh -> z, ch -> c, sh -> s) to match single-letter initials
pub fn normalize_compound_initials(query: &str) -> String {
    let lower = query.to_lowercase();
    let mut result = String::with_capacity(lower.len());
    let mut chars = lower.chars().peekable();

    while let Some(c) = chars.next() {
        if (c == 'z' || c == 'c' || c == 's') && chars.peek() == Some(&'h') {
            chars.next(); // skip 'h'
            result.push(c);
        } else {
            result.push(c);
        }
    }
    result
}

/// Extracts initials and full pinyin strings for a given text, including polyphonic variants.
pub fn extract_pinyin_shadow(text: &str) -> PinyinShadow {
    let mut primary_initials = String::with_capacity(text.len());
    let mut primary_full = String::with_capacity(text.len() * 4);
    let mut char_options: Vec<(Vec<char>, Vec<String>)> = Vec::with_capacity(text.len());

    for ch in text.chars() {
        if let Some(multi) = ch.to_pinyin_multi() {
            let mut inits: Vec<char> = Vec::new();
            let mut fulls: Vec<String> = Vec::new();

            for p in multi {
                let plain = p.plain();
                if let Some(first) = plain.chars().next() {
                    if !inits.contains(&first) {
                        inits.push(first);
                    }
                }
                let f_str = plain.to_string();
                if !fulls.contains(&f_str) {
                    fulls.push(f_str);
                }
            }

            if inits.is_empty() {
                let lower = ch.to_ascii_lowercase();
                inits.push(lower);
                fulls.push(lower.to_string());
            }

            primary_initials.push(inits[0]);
            primary_full.push_str(&fulls[0]);
            char_options.push((inits, fulls));
        } else {
            let lower = ch.to_ascii_lowercase();
            primary_initials.push(lower);
            primary_full.push(lower);
            char_options.push((vec![lower], vec![lower.to_string()]));
        }
    }

    // Generate alternative initials and full strings for polyphones (up to 4 variants)
    let mut alt_initials = Vec::new();
    let mut alt_full = Vec::new();

    for (i, (inits, fulls)) in char_options.iter().enumerate() {
        if inits.len() > 1 && alt_initials.len() < 4 {
            for alt_init in &inits[1..] {
                let mut alt_init_str = primary_initials.clone();
                if let Some(nth_byte_idx) = alt_init_str.char_indices().nth(i).map(|(idx, _)| idx) {
                    alt_init_str.replace_range(nth_byte_idx..nth_byte_idx + 1, &alt_init.to_string());
                    if !alt_initials.contains(&alt_init_str) && alt_init_str != primary_initials {
                        alt_initials.push(alt_init_str);
                    }
                }
            }
        }
        if fulls.len() > 1 && alt_full.len() < 4 {
            for alt_f in &fulls[1..] {
                let mut variant_full = String::with_capacity(primary_full.len());
                for (j, (_, f_list)) in char_options.iter().enumerate() {
                    if j == i {
                        variant_full.push_str(alt_f);
                    } else {
                        variant_full.push_str(&f_list[0]);
                    }
                }
                if !alt_full.contains(&variant_full) && variant_full != primary_full {
                    alt_full.push(variant_full);
                }
            }
        }
    }

    PinyinShadow {
        initials: primary_initials,
        full: primary_full,
        alt_initials,
        alt_full,
    }
}

/// Checks whether a string contains at least one Chinese (CJK) character.
pub fn contains_chinese(text: &str) -> bool {
    text.chars().any(|c| ('\u{4e00}'..='\u{9fa5}').contains(&c))
}

/// Performs a pinyin-aware fuzzy match against target text.
pub fn score_pinyin_aware_match(target: &str, query: &str) -> MatchScoreResult {
    let direct_res = score_fuzzy_match(target, query);
    if direct_res.quality != MatchQuality::None {
        return direct_res;
    }

    if query.is_empty() || !contains_chinese(target) {
        return direct_res;
    }

    let norm_query = query.to_lowercase();
    let shadow = extract_pinyin_shadow(target);

    // 1. Primary pinyin initials match (e.g. "jsq" vs "计算器.exe")
    if shadow.initials.starts_with(&norm_query) {
        return MatchScoreResult {
            quality: MatchQuality::Prefix,
            score: 750 + (norm_query.len() * 10) as i32,
            matched_ranges: vec![(0, norm_query.len())],
        };
    }

    // 1.5. Compound initials normalization (e.g. "zhw" -> "zw" matching "中文")
    let comp_query = normalize_compound_initials(&norm_query);
    if comp_query != norm_query && shadow.initials.starts_with(&comp_query) {
        return MatchScoreResult {
            quality: MatchQuality::Prefix,
            score: 740 + (comp_query.len() * 10) as i32,
            matched_ranges: vec![(0, comp_query.len())],
        };
    }

    // 1.8. Polyphonic alternative initials match (e.g. "cq" matching "重庆")
    for alt_init in &shadow.alt_initials {
        if alt_init.starts_with(&norm_query) || (comp_query != norm_query && alt_init.starts_with(&comp_query)) {
            return MatchScoreResult {
                quality: MatchQuality::Prefix,
                score: 735 + (norm_query.len() * 10) as i32,
                matched_ranges: vec![(0, norm_query.len())],
            };
        }
    }

    // 2. Full pinyin match (e.g. "jisuanqi" vs "jisuanqi.exe")
    if shadow.full.starts_with(&norm_query) {
        return MatchScoreResult {
            quality: MatchQuality::Prefix,
            score: 720 + (norm_query.len() * 8) as i32,
            matched_ranges: vec![(0, norm_query.len())],
        };
    }

    // 2.5. Polyphonic alternative full pinyin match (e.g. "chongqing" matching "重庆")
    for alt_f in &shadow.alt_full {
        if alt_f.starts_with(&norm_query) {
            return MatchScoreResult {
                quality: MatchQuality::Prefix,
                score: 710 + (norm_query.len() * 8) as i32,
                matched_ranges: vec![(0, norm_query.len())],
            };
        }
    }

    // 3. Substring match in primary or alternative pinyin initials
    if let Some(idx) = shadow.initials.find(&norm_query) {
        return MatchScoreResult {
            quality: MatchQuality::FuzzySubsequence,
            score: 550 + (norm_query.len() * 5) as i32,
            matched_ranges: vec![(idx, idx + norm_query.len())],
        };
    }
    for alt_init in &shadow.alt_initials {
        if let Some(idx) = alt_init.find(&norm_query) {
            return MatchScoreResult {
                quality: MatchQuality::FuzzySubsequence,
                score: 540 + (norm_query.len() * 5) as i32,
                matched_ranges: vec![(idx, idx + norm_query.len())],
            };
        }
    }

    // 4. Substring match in full pinyin
    if let Some(idx) = shadow.full.find(&norm_query) {
        return MatchScoreResult {
            quality: MatchQuality::FuzzySubsequence,
            score: 500 + (norm_query.len() * 5) as i32,
            matched_ranges: vec![(idx, idx + norm_query.len())],
        };
    }
    for alt_f in &shadow.alt_full {
        if let Some(idx) = alt_f.find(&norm_query) {
            return MatchScoreResult {
                quality: MatchQuality::FuzzySubsequence,
                score: 490 + (norm_query.len() * 5) as i32,
                matched_ranges: vec![(idx, idx + norm_query.len())],
            };
        }
    }

    // 5. Fuzzy subsequence match on initials (e.g. "jq" in "jsq")
    let init_res = score_fuzzy_match(&shadow.initials, &norm_query);
    if init_res.quality != MatchQuality::None {
        return MatchScoreResult {
            quality: MatchQuality::FuzzySubsequence,
            score: (init_res.score * 8) / 10,
            matched_ranges: Vec::new(),
        };
    }

    MatchScoreResult {
        quality: MatchQuality::None,
        score: 0,
        matched_ranges: Vec::new(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_pinyin_shadow() {
        let shadow = extract_pinyin_shadow("计算器.exe");
        assert_eq!(shadow.initials, "jsq.exe");
        assert_eq!(shadow.full, "jisuanqi.exe");

        let shadow2 = extract_pinyin_shadow("微信.lnk");
        assert_eq!(shadow2.initials, "wx.lnk");
        assert_eq!(shadow2.full, "weixin.lnk");
    }

    #[test]
    fn test_score_pinyin_aware_match() {
        // Initials prefix: "jsq" matches "计算器.exe"
        let res = score_pinyin_aware_match("计算器.exe", "jsq");
        assert_eq!(res.quality, MatchQuality::Prefix);
        assert!(res.score >= 750);

        // Full pinyin: "jisuanqi" matches "计算器.exe"
        let res_full = score_pinyin_aware_match("计算器.exe", "jisuanqi");
        assert_eq!(res_full.quality, MatchQuality::Prefix);
        assert!(res_full.score >= 720);

        // "wx" matches "微信.exe"
        let res_wx = score_pinyin_aware_match("微信.exe", "wx");
        assert_eq!(res_wx.quality, MatchQuality::Prefix);

        // "wz" matches "王者荣耀.exe"
        let res_wz = score_pinyin_aware_match("王者荣耀.exe", "wz");
        assert_eq!(res_wz.quality, MatchQuality::Prefix);

        // Direct Chinese input still matches directly
        let res_cn = score_pinyin_aware_match("计算器.exe", "计算");
        assert_eq!(res_cn.quality, MatchQuality::Prefix);
        assert!(res_cn.score >= 800);
    }

    #[test]
    fn test_to_pinyin_multi() {
        if let Some(multi) = '重'.to_pinyin_multi() {
            let list: Vec<&str> = multi.into_iter().map(|p| p.plain()).collect();
            assert!(list.contains(&"chong"));
            assert!(list.contains(&"zhong"));
        }
    }

    #[test]
    fn test_compound_initials_matching() {
        // "zhw" matches "中文.txt"
        let res_zh = score_pinyin_aware_match("中文.txt", "zhw");
        assert_eq!(res_zh.quality, MatchQuality::Prefix);
        assert!(res_zh.score >= 740);

        // "chq" matches "传奇.exe"
        let res_ch = score_pinyin_aware_match("传奇.exe", "chq");
        assert_eq!(res_ch.quality, MatchQuality::Prefix);
        assert!(res_ch.score >= 740);

        // "shj" matches "升级补丁.zip"
        let res_sh = score_pinyin_aware_match("升级补丁.zip", "shj");
        assert_eq!(res_sh.quality, MatchQuality::Prefix);
        assert!(res_sh.score >= 740);
    }

    #[test]
    fn test_polyphone_matching() {
        // "cq" and "zq" both match "重庆.pdf"
        let res_cq = score_pinyin_aware_match("重庆.pdf", "cq");
        let res_zq = score_pinyin_aware_match("重庆.pdf", "zq");
        assert_eq!(res_cq.quality, MatchQuality::Prefix);
        assert_eq!(res_zq.quality, MatchQuality::Prefix);

        // "yh" and "yx" both match "银行明细.xlsx"
        let res_yh = score_pinyin_aware_match("银行明细.xlsx", "yh");
        let res_yx = score_pinyin_aware_match("银行明细.xlsx", "yx");
        assert_eq!(res_yh.quality, MatchQuality::Prefix);
        assert_eq!(res_yx.quality, MatchQuality::Prefix);
    }
}
