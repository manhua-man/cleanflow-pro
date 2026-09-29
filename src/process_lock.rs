use anyhow::{bail, Result};
use serde::{Deserialize, Serialize};
use std::process::Command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessLockInfo {
    pub name: String,
    pub pid: u32,
    pub description: String,
}

pub fn check_common_locking_processes(path_hint: &str) -> Vec<ProcessLockInfo> {
    let mut found = Vec::new();
    let lower_hint = path_hint.to_lowercase();

    let candidates = if lower_hint.contains("wechat") || lower_hint.contains("xwechat") {
        vec![("WeChat.exe", "微信桌面端"), ("WeChatAppEx.exe", "微信小程序引擎")]
    } else if lower_hint.contains(".android") || lower_hint.contains("emulator") || lower_hint.contains("sdk") {
        vec![
            ("qemu-system-x86_64.exe", "Android 官方手机模拟器"),
            ("emulator.exe", "Android 模拟器主控进程"),
            ("studio64.exe", "Android Studio IDE"),
            ("adb.exe", "Android 调试桥"),
        ]
    } else if lower_hint.contains("cursor") {
        vec![("Cursor.exe", "Cursor AI 编辑器")]
    } else if lower_hint.contains("lark") || lower_hint.contains("feishu") {
        vec![("Lark.exe", "飞书客户端"), ("LarkShell.exe", "飞书容器")]
    } else if lower_hint.contains("unity") {
        vec![("Unity.exe", "Unity 编辑器"), ("UnityHub.exe", "Unity Hub")]
    } else {
        vec![]
    };

    for (proc_name, desc) in candidates {
        if let Some(pid) = get_process_pid(proc_name) {
            found.push(ProcessLockInfo {
                name: proc_name.to_string(),
                pid,
                description: desc.to_string(),
            });
        }
    }

    found
}

fn get_process_pid(proc_name: &str) -> Option<u32> {
    let script = format!(
        "(Get-Process -Name '{}' -ErrorAction SilentlyContinue | Select-Object -First 1).Id",
        proc_name.trim_end_matches(".exe")
    );

    if let Ok(output) = Command::new("powershell")
        .args(["-NoProfile", "-Command", &script])
        .output()
    {
        if output.status.success() {
            let out_str = String::from_utf8_lossy(&output.stdout).trim().to_string();
            if let Ok(pid) = out_str.parse::<u32>() {
                return Some(pid);
            }
        }
    }
    None
}

pub fn kill_process_by_name(proc_name: &str) -> Result<()> {
    let clean_name = proc_name.trim_end_matches(".exe");
    let script = format!("Stop-Process -Name '{}' -Force -ErrorAction SilentlyContinue", clean_name);

    let status = Command::new("powershell")
        .args(["-NoProfile", "-Command", &script])
        .status()?;

    if status.success() {
        Ok(())
    } else {
        bail!("终止进程 {} 失败", proc_name);
    }
}
