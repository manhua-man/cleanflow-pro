use std::process::Command;
use std::sync::atomic::{AtomicBool, AtomicU16, Ordering};
use std::sync::Arc;
use std::thread;

pub struct TrayService {
    running: Arc<AtomicBool>,
    port: u16,
}

static GLOBAL_PORT: AtomicU16 = AtomicU16::new(3000);

impl TrayService {
    pub fn new(port: u16) -> Self {
        GLOBAL_PORT.store(port, Ordering::SeqCst);
        Self {
            running: Arc::new(AtomicBool::new(true)),
            port,
        }
    }

    pub fn start(&self) {
        #[cfg(windows)]
        {
            let running = self.running.clone();
            let port = self.port;
            thread::spawn(move || {
                run_tray_message_loop(port, running);
            });
        }
        #[cfg(not(windows))]
        {
            let _ = self.port;
        }
    }
}

pub fn is_autostart_enabled() -> bool {
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        let mut cmd = Command::new("reg");
        cmd.creation_flags(0x08000000);
        let output = cmd
            .args([
                "query",
                "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                "/v",
                "CleanFlowPro",
            ])
            .output();
        if let Ok(out) = output {
            out.status.success()
        } else {
            false
        }
    }
    #[cfg(not(windows))]
    {
        false
    }
}

pub fn set_autostart_enabled(enable: bool) -> Result<bool, String> {
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        if enable {
            let exe_path = std::env::current_exe()
                .map_err(|e| format!("获取自身执行路径失败: {}", e))?;
            let exe_str = exe_path.to_string_lossy();
            let val = format!("\"{}\" --silent", exe_str);

            let mut cmd = Command::new("reg");
            cmd.creation_flags(0x08000000);
            let status = cmd
                .args([
                    "add",
                    "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                    "/v",
                    "CleanFlowPro",
                    "/t",
                    "REG_SZ",
                    "/d",
                    &val,
                    "/f",
                ])
                .status()
                .map_err(|e| format!("写入自启注册表失败: {}", e))?;

            if status.success() {
                Ok(true)
            } else {
                Err("注册表写入命令返回错误".to_string())
            }
        } else {
            let mut cmd = Command::new("reg");
            cmd.creation_flags(0x08000000);
            let status = cmd
                .args([
                    "delete",
                    "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                    "/v",
                    "CleanFlowPro",
                    "/f",
                ])
                .status()
                .map_err(|e| format!("删除自启注册表失败: {}", e))?;

            if status.success() {
                Ok(false)
            } else {
                Ok(false)
            }
        }
    }
    #[cfg(not(windows))]
    {
        let _ = enable;
        Ok(false)
    }
}

#[cfg(windows)]
mod ffi {
    #[repr(C)]
    pub struct NotifyIconDataW {
        pub cb_size: u32,
        pub h_wnd: isize,
        pub u_id: u32,
        pub u_flags: u32,
        pub u_callback_message: u32,
        pub h_icon: isize,
        pub sz_tip: [u16; 128],
        pub dw_state: u32,
        pub dw_state_mask: u32,
        pub sz_info: [u16; 256],
        pub u_timeout_or_version: u32,
        pub sz_info_title: [u16; 64],
        pub dw_info_flags: u32,
    }

    #[repr(C)]
    pub struct WndClassExW {
        pub cb_size: u32,
        pub style: u32,
        pub lpfn_wnd_proc: Option<unsafe extern "system" fn(isize, u32, usize, isize) -> isize>,
        pub cb_cls_extra: i32,
        pub cb_wnd_extra: i32,
        pub h_instance: isize,
        pub h_icon: isize,
        pub h_cursor: isize,
        pub hbr_background: isize,
        pub lpsz_menu_name: *const u16,
        pub lpsz_class_name: *const u16,
        pub h_icon_sm: isize,
    }

    #[repr(C)]
    pub struct Point {
        pub x: i32,
        pub y: i32,
    }

    #[repr(C)]
    pub struct Msg {
        pub hwnd: isize,
        pub message: u32,
        pub w_param: usize,
        pub l_param: isize,
        pub time: u32,
        pub pt: Point,
    }

    pub const NIF_MESSAGE: u32 = 0x00000001;
    pub const NIF_ICON: u32 = 0x00000002;
    pub const NIF_TIP: u32 = 0x00000004;

    pub const NIM_ADD: u32 = 0x00000000;
    pub const NIM_DELETE: u32 = 0x00000002;

    pub const WM_USER: u32 = 0x0400;
    pub const WM_TRAYICON: u32 = WM_USER + 100;
    pub const WM_LBUTTONUP: isize = 0x0202;
    pub const WM_LBUTTONDBLCLK: isize = 0x0203;
    pub const WM_RBUTTONUP: isize = 0x0205;
    pub const WM_DESTROY: u32 = 0x0002;

    pub const WM_NULL: u32 = 0x0000;
    pub const TPM_BOTTOMALIGN: u32 = 0x0020;
    pub const TPM_RIGHTALIGN: u32 = 0x0008;
    pub const TPM_RETURNCMD: u32 = 0x0100;

    pub const MF_STRING: u32 = 0x00000000;
    pub const MF_SEPARATOR: u32 = 0x00000800;

    pub const IDI_APPLICATION: usize = 32512;

    #[link(name = "shell32")]
    extern "system" {
        pub fn Shell_NotifyIconW(dw_message: u32, lp_data: *mut NotifyIconDataW) -> i32;
    }

    #[link(name = "user32")]
    extern "system" {
        pub fn RegisterClassExW(lp_wnd_class: *const WndClassExW) -> u16;
        pub fn CreateWindowExW(
            dw_ex_style: u32,
            lp_class_name: *const u16,
            lp_window_name: *const u16,
            dw_style: u32,
            x: i32,
            y: i32,
            n_width: i32,
            n_height: i32,
            h_wnd_parent: isize,
            h_menu: isize,
            h_instance: isize,
            lp_param: *mut std::ffi::c_void,
        ) -> isize;
        pub fn DefWindowProcW(h_wnd: isize, msg: u32, w_param: usize, l_param: isize) -> isize;
        pub fn DestroyWindow(h_wnd: isize) -> i32;
        pub fn LoadIconW(h_instance: isize, lp_icon_name: *const u16) -> isize;
        pub fn CreatePopupMenu() -> isize;
        pub fn AppendMenuW(
            h_menu: isize,
            u_flags: u32,
            u_id_new_item: usize,
            lp_new_item: *const u16,
        ) -> i32;
        pub fn DestroyMenu(h_menu: isize) -> i32;
        pub fn GetCursorPos(lp_point: *mut Point) -> i32;
        pub fn SetForegroundWindow(h_wnd: isize) -> i32;
        pub fn TrackPopupMenuEx(
            h_menu: isize,
            u_flags: u32,
            x: i32,
            y: i32,
            h_wnd: isize,
            lptpm: *mut std::ffi::c_void,
        ) -> i32;
        pub fn PostMessageW(h_wnd: isize, msg: u32, w_param: usize, l_param: isize) -> i32;
        pub fn GetMessageW(
            lp_msg: *mut Msg,
            h_wnd: isize,
            w_msg_filter_min: u32,
            w_msg_filter_max: u32,
        ) -> i32;
        pub fn TranslateMessage(lp_msg: *const Msg) -> i32;
        pub fn DispatchMessageW(lp_msg: *const Msg) -> isize;
        pub fn PostQuitMessage(n_exit_code: i32);
    }
}

#[cfg(windows)]
fn to_wide_str(s: &str) -> Vec<u16> {
    use std::os::windows::ffi::OsStrExt;
    std::ffi::OsStr::new(s).encode_wide().chain(Some(0)).collect()
}

#[cfg(windows)]
unsafe extern "system" fn tray_window_proc(
    hwnd: isize,
    msg: u32,
    wparam: usize,
    lparam: isize,
) -> isize {
    match msg {
        ffi::WM_TRAYICON => {
            let port = GLOBAL_PORT.load(Ordering::SeqCst);
            if lparam == ffi::WM_LBUTTONUP || lparam == ffi::WM_LBUTTONDBLCLK {
                let url = format!("http://127.0.0.1:{}", port);
                let _ = crate::launcher::open_browser(&url);
                return 0;
            } else if lparam == ffi::WM_RBUTTONUP {
                let mut pt = ffi::Point { x: 0, y: 0 };
                ffi::GetCursorPos(&mut pt);
                ffi::SetForegroundWindow(hwnd);

                let hmenu = ffi::CreatePopupMenu();
                let m1 = to_wide_str("打开 CleanFlow 控制台");
                let m2 = to_wide_str("呼出 Spotlight 搜索栏 (Alt+Space)");
                let auto_label = if is_autostart_enabled() {
                    "开机自启动: [已开启]"
                } else {
                    "开机自启动: [已关闭]"
                };
                let m3 = to_wide_str(auto_label);
                let m4 = to_wide_str("退出 CleanFlow Pro");

                ffi::AppendMenuW(hmenu, ffi::MF_STRING, 1001, m1.as_ptr());
                ffi::AppendMenuW(hmenu, ffi::MF_STRING, 1002, m2.as_ptr());
                ffi::AppendMenuW(hmenu, ffi::MF_STRING, 1003, m3.as_ptr());
                ffi::AppendMenuW(hmenu, ffi::MF_SEPARATOR, 0, std::ptr::null());
                ffi::AppendMenuW(hmenu, ffi::MF_STRING, 1004, m4.as_ptr());

                let cmd = ffi::TrackPopupMenuEx(
                    hmenu,
                    ffi::TPM_BOTTOMALIGN | ffi::TPM_RIGHTALIGN | ffi::TPM_RETURNCMD,
                    pt.x,
                    pt.y,
                    hwnd,
                    std::ptr::null_mut(),
                );
                ffi::DestroyMenu(hmenu);
                ffi::PostMessageW(hwnd, ffi::WM_NULL, 0, 0);

                match cmd {
                    1001 => {
                        let url = format!("http://127.0.0.1:{}", port);
                        let _ = crate::launcher::open_browser(&url);
                    }
                    1002 => {
                        // Launch browser to spotlight hash
                        let url = format!("http://127.0.0.1:{}#spotlight", port);
                        let _ = crate::launcher::open_browser(&url);
                    }
                    1003 => {
                        let cur = is_autostart_enabled();
                        let _ = set_autostart_enabled(!cur);
                    }
                    1004 => {
                        let mut nid: ffi::NotifyIconDataW = std::mem::zeroed();
                        nid.cb_size = std::mem::size_of::<ffi::NotifyIconDataW>() as u32;
                        nid.h_wnd = hwnd;
                        nid.u_id = 1;
                        ffi::Shell_NotifyIconW(ffi::NIM_DELETE, &mut nid);
                        ffi::DestroyWindow(hwnd);
                        std::process::exit(0);
                    }
                    _ => {}
                }
                return 0;
            }
        }
        ffi::WM_DESTROY => {
            ffi::PostQuitMessage(0);
            return 0;
        }
        _ => {}
    }
    ffi::DefWindowProcW(hwnd, msg, wparam, lparam)
}

#[cfg(windows)]
fn run_tray_message_loop(port: u16, running: Arc<AtomicBool>) {
    GLOBAL_PORT.store(port, Ordering::SeqCst);
    let class_name = to_wide_str("CleanFlowTrayWindowClass");
    let window_title = to_wide_str("CleanFlow Pro Background Daemon");

    unsafe {
        let mut wnd_class: ffi::WndClassExW = std::mem::zeroed();
        wnd_class.cb_size = std::mem::size_of::<ffi::WndClassExW>() as u32;
        wnd_class.lpfn_wnd_proc = Some(tray_window_proc);
        wnd_class.lpsz_class_name = class_name.as_ptr();
        wnd_class.h_icon = ffi::LoadIconW(0, ffi::IDI_APPLICATION as *const u16);
        wnd_class.h_icon_sm = wnd_class.h_icon;

        ffi::RegisterClassExW(&wnd_class);

        let hwnd = ffi::CreateWindowExW(
            0,
            class_name.as_ptr(),
            window_title.as_ptr(),
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            std::ptr::null_mut(),
        );

        if hwnd == 0 {
            return;
        }

        let mut nid: ffi::NotifyIconDataW = std::mem::zeroed();
        nid.cb_size = std::mem::size_of::<ffi::NotifyIconDataW>() as u32;
        nid.h_wnd = hwnd;
        nid.u_id = 1;
        nid.u_flags = ffi::NIF_MESSAGE | ffi::NIF_ICON | ffi::NIF_TIP;
        nid.u_callback_message = ffi::WM_TRAYICON;
        nid.h_icon = wnd_class.h_icon;

        let tip = "CleanFlow Pro - 智能空间管家与毫秒检索";
        let tip_wide = to_wide_str(tip);
        let len = tip_wide.len().min(127);
        nid.sz_tip[..len].copy_from_slice(&tip_wide[..len]);

        ffi::Shell_NotifyIconW(ffi::NIM_ADD, &mut nid);

        let mut msg: ffi::Msg = std::mem::zeroed();
        while running.load(Ordering::SeqCst) {
            let res = ffi::GetMessageW(&mut msg, 0, 0, 0);
            if res <= 0 {
                break;
            }
            ffi::TranslateMessage(&msg);
            ffi::DispatchMessageW(&msg);
        }

        ffi::Shell_NotifyIconW(ffi::NIM_DELETE, &mut nid);
        ffi::DestroyWindow(hwnd);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_autostart_query() {
        // Query should return without panic
        let enabled = is_autostart_enabled();
        let _ = enabled;
    }
}
