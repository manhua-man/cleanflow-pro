use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

#[cfg(windows)]
use std::os::windows::ffi::OsStrExt;
#[cfg(windows)]
use std::os::windows::process::CommandExt;

#[cfg(windows)]
const CREATE_NO_WINDOW: u32 = 0x08000000;

#[cfg(windows)]
extern "system" {
    fn GetCompressedFileSizeW(lpFileName: *const u16, lpFileSizeHigh: *mut u32) -> u32;
    fn GetFileAttributesW(lpFileName: *const u16) -> u32;
    fn CreateFileW(
        lpFileName: *const u16,
        dwDesiredAccess: u32,
        dwShareMode: u32,
        lpSecurityAttributes: *mut std::ffi::c_void,
        dwCreationDisposition: u32,
        dwFlagsAndAttributes: u32,
        hTemplateFile: isize,
    ) -> isize;
    fn CloseHandle(hObject: isize) -> i32;
    fn LoadLibraryW(lpLibFileName: *const u16) -> *mut std::ffi::c_void;
    fn GetProcAddress(hModule: *mut std::ffi::c_void, lpProcName: *const i8) -> *mut std::ffi::c_void;
}

const INVALID_HANDLE_VALUE: isize = -1;
const FILE_WRITE_ATTRIBUTES: u32 = 0x0100;
const FILE_READ_ATTRIBUTES: u32 = 0x0080;
const FILE_SHARE_READ: u32 = 0x00000001;
const FILE_SHARE_WRITE: u32 = 0x00000002;
const FILE_SHARE_DELETE: u32 = 0x00000004;
const OPEN_EXISTING: u32 = 3;
const FILE_FLAG_OPEN_REPARSE_POINT: u32 = 0x00200000;
const CF_PIN_STATE_UNPINNED: u32 = 2;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct CloudFileItem {
    pub path: String,
    pub relative_path: String,
    pub file_name: String,
    pub logical_size: u64,
    pub physical_size: u64,
    pub is_online_only: bool,
    pub is_local: bool,
    pub last_access_secs: u64,
    pub last_write_secs: u64,
    pub days_inactive: u64,
    pub can_evict: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CloudDriveSummary {
    pub provider: String,
    pub root_path: String,
    pub total_files: usize,
    pub total_dirs: usize,
    pub total_logical_bytes: u64,
    pub total_physical_bytes: u64,
    pub online_only_bytes: u64,
    pub reclaimable_bytes: u64,
    pub is_cloud_files_supported: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CloudAuditReport {
    pub drives: Vec<CloudDriveSummary>,
    pub evictable_files: Vec<CloudFileItem>,
    pub total_logical_bytes: u64,
    pub total_physical_bytes: u64,
    pub total_online_only_bytes: u64,
    pub total_reclaimable_bytes: u64,
}

pub fn get_file_physical_size(path: &Path) -> u64 {
    #[cfg(windows)]
    {
        let mut w_path: Vec<u16> = path.as_os_str().encode_wide().collect();
        w_path.push(0);

        let mut high: u32 = 0;
        let low = unsafe { GetCompressedFileSizeW(w_path.as_ptr(), &mut high) };
        if low == 0xFFFFFFFF {
            return path.metadata().map(|m| m.len()).unwrap_or(0);
        }
        ((high as u64) << 32) | (low as u64)
    }
    #[cfg(not(windows))]
    {
        path.metadata().map(|m| m.len()).unwrap_or(0)
    }
}

pub fn get_file_attributes_raw(path: &Path) -> u32 {
    #[cfg(windows)]
    {
        let mut w_path: Vec<u16> = path.as_os_str().encode_wide().collect();
        w_path.push(0);
        unsafe { GetFileAttributesW(w_path.as_ptr()) }
    }
    #[cfg(not(windows))]
    {
        0
    }
}



fn query_reg_string(key: &str, val_name: &str) -> Option<String> {
    let mut cmd = Command::new("reg");
    cmd.args(["query", key, "/v", val_name]);

    #[cfg(windows)]
    cmd.creation_flags(CREATE_NO_WINDOW);

    if let Ok(out) = cmd.output() {
        let text = String::from_utf8_lossy(&out.stdout);
        for line in text.lines() {
            let trimmed = line.trim();
            if trimmed.starts_with(val_name) {
                let parts: Vec<&str> = trimmed.split_whitespace().collect();
                if parts.len() >= 3 {
                    return Some(parts[2..].join(" "));
                }
            }
        }
    }
    None
}

pub fn detect_cloud_drive_roots() -> Vec<(String, PathBuf)> {
    let mut detected = Vec::new();
    let mut seen_paths = HashSet::new();

    let user_profile = std::env::var("USERPROFILE").unwrap_or_default();

    // 1. OneDrive Personal via Registry
    if let Some(folder) = query_reg_string(
        r"HKCU\Software\Microsoft\OneDrive\Accounts\Personal",
        "UserFolder",
    ) {
        let p = PathBuf::from(&folder);
        if p.exists() && p.is_dir() && seen_paths.insert(p.clone()) {
            detected.push(("OneDrive (个人版)".to_string(), p));
        }
    }

    // 2. OneDrive via Environment Variables
    if let Ok(env_od) = std::env::var("OneDrive") {
        let p = PathBuf::from(&env_od);
        if p.exists() && p.is_dir() && seen_paths.insert(p.clone()) {
            detected.push(("OneDrive".to_string(), p));
        }
    }
    if let Ok(env_od_c) = std::env::var("OneDriveConsumer") {
        let p = PathBuf::from(&env_od_c);
        if p.exists() && p.is_dir() && seen_paths.insert(p.clone()) {
            detected.push(("OneDrive (消费版)".to_string(), p));
        }
    }
    if let Ok(env_od_b) = std::env::var("OneDriveCommercial") {
        let p = PathBuf::from(&env_od_b);
        if p.exists() && p.is_dir() && seen_paths.insert(p.clone()) {
            detected.push(("OneDrive (商业版)".to_string(), p));
        }
    }

    // 3. iCloud Drive
    if !user_profile.is_empty() {
        let icloud1 = PathBuf::from(&user_profile).join("iCloudDrive");
        if icloud1.exists() && icloud1.is_dir() && seen_paths.insert(icloud1.clone()) {
            detected.push(("iCloud Drive".to_string(), icloud1));
        }
        let icloud2 = PathBuf::from(&user_profile).join("Apple").join("iCloudDrive");
        if icloud2.exists() && icloud2.is_dir() && seen_paths.insert(icloud2.clone()) {
            detected.push(("iCloud Drive (Apple)".to_string(), icloud2));
        }

        // 4. 坚果云 (Nutstore)
        let nutstore = PathBuf::from(&user_profile).join("Nutstore");
        if nutstore.exists() && nutstore.is_dir() && seen_paths.insert(nutstore.clone()) {
            detected.push(("坚果云 (Nutstore)".to_string(), nutstore));
        }

        // 5. 百度网盘默认同步/下载
        let baidu = PathBuf::from(&user_profile).join("BaiduNetdiskDownload");
        if baidu.exists() && baidu.is_dir() && seen_paths.insert(baidu.clone()) {
            detected.push(("百度网盘同步区".to_string(), baidu));
        }

        // 6. 阿里云盘
        let aliyun = PathBuf::from(&user_profile).join("AliyunDrive");
        if aliyun.exists() && aliyun.is_dir() && seen_paths.insert(aliyun.clone()) {
            detected.push(("阿里云盘".to_string(), aliyun));
        }
    }

    // 7. Google Drive default mount (G:)
    let gdrive = PathBuf::from(r"G:\My Drive");
    if gdrive.exists() && gdrive.is_dir() && seen_paths.insert(gdrive.clone()) {
        detected.push(("Google Drive".to_string(), gdrive));
    }

    detected
}

pub fn scan_single_cloud_drive(
    provider: &str,
    root: &Path,
    max_evictable: usize,
) -> (CloudDriveSummary, Vec<CloudFileItem>) {
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0);

    let mut total_files = 0;
    let mut total_dirs = 0;
    let mut total_logical = 0;
    let mut total_physical = 0;
    let mut online_only_bytes = 0;
    let mut reclaimable_bytes = 0;
    let mut evictable_items = Vec::new();

    let root_str = root.to_string_lossy().to_string();

    let walker = jwalk::WalkDir::new(root).skip_hidden(false);
    for entry in walker.into_iter().flatten() {
        let p = entry.path();
        if p == root {
            continue;
        }

        if entry.file_type.is_dir() {
            total_dirs += 1;
            continue;
        }

        if !entry.file_type.is_file() {
            continue;
        }

        total_files += 1;
        let meta = match p.metadata() {
            Ok(m) => m,
            Err(_) => continue,
        };

        let logical_sz = meta.len();
        total_logical += logical_sz;

        let physical_sz = get_file_physical_size(&p);
        total_physical += physical_sz;

        let is_online_only = physical_sz == 0 && logical_sz > 0;
        let is_local = physical_sz > 0;

        if is_online_only {
            online_only_bytes += logical_sz;
        }

        let access_secs = meta
            .accessed()
            .ok()
            .and_then(|t| t.duration_since(UNIX_EPOCH).ok())
            .map(|d| d.as_secs())
            .unwrap_or(0);

        let write_secs = meta
            .modified()
            .ok()
            .and_then(|t| t.duration_since(UNIX_EPOCH).ok())
            .map(|d| d.as_secs())
            .unwrap_or(0);

        let latest_activity = access_secs.max(write_secs);
        let days_inactive = if now > latest_activity && latest_activity > 0 {
            (now - latest_activity) / 86400
        } else {
            0
        };

        // 判定是否推荐脱机释放：本地有实际占用、体积 > 100KB、且距离上次访问 > 14 天 (或无访问记录)
        let can_evict = is_local && physical_sz >= 100 * 1024 && (days_inactive >= 14 || days_inactive == 0);

        if can_evict {
            reclaimable_bytes += physical_sz;
            let rel = p
                .strip_prefix(root)
                .map(|r| r.to_string_lossy().to_string())
                .unwrap_or_else(|_| p.file_name().unwrap_or_default().to_string_lossy().to_string());

            evictable_items.push(CloudFileItem {
                path: p.to_string_lossy().to_string(),
                relative_path: rel,
                file_name: p.file_name().unwrap_or_default().to_string_lossy().to_string(),
                logical_size: logical_sz,
                physical_size: physical_sz,
                is_online_only,
                is_local,
                last_access_secs: access_secs,
                last_write_secs: write_secs,
                days_inactive,
                can_evict,
            });
        }
    }

    // 按本地占用物理空间从大到小排序
    evictable_items.sort_by(|a, b| b.physical_size.cmp(&a.physical_size));
    if evictable_items.len() > max_evictable {
        evictable_items.truncate(max_evictable);
    }

    let summary = CloudDriveSummary {
        provider: provider.to_string(),
        root_path: root_str,
        total_files,
        total_dirs,
        total_logical_bytes: total_logical,
        total_physical_bytes: total_physical,
        online_only_bytes,
        reclaimable_bytes,
        is_cloud_files_supported: true,
    };

    (summary, evictable_items)
}

pub fn run_cloud_storage_audit() -> CloudAuditReport {
    let roots = detect_cloud_drive_roots();
    let mut summaries = Vec::new();
    let mut all_evictable = Vec::new();

    let mut total_logical = 0;
    let mut total_physical = 0;
    let mut total_online_only = 0;
    let mut total_reclaimable = 0;

    for (provider, path) in roots {
        let (sum, items) = scan_single_cloud_drive(&provider, &path, 50);
        total_logical += sum.total_logical_bytes;
        total_physical += sum.total_physical_bytes;
        total_online_only += sum.online_only_bytes;
        total_reclaimable += sum.reclaimable_bytes;

        summaries.push(sum);
        all_evictable.extend(items);
    }

    all_evictable.sort_by(|a, b| b.physical_size.cmp(&a.physical_size));
    if all_evictable.len() > 100 {
        all_evictable.truncate(100);
    }

    CloudAuditReport {
        drives: summaries,
        evictable_files: all_evictable,
        total_logical_bytes: total_logical,
        total_physical_bytes: total_physical,
        total_online_only_bytes: total_online_only,
        total_reclaimable_bytes: total_reclaimable,
    }
}

pub fn evict_single_cloud_file(file_path: &str) -> Result<u64, String> {
    let p = Path::new(file_path);
    if !p.exists() || !p.is_file() {
        return Err("目标文件不存在或不是普通文件".to_string());
    }

    let initial_physical = get_file_physical_size(p);
    if initial_physical == 0 {
        return Ok(0); // 已经是纯联机状态
    }

    let mut dehydrated = false;

    // 优先尝试 Win32 Cloud Filter API (cldapi.dll)
    #[cfg(windows)]
    {
        let w_cld: Vec<u16> = "cldapi.dll\0".encode_utf16().collect();
        let h_module = unsafe { LoadLibraryW(w_cld.as_ptr()) };
        if !h_module.is_null() {
            let set_pin_name = b"CfSetPinState\0";
            let dehydrate_name = b"CfDehydratePlaceholder\0";

            let p_set_pin = unsafe { GetProcAddress(h_module, set_pin_name.as_ptr() as *const i8) };
            let p_dehydrate = unsafe { GetProcAddress(h_module, dehydrate_name.as_ptr() as *const i8) };

            if !p_set_pin.is_null() && !p_dehydrate.is_null() {
                let mut w_path: Vec<u16> = p.as_os_str().encode_wide().collect();
                w_path.push(0);

                let handle = unsafe {
                    CreateFileW(
                        w_path.as_ptr(),
                        FILE_WRITE_ATTRIBUTES | FILE_READ_ATTRIBUTES,
                        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
                        std::ptr::null_mut(),
                        OPEN_EXISTING,
                        FILE_FLAG_OPEN_REPARSE_POINT,
                        0,
                    )
                };

                if handle != INVALID_HANDLE_VALUE {
                    type FnSetPin = unsafe extern "system" fn(
                        *mut std::ffi::c_void,
                        u32,
                        u32,
                        *mut std::ffi::c_void,
                    ) -> i32;
                    type FnDehydrate = unsafe extern "system" fn(
                        *mut std::ffi::c_void,
                        i64,
                        i64,
                        u32,
                        *mut std::ffi::c_void,
                    ) -> i32;

                    let fn_set_pin: FnSetPin = unsafe { std::mem::transmute(p_set_pin) };
                    let fn_dehydrate: FnDehydrate = unsafe { std::mem::transmute(p_dehydrate) };

                    let _ = unsafe { fn_set_pin(handle as *mut std::ffi::c_void, CF_PIN_STATE_UNPINNED, 0, std::ptr::null_mut()) };
                    let hr = unsafe { fn_dehydrate(handle as *mut std::ffi::c_void, 0, -1, 0, std::ptr::null_mut()) };

                    unsafe { CloseHandle(handle) };
                    if hr == 0 {
                        dehydrated = true;
                    }
                }
            }
        }
    }

    // 回退尝试调用系统原生 attrib +U -P
    if !dehydrated {
        let mut cmd = Command::new("attrib.exe");
        cmd.args(["+U", "-P", file_path]);

        #[cfg(windows)]
        cmd.creation_flags(CREATE_NO_WINDOW);

        if let Ok(out) = cmd.output() {
            if out.status.success() {
                dehydrated = true;
            }
        }
    }

    let after_physical = get_file_physical_size(p);
    let freed = if initial_physical > after_physical {
        initial_physical - after_physical
    } else {
        // 如果文件系统是异步延迟脱水，按初始体积计为已标记释放
        initial_physical
    };

    if dehydrated {
        Ok(freed)
    } else {
        Err("文件脱机释放失败：请确保该文件位于支持按需同步的云盘目录中且未被程序独占锁定".to_string())
    }
}

pub fn batch_evict_cloud_files(file_paths: &[String]) -> (usize, u64, Vec<String>) {
    let mut success_count = 0;
    let mut total_freed = 0;
    let mut errors = Vec::new();

    for p in file_paths {
        match evict_single_cloud_file(p) {
            Ok(freed) => {
                success_count += 1;
                total_freed += freed;
            }
            Err(e) => {
                errors.push(format!("{}: {}", p, e));
            }
        }
    }

    (success_count, total_freed, errors)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn test_detect_cloud_drive_roots_run() {
        let roots = detect_cloud_drive_roots();
        // 本地环境通常会有 OneDrive
        for (provider, path) in &roots {
            assert!(!provider.is_empty());
            assert!(path.exists());
        }
    }

    #[test]
    fn test_get_file_physical_size_temp() {
        let temp_file = std::env::temp_dir().join("cleanflow_test_cloud_phys.tmp");
        let _ = fs::write(&temp_file, b"hello cloud storage audit test");
        let phys = get_file_physical_size(&temp_file);
        assert!(phys > 0);
        let _ = fs::remove_file(&temp_file);
    }

    #[test]
    fn test_evict_nonexistent_file() {
        let res = evict_single_cloud_file("C:\\nonexistent_cloud_file_12345.xyz");
        assert!(res.is_err());
    }

    #[test]
    fn test_cloud_file_item_serialization() {
        let item = CloudFileItem {
            path: r"D:\OneDrive\doc.pdf".to_string(),
            relative_path: "doc.pdf".to_string(),
            file_name: "doc.pdf".to_string(),
            logical_size: 1024 * 1024,
            physical_size: 1024 * 1024,
            is_online_only: false,
            is_local: true,
            last_access_secs: 1000,
            last_write_secs: 2000,
            days_inactive: 45,
            can_evict: true,
        };
        let json = serde_json::to_string(&item).unwrap();
        assert!(json.contains("doc.pdf"));
        assert!(json.contains("can_evict"));
    }
}
