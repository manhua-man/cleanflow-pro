use anyhow::{bail, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::process::Command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessLockInfo {
    pub name: String,
    pub pid: u32,
    pub description: String,
}

fn get_running_processes_map() -> HashMap<String, u32> {
    let mut map = HashMap::new();
    let mut cmd = Command::new("tasklist");
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        cmd.creation_flags(0x08000000);
    }
    if let Ok(output) = cmd.args(["/FO", "CSV", "/NH"]).output() {
        let text = String::from_utf8_lossy(&output.stdout);
        for line in text.lines() {
            let line = line.trim();
            if line.is_empty() {
                continue;
            }
            let parts: Vec<&str> = line.split(',').collect();
            if parts.len() >= 2 {
                let name = parts[0].trim_matches('"').to_lowercase();
                let pid_str = parts[1].trim_matches('"');
                if let Ok(pid) = pid_str.parse::<u32>() {
                    map.entry(name).or_insert(pid);
                }
            }
        }
    }
    map
}

pub fn check_common_locking_processes(path_hint: &str) -> Vec<ProcessLockInfo> {
    let mut found = Vec::new();
    let lower_hint = path_hint.to_lowercase();

    let candidates: Vec<(&str, &str)> = if lower_hint.contains("wechat") || lower_hint.contains("xwechat") {
        vec![
            ("WeChat.exe", "微信桌面端"),
            ("WeChatAppEx.exe", "微信小程序引擎"),
            ("xwechat.exe", "微信 4.0 原生进程"),
        ]
    } else if lower_hint.contains(".android") || lower_hint.contains("emulator") || lower_hint.contains("sdk") {
        vec![
            ("qemu-system-x86_64.exe", "Android 官方手机模拟器"),
            ("emulator.exe", "Android 模拟器主控进程"),
            ("studio64.exe", "Android Studio IDE"),
            ("adb.exe", "Android 调试桥"),
        ]
    } else if lower_hint.contains("ollama") {
        vec![
            ("ollama.exe", "Ollama 本地大模型服务端"),
            ("ollama_llama_server.exe", "Ollama LLaMA 推理引擎"),
        ]
    } else if lower_hint.contains("huggingface") || lower_hint.contains("torch") {
        vec![
            ("python.exe", "Python / PyTorch 模型加载进程"),
            ("pythonw.exe", "Python 后台训练/推理进程"),
        ]
    } else if lower_hint.contains("steam") {
        vec![
            ("steam.exe", "Steam 客户端"),
            ("steamwebhelper.exe", "Steam 内嵌 Web 运行服务"),
        ]
    } else if lower_hint.contains("unity") {
        vec![
            ("Unity.exe", "Unity 编辑器"),
            ("UnityHub.exe", "Unity Hub 管理端"),
        ]
    } else if lower_hint.contains("visualstudio") || lower_hint.contains("devenv") {
        vec![
            ("devenv.exe", "Visual Studio 集成开发环境"),
            ("MSBuild.exe", "MSBuild 构建工具"),
        ]
    } else if lower_hint.contains("cursor") {
        vec![("Cursor.exe", "Cursor AI 编辑器")]
    } else if lower_hint.contains("lark") || lower_hint.contains("feishu") {
        vec![("Lark.exe", "飞书客户端"), ("LarkShell.exe", "飞书容器")]
    } else {
        vec![]
    };

    let running_map = get_running_processes_map();

    for (proc_name, desc) in candidates {
        if let Some(&pid) = running_map.get(&proc_name.to_lowercase()) {
            found.push(ProcessLockInfo {
                name: proc_name.to_string(),
                pid,
                description: desc.to_string(),
            });
        }
    }

    found
}

pub fn kill_process_by_name(proc_name: &str) -> Result<()> {
    let clean_name = if proc_name.ends_with(".exe") {
        proc_name.to_string()
    } else {
        format!("{}.exe", proc_name)
    };

    let mut cmd = Command::new("taskkill");
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        cmd.creation_flags(0x08000000);
    }
    let status = cmd
        .args(["/F", "/IM", &clean_name])
        .status()?;

    if status.success() {
        Ok(())
    } else {
        bail!("终止进程 {} 失败，可能需要管理员权限", clean_name);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_running_processes_map() {
        let map = get_running_processes_map();
        assert!(!map.is_empty(), "Running processes should not be empty");
    }

    #[test]
    fn test_check_common_locking_processes_empty() {
        let locks = check_common_locking_processes("C:\\random_non_existent_path_12345");
        assert!(locks.is_empty());
    }
}
