use std::ffi::OsStr;
use std::os::windows::ffi::OsStrExt;
use std::path::Path;

#[cfg(windows)]
extern "system" {
    fn GetForegroundWindow() -> isize;
    fn GetClassNameW(hWnd: isize, lpClassName: *mut u16, nMaxCount: i32) -> i32;
    fn FindWindowExW(
        hWndParent: isize,
        hWndChildAfter: isize,
        lpszClass: *const u16,
        lpszWindow: *const u16,
    ) -> isize;
    fn SendMessageW(hWnd: isize, Msg: u32, wParam: usize, lParam: isize) -> isize;
    fn PostMessageW(hWnd: isize, Msg: u32, wParam: usize, lParam: isize) -> i32;
    fn EnumChildWindows(
        hWndParent: isize,
        lpEnumFunc: unsafe extern "system" fn(isize, isize) -> i32,
        lParam: isize,
    ) -> i32;
}

const WM_SETTEXT: u32 = 0x000C;
const WM_KEYDOWN: u32 = 0x0100;
const WM_KEYUP: u32 = 0x0101;
const VK_RETURN: usize = 0x0D;

fn to_wide_null(s: &str) -> Vec<u16> {
    OsStr::new(s).encode_wide().chain(std::iter::once(0)).collect()
}

pub fn get_window_class_name(hwnd: isize) -> String {
    let mut buf = [0u16; 256];
    let len = unsafe { GetClassNameW(hwnd, buf.as_mut_ptr(), 256) };
    if len > 0 {
        String::from_utf16_lossy(&buf[..len as usize])
    } else {
        String::new()
    }
}

/// Detects if the current foreground window is a Windows File Open/Save Dialog (#32770)
pub fn get_foreground_file_dialog() -> Option<isize> {
    let hwnd = unsafe { GetForegroundWindow() };
    if hwnd == 0 {
        return None;
    }

    let class_name = get_window_class_name(hwnd);
    if class_name == "#32770" 
        || class_name == "TTOTAL_CMD" 
        || class_name.contains("dopus") 
        || class_name == "CabinetWClass" 
    {
        return Some(hwnd);
    }

    // Check if any direct child or popup has #32770
    let wide_dialog_class = to_wide_null("#32770");
    let child_dialog = unsafe {
        FindWindowExW(hwnd, 0, wide_dialog_class.as_ptr(), std::ptr::null())
    };
    if child_dialog != 0 {
        return Some(child_dialog);
    }

    None
}

/// Helper context for locating the file name input box in a #32770 dialog
struct EditSearchContext {
    found_edit: isize,
}

unsafe extern "system" fn enum_child_find_edit(hwnd: isize, lparam: isize) -> i32 {
    let ctx = &mut *(lparam as *mut EditSearchContext);
    let class_name = get_window_class_name(hwnd);

    if class_name.eq_ignore_ascii_case("Edit") {
        ctx.found_edit = hwnd;
        return 0; // stop enumeration
    }
    1 // continue
}

/// Finds the filename Edit control inside a #32770 File Dialog
pub fn find_dialog_filename_edit(dialog_hwnd: isize) -> Option<isize> {
    // 1. Try finding via ComboBoxEx32 -> ComboBox -> Edit
    let wide_combo_ex = to_wide_null("ComboBoxEx32");
    let combo_ex = unsafe {
        FindWindowExW(dialog_hwnd, 0, wide_combo_ex.as_ptr(), std::ptr::null())
    };
    if combo_ex != 0 {
        let wide_combo = to_wide_null("ComboBox");
        let combo = unsafe {
            FindWindowExW(combo_ex, 0, wide_combo.as_ptr(), std::ptr::null())
        };
        if combo != 0 {
            let wide_edit = to_wide_null("Edit");
            let edit = unsafe {
                FindWindowExW(combo, 0, wide_edit.as_ptr(), std::ptr::null())
            };
            if edit != 0 {
                return Some(edit);
            }
        }
    }

    // 2. Direct Edit child search
    let wide_edit = to_wide_null("Edit");
    let direct_edit = unsafe {
        FindWindowExW(dialog_hwnd, 0, wide_edit.as_ptr(), std::ptr::null())
    };
    if direct_edit != 0 {
        return Some(direct_edit);
    }

    // 3. Recursive EnumChildWindows search
    let mut ctx = EditSearchContext { found_edit: 0 };
    unsafe {
        EnumChildWindows(
            dialog_hwnd,
            enum_child_find_edit,
            &mut ctx as *mut EditSearchContext as isize,
        );
    }

    if ctx.found_edit != 0 {
        Some(ctx.found_edit)
    } else {
        None
    }
}

/// Switches an active File Dialog (#32770) to the specified folder path
pub fn switch_file_dialog_to_path(dialog_hwnd: isize, target_path: &str) -> bool {
    let p = Path::new(target_path);
    let target_folder = if p.is_file() {
        p.parent().unwrap_or(p)
    } else {
        p
    };

    let folder_str = target_folder.to_string_lossy().to_string();
    if folder_str.is_empty() {
        return false;
    }

    let edit_hwnd = match find_dialog_filename_edit(dialog_hwnd) {
        Some(h) => h,
        None => return false,
    };

    let wide_path = to_wide_null(&folder_str);

    unsafe {
        // Set path text in edit control
        SendMessageW(edit_hwnd, WM_SETTEXT, 0, wide_path.as_ptr() as isize);
        // Simulate pressing Enter to trigger dialog navigation
        PostMessageW(edit_hwnd, WM_KEYDOWN, VK_RETURN, 0);
        PostMessageW(edit_hwnd, WM_KEYUP, VK_RETURN, 0);
    }

    true
}

/// Executes Quick Switch: detects any active foreground File Dialog and switches it to target path
pub fn execute_quick_switch(target_path: &str) -> Result<bool, String> {
    match get_foreground_file_dialog() {
        Some(dialog_hwnd) => {
            if switch_file_dialog_to_path(dialog_hwnd, target_path) {
                Ok(true)
            } else {
                Err("找到文件对话框，但未定位到路径输入框".to_string())
            }
        }
        None => Err("当前前台无活动的文件打开/另存为对话框".to_string()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_to_wide_null() {
        let w = to_wide_null("C:\\Test");
        assert_eq!(w.last(), Some(&0));
        assert!(w.len() > 1);
    }

    #[test]
    fn test_get_foreground_dialog_call() {
        // Safe call verification
        let _ = get_foreground_file_dialog();
    }
}
