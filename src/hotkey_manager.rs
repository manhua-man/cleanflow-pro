use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{Arc, RwLock};
use std::thread;
use std::time::{SystemTime, UNIX_EPOCH};

#[cfg(windows)]
extern "system" {
    fn RegisterHotKey(hWnd: isize, id: i32, fsModifiers: u32, vk: u32) -> i32;
    fn UnregisterHotKey(hWnd: isize, id: i32) -> i32;
    fn SetWindowsHookExW(idHook: i32, lpfn: HookProc, hmod: isize, dwThreadId: u32) -> isize;
    fn UnhookWindowsHookEx(hhk: isize) -> i32;
    fn CallNextHookEx(hhk: isize, nCode: i32, wParam: usize, lParam: isize) -> isize;
    fn GetMessageW(lpMsg: *mut Msg, hWnd: isize, wMsgFilterMin: u32, wMsgFilterMax: u32) -> i32;
    fn TranslateMessage(lpMsg: *const Msg) -> i32;
    fn DispatchMessageW(lpMsg: *const Msg) -> isize;
    fn PostThreadMessageW(idThread: u32, Msg: u32, wParam: usize, lParam: isize) -> i32;
    fn GetCurrentThreadId() -> u32;
}

type HookProc = unsafe extern "system" fn(code: i32, w_param: usize, l_param: isize) -> isize;

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

#[repr(C)]
struct KbdLlHookStruct {
    vk_code: u32,
    scan_code: u32,
    flags: u32,
    time: u32,
    dw_extra_info: usize,
}

const MOD_ALT: u32 = 0x0001;
const MOD_CONTROL: u32 = 0x0002;
const MOD_NOREPEAT: u32 = 0x4000;
const VK_SPACE: u32 = 0x20;
const VK_G: u32 = 0x47;
const WM_HOTKEY: u32 = 0x0312;
const WM_QUIT: u32 = 0x0012;

const WH_KEYBOARD_LL: i32 = 13;
const WM_KEYDOWN: usize = 0x0100;
const WM_KEYUP: usize = 0x0101;
const WM_SYSKEYDOWN: usize = 0x0104;
const WM_SYSKEYUP: usize = 0x0105;

const VK_CONTROL: u32 = 0x11;
const VK_LCONTROL: u32 = 0xA2;
const VK_RCONTROL: u32 = 0xA3;

pub const HOTKEY_ID_SPOTLIGHT: i32 = 1001;
pub const HOTKEY_ID_QUICK_SWITCH: i32 = 1002;

// Double Ctrl detection state for Listary signature gesture
static LAST_CTRL_UP_TIME: AtomicU64 = AtomicU64::new(0);
static INTERVENING_KEY: AtomicBool = AtomicBool::new(false);
static SPOTLIGHT_CALLBACK: RwLock<Option<Arc<dyn Fn() + Send + Sync>>> = RwLock::new(None);

pub fn current_time_millis() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_millis() as u64
}

/// Checks if two timestamps represent a double-press interval (<= 350ms)
pub fn is_double_ctrl_interval(last_up_ms: u64, now_ms: u64) -> bool {
    last_up_ms > 0 && now_ms >= last_up_ms && (now_ms - last_up_ms) <= 350
}

/// Win32 Low-Level Keyboard Hook Callback for Listary Double-Ctrl detection
unsafe extern "system" fn low_level_keyboard_proc(
    n_code: i32,
    w_param: usize,
    l_param: isize,
) -> isize {
    if n_code == 0 {
        let kb_ptr = l_param as *const KbdLlHookStruct;
        if !kb_ptr.is_null() {
            let vk = (*kb_ptr).vk_code;
            let is_ctrl = vk == VK_CONTROL || vk == VK_LCONTROL || vk == VK_RCONTROL;

            if w_param == WM_KEYDOWN || w_param == WM_SYSKEYDOWN {
                if !is_ctrl {
                    // Any non-ctrl key pressed cancels the double-ctrl gesture
                    INTERVENING_KEY.store(true, Ordering::SeqCst);
                }
            } else if w_param == WM_KEYUP || w_param == WM_SYSKEYUP {
                if is_ctrl {
                    let had_intervening = INTERVENING_KEY.swap(false, Ordering::SeqCst);
                    if !had_intervening {
                        let now = current_time_millis();
                        let last = LAST_CTRL_UP_TIME.load(Ordering::SeqCst);

                        if is_double_ctrl_interval(last, now) {
                            // Double Ctrl detected! Reset timer to prevent re-triggering on 3rd tap
                            LAST_CTRL_UP_TIME.store(0, Ordering::SeqCst);
                            if let Ok(guard) = SPOTLIGHT_CALLBACK.read() {
                                if let Some(cb) = guard.as_ref() {
                                    cb();
                                }
                            }
                        } else {
                            LAST_CTRL_UP_TIME.store(now, Ordering::SeqCst);
                        }
                    } else {
                        LAST_CTRL_UP_TIME.store(0, Ordering::SeqCst);
                    }
                }
            }
        }
    }

    CallNextHookEx(0, n_code, w_param, l_param)
}

pub struct HotkeyService {
    is_running: Arc<AtomicBool>,
    thread_id: Arc<std::sync::atomic::AtomicU32>,
}

impl HotkeyService {
    pub fn new() -> Self {
        Self {
            is_running: Arc::new(AtomicBool::new(false)),
            thread_id: Arc::new(std::sync::atomic::AtomicU32::new(0)),
        }
    }

    /// Starts global hotkey listener with WH_KEYBOARD_LL (Double-Ctrl) and RegisterHotKey (Alt+Space, Ctrl+G)
    pub fn start<F1, F2>(&self, on_spotlight: F1, on_quick_switch: F2)
    where
        F1: Fn() + Send + Sync + 'static,
        F2: Fn() + Send + Sync + 'static,
    {
        if self.is_running.swap(true, Ordering::SeqCst) {
            return;
        }

        if let Ok(mut guard) = SPOTLIGHT_CALLBACK.write() {
            *guard = Some(Arc::new(on_spotlight));
        }

        let running_flag = self.is_running.clone();
        let tid_holder = self.thread_id.clone();

        thread::spawn(move || {
            #[cfg(windows)]
            {
                let tid = unsafe { GetCurrentThreadId() };
                tid_holder.store(tid, Ordering::SeqCst);
            }

            // 1. Install Win32 WH_KEYBOARD_LL hook for Listary signature Double-Ctrl
            let hook = unsafe {
                SetWindowsHookExW(
                    WH_KEYBOARD_LL,
                    low_level_keyboard_proc,
                    0,
                    0,
                )
            };

            // 2. Register Alt + Space for Spotlight (backup / standard combination)
            let _ = unsafe {
                RegisterHotKey(
                    0,
                    HOTKEY_ID_SPOTLIGHT,
                    MOD_ALT | MOD_NOREPEAT,
                    VK_SPACE,
                )
            };

            // 3. Register Ctrl + G for Quick Switch
            let _ = unsafe {
                RegisterHotKey(
                    0,
                    HOTKEY_ID_QUICK_SWITCH,
                    MOD_CONTROL | MOD_NOREPEAT,
                    VK_G,
                )
            };

            let mut msg: Msg = unsafe { std::mem::zeroed() };
            while running_flag.load(Ordering::SeqCst) {
                let ret = unsafe { GetMessageW(&mut msg, 0, 0, 0) };
                if ret <= 0 || msg.message == WM_QUIT {
                    break;
                }

                if msg.message == WM_HOTKEY {
                    match msg.w_param as i32 {
                        HOTKEY_ID_SPOTLIGHT => {
                            if let Ok(guard) = SPOTLIGHT_CALLBACK.read() {
                                if let Some(cb) = guard.as_ref() {
                                    cb();
                                }
                            }
                        }
                        HOTKEY_ID_QUICK_SWITCH => {
                            on_quick_switch();
                        }
                        _ => {}
                    }
                }

                unsafe {
                    TranslateMessage(&msg);
                    DispatchMessageW(&msg);
                }
            }

            // Cleanup hook and hotkeys
            if hook != 0 {
                unsafe {
                    UnhookWindowsHookEx(hook);
                }
            }
            unsafe {
                UnregisterHotKey(0, HOTKEY_ID_SPOTLIGHT);
                UnregisterHotKey(0, HOTKEY_ID_QUICK_SWITCH);
            }
        });
    }

    pub fn stop(&self) {
        self.is_running.store(false, Ordering::SeqCst);
        let tid = self.thread_id.swap(0, Ordering::SeqCst);
        if tid != 0 {
            #[cfg(windows)]
            unsafe {
                PostThreadMessageW(tid, WM_QUIT, 0, 0);
            }
        }
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

    #[test]
    fn test_double_ctrl_interval_math() {
        // Interval within 350ms threshold triggers true
        assert!(is_double_ctrl_interval(1000, 1200));
        assert!(is_double_ctrl_interval(1000, 1350));
        // Interval greater than 350ms triggers false
        assert!(!is_double_ctrl_interval(1000, 1351));
        assert!(!is_double_ctrl_interval(1000, 1800));
        assert!(!is_double_ctrl_interval(0, 1200));
    }
}
