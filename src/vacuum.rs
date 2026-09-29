use anyhow::{bail, Context, Result};
use std::ffi::{c_char, c_void, CStr, CString};
use std::path::Path;

#[cfg(windows)]
extern "system" {
    fn LoadLibraryA(lpLibFileName: *const c_char) -> *mut c_void;
    fn GetProcAddress(hModule: *mut c_void, lpProcName: *const c_char) -> *mut c_void;
    fn FreeLibrary(hLibModule: *mut c_void) -> i32;
}

type Sqlite3Open = unsafe extern "C" fn(*const c_char, *mut *mut c_void) -> i32;
type Sqlite3Exec = unsafe extern "C" fn(
    *mut c_void,
    *const c_char,
    *const c_void,
    *const c_void,
    *mut *mut c_char,
) -> i32;
type Sqlite3Close = unsafe extern "C" fn(*mut c_void) -> i32;
type Sqlite3Free = unsafe extern "C" fn(*mut c_void);
type Sqlite3Errmsg = unsafe extern "C" fn(*mut c_void) -> *const c_char;

#[derive(Debug, serde::Serialize)]
pub struct VacuumResult {
    pub path: String,
    pub original_size: u64,
    pub new_size: u64,
    pub bytes_freed: u64,
}

pub fn vacuum_sqlite_database<P: AsRef<Path>>(db_path: P) -> Result<VacuumResult> {
    let p = db_path.as_ref();
    if !p.exists() || !p.is_file() {
        bail!("数据库文件不存在: {}", p.display());
    }

    let orig_sz = std::fs::metadata(p)
        .context("获取数据库文件元数据失败")?
        .len();

    // 1. Try native Windows SQLite engine (C:\Windows\System32\winsqlite3.dll)
    let native_res = vacuum_via_winsqlite(p);
    match native_res {
        Ok(_) => {
            let new_sz = std::fs::metadata(p)
                .context("获取压缩后数据库元数据失败")?
                .len();
            let bytes_freed = orig_sz.saturating_sub(new_sz);
            return Ok(VacuumResult {
                path: p.to_string_lossy().to_string(),
                original_size: orig_sz,
                new_size: new_sz,
                bytes_freed,
            });
        }
        Err(err) => {
            // Fallback: If native engine was blocked or failed, attempt PowerShell embedded interop
            let ps_res = vacuum_via_powershell(p);
            if let Ok(_) = ps_res {
                let new_sz = std::fs::metadata(p)
                    .context("获取压缩后数据库元数据失败")?
                    .len();
                let bytes_freed = orig_sz.saturating_sub(new_sz);
                return Ok(VacuumResult {
                    path: p.to_string_lossy().to_string(),
                    original_size: orig_sz,
                    new_size: new_sz,
                    bytes_freed,
                });
            } else {
                bail!("原生与系统 SQLite 收缩均未能完成: {}", err);
            }
        }
    }
}

fn vacuum_via_winsqlite(p: &Path) -> Result<()> {
    #[cfg(windows)]
    unsafe {
        let dll_name = CString::new("winsqlite3.dll")?;
        let h_module = LoadLibraryA(dll_name.as_ptr());
        if h_module.is_null() {
            bail!("无法加载系统 winsqlite3.dll 动态链接库");
        }

        let sym_open = CString::new("sqlite3_open")?;
        let sym_exec = CString::new("sqlite3_exec")?;
        let sym_close = CString::new("sqlite3_close")?;
        let sym_free = CString::new("sqlite3_free")?;
        let sym_err = CString::new("sqlite3_errmsg")?;

        let fn_open: Sqlite3Open = std::mem::transmute(GetProcAddress(h_module, sym_open.as_ptr()));
        let fn_exec: Sqlite3Exec = std::mem::transmute(GetProcAddress(h_module, sym_exec.as_ptr()));
        let fn_close: Sqlite3Close = std::mem::transmute(GetProcAddress(h_module, sym_close.as_ptr()));
        let fn_free: Sqlite3Free = std::mem::transmute(GetProcAddress(h_module, sym_free.as_ptr()));
        let fn_err: Sqlite3Errmsg = std::mem::transmute(GetProcAddress(h_module, sym_err.as_ptr()));

        let path_str = p.to_string_lossy().to_string();
        let c_path = CString::new(path_str.as_bytes())?;

        let mut db: *mut c_void = std::ptr::null_mut();
        let rc_open = fn_open(c_path.as_ptr(), &mut db);
        if rc_open != 0 || db.is_null() {
            FreeLibrary(h_module);
            bail!("打开数据库失败，错误码: {}", rc_open);
        }

        // Run VACUUM and WAL truncation
        let sql = CString::new("PRAGMA busy_timeout = 8000; PRAGMA wal_checkpoint(TRUNCATE); VACUUM; PRAGMA optimize;")?;
        let mut err_ptr: *mut c_char = std::ptr::null_mut();
        let rc_exec = fn_exec(db, sql.as_ptr(), std::ptr::null(), std::ptr::null(), &mut err_ptr);

        let mut err_msg = String::new();
        if rc_exec != 0 {
            if !err_ptr.is_null() {
                err_msg = CStr::from_ptr(err_ptr).to_string_lossy().to_string();
                fn_free(err_ptr as *mut c_void);
            } else {
                let msg_c = fn_err(db);
                if !msg_c.is_null() {
                    err_msg = CStr::from_ptr(msg_c).to_string_lossy().to_string();
                }
            }
        }

        fn_close(db);
        FreeLibrary(h_module);

        if rc_exec != 0 {
            bail!("执行 VACUUM 失败: {} (代码: {})", err_msg, rc_exec);
        }

        Ok(())
    }

    #[cfg(not(windows))]
    {
        bail!("原生 Windows SQLite 仅支持在 Windows 平台运行");
    }
}

fn vacuum_via_powershell(p: &Path) -> Result<()> {
    let script = format!(
        r#"$code = @"
using System;
using System.Runtime.InteropServices;
public class WinSqliteRunner {{
    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_open(string f, out IntPtr db);
    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_exec(IntPtr db, string s, IntPtr cb, IntPtr arg, out IntPtr err);
    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_close(IntPtr db);
    public static int Compact(string file) {{
        IntPtr db;
        int rc = sqlite3_open(file, out db);
        if (rc != 0) return rc;
        IntPtr err;
        rc = sqlite3_exec(db, "PRAGMA wal_checkpoint(TRUNCATE); VACUUM;", IntPtr.Zero, IntPtr.Zero, out err);
        sqlite3_close(db);
        return rc;
    }}
}}
"@
Add-Type -TypeDefinition $code -ErrorAction SilentlyContinue
[WinSqliteRunner]::Compact('{}')
"#,
        p.to_string_lossy().replace("'", "''")
    );

    let output = std::process::Command::new("powershell")
        .args(["-NoProfile", "-NonInteractive", "-Command", &script])
        .output()
        .context("执行系统 PowerShell 辅助进程失败")?;

    let text = String::from_utf8_lossy(&output.stdout).trim().to_string();
    if text == "0" {
        Ok(())
    } else {
        bail!("PowerShell 收缩返回非零状态: {}", text)
    }
}
