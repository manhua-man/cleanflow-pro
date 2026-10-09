use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::thread;

#[cfg(windows)]
extern "system" {
    fn RegisterHotKey(hWnd: isize, id: i32, fsModifiers: u32, vk: u32) -> i32;
    fn UnregisterHotKey(hWnd: isize, id: i32) -> i32;
    fn GetMessageW(lpMsg: *mut Msg, hWnd: isize, wMsgFilterMin: u32, wMsgFilterMax: u32) -> i32;
}

#[repr(C)]
struct Point {
    x: i32,
    y: i32,
}

#[repr(C)]
struct Msg {
    hwnd: isize,
    message: u32,
    w_param: usize,
    l_param: isize,
    time: u32,
    pt: Point,
}

const MOD_ALT: u32 = 0x0001;
const MOD_CONTROL: u32 = 0x0002;
const MOD_NOREPEAT: u32 = 0x4000;
const VK_SPACE: u32 = 0x20;
const VK_G: u32 = 0x47;
const WM_HOTKEY: u32 = 0x0312;
const WM_QUIT: u32 = 0x0012;

pub const HOTKEY_ID_SPOTLIGHT: i32 = 1001;
pub const HOTKEY_ID_QUICK_SWITCH: i32 = 1002;

pub struct HotkeyService {
    is_running: Arc<AtomicBool>,
}

impl HotkeyService {
    pub fn new() -> Self {
        Self {
            is_running: Arc::new(AtomicBool::new(false)),
        }
    }

    /// Starts global hotkey listener in a background worker thread
    /// on_spotlight_triggered: callback for Alt+Space (Spotlight Launcher)
    /// on_quick_switch_triggered: callback for Ctrl+G (Quick Switch)
    pub fn start<F1, F2>(&self, on_spotlight: F1, on_quick_switch: F2)
    where
        F1: Fn() + Send + Sync + 'static,
        F2: Fn() + Send + Sync + 'static,
    {
        if self.is_running.swap(true, Ordering::SeqCst) {
            return;
        }

        let running_flag = self.is_running.clone();

        thread::spawn(move || {
            // Register Alt + Space for Spotlight
            let res_spotlight = unsafe {
                RegisterHotKey(
                    0,
                    HOTKEY_ID_SPOTLIGHT,
                    MOD_ALT | MOD_NOREPEAT,
                    VK_SPACE,
                )
            };

            // Register Ctrl + G for Quick Switch
            let res_qs = unsafe {
                RegisterHotKey(
                    0,
                    HOTKEY_ID_QUICK_SWITCH,
                    MOD_CONTROL | MOD_NOREPEAT,
                    VK_G,
                )
            };

            if res_spotlight == 0 && res_qs == 0 {
                eprintln!("[CleanFlow Hotkey] Failed to register global hotkeys");
                running_flag.store(false, Ordering::SeqCst);
                return;
            }

            let mut msg: Msg = unsafe { std::mem::zeroed() };
            while running_flag.load(Ordering::SeqCst) {
                let ret = unsafe { GetMessageW(&mut msg, 0, 0, 0) };
                if ret <= 0 || msg.message == WM_QUIT {
                    break;
                }

                if msg.message == WM_HOTKEY {
                    match msg.w_param as i32 {
                        HOTKEY_ID_SPOTLIGHT => {
                            on_spotlight();
                        }
                        HOTKEY_ID_QUICK_SWITCH => {
                            on_quick_switch();
                        }
                        _ => {}
                    }
                }
            }

            // Cleanup hotkeys
            unsafe {
                UnregisterHotKey(0, HOTKEY_ID_SPOTLIGHT);
                UnregisterHotKey(0, HOTKEY_ID_QUICK_SWITCH);
            }
        });
    }

    pub fn stop(&self) {
        self.is_running.store(false, Ordering::SeqCst);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hotkey_service_init() {
        let service = HotkeyService::new();
        assert!(!service.is_running.load(Ordering::SeqCst));
    }
}
