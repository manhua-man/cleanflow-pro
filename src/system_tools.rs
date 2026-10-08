use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;
use std::process::Command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RecycleBinStats {
    pub size_bytes: u64,
    pub file_count: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemMaintenanceStatus {
    pub recycle_bin: RecycleBinStats,
    pub prefetch_size_bytes: u64,
    pub prefetch_files: u64,
    pub wer_size_bytes: u64,
    pub wer_files: u64,
}

pub fn get_recycle_bin_stats() -> RecycleBinStats {
    // Query C:\$Recycle.Bin via PowerShell for reliable permission traversal
    let script = r#"
        $ErrorActionPreference = 'SilentlyContinue'
        $drives = Get-PSDrive -PSProvider FileSystem | Select-Object -ExpandProperty Root
        $totalBytes = 0
        $totalCount = 0
        foreach ($d in $drives) {
            $rbPath = Join-Path $d '$Recycle.Bin'
            if (Test-Path $rbPath) {
                $measure = Get-ChildItem -Path $rbPath -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum
                if ($measure.Sum) { $totalBytes += $measure.Sum }
                if ($measure.Count) { $totalCount += $measure.Count }
            }
        }
        Write-Output "$totalBytes,$totalCount"
    "#;

    let output = Command::new("powershell")
        .args(["-NoProfile", "-Command", script])
        .output();

    if let Ok(out) = output {
        let text = String::from_utf8_lossy(&out.stdout).trim().to_string();
        let parts: Vec<&str> = text.split(',').collect();
        if parts.len() == 2 {
            let size = parts[0].trim().parse::<u64>().unwrap_or(0);
            let count = parts[1].trim().parse::<u64>().unwrap_or(0);
            return RecycleBinStats {
                size_bytes: size,
                file_count: count,
            };
        }
    }

    RecycleBinStats {
        size_bytes: 0,
        file_count: 0,
    }
}

pub fn empty_recycle_bin() -> Result<u64, String> {
    let before = get_recycle_bin_stats();

    let script = r#"
        $ErrorActionPreference = 'SilentlyContinue'
        try {
            $code = @"
using System;
using System.Runtime.InteropServices;
public class Win32RecycleBin {
    [DllImport("Shell32.dll", CharSet = CharSet.Unicode)]
    public static extern uint SHEmptyRecycleBin(IntPtr hwnd, string pszRootPath, uint dwFlags);
}
"@
            Add-Type -TypeDefinition $code -ErrorAction SilentlyContinue
            [Win32RecycleBin]::SHEmptyRecycleBin([IntPtr]::Zero, $null, 7) | Out-Null
        } catch {}

        try {
            Clear-RecycleBin -Force -ErrorAction SilentlyContinue
        } catch {}

        $drives = Get-PSDrive -PSProvider FileSystem | Select-Object -ExpandProperty Root
        foreach ($d in $drives) {
            $rbPath = Join-Path $d '$Recycle.Bin'
            if (Test-Path $rbPath) {
                Get-ChildItem -Path $rbPath -Recurse -Force -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
            }
        }
    "#;

    let _ = Command::new("powershell")
        .args(["-NoProfile", "-Command", script])
        .output();

    let after = get_recycle_bin_stats();
    let freed = if before.size_bytes > after.size_bytes {
        before.size_bytes - after.size_bytes
    } else {
        before.size_bytes
    };

    Ok(freed)
}

pub fn flush_dns() -> Result<String, String> {
    let output = Command::new("ipconfig")
        .arg("/flushdns")
        .output()
        .map_err(|e| format!("执行 ipconfig 失败: {}", e))?;

    if output.status.success() {
        let text = String::from_utf8_lossy(&output.stdout).trim().to_string();
        Ok(text)
    } else {
        let err = String::from_utf8_lossy(&output.stderr).trim().to_string();
        Err(if err.is_empty() { "刷新 DNS 缓存失败".to_string() } else { err })
    }
}

pub fn get_system_maintenance_status() -> SystemMaintenanceStatus {
    let rb = get_recycle_bin_stats();

    // Prefetch (C:\Windows\Prefetch)
    let prefetch_dir = Path::new(r"C:\Windows\Prefetch");
    let (prefetch_sz, prefetch_cnt) = crate::scanner::calculate_path_stats(prefetch_dir);

    // WER (C:\ProgramData\Microsoft\Windows\WER)
    let wer_dir = Path::new(r"C:\ProgramData\Microsoft\Windows\WER");
    let (wer_sz, wer_cnt) = crate::scanner::calculate_path_stats(wer_dir);

    SystemMaintenanceStatus {
        recycle_bin: rb,
        prefetch_size_bytes: prefetch_sz,
        prefetch_files: prefetch_cnt,
        wer_size_bytes: wer_sz,
        wer_files: wer_cnt,
    }
}

pub fn scan_empty_directories(target_dir: &str) -> Vec<String> {
    let mut empty_dirs = Vec::new();
    let root = Path::new(target_dir);
    if !root.exists() || !root.is_dir() {
        return empty_dirs;
    }

    // Traverse bottom-up (directories with 0 entries)
    if let Ok(entries) = fs::read_dir(root) {
        for entry in entries.flatten() {
            let p = entry.path();
            if p.is_dir() {
                // If sub-directory is empty
                if let Ok(mut sub_entries) = fs::read_dir(&p) {
                    if sub_entries.next().is_none() {
                        empty_dirs.push(p.to_string_lossy().to_string());
                    }
                }
            }
        }
    }

    empty_dirs
}

pub fn clean_empty_directories(paths: &[String]) -> (usize, Vec<String>) {
    let mut cleaned = 0;
    let mut errors = Vec::new();

    for p in paths {
        let path = Path::new(p);
        if path.exists() && path.is_dir() {
            match fs::remove_dir(path) {
                Ok(_) => cleaned += 1,
                Err(e) => errors.push(format!("删除空目录失败 {}: {}", p, e)),
            }
        }
    }

    (cleaned, errors)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_flush_dns() {
        let res = flush_dns();
        assert!(res.is_ok(), "DNS flush should succeed on Windows");
    }
}
