use anyhow::{bail, Context, Result};
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::{Arc, Mutex, OnceLock};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JunctionRecord {
    pub id: String,
    pub name: String,
    pub source_path: String,
    pub target_path: String,
    pub target_drive: String,
    pub size_bytes: u64,
    pub created_at: String,
    pub is_healthy: bool,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MigrationOutcome {
    pub source_path: PathBuf,
    pub target_path: PathBuf,
    pub bytes_moved: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MigrationJobStatus {
    pub is_active: bool,
    pub job_id: String,
    pub source_path: String,
    pub target_path: String,
    pub target_drive: String,
    pub state: String, // "IDLE" | "SCANNING" | "COPYING" | "LINKING" | "COMPLETED" | "FAILED"
    pub total_bytes: u64,
    pub copied_bytes: u64,
    pub total_files: u64,
    pub copied_files: u64,
    pub current_file: String,
    pub percent: f32,
    pub error_msg: Option<String>,
}

static CURRENT_MIGRATION: OnceLock<Arc<Mutex<MigrationJobStatus>>> = OnceLock::new();

fn get_job_state() -> Arc<Mutex<MigrationJobStatus>> {
    CURRENT_MIGRATION
        .get_or_init(|| {
            Arc::new(Mutex::new(MigrationJobStatus {
                is_active: false,
                job_id: String::new(),
                source_path: String::new(),
                target_path: String::new(),
                target_drive: String::new(),
                state: "IDLE".to_string(),
                total_bytes: 0,
                copied_bytes: 0,
                total_files: 0,
                copied_files: 0,
                current_file: String::new(),
                percent: 0.0,
                error_msg: None,
            }))
        })
        .clone()
}

pub fn get_migration_status() -> MigrationJobStatus {
    get_job_state().lock().unwrap().clone()
}

pub fn start_migration_task(source_str: String, target_drive_str: String) -> Result<String> {
    let src = PathBuf::from(&source_str);
    if !src.exists() {
        bail!("源目录不存在: {}", src.display());
    }

    if is_junction(&src) {
        bail!("该目录已经是系统虚拟联接 (Junction)，无需重复搬家: {}", src.display());
    }

    let folder_name = src.file_name().context("无法解析目录名")?.to_string_lossy().to_string();
    let parent_name = src.parent().and_then(|p| p.file_name()).unwrap_or_default().to_string_lossy().to_string();

    let dest_dir_name = format!("{}_{}", parent_name, folder_name);
    let dest_base = PathBuf::from(format!(r"{}:\CleanFlow_Storage", target_drive_str));
    if !dest_base.exists() {
        fs::create_dir_all(&dest_base).context("创建目标存储根目录失败")?;
    }

    let dst = dest_base.join(&dest_dir_name);
    if dst.exists() {
        bail!("目标目录已存在: {}，请先清理或重命名", dst.display());
    }

    let locks = crate::process_lock::check_common_locking_processes(&src.to_string_lossy());
    if !locks.is_empty() {
        let procs = locks.iter().map(|p| p.name.clone()).collect::<Vec<_>>().join(", ");
        bail!("检测到有进程正在占用待搬迁目录: {}。请先关闭这些应用后再启动搬迁，以防止数据冲突或写入中断。", procs);
    }

    let job_id = format!("{}_{}", target_drive_str, std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_millis());

    let state_arc = get_job_state();
    {
        let mut state = state_arc.lock().unwrap();
        if state.is_active && (state.state == "SCANNING" || state.state == "COPYING" || state.state == "LINKING") {
            bail!("当前已有正在执行的搬迁任务，请等待完成");
        }

        *state = MigrationJobStatus {
            is_active: true,
            job_id: job_id.clone(),
            source_path: src.to_string_lossy().to_string(),
            target_path: dst.to_string_lossy().to_string(),
            target_drive: target_drive_str.clone(),
            state: "SCANNING".to_string(),
            total_bytes: 0,
            copied_bytes: 0,
            total_files: 0,
            copied_files: 0,
            current_file: "正在统计待搬迁目录容量与文件数...".to_string(),
            percent: 0.0,
            error_msg: None,
        };
    }

    let thread_state = state_arc.clone();
    let thread_src = src.clone();
    let thread_dst = dst.clone();
    let thread_drive = target_drive_str.clone();
    let thread_folder_name = folder_name.clone();
    let thread_dest_dir_name = dest_dir_name.clone();

    std::thread::spawn(move || {
        let (src_size, total_files) = crate::scanner::calculate_path_stats(&thread_src);

        // Pre-flight check: Target drive space
        let drives = crate::disks::get_disk_drives();
        if let Some(target_d) = drives.iter().find(|d| d.letter.to_uppercase() == thread_drive.to_uppercase()) {
            let required = src_size + 1024 * 1024 * 1024; // +1GB margin
            if target_d.free_bytes < required {
                let mut s = thread_state.lock().unwrap();
                s.is_active = false;
                s.state = "FAILED".to_string();
                s.error_msg = Some(format!(
                    "目标盘 {} 空间不足! (需 {:.2} GB，当前仅剩 {:.2} GB)",
                    thread_drive,
                    required as f64 / (1024.0 * 1024.0 * 1024.0),
                    target_d.free_bytes as f64 / (1024.0 * 1024.0 * 1024.0)
                ));
                return;
            }
        }

        {
            let mut s = thread_state.lock().unwrap();
            s.total_bytes = src_size;
            s.total_files = total_files;
            s.state = "COPYING".to_string();
            s.current_file = "启动多线程无缓存极速同步...".to_string();
            s.percent = 0.0;
        }

        // Multi-threaded Robocopy execution with unbuffered I/O (/J) and directory attribute replication (/DCOPY:DAT)
        let copy_child = Command::new("robocopy")
            .args([
                thread_src.to_str().unwrap(),
                thread_dst.to_str().unwrap(),
                "/E", "/MT:16", "/J", "/DCOPY:DAT", "/R:1", "/W:1", "/NFL", "/NDL", "/NP", "/NC", "/NS",
            ])
            .spawn();

        let mut child = match copy_child {
            Ok(c) => c,
            Err(e) => {
                let mut s = thread_state.lock().unwrap();
                s.is_active = false;
                s.state = "FAILED".to_string();
                s.error_msg = Some(format!("启动 robocopy 传输失败: {}", e));
                let _ = fs::remove_dir_all(&thread_dst);
                return;
            }
        };

        // Real-time copy progress tracker loop
        while let Ok(None) = child.try_wait() {
            std::thread::sleep(std::time::Duration::from_millis(800));
            if thread_dst.exists() {
                let (dst_size, dst_files) = crate::scanner::calculate_path_stats(&thread_dst);
                let mut s = thread_state.lock().unwrap();
                s.copied_bytes = dst_size;
                s.copied_files = dst_files;
                if src_size > 0 {
                    let pct = ((dst_size as f32 / src_size as f32) * 92.0).clamp(0.0, 92.0);
                    s.percent = pct;
                    s.current_file = format!(
                        "已同步 {:.1} MB / {:.1} MB ({:.1}%)",
                        dst_size as f64 / (1024.0 * 1024.0),
                        src_size as f64 / (1024.0 * 1024.0),
                        pct
                    );
                }
            }
        }

        let copy_status = child.wait();
        match copy_status {
            Ok(status) if status.code().unwrap_or(-1) <= 7 => {
                // Copy succeeded, enter transactional atomic linking
                {
                    let mut s = thread_state.lock().unwrap();
                    s.copied_bytes = src_size;
                    s.copied_files = total_files;
                    s.percent = 95.0;
                    s.state = "LINKING".to_string();
                    s.current_file = "正在原子置换原目录并建立 NTFS 虚拟联接...".to_string();
                }

                // Transactional Staging: Attempt atomic rename of source directory
                let timestamp = std::time::SystemTime::now()
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap_or_default()
                    .as_secs();
                let staging_dir = thread_src.with_file_name(format!("{}.cleanflow_staging_{}", thread_folder_name, timestamp));

                if let Err(e) = fs::rename(&thread_src, &staging_dir) {
                    let mut s = thread_state.lock().unwrap();
                    s.is_active = false;
                    s.state = "FAILED".to_string();
                    s.error_msg = Some(format!("源目录被运行中的应用进程锁定（无法重命名）: {}。源数据毫发无损，请完全关闭对应软件后重试。", e));
                    let _ = fs::remove_dir_all(&thread_dst);
                    return;
                }

                match create_ntfs_junction(&thread_src, &thread_dst) {
                    Ok(()) => {
                        let record = JunctionRecord {
                            id: format!("{}_{}", thread_drive, thread_dest_dir_name),
                            name: thread_folder_name,
                            source_path: thread_src.to_string_lossy().to_string(),
                            target_path: thread_dst.to_string_lossy().to_string(),
                            target_drive: thread_drive,
                            size_bytes: src_size,
                            created_at: chrono_like_now(),
                            is_healthy: true,
                        };
                        let _ = register_junction(record);

                        // Asynchronously clean up staging directory now that junction is live
                        let _ = fs::remove_dir_all(&staging_dir);

                        let mut s = thread_state.lock().unwrap();
                        s.is_active = false;
                        s.state = "COMPLETED".to_string();
                        s.percent = 100.0;
                        s.current_file = "搬迁完成! 已建立透明符号联接".to_string();
                    }
                    Err(e) => {
                        // Rollback: Restore original source folder from staging
                        let _ = fs::rename(&staging_dir, &thread_src);
                        let _ = fs::remove_dir_all(&thread_dst);

                        let mut s = thread_state.lock().unwrap();
                        s.is_active = false;
                        s.state = "FAILED".to_string();
                        s.error_msg = Some(format!("{}。已安全自动回滚源目录。", e));
                    }
                }
            }
            Ok(status) => {
                let mut s = thread_state.lock().unwrap();
                s.is_active = false;
                s.state = "FAILED".to_string();
                s.error_msg = Some(format!("数据拷贝至目标盘失败，退出码: {:?}", status.code()));
                let _ = fs::remove_dir_all(&thread_dst);
            }
            Err(e) => {
                let mut s = thread_state.lock().unwrap();
                s.is_active = false;
                s.state = "FAILED".to_string();
                s.error_msg = Some(format!("等待 robocopy 完成失败: {}", e));
                let _ = fs::remove_dir_all(&thread_dst);
            }
        }
    });

    Ok(job_id)
}

pub fn migrate_to_drive<P: AsRef<Path>>(source: P, target_drive_letter: &str) -> Result<MigrationOutcome> {
    let src = source.as_ref();
    if !src.exists() {
        bail!("源目录不存在: {}", src.display());
    }

    if is_junction(src) {
        bail!("该目录已经是系统虚拟联接 (Junction)，无需重复搬家: {}", src.display());
    }

    let folder_name = src.file_name().context("无法解析目录名")?;
    let parent_name = src.parent().and_then(|p| p.file_name()).unwrap_or_default();

    let dest_dir_name = format!("{}_{}", parent_name.to_string_lossy(), folder_name.to_string_lossy());
    let dest_base = PathBuf::from(format!(r"{}:\CleanFlow_Storage", target_drive_letter));
    if !dest_base.exists() {
        fs::create_dir_all(&dest_base).context("创建目标存储根目录失败")?;
    }

    let dst = dest_base.join(&dest_dir_name);
    if dst.exists() {
        bail!("目标目录已存在: {}，请先清理或重命名", dst.display());
    }

    let locks = crate::process_lock::check_common_locking_processes(&src.to_string_lossy());
    if !locks.is_empty() {
        let procs = locks.iter().map(|p| p.name.clone()).collect::<Vec<_>>().join(", ");
        bail!("检测到有进程正在占用待搬迁目录: {}。请先关闭这些应用后再启动搬迁，以防止数据冲突或写入中断。", procs);
    }

    let (src_size, _) = crate::scanner::calculate_path_stats(src);

    // Pre-flight check: Target drive space
    let drives = crate::disks::get_disk_drives();
    if let Some(target_d) = drives.iter().find(|d| d.letter.to_uppercase() == target_drive_letter.to_uppercase()) {
        let required = src_size + 1024 * 1024 * 1024;
        if target_d.free_bytes < required {
            bail!(
                "目标盘 {} 空间不足! (需 {:.2} GB，当前仅剩 {:.2} GB)",
                target_drive_letter,
                required as f64 / (1024.0 * 1024.0 * 1024.0),
                target_d.free_bytes as f64 / (1024.0 * 1024.0 * 1024.0)
            );
        }
    }

    // 1. Robocopy with multi-thread & unbuffered I/O
    let status = Command::new("robocopy")
        .args([
            src.to_str().context("路径转字符串失败")?,
            dst.to_str().context("路径转字符串失败")?,
            "/E", "/MT:16", "/J", "/DCOPY:DAT", "/R:1", "/W:1", "/NFL", "/NDL", "/NP", "/NC", "/NS",
        ])
        .status()
        .context("执行系统拷贝命令失败")?;

    if status.code().unwrap_or(-1) > 7 {
        let _ = fs::remove_dir_all(&dst);
        bail!("复制数据到目标盘失败，退出码: {:?}", status.code());
    }

    // 2. Transactional Staging: Attempt atomic rename
    let timestamp = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs();
    let staging_dir = src.with_file_name(format!("{}.cleanflow_staging_{}", folder_name.to_string_lossy(), timestamp));

    if let Err(e) = fs::rename(src, &staging_dir) {
        let _ = fs::remove_dir_all(&dst);
        bail!("源目录被运行中的应用进程锁定（无法重命名）: {}。源数据毫发无损，请完全关闭对应软件后重试。", e);
    }

    // 3. Create NTFS Directory Junction
    if let Err(e) = create_ntfs_junction(src, &dst) {
        let _ = fs::rename(&staging_dir, src);
        let _ = fs::remove_dir_all(&dst);
        bail!("{}。已安全自动回滚源目录。", e);
    }

    // 4. Remove staging directory
    let _ = fs::remove_dir_all(&staging_dir);

    // 5. Save to junction registry
    let record = JunctionRecord {
        id: format!("{}_{}", target_drive_letter, dest_dir_name),
        name: folder_name.to_string_lossy().to_string(),
        source_path: src.to_string_lossy().to_string(),
        target_path: dst.to_string_lossy().to_string(),
        target_drive: target_drive_letter.to_string(),
        size_bytes: src_size,
        created_at: chrono_like_now(),
        is_healthy: true,
    };
    let _ = register_junction(record);

    Ok(MigrationOutcome {
        source_path: src.to_path_buf(),
        target_path: dst,
        bytes_moved: src_size,
    })
}

pub fn rollback_junction(source_path_str: &str) -> Result<u64> {
    let src = Path::new(source_path_str);
    if !src.exists() {
        bail!("源路径不存在: {}", source_path_str);
    }

    if !is_junction(src) {
        bail!("目标路径不是有效的 NTFS 目录联接: {}", source_path_str);
    }

    // Read target of the junction
    let target = fs::read_link(src).context("无法读取目录联接的目标路径")?;
    let target_path = if target.is_relative() {
        src.parent().unwrap_or(Path::new("")).join(&target)
    } else {
        target
    };

    if !target_path.exists() {
        bail!("联接指向的目标物理数据不存在: {}", target_path.display());
    }

    let (target_size, _) = crate::scanner::calculate_path_stats(&target_path);

    // Pre-flight check: Verify C: drive has enough free disk space
    let drives = crate::disks::get_disk_drives();
    if let Some(c_drive) = drives.iter().find(|d| d.letter.to_uppercase() == "C") {
        let required = target_size + 500 * 1024 * 1024; // safety margin
        if c_drive.free_bytes < required {
            bail!(
                "C 盘可用空间不足以迁回当前资产! (需要 {:.2} GB，当前仅剩 {:.2} GB)",
                required as f64 / (1024.0 * 1024.0 * 1024.0),
                c_drive.free_bytes as f64 / (1024.0 * 1024.0 * 1024.0)
            );
        }
    }

    // 1. Remove ONLY the junction link
    fs::remove_dir(src).context("解除目录联接失败，可能有程序正在访问该路径")?;

    // 2. Re-create normal directory at source
    fs::create_dir_all(src).context("重建源物理目录失败")?;

    // 3. Robocopy data back from target to source with /J unbuffered and /DCOPY:DAT
    let status = Command::new("robocopy")
        .args([
            target_path.to_str().context("路径转字符串失败")?,
            src.to_str().context("路径转字符串失败")?,
            "/E", "/MT:16", "/J", "/DCOPY:DAT", "/R:1", "/W:1", "/NFL", "/NDL", "/NP", "/NC", "/NS",
        ])
        .status()
        .context("执行还原数据拷贝失败")?;

    if status.code().unwrap_or(-1) > 7 {
        bail!("还原复制数据失败，退出码: {:?}", status.code());
    }

    // 4. Remove physical data on target drive
    let _ = fs::remove_dir_all(&target_path);

    // 5. Unregister
    let _ = unregister_junction(source_path_str);

    Ok(target_size)
}

pub fn create_ntfs_junction<P: AsRef<Path>, Q: AsRef<Path>>(source: P, destination: Q) -> Result<()> {
    let src = source.as_ref().to_str().context("源路径转字符串失败")?;
    let dst = destination.as_ref().to_str().context("目标路径转字符串失败")?;

    let output = Command::new("cmd")
        .args(["/C", "mklink", "/J", src, dst])
        .output()
        .context("执行系统 cmd mklink 失败")?;

    if output.status.success() {
        Ok(())
    } else {
        let err = String::from_utf8_lossy(&output.stderr).to_string();
        let out = String::from_utf8_lossy(&output.stdout).to_string();
        let msg = if !err.trim().is_empty() { err } else { out };
        bail!("创建 NTFS 目录联接失败: {}", msg.trim());
    }
}

pub fn is_junction<P: AsRef<Path>>(path: P) -> bool {
    let p = path.as_ref();
    if let Ok(meta) = fs::symlink_metadata(p) {
        meta.file_type().is_symlink()
    } else {
        false
    }
}

pub fn reveal_in_explorer<P: AsRef<Path>>(path: P) -> Result<()> {
    let p = path.as_ref();
    if !p.exists() {
        bail!("路径不存在: {}", p.display());
    }

    let path_str = p.to_string_lossy().to_string();
    if p.is_file() {
        let _ = Command::new("explorer")
            .arg(format!("/select,\"{}\"", path_str))
            .spawn();
    } else {
        let _ = Command::new("explorer")
            .arg(&path_str)
            .spawn();
    }
    Ok(())
}

fn registry_file_path() -> PathBuf {
    if let Ok(app_data) = std::env::var("LOCALAPPDATA") {
        let mut p = PathBuf::from(app_data);
        p.push("CleanFlow");
        let _ = fs::create_dir_all(&p);
        p.push("junctions.json");
        p
    } else {
        PathBuf::from("junctions.json")
    }
}

pub fn list_active_junctions() -> Vec<JunctionRecord> {
    let reg_path = registry_file_path();
    let mut records: Vec<JunctionRecord> = if reg_path.exists() {
        fs::read_to_string(&reg_path)
            .ok()
            .and_then(|s| serde_json::from_str(&s).ok())
            .unwrap_or_default()
        } else {
            Vec::new()
        };

    // Update real-time size and health status
    for item in &mut records {
        let src = Path::new(&item.source_path);
        let dst = Path::new(&item.target_path);

        let src_is_junc = is_junction(src);
        let dst_exists = dst.exists();

        item.is_healthy = src_is_junc && dst_exists;

        if dst_exists && item.size_bytes == 0 {
            let (sz, _) = crate::scanner::calculate_path_stats(dst);
            item.size_bytes = sz;
        }
    }

    records
}

pub fn register_junction(record: JunctionRecord) -> Result<()> {
    let mut records = list_active_junctions();
    records.retain(|r| r.source_path != record.source_path);
    records.push(record);
    save_junction_registry(&records)
}

pub fn unregister_junction(source_path_str: &str) -> Result<()> {
    let mut records = list_active_junctions();
    records.retain(|r| r.source_path != source_path_str);
    save_junction_registry(&records)
}

fn save_junction_registry(records: &[JunctionRecord]) -> Result<()> {
    let reg_path = registry_file_path();
    let content = serde_json::to_string_pretty(records)?;
    fs::write(reg_path, content)?;
    Ok(())
}

fn chrono_like_now() -> String {
    if let Ok(output) = Command::new("powershell")
        .args(["-NoProfile", "-Command", "Get-Date -Format 'yyyy-MM-dd HH:mm'"])
        .output()
    {
        if output.status.success() {
            return String::from_utf8_lossy(&output.stdout).trim().to_string();
        }
    }
    "最近创建".to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_junction_on_normal_dir() {
        let temp = std::env::temp_dir();
        assert!(!is_junction(&temp));
    }

    #[test]
    fn test_get_migration_status_idle() {
        let st = get_migration_status();
        assert!(!st.is_active || st.state == "COMPLETED" || st.state == "FAILED" || st.state == "IDLE");
    }

    #[test]
    fn test_create_and_detect_junction() {
        let temp = std::env::temp_dir();
        let target_dir = temp.join("cleanflow_test_target_dir");
        let link_dir = temp.join("cleanflow_test_link_dir");

        let _ = fs::remove_dir_all(&target_dir);
        let _ = fs::remove_dir(&link_dir);
        let _ = fs::create_dir_all(&target_dir);

        let res = create_ntfs_junction(&link_dir, &target_dir);
        assert!(res.is_ok(), "create_ntfs_junction failed: {:?}", res.err());
        assert!(is_junction(&link_dir));

        let _ = fs::remove_dir(&link_dir);
        let _ = fs::remove_dir_all(&target_dir);
    }
}
