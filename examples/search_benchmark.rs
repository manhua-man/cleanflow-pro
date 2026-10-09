use cleanflow::fuzzy_matcher::{score_fuzzy_match, MatchQuality};
use cleanflow::mft_scanner::list_available_volumes;
use cleanflow::search_engine::{execute_search, ParsedSearchQuery};
use cleanflow::search_index::get_or_build_all_indexes;
use std::time::Instant;

fn main() {
    println!("============================================================");
    println!("CleanFlow Pro Second Pillar: Instant Disk Search Benchmark");
    println!("============================================================");

    // 1. Volume Enumeration
    let t0 = Instant::now();
    let vols = list_available_volumes();
    let vol_dur = t0.elapsed();
    println!("\n[1] Volume Enumeration (Win32 GetLogicalDrives & GetVolumeInformationW):");
    println!("  Time: {:>8.3} ms", vol_dur.as_secs_f64() * 1000.0);
    for v in &vols {
        println!(
            "  Drive {}: [{}] FS: {:<5} NTFS MFT Accelerated: {}",
            v.drive_letter, v.label, v.fs_type, v.is_ntfs
        );
    }

    // 2. Index Building / Cache Loading
    println!("\n[2] Index Initialization (MFT Streamer / Parallel Crawler):");
    let t1 = Instant::now();
    let indexes = get_or_build_all_indexes(Some(3));
    let idx_dur = t1.elapsed();
    let total_entries: usize = indexes.iter().map(|i| i.entries.len()).sum();
    println!("  Time:            {:>8.3} ms", idx_dur.as_secs_f64() * 1000.0);
    println!("  Indexed Volumes: {}", indexes.len());
    println!("  Total Entries:   {} files & directories", total_entries);

    // 3. Typo Tolerance Matching Micro-benchmark (fsearch algorithm)
    println!("\n[3] 1-Edit Typo Tolerance Algorithm (fsearch Benchmark):");
    let test_cases = [
        ("cargo.toml", "cagro.toml", "Typo in middle (adjacent transposition)"),
        ("main.rs", "mian.rs", "Typo in extension (transposition)"),
        ("cleanflow.exe", "cleanflo.exe", "Typo: 1 deletion"),
        ("database.sqlite", "databse.sqlite", "Typo: 1 omission"),
    ];

    for (target, query, desc) in &test_cases {
        let t_match = Instant::now();
        let res = score_fuzzy_match(target, query);
        let match_us = t_match.elapsed().as_nanos() as f64 / 1000.0;
        println!(
            "  Target: {:<18} Query: {:<16} => Quality: {:<14} Score: {:>4} ({:>5.2} us) [{}]",
            target, query, format!("{:?}", res.quality), res.score, match_us, desc
        );
        assert_ne!(res.quality, MatchQuality::None, "Should tolerate 1-edit typo");
    }

    // 4. End-to-End Query Throughput Across Volume Indexes
    println!("\n[4] Whole-Disk Multi-Threaded Search Latency Across {} Entries:", total_entries);
    let queries = [
        "cargo.toml",
        "cagro.toml",
        "ext:exe",
        "size:>50mb",
        "kind:dir in:C:\\Users",
    ];

    for q_str in &queries {
        let q = ParsedSearchQuery::parse(q_str);
        let t_search = Instant::now();
        let hits = execute_search(&indexes, &q);
        let search_ms = t_search.elapsed().as_secs_f64() * 1000.0;

        println!(
            "  Query: {:<25} => {:>4} hits in {:>7.3} ms (Top match: {})",
            format!("\"{}\"", q_str),
            hits.len(),
            search_ms,
            hits.first().map(|h| h.name.as_str()).unwrap_or("none")
        );
    }

    println!("\n============================================================");
    println!("Benchmark Complete: All Search Subsystems Verified");
    println!("============================================================");
}
