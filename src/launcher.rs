use serde::{Deserialize, Serialize};
use std::process::Command;

#[cfg(windows)]
#[link(name = "shell32")]
extern "system" {
    fn ShellExecuteW(
        hwnd: isize,
        lpOperation: *const u16,
        lpFile: *const u16,
        lpParameters: *const u16,
        lpDirectory: *const u16,
        nShowCmd: i32,
    ) -> isize;
}

fn to_wide_null(s: &str) -> Vec<u16> {
    s.encode_utf16().chain(std::iter::once(0)).collect()
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct LauncherActionHit {
    pub id: String,
    pub title: String,
    pub subtitle: String,
    pub kind: String, // "web_search", "system_command", "quick_tool"
    pub execute_payload: String,
    pub icon: String,
}

/// Detects if the query matches a web search shortcut or system command
pub fn detect_launcher_action(query: &str) -> Option<LauncherActionHit> {
    let trimmed = query.trim();
    if trimmed.is_empty() {
        return None;
    }

    // 1. Web Search Shortcuts (Listary Pro feature alignment)
    let parts: Vec<&str> = trimmed.splitn(2, ' ').collect();
    let prefix = parts[0].to_lowercase();
    let arg = if parts.len() > 1 { parts[1].trim() } else { "" };

    if !arg.is_empty() {
        match prefix.as_str() {
            "gh" | "github" => return Some(LauncherActionHit {
                id: "web_github".to_string(),
                title: format!("GitHub 搜索: {}", arg),
                subtitle: format!("直达 https://github.com/search?q={}", arg),
                kind: "web_search".to_string(),
                execute_payload: format!("https://github.com/search?q={}", urlencoding(arg)),
                icon: "github".to_string(),
            }),
            "cargo" | "crate" => return Some(LauncherActionHit {
                id: "web_cargo".to_string(),
                title: format!("Crates.io 搜索: {}", arg),
                subtitle: format!("直达 https://crates.io/search?q={}", arg),
                kind: "web_search".to_string(),
                execute_payload: format!("https://crates.io/search?q={}", urlencoding(arg)),
                icon: "cargo".to_string(),
            }),
            "npm" => return Some(LauncherActionHit {
                id: "web_npm".to_string(),
                title: format!("npm 搜索: {}", arg),
                subtitle: format!("直达 https://www.npmjs.com/search?q={}", arg),
                kind: "web_search".to_string(),
                execute_payload: format!("https://www.npmjs.com/search?q={}", urlencoding(arg)),
                icon: "npm".to_string(),
            }),
            "so" | "stack" => return Some(LauncherActionHit {
                id: "web_so".to_string(),
                title: format!("Stack Overflow 搜索: {}", arg),
                subtitle: format!("直达 https://stackoverflow.com/search?q={}", arg),
                kind: "web_search".to_string(),
                execute_payload: format!("https://stackoverflow.com/search?q={}", urlencoding(arg)),
                icon: "stackoverflow".to_string(),
            }),
            "py" | "pypi" => return Some(LauncherActionHit {
                id: "web_pypi".to_string(),
                title: format!("PyPI 搜索: {}", arg),
                subtitle: format!("直达 https://pypi.org/search/?q={}", arg),
                kind: "web_search".to_string(),
                execute_payload: format!("https://pypi.org/search/?q={}", urlencoding(arg)),
                icon: "python".to_string(),
            }),
            "docker" | "hub" => return Some(LauncherActionHit {
                id: "web_docker".to_string(),
                title: format!("Docker Hub 搜索: {}", arg),
                subtitle: format!("直达 https://hub.docker.com/search?q={}", arg),
                kind: "web_search".to_string(),
                execute_payload: format!("https://hub.docker.com/search?q={}", urlencoding(arg)),
                icon: "docker".to_string(),
            }),
            "bd" | "baidu" => return Some(LauncherActionHit {
                id: "web_baidu".to_string(),
                title: format!("百度搜索: {}", arg),
                subtitle: format!("直达 https://www.baidu.com/s?wd={}", arg),
                kind: "web_search".to_string(),
                execute_payload: format!("https://www.baidu.com/s?wd={}", urlencoding(arg)),
                icon: "search".to_string(),
            }),
            "bing" => return Some(LauncherActionHit {
                id: "web_bing".to_string(),
                title: format!("必应搜索: {}", arg),
                subtitle: format!("直达 https://www.bing.com/search?q={}", arg),
                kind: "web_search".to_string(),
                execute_payload: format!("https://www.bing.com/search?q={}", urlencoding(arg)),
                icon: "search".to_string(),
            }),
            "gg" | "google" => return Some(LauncherActionHit {
                id: "web_google".to_string(),
                title: format!("Google 搜索: {}", arg),
                subtitle: format!("直达 https://www.google.com/search?q={}", arg),
                kind: "web_search".to_string(),
                execute_payload: format!("https://www.google.com/search?q={}", urlencoding(arg)),
                icon: "search".to_string(),
            }),
            _ => {}
        }
    }

    // 2. Custom Command Execution (Listary Pro feature alignment)
    if trimmed.starts_with("cmd:") || trimmed.starts_with("cmd ") {
        let cmd_str = trimmed[4..].trim();
        return Some(LauncherActionHit {
            id: "cmd_runner".to_string(),
            title: format!("运行命令: {}", cmd_str),
            subtitle: "在 Windows CMD 命令提示符中执行".to_string(),
            kind: "system_command".to_string(),
            execute_payload: format!("cmd.exe /k {}", cmd_str),
            icon: "terminal".to_string(),
        });
    }

    if trimmed.starts_with("wt:") || trimmed.starts_with("wt ") {
        let cmd_str = trimmed[3..].trim();
        return Some(LauncherActionHit {
            id: "wt_runner".to_string(),
            title: format!("Terminal 运行: {}", cmd_str),
            subtitle: "在 Windows Terminal 中执行命令".to_string(),
            kind: "system_command".to_string(),
            execute_payload: format!("wt.exe -d . pwsh -NoExit -Command {}", cmd_str),
            icon: "terminal".to_string(),
        });
    }

    if trimmed.starts_with("pwsh:") || trimmed.starts_with("pwsh ") {
        let cmd_str = trimmed[5..].trim();
        return Some(LauncherActionHit {
            id: "pwsh_runner".to_string(),
            title: format!("PowerShell 运行: {}", cmd_str),
            subtitle: "在 PowerShell 终端执行".to_string(),
            kind: "system_command".to_string(),
            execute_payload: format!("powershell.exe -NoExit -Command {}", cmd_str),
            icon: "terminal".to_string(),
        });
    }

    if trimmed.starts_with("code:") || trimmed.starts_with("code ") {
        let target = trimmed[5..].trim();
        return Some(LauncherActionHit {
            id: "code_runner".to_string(),
            title: format!("VS Code 打开: {}", target),
            subtitle: "唤起 Visual Studio Code 编辑器".to_string(),
            kind: "system_command".to_string(),
            execute_payload: format!("code {}", target),
            icon: "code".to_string(),
        });
    }

    // 3. Quick System Tool Aliases
    match trimmed.to_lowercase().as_str() {
        "calc" | "jisuanqi" => Some(LauncherActionHit {
            id: "tool_calc".to_string(),
            title: "打开计算器 (calc)".to_string(),
            subtitle: "Windows 系统内置计算器应用".to_string(),
            kind: "quick_tool".to_string(),
            execute_payload: "calc.exe".to_string(),
            icon: "calculator".to_string(),
        }),
        "notepad" | "jishiben" => Some(LauncherActionHit {
            id: "tool_notepad".to_string(),
            title: "打开记事本 (notepad)".to_string(),
            subtitle: "Windows 系统内置文本编辑器".to_string(),
            kind: "quick_tool".to_string(),
            execute_payload: "notepad.exe".to_string(),
            icon: "document".to_string(),
        }),
        "regedit" => Some(LauncherActionHit {
            id: "tool_regedit".to_string(),
            title: "注册表编辑器 (regedit)".to_string(),
            subtitle: "管理 Windows 注册表配置库".to_string(),
            kind: "quick_tool".to_string(),
            execute_payload: "regedit.exe".to_string(),
            icon: "registry".to_string(),
        }),
        "taskmgr" => Some(LauncherActionHit {
            id: "tool_taskmgr".to_string(),
            title: "任务管理器 (taskmgr)".to_string(),
            subtitle: "查看并管理运行中的进程与资源占用".to_string(),
            kind: "quick_tool".to_string(),
            execute_payload: "taskmgr.exe".to_string(),
            icon: "taskmgr".to_string(),
        }),
        "cleanmgr" => Some(LauncherActionHit {
            id: "tool_cleanmgr".to_string(),
            title: "磁盘清理工具 (cleanmgr)".to_string(),
            subtitle: "Windows 原生磁盘释放管理器".to_string(),
            kind: "quick_tool".to_string(),
            execute_payload: "cleanmgr.exe".to_string(),
            icon: "clean".to_string(),
        }),
        "devmgmt" => Some(LauncherActionHit {
            id: "tool_devmgmt".to_string(),
            title: "设备管理器 (devmgmt.msc)".to_string(),
            subtitle: "管理系统硬件外设与驱动配置".to_string(),
            kind: "quick_tool".to_string(),
            execute_payload: "devmgmt.msc".to_string(),
            icon: "hardware".to_string(),
        }),
        _ => None,
    }
}

/// Opens a URL in default browser
pub fn open_browser(url: &str) -> Result<String, String> {
    execute_launcher_action("web_search", url)
}

/// Executes a detected launcher action
pub fn execute_launcher_action(kind: &str, payload: &str) -> Result<String, String> {
    if kind == "web_search" {
        // Open URL in default browser using Win32 ShellExecuteW
        let wide_open = to_wide_null("open");
        let wide_url = to_wide_null(payload);

        let ret = unsafe {
            ShellExecuteW(
                0,
                wide_open.as_ptr(),
                wide_url.as_ptr(),
                std::ptr::null(),
                std::ptr::null(),
                1, // SW_SHOWNORMAL
            )
        };

        if ret > 32 {
            Ok(format!("已在默认浏览器打开: {}", payload))
        } else {
            // Fallback to cmd start
            let _ = Command::new("cmd")
                .args(["/c", "start", "", payload])
                .spawn();
            Ok(format!("已启动浏览器检索: {}", payload))
        }
    } else if kind == "system_command" {
        let parts: Vec<&str> = payload.split_whitespace().collect();
        if parts.is_empty() {
            return Err("空的命令内容".to_string());
        }

        let program = parts[0];
        let args = &parts[1..];

        let mut cmd = Command::new(program);
        cmd.args(args);

        match cmd.spawn() {
            Ok(_) => Ok(format!("已成功启动命令: {}", payload)),
            Err(e) => Err(format!("启动失败: {}", e)),
        }
    } else if kind == "quick_tool" {
        match Command::new(payload).spawn() {
            Ok(_) => Ok(format!("已成功唤起工具: {}", payload)),
            Err(e) => {
                // Try shell execute
                let wide_open = to_wide_null("open");
                let wide_file = to_wide_null(payload);
                let ret = unsafe {
                    ShellExecuteW(
                        0,
                        wide_open.as_ptr(),
                        wide_file.as_ptr(),
                        std::ptr::null(),
                        std::ptr::null(),
                        1,
                    )
                };
                if ret > 32 {
                    Ok(format!("已唤起工具: {}", payload))
                } else {
                    Err(format!("唤起工具失败: {}", e))
                }
            }
        }
    } else {
        Err(format!("不支持的动作类型: {}", kind))
    }
}

fn urlencoding(s: &str) -> String {
    let mut encoded = String::new();
    for b in s.bytes() {
        if b.is_ascii_alphanumeric() || b == b'-' || b == b'_' || b == b'.' || b == b'~' {
            encoded.push(b as char);
        } else {
            encoded.push_str(&format!("%{:02X}", b));
        }
    }
    encoded
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_detect_web_search_shortcuts() {
        let hit = detect_launcher_action("gh tokio").unwrap();
        assert_eq!(hit.kind, "web_search");
        assert!(hit.execute_payload.contains("github.com/search?q=tokio"));

        let hit_cargo = detect_launcher_action("cargo serde").unwrap();
        assert_eq!(hit_cargo.kind, "web_search");
        assert!(hit_cargo.execute_payload.contains("crates.io/search?q=serde"));

        let hit_bd = detect_launcher_action("bd rust教程").unwrap();
        assert_eq!(hit_bd.kind, "web_search");
        assert!(hit_bd.execute_payload.contains("baidu.com/s?wd="));
    }

    #[test]
    fn test_detect_system_commands() {
        let hit_cmd = detect_launcher_action("cmd: ipconfig").unwrap();
        assert_eq!(hit_cmd.kind, "system_command");
        assert!(hit_cmd.execute_payload.contains("ipconfig"));

        let hit_code = detect_launcher_action("code C:\\Projects").unwrap();
        assert_eq!(hit_code.kind, "system_command");
        assert!(hit_code.execute_payload.contains("C:\\Projects"));
    }

    #[test]
    fn test_detect_quick_tools() {
        let hit_calc = detect_launcher_action("calc").unwrap();
        assert_eq!(hit_calc.kind, "quick_tool");
        assert_eq!(hit_calc.execute_payload, "calc.exe");

        let hit_task = detect_launcher_action("taskmgr").unwrap();
        assert_eq!(hit_task.kind, "quick_tool");
        assert_eq!(hit_task.execute_payload, "taskmgr.exe");
    }

    #[test]
    fn test_empty_and_normal_queries() {
        assert!(detect_launcher_action("").is_none());
        assert!(detect_launcher_action("cargo.toml").is_none());
        assert!(detect_launcher_action("normal_file.txt").is_none());
    }
}
