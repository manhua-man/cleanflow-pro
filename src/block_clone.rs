use serde::{Deserialize, Serialize};
use std::ffi::OsStr;
use std::os::windows::ffi::OsStrExt;
use std::path::Path;

pub const FILE_SUPPORTS_BLOCK_REFCOUNTING: u32 = 0x08000000;
pub const FSCTL_DUPLICATE_EXTENTS_TO_FILE: u32 = 0x00098344;

const GENERIC_READ: u32 = 0x80000000;
const GENERIC_WRITE: u32 = 0x40000000;
const FILE_SHARE_READ: u32 = 0x00000001;
const FILE_SHARE_WRITE: u32 = 0x00000002;
const OPEN_EXISTING: u32 = 3;
const FILE_ATTRIBUTE_NORMAL: u32 = 0x00000080;
const INVALID_HANDLE_VALUE: isize = -1;

#[repr(C)]
struct DuplicateExtentsData {
    file_handle: isize,
    source_file_offset: i64,
    target_file_offset: i64,
    byte_count: i64,
}

#[link(name = "kernel32")]
extern "system" {
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
    fn GetLastError() -> u32;
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VolumeBlockCloneStatus {
    pub root_path: String,
    pub file_system: String,
    pub flags: u32,
    pub supports_block_cloning: bool,
    pub mode_recommended: String,
}

fn to_wide_null(s: &str) -> Vec<u16> {
    OsStr::new(s).encode_wide().chain(std::iter::once(0)).collect()
}

pub fn get_volume_root<P: AsRef<Path>>(path: P) -> String {
    let p = path.as_ref();
    if let Some(prefix) = p.components().next() {
        let prefix_str = prefix.as_os_str().to_string_lossy();
        if prefix_str.len() >= 2 && prefix_str.chars().nth(1) == Some(':') {
            return format!("{}\\", &prefix_str[0..2]);
        }
    }
    "C:\\".to_string()
}

pub fn check_volume_block_clone_support<P: AsRef<Path>>(path: P) -> VolumeBlockCloneStatus {
    let root = get_volume_root(path);
    let wide_root = to_wide_null(&root);

    let mut fs_name_buf = [0u16; 260];
    let mut flags: u32 = 0;

    let res = unsafe {
        GetVolumeInformationW(
            wide_root.as_ptr(),
            std::ptr::null_mut(),
            0,
            std::ptr::null_mut(),
            std::ptr::null_mut(),
            &mut flags,
            fs_name_buf.as_mut_ptr(),
            fs_name_buf.len() as u32,
        )
    };

    if res != 0 {
        let len = fs_name_buf.iter().position(|&c| c == 0).unwrap_or(0);
        let fs_name = String::from_utf16_lossy(&fs_name_buf[..len]);
        let supports = (flags & FILE_SUPPORTS_BLOCK_REFCOUNTING) != 0;

        let mode = if supports {
            "refs_block_clone".to_string()
        } else {
            "ntfs_copy_clean".to_string()
        };

        VolumeBlockCloneStatus {
            root_path: root,
            file_system: fs_name,
            flags,
            supports_block_cloning: supports,
            mode_recommended: mode,
        }
    } else {
        VolumeBlockCloneStatus {
            root_path: root,
            file_system: "Unknown".to_string(),
            flags: 0,
            supports_block_cloning: false,
            mode_recommended: "ntfs_copy_clean".to_string(),
        }
    }
}

pub fn clone_file_extents<P: AsRef<Path>, Q: AsRef<Path>>(
    source_path: P,
    target_path: Q,
) -> Result<u64, String> {
    let src_meta = std::fs::metadata(source_path.as_ref())
        .map_err(|e| format!("Failed to read source metadata: {}", e))?;
    let file_len = src_meta.len();

    let src_wide = to_wide_null(&source_path.as_ref().to_string_lossy());
    let tgt_wide = to_wide_null(&target_path.as_ref().to_string_lossy());

    let h_src = unsafe {
        CreateFileW(
            src_wide.as_ptr(),
            GENERIC_READ,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            std::ptr::null_mut(),
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            0,
        )
    };

    if h_src == INVALID_HANDLE_VALUE {
        let err = unsafe { GetLastError() };
        return Err(format!("Failed to open source file with GENERIC_READ, error code: {}", err));
    }

    let h_tgt = unsafe {
        CreateFileW(
            tgt_wide.as_ptr(),
            GENERIC_READ | GENERIC_WRITE,
            FILE_SHARE_READ,
            std::ptr::null_mut(),
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            0,
        )
    };

    if h_tgt == INVALID_HANDLE_VALUE {
        unsafe { CloseHandle(h_src) };
        let err = unsafe { GetLastError() };
        return Err(format!("Failed to open target file with GENERIC_WRITE, error code: {}", err));
    }

    let params = DuplicateExtentsData {
        file_handle: h_src,
        source_file_offset: 0,
        target_file_offset: 0,
        byte_count: file_len as i64,
    };

    let mut bytes_returned = 0u32;
    let res = unsafe {
        DeviceIoControl(
            h_tgt,
            FSCTL_DUPLICATE_EXTENTS_TO_FILE,
            &params as *const _ as *const std::ffi::c_void,
            std::mem::size_of::<DuplicateExtentsData>() as u32,
            std::ptr::null_mut(),
            0,
            &mut bytes_returned,
            std::ptr::null_mut(),
        )
    };

    unsafe {
        CloseHandle(h_tgt);
        CloseHandle(h_src);
    }

    if res != 0 {
        Ok(file_len)
    } else {
        let err = unsafe { GetLastError() };
        Err(format!(
            "FSCTL_DUPLICATE_EXTENTS_TO_FILE failed with Windows error: {}. Target volume might not support ReFS Block Cloning.",
            err
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_volume_root() {
        assert_eq!(get_volume_root("C:\\Users\\test"), "C:\\");
        assert_eq!(get_volume_root("D:\\Projects\\repo"), "D:\\");
    }

    #[test]
    fn test_check_volume_block_clone_support() {
        let status = check_volume_block_clone_support("C:\\");
        assert_eq!(status.root_path, "C:\\");
        assert!(!status.file_system.is_empty());
        // For NTFS, supports_block_cloning is false and recommends ntfs_copy_clean
        if status.file_system == "NTFS" {
            assert!(!status.supports_block_cloning);
            assert_eq!(status.mode_recommended, "ntfs_copy_clean");
        }
    }
}
