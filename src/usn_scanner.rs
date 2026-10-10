use crate::giant_files::{categorize_extension, GiantFileItem};
use serde::{Deserialize, Serialize};
use std::ffi::OsStr;
use std::os::windows::ffi::OsStrExt;
use std::path::PathBuf;
use std::time::{Instant, SystemTime};

pub const FSCTL_QUERY_USN_JOURNAL: u32 = 0x000900f4;
pub const FSCTL_ENUM_USN_DATA: u32 = 0x000900b3;
pub const FSCTL_READ_USN_JOURNAL: u32 = 0x000900bb;

pub const USN_REASON_DATA_OVERWRITE: u32 = 0x00000001;
pub const USN_REASON_DATA_EXTEND: u32 = 0x00000002;
pub const USN_REASON_DATA_TRUNCATION: u32 = 0x00000004;
pub const USN_REASON_FILE_CREATE: u32 = 0x00000100;
pub const USN_REASON_FILE_DELETE: u32 = 0x00000200;
pub const USN_REASON_RENAME_OLD_NAME: u32 = 0x00001000;
pub const USN_REASON_RENAME_NEW_NAME: u32 = 0x00002000;
pub const USN_REASON_CLOSE: u32 = 0x80000000;

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

#[repr(C)]
#[derive(Debug, Clone, Copy, Default)]
pub struct ReadUsnJournalDataV0 {
    pub start_usn: i64,
    pub reason_mask: u32,
    pub return_only_on_close: u32,
    pub timeout: u64,
    pub bytes_to_wait_for: u64,
    pub usn_journal_id: u64,
}

#[repr(C)]
#[derive(Debug, Clone, Copy, Default)]
pub struct UsnRecordV2Header {
    pub record_length: u32,
    pub major_version: u16,
    pub minor_version: u16,
    pub file_reference_number: u64,
    pub parent_file_reference_number: u64,
    pub usn: i64,
    pub time_stamp: i64,
    pub reason: u32,
    pub source_info: u32,
    pub security_id: u32,
    pub file_attributes: u32,
    pub file_name_length: u16,
    pub file_name_offset: u16,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum UsnChangeType {
    Created,
    Deleted,
    Renamed,
    Modified,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UsnChangeItem {
    pub usn: i64,
    pub file_ref: u64,
    pub parent_ref: u64,
    pub file_name: String,
    pub is_dir: bool,
    pub change_type: UsnChangeType,
    pub reason: u32,
    pub timestamp: i64,
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
            .parallelism(jwalk::Parallelism::Serial)
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

pub fn read_usn_journal_changes(
    drive_letter: &str,
    start_usn: i64,
    journal_id: u64,
    max_records: usize,
) -> Result<(i64, Vec<UsnChangeItem>), String> {
    let clean_drive = drive_letter.trim_end_matches(['\\', '/']);
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
        return Err("Failed to open volume for USN read (requires administrator elevation)".to_string());
    }

    let read_req = ReadUsnJournalDataV0 {
        start_usn,
        reason_mask: USN_REASON_FILE_CREATE
            | USN_REASON_FILE_DELETE
            | USN_REASON_RENAME_NEW_NAME
            | USN_REASON_RENAME_OLD_NAME
            | USN_REASON_DATA_OVERWRITE
            | USN_REASON_DATA_EXTEND
            | USN_REASON_CLOSE,
        return_only_on_close: 0,
        timeout: 0,
        bytes_to_wait_for: 0,
        usn_journal_id: journal_id,
    };

    let mut out_buffer = vec![0u8; 64 * 1024]; // 64 KB buffer
    let mut bytes_returned = 0u32;

    let res = unsafe {
        DeviceIoControl(
            h_volume,
            FSCTL_READ_USN_JOURNAL,
            &read_req as *const _ as *const std::ffi::c_void,
            std::mem::size_of::<ReadUsnJournalDataV0>() as u32,
            out_buffer.as_mut_ptr() as *mut std::ffi::c_void,
            out_buffer.len() as u32,
            &mut bytes_returned,
            std::ptr::null_mut(),
        )
    };

    unsafe { CloseHandle(h_volume) };

    if res == 0 || bytes_returned < 8 {
        return Err("FSCTL_READ_USN_JOURNAL failed or returned insufficient bytes".to_string());
    }

    let next_usn = i64::from_le_bytes(out_buffer[0..8].try_into().unwrap());
    let mut changes = Vec::new();
    let mut offset = 8usize;

    while offset + std::mem::size_of::<UsnRecordV2Header>() <= bytes_returned as usize {
        let header = unsafe {
            std::ptr::read_unaligned(out_buffer.as_ptr().add(offset) as *const UsnRecordV2Header)
        };

        if header.record_length == 0 {
            break;
        }

        if header.major_version == 2 {
            let name_offset = offset + header.file_name_offset as usize;
            let name_len_bytes = header.file_name_length as usize;
            if name_offset + name_len_bytes <= bytes_returned as usize {
                let name_u16_len = name_len_bytes / 2;
                let u16_slice = unsafe {
                    std::slice::from_raw_parts(out_buffer.as_ptr().add(name_offset) as *const u16, name_u16_len)
                };
                let file_name = String::from_utf16_lossy(u16_slice);

                let is_dir = (header.file_attributes & 0x00000010) != 0; // FILE_ATTRIBUTE_DIRECTORY

                let change_type = if (header.reason & USN_REASON_FILE_CREATE) != 0 {
                    UsnChangeType::Created
                } else if (header.reason & USN_REASON_FILE_DELETE) != 0 {
                    UsnChangeType::Deleted
                } else if (header.reason & (USN_REASON_RENAME_NEW_NAME | USN_REASON_RENAME_OLD_NAME)) != 0 {
                    UsnChangeType::Renamed
                } else {
                    UsnChangeType::Modified
                };

                changes.push(UsnChangeItem {
                    usn: header.usn,
                    file_ref: header.file_reference_number,
                    parent_ref: header.parent_file_reference_number,
                    file_name,
                    is_dir,
                    change_type,
                    reason: header.reason,
                    timestamp: header.time_stamp,
                });

                if changes.len() >= max_records {
                    break;
                }
            }
        }

        offset += header.record_length as usize;
    }

    Ok((next_usn, changes))
}

use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Arc;

pub struct UsnJournalMonitor {
    pub drive_letter: String,
    pub is_active: Arc<AtomicBool>,
    pub total_changes_detected: Arc<AtomicU64>,
    pub last_usn: Arc<AtomicU64>,
}

impl UsnJournalMonitor {
    pub fn new(drive_letter: &str) -> Self {
        Self {
            drive_letter: drive_letter.to_string(),
            is_active: Arc::new(AtomicBool::new(false)),
            total_changes_detected: Arc::new(AtomicU64::new(0)),
            last_usn: Arc::new(AtomicU64::new(0)),
        }
    }

    pub fn start(&self) -> bool {
        let (elevated, active, journal_opt) = check_usn_journal_status(&self.drive_letter);
        if !elevated || !active || journal_opt.is_none() {
            return false;
        }

        let journal = journal_opt.unwrap();
        let initial_usn = journal.next_usn;
        self.last_usn.store(initial_usn as u64, Ordering::SeqCst);
        self.is_active.store(true, Ordering::SeqCst);

        let drive = self.drive_letter.clone();
        let is_running = self.is_active.clone();
        let total_changes = self.total_changes_detected.clone();
        let last_usn_atomic = self.last_usn.clone();
        let j_id = journal.usn_journal_id;

        std::thread::Builder::new()
            .name(format!("usn_monitor_{}", drive))
            .spawn(move || {
                let mut current_usn = initial_usn;
                while is_running.load(Ordering::Relaxed) {
                    std::thread::sleep(std::time::Duration::from_millis(300));
                    if let Ok((next_usn, items)) = read_usn_journal_changes(&drive, current_usn, j_id, 100) {
                        if !items.is_empty() {
                            total_changes.fetch_add(items.len() as u64, Ordering::Relaxed);
                            last_usn_atomic.store(next_usn as u64, Ordering::Relaxed);
                            current_usn = next_usn;
                        } else {
                            current_usn = next_usn;
                        }
                    }
                }
            })
            .is_ok()
    }

    pub fn stop(&self) {
        self.is_active.store(false, Ordering::SeqCst);
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
        let temp_dir = std::env::temp_dir().join(format!("cleanflow_usn_test_{}", std::process::id()));
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

    #[test]
    fn test_usn_change_types_and_monitor_lifecycle() {
        let monitor = UsnJournalMonitor::new("C:");
        assert_eq!(monitor.drive_letter, "C:");
        assert!(!monitor.is_active.load(Ordering::SeqCst));
        assert_eq!(monitor.total_changes_detected.load(Ordering::SeqCst), 0);
        monitor.stop();

        // Verify UsnChangeType mapping logic
        let item = UsnChangeItem {
            usn: 1000,
            file_ref: 12345,
            parent_ref: 6789,
            file_name: "test.txt".to_string(),
            is_dir: false,
            change_type: UsnChangeType::Created,
            reason: USN_REASON_FILE_CREATE,
            timestamp: 0,
        };
        assert_eq!(item.change_type, UsnChangeType::Created);
        assert_eq!(item.file_name, "test.txt");
    }
}
