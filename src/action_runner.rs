use crate::migrator::reveal_in_explorer;
use crate::process_lock::{check_common_locking_processes, ProcessLockInfo};
use crate::quick_switch::execute_quick_switch;
use serde::{Deserialize, Serialize};
use std::env;
use std::fs;
use std::path::Path;
use std::process::Command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ActionItem {
    pub id: String,
    pub title: String,
    pub description: String,
    pub icon: String,
    pub shortcut: String,
    pub category: String,
    pub is_pro: bool,
    pub is_recommended: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ActionExecutionResult {
    pub success: bool,
    pub action_id: String,
    pub message: String,
    pub details: Option<serde_json::Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct CustomActionDef {
    pub id: String,
    pub name: String,
    pub description: String,
    pub program_path: String,
    pub arguments_template: String,
    pub target_pattern: String,
    pub run_as_admin: bool,
    pub shortcut: Option<String>,
    pub is_enabled: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DetectedToolsStatus {
    pub vscode: bool,
    pub vscode_path: Option<String>,
    pub windows_terminal: bool,
    pub notepad_plus: bool,
    pub seven_zip: bool,
    pub git: bool,
}

/// Detects common productivity tools on Windows
pub fn detect_installed_tools() -> DetectedToolsStatus {
    let vscode = find_executable_in_paths(&[
        "code.cmd",
        "code.exe",
        "%LOCALAPPDATA%\\Programs\\Microsoft VS Code\\bin\\code.cmd",
        "%PROGRAMFILES%\\Microsoft VS Code\\bin\\code.cmd",
    ]);

    let wt = is_executable_available("wt.exe");

    let np = find_executable_in_paths(&[
        "notepad++.exe",
        "%PROGRAMFILES%\\Notepad++\\notepad++.exe",
        "%PROGRAMFILES(X86)%\\Notepad++\\notepad++.exe",
    ]);

    let sz = find_executable_in_paths(&[
        "7zFM.exe",
        "7z.exe",
        "%PROGRAMFILES%\\7-Zip\\7zFM.exe",
        "%PROGRAMFILES(X86)%\\7-Zip\\7zFM.exe",
    ]);

    let git = is_executable_available("git.exe");

    DetectedToolsStatus {
        vscode: vscode.is_some(),
        vscode_path: vscode,
        windows_terminal: wt,
        notepad_plus: np.is_some(),
        seven_zip: sz.is_some(),
        git,
    }
}

fn expand_env(input: &str) -> String {
    let mut s = input.to_string();
    for (k, v) in env::vars() {
        let pattern = format!("%{}%", k);
        if s.contains(&pattern) {
            s = s.replace(&pattern, &v);
        }
    }
    s
}

fn is_executable_available(exe_name: &str) -> bool {
    Command::new("where.exe")
        .arg(exe_name)
        .output()
        .map(|out| out.status.success())
        .unwrap_or(false)
}

fn find_executable_in_paths(candidates: &[&str]) -> Option<String> {
    for c in candidates {
        let expanded = expand_env(c);
        let p = Path::new(&expanded);
        if p.exists() {
            return Some(expanded);
        }
    }
    None
}

/// Macro placeholder replacer for action commands
pub fn expand_action_macro(template: &str, target_path: &str) -> String {
    let p = Path::new(target_path);
    let full_path = target_path;
    let dir_path = if p.is_dir() {
        full_path.to_string()
    } else {
        p.parent().unwrap_or(p).to_string_lossy().to_string()
    };
    let file_name = p.file_name().unwrap_or_default().to_string_lossy().to_string();
    let basename = p.file_stem().unwrap_or_default().to_string_lossy().to_string();
    let ext = p.extension().unwrap_or_default().to_string_lossy().to_string();

    template
        .replace("{path}", full_path)
        .replace("{dir}", &dir_path)
        .replace("{name}", &file_name)
        .replace("{basename}", &basename)
        .replace("{ext}", &ext)
}

/// Lists all available actions intelligently classified and recommended for target
pub fn get_available_actions(target_path: &str) -> Vec<ActionItem> {
    let p = Path::new(target_path);
    let is_dir = p.is_dir();
    let ext = p.extension().and_then(|s| s.to_str()).unwrap_or("").to_lowercase();
    let tools = detect_installed_tools();

    let mut actions = Vec::new();

    // 1. Universal primary actions
    actions.push(ActionItem {
        id: "reveal".to_string(),
        title: "在文件资源管理器中定位".to_string(),
        description: "打开所在目录并高亮选中目标项".to_string(),
        icon: "folder".to_string(),
        shortcut: "1".to_string(),
        category: "system".to_string(),
        is_pro: false,
        is_recommended: true,
    });

    actions.push(ActionItem {
        id: "quick_switch".to_string(),
        title: "快速跳转前台对话框 (Quick Switch)".to_string(),
        description: "若有打开或另存为窗口，将路径秒级穿透注入".to_string(),
        icon: "switch".to_string(),
        shortcut: "2".to_string(),
        category: "system".to_string(),
        is_pro: true,
        is_recommended: true,
    });

    // 2. Directory contextual actions
    if is_dir {
        if tools.vscode {
            actions.push(ActionItem {
                id: "open_vscode".to_string(),
                title: "在 VS Code 中打开工作区".to_string(),
                description: "以 VS Code 打开该工程目录".to_string(),
                icon: "code".to_string(),
                shortcut: "3".to_string(),
                category: "editor".to_string(),
                is_pro: false,
                is_recommended: true,
            });
        }

        actions.push(ActionItem {
            id: "open_terminal".to_string(),
            title: "在此处打开终端 (Terminal)".to_string(),
            description: "以该目录为工作区启动 Windows Terminal 或命令行".to_string(),
            icon: "terminal".to_string(),
            shortcut: "4".to_string(),
            category: "terminal".to_string(),
            is_pro: false,
            is_recommended: true,
        });

        actions.push(ActionItem {
            id: "junction_migrate".to_string(),
            title: "Junction 跨盘搬迁打桩".to_string(),
            description: "安全将该目录迁至其他硬盘并创建透明软链接".to_string(),
            icon: "migrate".to_string(),
            shortcut: "5".to_string(),
            category: "storage".to_string(),
            is_pro: true,
            is_recommended: false,
        });
    } else {
        // 3. File contextual actions by type
        let is_code = matches!(
            ext.as_str(),
            "rs" | "py" | "js" | "ts" | "json" | "toml" | "md" | "txt" | "c" | "cpp" | "go" | "java" | "html" | "css" | "yaml" | "yml" | "bat" | "ps1" | "sh" | "xml"
        );
        let is_archive = matches!(ext.as_str(), "zip" | "7z" | "rar" | "tar" | "gz" | "tgz" | "bz2");
        let is_media = matches!(ext.as_str(), "mp4" | "mkv" | "avi" | "mov" | "flv" | "mp3" | "flac" | "wav" | "png" | "jpg" | "jpeg" | "webp");

        if is_code {
            if tools.vscode {
                actions.push(ActionItem {
                    id: "open_vscode".to_string(),
                    title: "在 VS Code 中编辑打开".to_string(),
                    description: "使用 Visual Studio Code 极速查看并编辑源码".to_string(),
                    icon: "code".to_string(),
                    shortcut: "3".to_string(),
                    category: "editor".to_string(),
                    is_pro: false,
                    is_recommended: true,
                });
            } else if tools.notepad_plus {
                actions.push(ActionItem {
                    id: "open_notepad_plus".to_string(),
                    title: "在 Notepad++ 中编辑打开".to_string(),
                    description: "使用 Notepad++ 极速查看并编辑文本".to_string(),
                    icon: "code".to_string(),
                    shortcut: "3".to_string(),
                    category: "editor".to_string(),
                    is_pro: false,
                    is_recommended: true,
                });
            } else {
                actions.push(ActionItem {
                    id: "open_notepad".to_string(),
                    title: "使用系统记事本打开".to_string(),
                    description: "调用 Windows 原生记事本进行快速查看".to_string(),
                    icon: "text".to_string(),
                    shortcut: "3".to_string(),
                    category: "editor".to_string(),
                    is_pro: false,
                    is_recommended: true,
                });
            }
        } else if is_archive {
            actions.push(ActionItem {
                id: "extract_archive".to_string(),
                title: "一键解压到同名文件夹".to_string(),
                description: "智能解压归档内容，避免多余散落文件".to_string(),
                icon: "archive".to_string(),
                shortcut: "3".to_string(),
                category: "archive".to_string(),
                is_pro: false,
                is_recommended: true,
            });
        } else if is_media {
            actions.push(ActionItem {
                id: "open_default".to_string(),
                title: "默认多媒体播放器播放".to_string(),
                description: "调用系统默认或关联程序秒级播放预览".to_string(),
                icon: "media".to_string(),
                shortcut: "3".to_string(),
                category: "system".to_string(),
                is_pro: false,
                is_recommended: true,
            });
        }

        actions.push(ActionItem {
            id: "open_terminal".to_string(),
            title: "在上级目录打开终端 (Terminal)".to_string(),
            description: "在该文件所在目录直接唤起命令行控制台".to_string(),
            icon: "terminal".to_string(),
            shortcut: "4".to_string(),
            category: "terminal".to_string(),
            is_pro: false,
            is_recommended: false,
        });

        actions.push(ActionItem {
            id: "blake3_hash".to_string(),
            title: "计算 BLAKE3 极速指纹".to_string(),
            description: "微秒级生成 256 位加密散列哈希校验码".to_string(),
            icon: "hash".to_string(),
            shortcut: "H".to_string(),
            category: "system".to_string(),
            is_pro: false,
            is_recommended: false,
        });
    }

    // 4. Universal safety & clipboard tools
    actions.push(ActionItem {
        id: "check_lock".to_string(),
        title: "排查文件占用与进程锁".to_string(),
        description: "检索谁在占用此文件并支持一键强力解锁".to_string(),
        icon: "lock".to_string(),
        shortcut: "L".to_string(),
        category: "storage".to_string(),
        is_pro: true,
        is_recommended: false,
    });

    actions.push(ActionItem {
        id: "copy_path".to_string(),
        title: "复制绝对路径".to_string(),
        description: "将完整绝对路径存入系统剪贴板".to_string(),
        icon: "copy".to_string(),
        shortcut: "C".to_string(),
        category: "system".to_string(),
        is_pro: false,
        is_recommended: false,
    });

    // 5. Append Custom Actions matching this target
    if let Ok(mgr) = get_global_custom_actions().read() {
        for ca in mgr.get_matching_actions(target_path, is_dir) {
            actions.push(ActionItem {
                id: format!("custom:{}", ca.id),
                title: ca.name.clone(),
                description: if ca.description.is_empty() { format!("自定义程序: {}", ca.program_path) } else { ca.description.clone() },
                icon: "custom".to_string(),
                shortcut: ca.shortcut.clone().unwrap_or_default(),
                category: "custom".to_string(),
                is_pro: true,
                is_recommended: false,
            });
        }
    }

    actions
}

/// Executes a selected action on the target path
pub fn execute_action(action_id: &str, target_path: &str) -> ActionExecutionResult {
    let p = Path::new(target_path);

    if action_id.starts_with("custom:") {
        let custom_id = &action_id[7..];
        if let Ok(mgr) = get_global_custom_actions().read() {
            match mgr.execute_custom_action(custom_id, target_path) {
                Ok(msg) => return ActionExecutionResult {
                    success: true,
                    action_id: action_id.to_string(),
                    message: msg,
                    details: None,
                },
                Err(err) => return ActionExecutionResult {
                    success: false,
                    action_id: action_id.to_string(),
                    message: err,
                    details: None,
                },
            }
        }
    }

    match action_id {
        "reveal" => {
            let _ = reveal_in_explorer(target_path);
            ActionExecutionResult {
                success: true,
                action_id: action_id.to_string(),
                message: "已在文件资源管理器中定位并选中目标".to_string(),
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
        "open_vscode" => {
            let status = Command::new("code.cmd")
                .arg(target_path)
                .spawn()
                .or_else(|_| Command::new("code").arg(target_path).spawn())
                .or_else(|_| {
                    if let Some(path) = detect_installed_tools().vscode_path {
                        Command::new(path).arg(target_path).spawn()
                    } else {
                        Err(std::io::Error::new(std::io::ErrorKind::NotFound, "VS Code not found"))
                    }
                });

            match status {
                Ok(_) => ActionExecutionResult {
                    success: true,
                    action_id: action_id.to_string(),
                    message: "已在 VS Code 中成功唤起目标".to_string(),
                    details: None,
                },
                Err(e) => ActionExecutionResult {
                    success: false,
                    action_id: action_id.to_string(),
                    message: format!("唤起 VS Code 失败: {}", e),
                    details: None,
                },
            }
        }
        "open_notepad" => match Command::new("notepad.exe").arg(target_path).spawn() {
            Ok(_) => ActionExecutionResult {
                success: true,
                action_id: action_id.to_string(),
                message: "已在系统记事本中打开".to_string(),
                details: None,
            },
            Err(e) => ActionExecutionResult {
                success: false,
                action_id: action_id.to_string(),
                message: format!("打开记事本失败: {}", e),
                details: None,
            },
        },
        "open_notepad_plus" => match Command::new("notepad++.exe").arg(target_path).spawn() {
            Ok(_) => ActionExecutionResult {
                success: true,
                action_id: action_id.to_string(),
                message: "已在 Notepad++ 中打开".to_string(),
                details: None,
            },
            Err(e) => ActionExecutionResult {
                success: false,
                action_id: action_id.to_string(),
                message: format!("打开 Notepad++ 失败: {}", e),
                details: None,
            },
        },
        "open_default" => {
            let wide_open = encode_wide_null("open");
            let wide_target = encode_wide_null(target_path);
            let ret = unsafe {
                ShellExecuteW(
                    0,
                    wide_open.as_ptr(),
                    wide_target.as_ptr(),
                    std::ptr::null(),
                    std::ptr::null(),
                    1,
                )
            };
            if ret > 32 {
                ActionExecutionResult {
                    success: true,
                    action_id: action_id.to_string(),
                    message: "已调用默认程序打开".to_string(),
                    details: None,
                }
            } else {
                ActionExecutionResult {
                    success: false,
                    action_id: action_id.to_string(),
                    message: "调用系统默认打开关联程序失败".to_string(),
                    details: None,
                }
            }
        }
        "extract_archive" => {
            let parent_dir = p.parent().unwrap_or(p).to_string_lossy().to_string();
            let stem = p.file_stem().unwrap_or_default().to_string_lossy().to_string();
            let dest_dir = Path::new(&parent_dir).join(&stem);
            let _ = fs::create_dir_all(&dest_dir);

            // Attempt using tar or 7z
            let status = Command::new("tar.exe")
                .args(["-xf", target_path, "-C", &dest_dir.to_string_lossy()])
                .spawn()
                .or_else(|_| {
                    Command::new("7z.exe")
                        .args(["x", target_path, &format!("-o{}", dest_dir.to_string_lossy()), "-y"])
                        .spawn()
                });

            match status {
                Ok(_) => ActionExecutionResult {
                    success: true,
                    action_id: action_id.to_string(),
                    message: format!("已成功提交解压任务至: {}", dest_dir.to_string_lossy()),
                    details: Some(serde_json::json!({ "dest_dir": dest_dir.to_string_lossy() })),
                },
                Err(e) => ActionExecutionResult {
                    success: false,
                    action_id: action_id.to_string(),
                    message: format!("提取归档文件异常: {}", e),
                    details: None,
                },
            }
        }
        "open_terminal" => {
            let working_dir = if p.is_dir() {
                p.to_string_lossy().to_string()
            } else {
                p.parent().unwrap_or(p).to_string_lossy().to_string()
            };

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

#[derive(Debug)]
pub struct CustomActionManager {
    actions: Vec<CustomActionDef>,
    storage_path: std::path::PathBuf,
}

impl CustomActionManager {
    pub fn new(storage_path: std::path::PathBuf) -> Self {
        let mut mgr = Self {
            actions: Vec::new(),
            storage_path,
        };
        mgr.load();
        mgr
    }

    pub fn load(&mut self) {
        if !self.storage_path.exists() {
            return;
        }
        if let Ok(content) = fs::read_to_string(&self.storage_path) {
            if let Ok(list) = serde_json::from_str::<Vec<CustomActionDef>>(&content) {
                self.actions = list;
            }
        }
    }

    pub fn save(&self) {
        if let Ok(json_str) = serde_json::to_string_pretty(&self.actions) {
            let tmp_path = self.storage_path.with_extension("tmp");
            if fs::write(&tmp_path, json_str).is_ok() {
                let _ = fs::rename(&tmp_path, &self.storage_path);
            }
        }
    }

    pub fn list_all(&self) -> Vec<CustomActionDef> {
        self.actions.clone()
    }

    pub fn save_action(&mut self, action: CustomActionDef) -> CustomActionDef {
        if let Some(pos) = self.actions.iter().position(|a| a.id == action.id) {
            self.actions[pos] = action.clone();
        } else {
            self.actions.push(action.clone());
        }
        self.save();
        action
    }

    pub fn delete_action(&mut self, id: &str) -> bool {
        let prev_len = self.actions.len();
        self.actions.retain(|a| a.id != id);
        let changed = self.actions.len() < prev_len;
        if changed {
            self.save();
        }
        changed
    }

    pub fn matches_target(&self, action: &CustomActionDef, target_path: &str, is_dir: bool) -> bool {
        if !action.is_enabled {
            return false;
        }
        let pattern = action.target_pattern.trim().to_lowercase();
        if pattern.is_empty() || pattern == "*" {
            return true;
        }
        if pattern == "directory" || pattern == "dir" || pattern == "folder" {
            return is_dir;
        }
        if is_dir {
            return false;
        }
        let ext = Path::new(target_path).extension().and_then(|s| s.to_str()).unwrap_or("").to_lowercase();
        for sub_pat in pattern.split([';', ',']) {
            let p = sub_pat.trim().trim_start_matches('*').trim_start_matches('.');
            if !p.is_empty() && ext == p {
                return true;
            }
        }
        false
    }

    pub fn get_matching_actions(&self, target_path: &str, is_dir: bool) -> Vec<CustomActionDef> {
        self.actions.iter()
            .filter(|a| self.matches_target(a, target_path, is_dir))
            .cloned()
            .collect()
    }

    pub fn execute_custom_action(&self, id: &str, target_path: &str) -> Result<String, String> {
        let action = self.actions.iter().find(|a| a.id == id)
            .ok_or_else(|| format!("Custom action not found: {}", id))?;

        let expanded_program = expand_env(&action.program_path);
        let expanded_args = expand_action_macro(&action.arguments_template, target_path);

        #[cfg(windows)]
        {
            if action.run_as_admin {
                let wide_prog = encode_wide_null(&expanded_program);
                let wide_args = encode_wide_null(&expanded_args);
                let wide_verb = encode_wide_null("runas");
                let res = unsafe {
                    ShellExecuteW(
                        0,
                        wide_verb.as_ptr(),
                        wide_prog.as_ptr(),
                        wide_args.as_ptr(),
                        std::ptr::null(),
                        1,
                    )
                };
                if res > 32 {
                    return Ok(format!("自定义动作 '{}' 已通过管理员权限提权启动", action.name));
                } else {
                    return Err(format!("ShellExecuteW 提权启动失败 (错误代码: {})", res));
                }
            }
        }

        let res = Command::new(&expanded_program)
            .args(expanded_args.split_whitespace())
            .spawn();

        match res {
            Ok(_) => Ok(format!("自定义动作 '{}' 已成功执行唤起", action.name)),
            Err(e) => Err(format!("执行自定义动作异常: {}", e)),
        }
    }
}

static GLOBAL_CUSTOM_ACTIONS: std::sync::OnceLock<std::sync::RwLock<CustomActionManager>> = std::sync::OnceLock::new();

pub fn get_global_custom_actions() -> &'static std::sync::RwLock<CustomActionManager> {
    GLOBAL_CUSTOM_ACTIONS.get_or_init(|| {
        let path = std::path::PathBuf::from("cleanflow_custom_actions.json");
        std::sync::RwLock::new(CustomActionManager::new(path))
    })
}

fn encode_wide_null(s: &str) -> Vec<u16> {
    s.encode_utf16().chain(std::iter::once(0)).collect()
}

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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_custom_action_manager_lifecycle() {
        let temp_dir = std::env::temp_dir().join(format!("cleanflow_custom_act_test_{}", std::process::id()));
        let _ = fs::remove_dir_all(&temp_dir);
        let _ = fs::create_dir_all(&temp_dir);
        let store_file = temp_dir.join("actions.json");

        let mut mgr = CustomActionManager::new(store_file.clone());
        assert_eq!(mgr.list_all().len(), 0);

        let action = CustomActionDef {
            id: "cursor_open".to_string(),
            name: "在 Cursor 中打开".to_string(),
            description: "以 Cursor AI 编辑器打开目标".to_string(),
            program_path: "cursor.exe".to_string(),
            arguments_template: "\"{path}\"".to_string(),
            target_pattern: "*".to_string(),
            run_as_admin: false,
            shortcut: Some("U".to_string()),
            is_enabled: true,
        };

        mgr.save_action(action.clone());
        assert_eq!(mgr.list_all().len(), 1);

        // Matching test
        let matches = mgr.get_matching_actions("C:\\Projects\\main.rs", false);
        assert_eq!(matches.len(), 1);
        assert_eq!(matches[0].name, "在 Cursor 中打开");

        // Specific pattern test
        let py_action = CustomActionDef {
            id: "py_run".to_string(),
            name: "运行 Python 脚本".to_string(),
            description: "执行脚本".to_string(),
            program_path: "python.exe".to_string(),
            arguments_template: "\"{path}\"".to_string(),
            target_pattern: "*.py".to_string(),
            run_as_admin: false,
            shortcut: None,
            is_enabled: true,
        };
        mgr.save_action(py_action);

        assert_eq!(mgr.get_matching_actions("C:\\Projects\\test.py", false).len(), 2);
        assert_eq!(mgr.get_matching_actions("C:\\Projects\\main.rs", false).len(), 1);

        // Delete test
        assert!(mgr.delete_action("cursor_open"));
        assert_eq!(mgr.list_all().len(), 1);

        let _ = fs::remove_dir_all(&temp_dir);
    }

    #[test]
    fn test_get_available_actions_directory() {
        let actions = get_available_actions("C:\\Windows\\System32");
        assert!(!actions.is_empty());
        assert!(actions.iter().any(|a| a.id == "reveal"));
        assert!(actions.iter().any(|a| a.id == "quick_switch"));
        assert!(actions.iter().any(|a| a.id == "junction_migrate"));
    }

    #[test]
    fn test_get_available_actions_code_file() {
        let actions = get_available_actions("C:\\Projects\\app\\main.rs");
        assert!(!actions.is_empty());
        assert!(actions.iter().any(|a| a.id == "reveal"));
        assert!(actions.iter().any(|a| a.id == "open_vscode" || a.id == "open_notepad"));
        assert!(actions.iter().any(|a| a.id == "blake3_hash"));
    }

    #[test]
    fn test_expand_action_macro() {
        let expanded = expand_action_macro("cmd.exe /K cd /d \"{dir}\"", "C:\\Projects\\app\\main.rs");
        assert!(expanded.contains("C:\\Projects\\app"));

        let expanded_file = expand_action_macro("view {name} {ext}", "C:\\Projects\\app\\main.rs");
        assert_eq!(expanded_file, "view main.rs rs");
    }

    #[test]
    fn test_execute_copy_path_action() {
        let res = execute_action("copy_path", "C:\\TestPath\\demo.txt");
        assert!(res.success);
        assert_eq!(res.message, "C:\\TestPath\\demo.txt");
    }
}
