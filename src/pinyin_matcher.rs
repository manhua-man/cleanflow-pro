use crate::fuzzy_matcher::{score_fuzzy_match, MatchQuality, MatchScoreResult};
use pinyin::ToPinyin;

#[derive(Debug, Clone)]
pub struct PinyinShadow {
    pub initials: String,
    pub full: String,
}

/// Extracts initials and full pinyin strings for a given text.
/// For ASCII characters, characters are kept as lowercase.
pub fn extract_pinyin_shadow(text: &str) -> PinyinShadow {
    let mut initials = String::with_capacity(text.len());
    let mut full = String::with_capacity(text.len() * 4);

    for ch in text.chars() {
        if let Some(p) = ch.to_pinyin() {
            let plain = p.plain();
            if let Some(first_char) = plain.chars().next() {
                initials.push(first_char);
            }
            full.push_str(plain);
        } else {
            let lower = ch.to_ascii_lowercase();
            initials.push(lower);
            full.push(lower);
        }
    }

    PinyinShadow { initials, full }
}

/// Checks whether a string contains at least one Chinese (CJK) character.
pub fn contains_chinese(text: &str) -> bool {
    text.chars().any(|c| ('\u{4e00}'..='\u{9fa5}').contains(&c))
}

/// Performs a pinyin-aware fuzzy match against target text.
/// 1. Tries direct fuzzy match against target first.
/// 2. If no direct match and target contains Chinese while query is ASCII, tries matching against pinyin initials and full pinyin.
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

    // 1. Pinyin initials match (e.g. "jsq" vs "jsq.exe")
    if shadow.initials.starts_with(&norm_query) {
        return MatchScoreResult {
            quality: MatchQuality::Prefix,
            score: 750 + (norm_query.len() * 10) as i32,
            matched_ranges: vec![(0, norm_query.len())],
        };
    }

    // 2. Full pinyin match (e.g. "jisuanqi" vs "jisuanqi.exe")
    if shadow.full.starts_with(&norm_query) {
        return MatchScoreResult {
            quality: MatchQuality::Prefix,
            score: 720 + (norm_query.len() * 8) as i32,
            matched_ranges: vec![(0, norm_query.len())],
        };
    }

    // 3. Substring match in pinyin initials
    if let Some(idx) = shadow.initials.find(&norm_query) {
        return MatchScoreResult {
            quality: MatchQuality::FuzzySubsequence,
            score: 550 + (norm_query.len() * 5) as i32,
            matched_ranges: vec![(idx, idx + norm_query.len())],
        };
    }

    // 4. Substring match in full pinyin
    if let Some(idx) = shadow.full.find(&norm_query) {
        return MatchScoreResult {
            quality: MatchQuality::FuzzySubsequence,
            score: 500 + (norm_query.len() * 5) as i32,
            matched_ranges: vec![(idx, idx + norm_query.len())],
        };
    }

    // 5. Fuzzy subsequence match on initials (e.g. "jq" in "jsq")
    let init_res = score_fuzzy_match(&shadow.initials, &norm_query);
    if init_res.quality != MatchQuality::None {
        return MatchScoreResult {
            quality: MatchQuality::FuzzySubsequence,
            score: (init_res.score * 8) / 10, // slight discount for pinyin fuzzy
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
}
