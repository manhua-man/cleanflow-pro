use md5::{Digest, Md5};
use std::fs::{self, File};
use std::io::{Read, Write};
use std::time::Instant;

const BENCH_PAYLOAD_MB: usize = 64; // 64 MB test payload

fn bench_hashing_throughput() {
    println!("[Benchmark 1] Core Hashing Throughput: MD5 vs BLAKE3");
    println!("------------------------------------------------------------");
    let total_bytes = BENCH_PAYLOAD_MB * 1024 * 1024;
    println!("Allocating {} MB test stream payload in memory...", BENCH_PAYLOAD_MB);
    
    // Create non-trivial deterministic buffer
    let mut data = vec![0u8; total_bytes];
    for (i, b) in data.iter_mut().enumerate() {
        *b = (i % 251) as u8;
    }

    // 1. MD5 Benchmark
    let start_md5 = Instant::now();
    let mut md5_hasher = Md5::new();
    let chunk_size = 128 * 1024;
    for chunk in data.chunks(chunk_size) {
        md5_hasher.update(chunk);
    }
    let md5_digest = md5_hasher.finalize();
    let md5_duration = start_md5.elapsed();
    let md5_mb_per_sec = (BENCH_PAYLOAD_MB as f64) / md5_duration.as_secs_f64();
    let md5_hex = hex::encode(md5_digest);

    println!("  MD5 (Legacy v0.1/v0.2):");
    println!("    Time:       {:>8.2} ms", md5_duration.as_secs_f64() * 1000.0);
    println!("    Throughput: {:>8.2} MB/s", md5_mb_per_sec);
    println!("    Digest:     {} (32 hex chars)", &md5_hex[0..16]);

    // 2. BLAKE3 Benchmark
    let start_b3 = Instant::now();
    let mut b3_hasher = blake3::Hasher::new();
    for chunk in data.chunks(chunk_size) {
        b3_hasher.update(chunk);
    }
    let b3_digest = b3_hasher.finalize();
    let b3_duration = start_b3.elapsed();
    let b3_mb_per_sec = (BENCH_PAYLOAD_MB as f64) / b3_duration.as_secs_f64();
    let b3_hex = b3_digest.to_hex().to_string();

    println!("  BLAKE3 (v0.3.0 Engine):");
    println!("    Time:       {:>8.2} ms", b3_duration.as_secs_f64() * 1000.0);
    println!("    Throughput: {:>8.2} MB/s", b3_mb_per_sec);
    println!("    Digest:     {}... (64 hex chars)", &b3_hex[0..16]);

    let speedup = md5_duration.as_secs_f64() / b3_duration.as_secs_f64();
    println!("  -> Result: BLAKE3 is {:.2}x faster than MD5 ({:.1}% speedup)\n", speedup, (speedup - 1.0) * 100.0);
}

fn bench_pipeline_io_reduction() {
    println!("[Benchmark 2] Deduplication Pipeline I/O & Latency Reduction");
    println!("------------------------------------------------------------");
    println!("Simulating 20 candidate files of 4 MB each (total candidate volume: 80 MB)");
    println!("Setup: 16 files have different headers; 4 files are exact duplicates.");

    let temp_dir = std::env::temp_dir().join("cleanflow_bench_pipeline");
    let _ = fs::remove_dir_all(&temp_dir);
    fs::create_dir_all(&temp_dir).unwrap();

    let file_size = 4 * 1024 * 1024; // 4 MB each
    let mut files = Vec::new();

    // 16 distinct files
    for i in 0..16 {
        let p = temp_dir.join(format!("distinct_{}.bin", i));
        let mut f = File::create(&p).unwrap();
        let header = format!("DISTINCT_HEADER_SEQ_{:08}", i);
        f.write_all(header.as_bytes()).unwrap();
        let rem = file_size - header.len();
        f.write_all(&vec![0xAA; rem]).unwrap();
        files.push(p);
    }

    // 4 duplicate files
    let dup_header = b"IDENTICAL_DUP_HEADER_0000";
    for i in 0..4 {
        let p = temp_dir.join(format!("duplicate_{}.bin", i));
        let mut f = File::create(&p).unwrap();
        f.write_all(dup_header).unwrap();
        let rem = file_size - dup_header.len();
        f.write_all(&vec![0xBB; rem]).unwrap();
        files.push(p);
    }

    // Approach A: Legacy Single-Stage Full Hash (reads all 80 MB from disk)
    let start_legacy = Instant::now();
    let mut legacy_bytes_read = 0u64;
    for p in &files {
        let mut f = File::open(p).unwrap();
        let mut buf = [0u8; 64 * 1024];
        let mut hasher = Md5::new();
        while let Ok(n) = f.read(&mut buf) {
            if n == 0 { break; }
            hasher.update(&buf[..n]);
            legacy_bytes_read += n as u64;
        }
    }
    let duration_legacy = start_legacy.elapsed();

    // Approach B: v0.3.0 Three-Stage Pipeline (16KB Partial Head Hash -> Filter -> Full BLAKE3 on duplicates)
    let start_v3 = Instant::now();
    let mut v3_bytes_read = 0u64;

    // Stage 1: Partial 16KB head hash on all 20 files
    let mut head_matches: std::collections::HashMap<String, Vec<&std::path::PathBuf>> = std::collections::HashMap::new();
    for p in &files {
        let mut f = File::open(p).unwrap();
        let mut head_buf = [0u8; 16 * 1024];
        let n = f.read(&mut head_buf).unwrap();
        v3_bytes_read += n as u64;
        let mut hasher = blake3::Hasher::new();
        hasher.update(&head_buf[..n]);
        let h = hasher.finalize().to_hex().to_string();
        head_matches.entry(h).or_default().push(p);
    }

    // Stage 2: Only compute full BLAKE3 on candidate groups with >= 2 matching heads
    for (_head, paths) in head_matches {
        if paths.len() >= 2 {
            for p in paths {
                let mut f = File::open(p).unwrap();
                let mut buf = [0u8; 128 * 1024];
                let mut hasher = blake3::Hasher::new();
                while let Ok(n) = f.read(&mut buf) {
                    if n == 0 { break; }
                    hasher.update(&buf[..n]);
                    v3_bytes_read += n as u64;
                }
            }
        }
    }
    let duration_v3 = start_v3.elapsed();

    let legacy_mb = legacy_bytes_read as f64 / (1024.0 * 1024.0);
    let v3_mb = v3_bytes_read as f64 / (1024.0 * 1024.0);
    let io_saved_pct = (1.0 - (v3_bytes_read as f64 / legacy_bytes_read as f64)) * 100.0;
    let speedup = duration_legacy.as_secs_f64() / duration_v3.as_secs_f64();

    println!("  Approach A: Legacy Full-File Hashing (v0.1/v0.2):");
    println!("    Total I/O Read: {:>8.2} MB", legacy_mb);
    println!("    Latency:        {:>8.2} ms", duration_legacy.as_secs_f64() * 1000.0);

    println!("  Approach B: Three-Stage Partial Hash Pipeline (v0.3.0):");
    println!("    Total I/O Read: {:>8.2} MB (16KB heads + full only on 4 duplicate files)", v3_mb);
    println!("    Latency:        {:>8.2} ms", duration_v3.as_secs_f64() * 1000.0);

    println!("  -> Physical Disk I/O Saved: {:.1}% reduction", io_saved_pct);
    println!("  -> Pipeline Speedup:        {:.2}x faster\n", speedup);

    let _ = fs::remove_dir_all(&temp_dir);
}

fn bench_scan_throughput() {
    println!("[Benchmark 3] Hybrid Giant Files Scanner Throughput");
    println!("------------------------------------------------------------");
    let (elevated, active, _) = cleanflow::usn_scanner::check_usn_journal_status("C:");
    println!("  Environment Status: Elevation = {}, USN Active = {}", elevated, active);

    let start = Instant::now();
    let res = cleanflow::usn_scanner::scan_giant_files_hybrid(None, 100 * 1024 * 1024, 50);
    let elapsed = start.elapsed();

    let mut total_giant_bytes = 0u64;
    for f in &res.files {
        total_giant_bytes += f.size_bytes;
    }
    let total_gb = total_giant_bytes as f64 / (1024.0 * 1024.0 * 1024.0);

    println!("  Engine In Use:   {}", res.engine);
    println!("  Files Found:     {} files (> 100 MB)", res.files.len());
    println!("  Total Volume:    {:.2} GB", total_gb);
    println!("  Scan Duration:   {:.2} ms ({:.2} s)", elapsed.as_secs_f64() * 1000.0, elapsed.as_secs_f64());
    if elapsed.as_secs_f64() > 0.0 {
        println!("  Throughput Rate: {:.2} GB/s analyzed", total_gb / elapsed.as_secs_f64());
    }
}

fn main() {
    println!("============================================================");
    println!("CleanFlow Pro v0.3.0 Benchmark Suite");
    println!("Running on Windows x86_64 Hardware");
    println!("============================================================\n");

    bench_hashing_throughput();
    bench_pipeline_io_reduction();
    bench_scan_throughput();

    println!("============================================================");
    println!("Benchmark Suite Completed Successfully.");
    println!("============================================================");
}
