use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::ffi::OsStr;
use std::os::windows::ffi::OsStrExt;

pub const FSCTL_QUERY_USN_JOURNAL: u32 = 0x000900f4;
pub const FSCTL_ENUM_USN_DATA: u32 = 0x000900b3;

const GENERIC_READ: u32 = 0x80000000;
const FILE_SHARE_READ: u32 = 0x00000001;
const FILE_SHARE_WRITE: u32 = 0x00000002;
const OPEN_EXISTING: u32 = 3;
const FILE_ATTRIBUTE_NORMAL: u32 = 0x00000080;
const FILE_ATTRIBUTE_DIRECTORY: u32 = 0x00000010;
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
pub struct MftEnumDataV0 {
    pub start_file_reference_number: u64,
    pub low_usn: i64,
    pub high_usn: i64,
}

#[repr(C)]
#[derive(Debug, Clone, Copy)]
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

    fn GetLogicalDrives() -> u32;

    fn GetVolumeInformationW(
        lpRootPathName: *const u16,
        lpVolumeNameBuffer: *mut u16,
        nVolumeNameSize: u32,
        lpVolumeSerialNumber: *mut u32,
        lpMaximumComponentLength: *mut u32,
        lpFileSystemFlags: *mut u32,
        lpFileSystemNameBuffer: *mut u16,
        nFileSystemNameSize: u32,
    ) -> i32;
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VolumeInfo {
    pub drive_letter: char,
    pub root_path: String,
    pub label: String,
    pub fs_type: String,
    pub serial_number: u32,
    pub is_ntfs: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RawMftEntry {
    pub frn: u64,
    pub parent_frn: u64,
    pub name: String,
    pub is_dir: bool,
    pub file_attributes: u32,
    pub timestamp: i64,
}

fn to_wide_null(s: &str) -> Vec<u16> {
    OsStr::new(s).encode_wide().chain(std::iter::once(0)).collect()
}

pub fn list_available_volumes() -> Vec<VolumeInfo> {
    let mut volumes = Vec::new();
    let drives_bitmask = unsafe { GetLogicalDrives() };

    for i in 0..26 {
        if (drives_bitmask & (1 << i)) != 0 {
            let letter = (b'A' + i as u8) as char;
            let root = format!("{}:\\", letter);
            let wide_root = to_wide_null(&root);

            let mut vol_name = [0u16; 260];
            let mut fs_name = [0u16; 260];
            let mut serial = 0u32;
            let mut max_comp = 0u32;
            let mut flags = 0u32;

            let res = unsafe {
                GetVolumeInformationW(
                    wide_root.as_ptr(),
                    vol_name.as_mut_ptr(),
                    vol_name.len() as u32,
                    &mut serial,
                    &mut max_comp,
                    &mut flags,
                    fs_name.as_mut_ptr(),
                    fs_name.len() as u32,
                )
            };

            if res != 0 {
                let label = String::from_utf16_lossy(&vol_name)
                    .trim_matches('\0')
                    .to_string();
                let fs = String::from_utf16_lossy(&fs_name)
                    .trim_matches('\0')
                    .to_string();
                let is_ntfs = fs.eq_ignore_ascii_case("NTFS");

                volumes.push(VolumeInfo {
                    drive_letter: letter,
                    root_path: root,
                    label,
                    fs_type: fs,
                    serial_number: serial,
                    is_ntfs,
                });
            }
        }
    }

    volumes
}

pub fn read_volume_mft_stream(drive_letter: char) -> Result<Vec<RawMftEntry>, String> {
    let dev_path = format!("\\\\.\\{}:", drive_letter);
    let wide_dev = to_wide_null(&dev_path);

    let h_volume = unsafe {
        CreateFileW(
            wide_dev.as_ptr(),
            GENERIC_READ,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            std::ptr::null_mut(),
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            0,
        )
    };

    if h_volume == INVALID_HANDLE_VALUE {
        return Err(format!("无法打开卷句柄 (需要管理员权限): {}", dev_path));
    }

    let mut journal_data = UsnJournalDataV0::default();
    let mut bytes_returned = 0u32;

    let journal_res = unsafe {
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

    if journal_res == 0 {
        unsafe { CloseHandle(h_volume) };
        return Err("当前卷未启用 USN Journal 日志".to_string());
    }

    let mut enum_data = MftEnumDataV0 {
        start_file_reference_number: 0,
        low_usn: 0,
        high_usn: journal_data.next_usn,
    };

    let mut entries = Vec::with_capacity(100_000);
    let mut buffer = vec![0u8; 64 * 1024];

    loop {
        let mut out_bytes = 0u32;
        let io_res = unsafe {
            DeviceIoControl(
                h_volume,
                FSCTL_ENUM_USN_DATA,
                &enum_data as *const _ as *const std::ffi::c_void,
                std::mem::size_of::<MftEnumDataV0>() as u32,
                buffer.as_mut_ptr() as *mut std::ffi::c_void,
                buffer.len() as u32,
                &mut out_bytes,
                std::ptr::null_mut(),
            )
        };

        if io_res == 0 || out_bytes <= 8 {
            break;
        }

        // The first 8 bytes of the output buffer contains the next starting USN / FRN
        let next_frn = unsafe { *(buffer.as_ptr() as *const u64) };
        enum_data.start_file_reference_number = next_frn;

        let mut offset = 8usize;
        while offset + std::mem::size_of::<UsnRecordV2Header>() <= out_bytes as usize {
            let p_record = unsafe { &*(buffer.as_ptr().add(offset) as *const UsnRecordV2Header) };
            if p_record.record_length == 0 {
                break;
            }

            if p_record.major_version == 2 {
                let name_offset = offset + p_record.file_name_offset as usize;
                let name_len_bytes = p_record.file_name_length as usize;

                if name_offset + name_len_bytes <= out_bytes as usize {
                    let u16_slice = unsafe {
                        std::slice::from_raw_parts(
                            buffer.as_ptr().add(name_offset) as *const u16,
                            name_len_bytes / 2,
                        )
                    };
                    let file_name = String::from_utf16_lossy(u16_slice);
                    let is_dir = (p_record.file_attributes & FILE_ATTRIBUTE_DIRECTORY) != 0;

                    // Exclude internal NTFS meta-files that begin with $
                    if !file_name.is_empty() && (!file_name.starts_with('$') || file_name == "$Recycle.Bin") {
                        entries.push(RawMftEntry {
                            frn: p_record.file_reference_number,
                            parent_frn: p_record.parent_file_reference_number,
                            name: file_name,
                            is_dir,
                            file_attributes: p_record.file_attributes,
                            timestamp: p_record.time_stamp,
                        });
                    }
                }
            }

            offset += p_record.record_length as usize;
        }
    }

    unsafe { CloseHandle(h_volume) };
    Ok(entries)
}

pub fn filetime_to_unix_secs(ft: i64) -> u64 {
    const UNIX_EPOCH_FILETIME: i64 = 116444736000000000;
    if ft <= UNIX_EPOCH_FILETIME {
        0
    } else {
        ((ft - UNIX_EPOCH_FILETIME) / 10_000_000) as u64
    }
}

pub fn reconstruct_paths(
    drive_letter: char,
    entries: &[RawMftEntry],
) -> Vec<(String, bool, u64, u64)> {
    let mut frn_to_parent: HashMap<u64, (u64, &str, bool)> = HashMap::with_capacity(entries.len());
    for e in entries {
        frn_to_parent.insert(e.frn, (e.parent_frn, &e.name, e.is_dir));
    }

    let root_prefix = format!("{}:\\", drive_letter);
    let mut resolved: Vec<(String, bool, u64, u64)> = Vec::with_capacity(entries.len());

    let mut path_cache: HashMap<u64, String> = HashMap::new();

    for e in entries {
        let mut curr_frn = e.frn;
        let mut segments: Vec<&str> = Vec::new();
        let mut hit_cached = None;

        while let Some(&(parent_frn, name, _)) = frn_to_parent.get(&curr_frn) {
            segments.push(name);
            if let Some(cached_path) = path_cache.get(&parent_frn) {
                hit_cached = Some(cached_path.clone());
                break;
            }
            if parent_frn == curr_frn || parent_frn == 0 || (parent_frn & 0x0000FFFFFFFFFFFF) == 5 {
                break;
            }
            curr_frn = parent_frn;
        }

        segments.reverse();
        let full_path = if let Some(base) = hit_cached {
            format!("{}\\{}", base, segments.join("\\"))
        } else {
            format!("{}{}", root_prefix, segments.join("\\"))
        };

        if e.is_dir {
            path_cache.insert(e.frn, full_path.clone());
        }

        let ts_sec = filetime_to_unix_secs(e.timestamp);
        resolved.push((full_path, e.is_dir, e.frn, ts_sec));
    }

    resolved
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_list_available_volumes() {
        let vols = list_available_volumes();
        assert!(!vols.is_empty(), "Should detect at least one Windows drive");
        let has_c = vols.iter().any(|v| v.drive_letter == 'C');
        assert!(has_c, "C: drive must be detected");
    }

    #[test]
    fn test_reconstruct_paths_mock() {
        let entries = vec![
            RawMftEntry {
                frn: 1,
                parent_frn: 0,
                name: "Users".to_string(),
                is_dir: true,
                file_attributes: FILE_ATTRIBUTE_DIRECTORY,
                timestamp: 0,
            },
            RawMftEntry {
                frn: 2,
                parent_frn: 1,
                name: "EDY".to_string(),
                is_dir: true,
                file_attributes: FILE_ATTRIBUTE_DIRECTORY,
                timestamp: 0,
            },
            RawMftEntry {
                frn: 3,
                parent_frn: 2,
                name: "test.txt".to_string(),
                is_dir: false,
                file_attributes: FILE_ATTRIBUTE_NORMAL,
                timestamp: 0,
            },
        ];

        let paths = reconstruct_paths('C', &entries);
        assert_eq!(paths.len(), 3);
        assert_eq!(paths[0].0, "C:\\Users");
        assert_eq!(paths[0].3, 0);
        assert_eq!(paths[1].0, "C:\\Users\\EDY");
        assert_eq!(paths[2].0, "C:\\Users\\EDY\\test.txt");
    }

    #[test]
    fn test_filetime_to_unix_secs() {
        // Windows FILETIME for approx 2024+
        let ft = 133500000000000000i64;
        let s = filetime_to_unix_secs(ft);
        assert!(s > 1700000000);
        assert_eq!(filetime_to_unix_secs(0), 0);
    }
}
