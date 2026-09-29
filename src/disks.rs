use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DiskInfo {
    pub letter: String,
    pub total_bytes: u64,
    pub free_bytes: u64,
    pub used_bytes: u64,
    pub usage_percent: f64,
}

#[cfg(windows)]
extern "system" {
    fn GetLogicalDriveStringsW(n_buffer_length: u32, lp_buffer: *mut u16) -> u32;
    fn GetDiskFreeSpaceExW(
        lp_directory_name: *const u16,
        lp_free_bytes_available_to_caller: *mut u64,
        lp_total_number_of_bytes: *mut u64,
        lp_total_number_of_free_bytes: *mut u64,
    ) -> i32;
}

pub fn get_disk_drives() -> Vec<DiskInfo> {
    let mut drives = Vec::new();
    #[cfg(windows)]
    unsafe {
        let mut buffer = [0u16; 512];
        let len = GetLogicalDriveStringsW(buffer.len() as u32, buffer.as_mut_ptr());
        if len > 0 {
            let mut start = 0;
            while start < len as usize {
                let slice = &buffer[start..];
                if let Some(null_pos) = slice.iter().position(|&c| c == 0) {
                    if null_pos > 0 {
                        let drive_str = String::from_utf16_lossy(&slice[..null_pos]);
                        let drive_wide: Vec<u16> = drive_str.encode_utf16().chain(std::iter::once(0)).collect();
                        let mut free_avail = 0u64;
                        let mut total = 0u64;
                        let mut total_free = 0u64;
                        if GetDiskFreeSpaceExW(
                            drive_wide.as_ptr(),
                            &mut free_avail,
                            &mut total,
                            &mut total_free,
                        ) != 0
                            && total > 0
                        {
                            let used = total.saturating_sub(free_avail);
                            let usage_percent = (used as f64 / total as f64) * 100.0;
                            let clean_letter = drive_str.trim_end_matches('\\').to_string();
                            drives.push(DiskInfo {
                                letter: clean_letter,
                                total_bytes: total,
                                free_bytes: free_avail,
                                used_bytes: used,
                                usage_percent: (usage_percent * 10.0).round() / 10.0,
                            });
                        }
                    }
                    start += null_pos + 1;
                } else {
                    break;
                }
            }
        }
    }
    drives
}
