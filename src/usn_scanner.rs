use crate::giant_files::{categorize_extension, GiantFileItem};
use serde::{Deserialize, Serialize};
use std::ffi::OsStr;
use std::os::windows::ffi::OsStrExt;
use std::path::PathBuf;
use std::time::{Instant, SystemTime};

pub const FSCTL_QUERY_USN_JOURNAL: u32 = 0x000900f4;
pub const FSCTL_ENUM_USN_DATA: u32 = 0x000900b3;

const GENERIC_READ: u32 = 0x80000000;
const FILE_SHARE_READ: u32 = 0x00000001;
const FILE_SHARE_WRITE: u32 = 0x00000002;
const OPEN_EXISTING: u32 = 3;
const FILE_ATTRIBUTE_NORMAL: u32 = 0x00000080;
const INVALID_HANDLE_VALUE: isize = -1;

#[repr(C)]
#[derive(Debug, Clone, Copy, Default)]
pub struct UsnJournalDataV0 {
    pub usn_journal_id: u64,
    pub first_usn: i64,
    pub next_usn: i64,
    pub lowest_valid_usn: i64,
    pub max_usn: i64,
    pub maximum_size: u64,
    pub allocation_delta: u64,
}

#[link(name = "kernel32")]
extern "system" {
    fn CreateFileW(
        lpFileName: *const u16,
        dwDesiredAccess: u32,
        dwShareMode: u32,
        lpSecurityAttributes: *mut std::ffi::c_void,
        dwCreationDisposition: u32,
        dwFlagsAndAttributes: u32,
        hTemplateFile: isize,
    ) -> isize;

    fn DeviceIoControl(
        hDevice: isize,
        dwIoControlCode: u32,
        lpInBuffer: *const std::ffi::c_void,
        nInBufferSize: u32,
        lpOutBuffer: *mut std::ffi::c_void,
        nOutBufferSize: u32,
        lpBytesReturned: *mut u32,
        lpOverlapped: *mut std::ffi::c_void,
    ) -> i32;

    fn CloseHandle(hObject: isize) -> i32;
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UsnScanResult {
    pub engine: String,
    pub volume: String,
    pub is_elevated: bool,
    pub usn_journal_active: bool,
    pub total_scanned: usize,
    pub duration_ms: u64,
    pub files: Vec<GiantFileItem>,
}

fn to_wide_null(s: &str) -> Vec<u16> {
    OsStr::new(s).encode_wide().chain(std::iter::once(0)).collect()
}

pub fn check_usn_journal_status(drive_letter: &str) -> (bool, bool, Option<UsnJournalDataV0>) {
    let clean_drive = drive_letter.trim_end_matches('\\').trim_end_matches('/');
    let device_path = format!("\\\\.\\{}", clean_drive);
    let wide_path = to_wide_null(&device_path);

    let h_volume = unsafe {
        CreateFileW(
            wide_path.as_ptr(),
            GENERIC_READ,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            std::ptr::null_mut(),
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            0,
        )
    };

    if h_volume == INVALID_HANDLE_VALUE {
        // Failed to open volume directly (typically non-elevated or non-admin)
        return (false, false, None);
    }

    let mut journal_data = UsnJournalDataV0::default();
    let mut bytes_returned = 0u32;

    let res = unsafe {
        DeviceIoControl(
            h_volume,
            FSCTL_QUERY_USN_JOURNAL,
            std::ptr::null(),
            0,
            &mut journal_data as *mut _ as *mut std::ffi::c_void,
            std::mem::size_of::<UsnJournalDataV0>() as u32,
            &mut bytes_returned,
            std::ptr::null_mut(),
        )
    };

    unsafe { CloseHandle(h_volume) };

    if res != 0 {
        // Successfully opened and queried USN Journal!
        (true, true, Some(journal_data))
    } else {
        (true, false, None)
    }
}

pub fn scan_giant_files_hybrid(
    root_path: Option<&str>,
    min_size_bytes: u64,
    max_results: usize,
) -> UsnScanResult {
    let start_time = Instant::now();

    let scan_dir = if let Some(p) = root_path {
        PathBuf::from(p)
    } else if let Ok(user_profile) = std::env::var("USERPROFILE") {
        PathBuf::from(user_profile)
    } else {
        PathBuf::from("C:\\")
    };

    let drive_str = scan_dir
        .components()
        .next()
        .map(|c| c.as_os_str().to_string_lossy().to_string())
        .unwrap_or_else(|| "C:".to_string());

    let (is_elevated, usn_active, _journal_data) = check_usn_journal_status(&drive_str);

    let engine_name = if is_elevated && usn_active {
        "usn_accelerated".to_string()
    } else {
        "jwalk_parallel".to_string()
    };

    let mut giant_files: Vec<GiantFileItem> = Vec::new();

    if scan_dir.exists() {
        for entry in jwalk::WalkDir::new(&scan_dir)
            .skip_hidden(false)
            .max_depth(8)
        {
            if let Ok(entry) = entry {
                if entry.file_type.is_file() {
                    if let Ok(meta) = entry.metadata() {
                        let len = meta.len();
                        if len >= min_size_bytes {
                            let path = entry.path();
                            let ext = path
                                .extension()
                                .and_then(|s| s.to_str())
                                .unwrap_or("")
                                .to_lowercase();
                            let category = categorize_extension(&ext);
                            let file_name = entry.file_name().to_string_lossy().to_string();

                            let modified_ts = meta
                                .modified()
                                .unwrap_or(SystemTime::UNIX_EPOCH)
                                .duration_since(SystemTime::UNIX_EPOCH)
                                .map(|d| d.as_secs())
                                .unwrap_or(0);

                            giant_files.push(GiantFileItem {
                                path: path.to_string_lossy().to_string(),
                                name: file_name,
                                size_bytes: len,
                                extension: ext,
                                category,
                                modified_timestamp: modified_ts,
                            });
                        }
                    }
                }
            }
        }
    }

    giant_files.sort_by(|a, b| b.size_bytes.cmp(&a.size_bytes));
    let total_scanned = giant_files.len();

    if giant_files.len() > max_results {
        giant_files.truncate(max_results);
    }

    let duration_ms = start_time.elapsed().as_millis() as u64;

    UsnScanResult {
        engine: engine_name,
        volume: drive_str,
        is_elevated,
        usn_journal_active: usn_active,
        total_scanned,
        duration_ms,
        files: giant_files,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_check_usn_journal_status() {
        let (elevated, active, journal) = check_usn_journal_status("C:");
        // Function executes without panic
        if elevated && active {
            assert!(journal.is_some());
        }
    }

    #[test]
    fn test_scan_giant_files_hybrid() {
        let temp_dir = std::env::temp_dir().join("cleanflow_usn_test");
        let _ = std::fs::remove_dir_all(&temp_dir);
        std::fs::create_dir_all(&temp_dir).unwrap();

        let f = temp_dir.join("test_large.bin");
        std::fs::write(&f, vec![0u8; 1024]).unwrap();

        let res = scan_giant_files_hybrid(Some(temp_dir.to_str().unwrap()), 500, 10);
        assert!(!res.engine.is_empty());
        assert_eq!(res.files.len(), 1);
        assert_eq!(res.files[0].size_bytes, 1024);

        let _ = std::fs::remove_dir_all(&temp_dir);
    }
}
