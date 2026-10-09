use serde::{Deserialize, Serialize};
use std::ffi::OsStr;
use std::os::windows::ffi::OsStrExt;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

#[cfg(windows)]
extern "system" {
    fn GetDiskFreeSpaceExW(
        lpDirectoryName: *const u16,
        lpFreeBytesAvailableToCaller: *mut u64,
        lpTotalNumberOfBytes: *mut u64,
        lpTotalNumberOfFreeBytes: *mut u64,
    ) -> i32;
}

fn to_wide_null(s: &str) -> Vec<u16> {
    OsStr::new(s).encode_wide().chain(std::iter::once(0)).collect()
}

pub fn get_disk_free_bytes(drive_root: &str) -> Option<(u64, u64)> {
    let wide = to_wide_null(drive_root);
    let mut free_caller: u64 = 0;
    let mut total_bytes: u64 = 0;
    let mut free_total: u64 = 0;

    let res = unsafe {
        GetDiskFreeSpaceExW(
            wide.as_ptr(),
            &mut free_caller,
            &mut total_bytes,
            &mut free_total,
        )
    };

    if res != 0 {
        Some((free_caller, total_bytes))
    } else {
        None
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DaemonConfig {
    pub enabled: bool,
    pub check_interval_secs: u64,
    pub warning_threshold_bytes: u64, // e.g. 10 GB
    pub target_drive: String,
}

impl Default for DaemonConfig {
    fn default() -> Self {
        Self {
            enabled: true,
            check_interval_secs: 900, // 15 mins
            warning_threshold_bytes: 10 * 1024 * 1024 * 1024, // 10 GB
            target_drive: "C:\\".to_string(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DaemonStatus {
    pub is_running: bool,
    pub target_drive: String,
    pub free_space_bytes: u64,
    pub total_space_bytes: u64,
    pub is_space_low: bool,
    pub last_check_timestamp: u64,
    pub auto_clean_count: u64,
}

pub struct DaemonService {
    config: Arc<Mutex<DaemonConfig>>,
    is_running: Arc<AtomicBool>,
    free_bytes: Arc<AtomicU64>,
    total_bytes: Arc<AtomicU64>,
    last_check_ts: Arc<AtomicU64>,
    clean_count: Arc<AtomicU64>,
}

impl DaemonService {
    pub fn new() -> Self {
        Self {
            config: Arc::new(Mutex::new(DaemonConfig::default())),
            is_running: Arc::new(AtomicBool::new(false)),
            free_bytes: Arc::new(AtomicU64::new(0)),
            total_bytes: Arc::new(AtomicU64::new(0)),
            last_check_ts: Arc::new(AtomicU64::new(0)),
            clean_count: Arc::new(AtomicU64::new(0)),
        }
    }

    pub fn start(&self) {
        if self.is_running.swap(true, Ordering::SeqCst) {
            return;
        }

        let is_running = self.is_running.clone();
        let config = self.config.clone();
        let free_bytes = self.free_bytes.clone();
        let total_bytes = self.total_bytes.clone();
        let last_check_ts = self.last_check_ts.clone();

        thread::spawn(move || {
            while is_running.load(Ordering::SeqCst) {
                let (drive, interval) = {
                    let cfg = config.lock().unwrap();
                    (cfg.target_drive.clone(), cfg.check_interval_secs)
                };

                if let Some((free, total)) = get_disk_free_bytes(&drive) {
                    free_bytes.store(free, Ordering::SeqCst);
                    total_bytes.store(total, Ordering::SeqCst);
                }

                let now = std::time::SystemTime::now()
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap_or_default()
                    .as_secs();
                last_check_ts.store(now, Ordering::SeqCst);

                // Sleep for interval in small increments to allow graceful shutdown
                for _ in 0..interval {
                    if !is_running.load(Ordering::SeqCst) {
                        break;
                    }
                    thread::sleep(Duration::from_secs(1));
                }
            }
        });
    }

    pub fn get_status(&self) -> DaemonStatus {
        let cfg = self.config.lock().unwrap();
        let free = self.free_bytes.load(Ordering::SeqCst);
        let total = self.total_bytes.load(Ordering::SeqCst);
        let is_low = free > 0 && free < cfg.warning_threshold_bytes;

        DaemonStatus {
            is_running: self.is_running.load(Ordering::SeqCst),
            target_drive: cfg.target_drive.clone(),
            free_space_bytes: free,
            total_space_bytes: total,
            is_space_low: is_low,
            last_check_timestamp: self.last_check_ts.load(Ordering::SeqCst),
            auto_clean_count: self.clean_count.load(Ordering::SeqCst),
        }
    }

    pub fn stop(&self) {
        self.is_running.store(false, Ordering::SeqCst);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_daemon_disk_free_call() {
        let res = get_disk_free_bytes("C:\\");
        if let Some((free, total)) = res {
            assert!(total > 0);
            assert!(free > 0);
        }
    }

    #[test]
    fn test_daemon_status() {
        let service = DaemonService::new();
        let status = service.get_status();
        assert_eq!(status.target_drive, "C:\\");
        assert!(!status.is_running);
    }
}
