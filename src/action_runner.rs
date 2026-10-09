use crate::migrator::reveal_in_explorer;
use crate::process_lock::{check_common_locking_processes, ProcessLockInfo};
use crate::quick_switch::execute_quick_switch;
use serde::{Deserialize, Serialize};
use std::path::Path;
use std::process::Command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ActionItem {
    pub id: String,
    pub title: String,
    pub description: String,
    pub icon: String,
    pub shortcut: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ActionExecutionResult {
    pub success: bool,
    pub action_id: String,
    pub message: String,
    pub details: Option<serde_json::Value>,
}

/// Lists all available actions for a given file or folder target
pub fn get_available_actions(target_path: &str) -> Vec<ActionItem> {
    let p = Path::new(target_path);
    let is_dir = p.is_dir();

    let mut actions = vec![
        ActionItem {
            id: "reveal".to_string(),
            title: "在文件资源管理器中定位".to_string(),
            description: "打开包含该文件的目录并高亮选中".to_string(),
            icon: "folder".to_string(),
            shortcut: "Enter".to_string(),
        },
        ActionItem {
            id: "quick_switch".to_string(),
            title: "快速跳转对话框 (Quick Switch)".to_string(),
            description: "若有打开/另存为窗口，将视图直接跳至该目录".to_string(),
            icon: "switch".to_string(),
            shortcut: "Ctrl+G".to_string(),
        },
        ActionItem {
            id: "open_terminal".to_string(),
            title: "在终端中打开 (pwsh / cmd)".to_string(),
            description: "在当前目录唤起命令行终端控制台".to_string(),
            icon: "terminal".to_string(),
            shortcut: "Ctrl+T".to_string(),
        },
        ActionItem {
            id: "copy_path".to_string(),
            title: "复制绝对路径".to_string(),
            description: "将完整文件/目录路径存入剪贴板".to_string(),
            icon: "copy".to_string(),
            shortcut: "Ctrl+C".to_string(),
        },
    ];

    if is_dir {
        actions.push(ActionItem {
            id: "junction_migrate".to_string(),
            title: "Junction 跨盘搬迁打桩".to_string(),
            description: "将该目录安全迁至大容量硬盘并创建透明软链接".to_string(),
            icon: "migrate".to_string(),
            shortcut: "Ctrl+M".to_string(),
        });
    }

    actions.push(ActionItem {
        id: "check_lock".to_string(),
        title: "排查文件占用与进程锁".to_string(),
        description: "检索谁在占用此文件并支持一键释放".to_string(),
        icon: "lock".to_string(),
        shortcut: "Ctrl+L".to_string(),
    });

    if !is_dir {
        actions.push(ActionItem {
            id: "blake3_hash".to_string(),
            title: "计算 BLAKE3 极速指纹".to_string(),
            description: "微秒级生成 256 位加密散列哈希校验码".to_string(),
            icon: "hash".to_string(),
            shortcut: "Ctrl+H".to_string(),
        });
    }

    actions
}

/// Executes a selected action on the target path
pub fn execute_action(action_id: &str, target_path: &str) -> ActionExecutionResult {
    let p = Path::new(target_path);

    match action_id {
        "reveal" => {
            let _ = reveal_in_explorer(target_path);
            ActionExecutionResult {
                success: true,
                action_id: action_id.to_string(),
                message: "已在文件资源管理器中定位并选中".to_string(),
                details: None,
            }
        }
        "quick_switch" => match execute_quick_switch(target_path) {
            Ok(_) => ActionExecutionResult {
                success: true,
                action_id: action_id.to_string(),
                message: "已成功将前台文件对话框跳转至目标路径".to_string(),
                details: None,
            },
            Err(e) => ActionExecutionResult {
                success: false,
                action_id: action_id.to_string(),
                message: e,
                details: None,
            },
        },
        "open_terminal" => {
            let working_dir = if p.is_dir() {
                p.to_string_lossy().to_string()
            } else {
                p.parent().unwrap_or(p).to_string_lossy().to_string()
            };

            // Attempt launching Windows Terminal (wt.exe) or fallback to pwsh / cmd
            let status = Command::new("wt.exe")
                .args(["-d", &working_dir])
                .spawn()
                .or_else(|_| {
                    Command::new("powershell.exe")
                        .args(["-NoExit", "-Command", &format!("Set-Location '{}'", working_dir)])
                        .spawn()
                })
                .or_else(|_| {
                    Command::new("cmd.exe")
                        .args(["/K", &format!("cd /d \"{}\"", working_dir)])
                        .spawn()
                });

            match status {
                Ok(_) => ActionExecutionResult {
                    success: true,
                    action_id: action_id.to_string(),
                    message: format!("已在 {} 启动终端窗口", working_dir),
                    details: None,
                },
                Err(e) => ActionExecutionResult {
                    success: false,
                    action_id: action_id.to_string(),
                    message: format!("启动终端失败: {}", e),
                    details: None,
                },
            }
        }
        "copy_path" => ActionExecutionResult {
            success: true,
            action_id: action_id.to_string(),
            message: target_path.to_string(),
            details: Some(serde_json::json!({ "path": target_path })),
        },
        "check_lock" => {
            let locks: Vec<ProcessLockInfo> = check_common_locking_processes(target_path);
            let count = locks.len();
            ActionExecutionResult {
                success: true,
                action_id: action_id.to_string(),
                message: if count > 0 {
                    format!("发现 {} 个进程正在占用该路径", count)
                } else {
                    "该文件/目录未检测到常见活动进程锁占用".to_string()
                },
                details: Some(serde_json::to_value(&locks).unwrap_or_default()),
            }
        }
        "blake3_hash" => {
            if let Some(hash) = crate::duplicates::compute_file_hash(p) {
                ActionExecutionResult {
                    success: true,
                    action_id: action_id.to_string(),
                    message: format!("BLAKE3: {}", hash),
                    details: Some(serde_json::json!({ "hash": hash })),
                }
            } else {
                ActionExecutionResult {
                    success: false,
                    action_id: action_id.to_string(),
                    message: "计算哈希失败，文件不存在或无读取权限".to_string(),
                    details: None,
                }
            }
        }
        _ => ActionExecutionResult {
            success: false,
            action_id: action_id.to_string(),
            message: format!("未知的动作标识: {}", action_id),
            details: None,
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_available_actions() {
        let actions = get_available_actions("C:\\Windows\\System32");
        assert!(!actions.is_empty());
        assert!(actions.iter().any(|a| a.id == "reveal"));
        assert!(actions.iter().any(|a| a.id == "quick_switch"));
        assert!(actions.iter().any(|a| a.id == "junction_migrate"));
    }

    #[test]
    fn test_execute_copy_path_action() {
        let res = execute_action("copy_path", "C:\\TestPath\\demo.txt");
        assert!(res.success);
        assert_eq!(res.message, "C:\\TestPath\\demo.txt");
    }
}
