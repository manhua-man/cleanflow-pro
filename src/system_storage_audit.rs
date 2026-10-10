use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::process::Command;

#[cfg(windows)]
use std::os::windows::process::CommandExt;

#[cfg(windows)]
const CREATE_NO_WINDOW: u32 = 0x08000000;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct DriverPackageInfo {
    pub published_name: String,   // 例如 oem127.inf
    pub original_name: String,    // 例如 rtkfilter.inf
    pub provider: String,         // 例如 Realtek Semiconductor Corp.
    pub class_name: String,       // 例如 Bluetooth
    pub driver_version: String,   // 例如 1.9.1051.3002
    pub driver_date: String,      // 例如 06/10/2022
    pub signer_name: String,      // 签名者
    pub size_bytes: u64,          // DriverStore\FileRepository 物理尺寸
    pub is_outdated: bool,        // 是否为被新版本取代的废弃旧驱动包
    pub is_latest: bool,          // 是否为当前最新主版本
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HibernationStatus {
    pub enabled: bool,
    pub file_path: String,
    pub size_bytes: u64,
    pub size_formatted: String,
    pub can_reduce: bool,
    pub status_description: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReservedStorageStatus {
    pub enabled: bool,
    pub hard_reserve_bytes: u64,
    pub soft_reserve_bytes: u64,
    pub total_reserve_bytes: u64,
    pub total_formatted: String,
    pub state_description: String,
    pub optimization_tip: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemStorageAuditReport {
    pub driver_packages: Vec<DriverPackageInfo>,
    pub total_driver_count: usize,
    pub outdated_driver_count: usize,
    pub total_driver_store_bytes: u64,
    pub outdated_driver_store_bytes: u64,
    pub hibernation: HibernationStatus,
    pub reserved_storage: ReservedStorageStatus,
    pub total_potential_reclaimable_bytes: u64,
}

pub fn format_size(bytes: u64) -> String {
    const KB: u64 = 1024;
    const MB: u64 = KB * 1024;
    const GB: u64 = MB * 1024;

    if bytes >= GB {
        format!("{:.2} GB", bytes as f64 / GB as f64)
    } else if bytes >= MB {
        format!("{:.2} MB", bytes as f64 / MB as f64)
    } else if bytes >= KB {
        format!("{:.2} KB", bytes as f64 / KB as f64)
    } else {
        format!("{} B", bytes)
    }
}

pub fn parse_pnputil_output(output: &str) -> Vec<DriverPackageInfo> {
    let mut packages = Vec::new();
    let blocks: Vec<&str> = output.split("\n\n").collect();

    for block in blocks {
        let trimmed = block.trim();
        if !trimmed.contains("Published Name:") && !trimmed.contains("发布名称:") {
            continue;
        }

        let mut published_name = String::new();
        let mut original_name = String::new();
        let mut provider = String::new();
        let mut class_name = String::new();
        let mut driver_version = String::new();
        let mut driver_date = String::new();
        let mut signer_name = String::new();

        for line in trimmed.lines() {
            let line_trim = line.trim();
            if let Some((k, v)) = line_trim.split_once(':') {
                let key = k.trim();
                let val = v.trim();
                match key {
                    "Published Name" | "发布名称" => published_name = val.to_string(),
                    "Original Name" | "原始名称" => original_name = val.to_string(),
                    "Provider Name" | "提供程序名称" => provider = val.to_string(),
                    "Class Name" | "类名称" => class_name = val.to_string(),
                    "Driver Version" | "驱动程序版本" => {
                        // 格式通常为 "06/10/2022 1.9.1051.3002"
                        let parts: Vec<&str> = val.split_whitespace().collect();
                        if parts.len() >= 2 {
                            driver_date = parts[0].to_string();
                            driver_version = parts[1..].join(" ");
                        } else {
                            driver_version = val.to_string();
                        }
                    }
                    "Driver Date and Version" | "驱动程序日期和版本" => {
                        let parts: Vec<&str> = val.split_whitespace().collect();
                        if parts.len() >= 2 {
                            driver_date = parts[0].to_string();
                            driver_version = parts[1..].join(" ");
                        } else {
                            driver_version = val.to_string();
                        }
                    }
                    "Signer Name" | "签名者名称" => signer_name = val.to_string(),
                    _ => {}
                }
            }
        }

        if !published_name.is_empty() {
            packages.push(DriverPackageInfo {
                published_name,
                original_name,
                provider,
                class_name,
                driver_version,
                driver_date,
                signer_name,
                size_bytes: 0,
                is_outdated: false,
                is_latest: true,
            });
        }
    }

    packages
}

pub fn parse_version_numbers(ver: &str) -> Vec<u64> {
    ver.split('.')
        .filter_map(|part| part.trim().parse::<u64>().ok())
        .collect()
}

pub fn parse_date_components(date_str: &str) -> (u32, u32, u32) {
    // 处理 MM/DD/YYYY 或 YYYY-MM-DD 或 YYYY/MM/DD
    let parts: Vec<&str> = date_str.split(&['/', '-'][..]).collect();
    if parts.len() == 3 {
        if parts[0].len() == 4 {
            // YYYY-MM-DD
            let y = parts[0].parse::<u32>().unwrap_or(0);
            let m = parts[1].parse::<u32>().unwrap_or(0);
            let d = parts[2].parse::<u32>().unwrap_or(0);
            return (y, m, d);
        } else if parts[2].len() == 4 {
            // MM/DD/YYYY
            let m = parts[0].parse::<u32>().unwrap_or(0);
            let d = parts[1].parse::<u32>().unwrap_or(0);
            let y = parts[2].parse::<u32>().unwrap_or(0);
            return (y, m, d);
        }
    }
    (0, 0, 0)
}

pub fn compare_driver_versions(ver_a: &str, date_a: &str, ver_b: &str, date_b: &str) -> std::cmp::Ordering {
    let nums_a = parse_version_numbers(ver_a);
    let nums_b = parse_version_numbers(ver_b);

    if !nums_a.is_empty() && !nums_b.is_empty() {
        let max_len = nums_a.len().max(nums_b.len());
        for i in 0..max_len {
            let na = nums_a.get(i).copied().unwrap_or(0);
            let nb = nums_b.get(i).copied().unwrap_or(0);
            if na != nb {
                return na.cmp(&nb);
            }
        }
    }

    // 若版本号相等或无法数字比对，退化为日期比对
    let d_a = parse_date_components(date_a);
    let d_b = parse_date_components(date_b);
    d_a.cmp(&d_b)
}

fn calculate_dir_size_fast(path: &Path) -> u64 {
    let mut total = 0;
    if let Ok(entries) = fs::read_dir(path) {
        for entry in entries.flatten() {
            if let Ok(meta) = entry.metadata() {
                if meta.is_file() {
                    total += meta.len();
                } else if meta.is_dir() {
                    total += calculate_dir_size_fast(&entry.path());
                }
            }
        }
    }
    total
}

pub fn scan_file_repository_dir_sizes() -> HashMap<String, u64> {
    let mut map = HashMap::new();
    let repo_dir = Path::new(r"C:\Windows\System32\DriverStore\FileRepository");
    if !repo_dir.exists() {
        return map;
    }

    if let Ok(entries) = fs::read_dir(repo_dir) {
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_dir() {
                if let Some(folder_name) = path.file_name().and_then(|n| n.to_str()) {
                    let sz = calculate_dir_size_fast(&path);
                    map.insert(folder_name.to_lowercase(), sz);
                }
            }
        }
    }

    map
}

pub fn classify_and_populate_drivers(
    mut drivers: Vec<DriverPackageInfo>,
    repo_sizes: &HashMap<String, u64>,
) -> Vec<DriverPackageInfo> {
    // 1. 关联物理体积：在 repo_sizes 中寻找匹配的前缀
    for d in &mut drivers {
        let inf_prefix = d.original_name.to_lowercase();
        // 查找所有以 "{inf_prefix}_" 开头的目录
        let mut matched_size = 0;
        let mut match_count = 0;
        for (folder, sz) in repo_sizes {
            if folder.starts_with(&format!("{}_", inf_prefix)) {
                matched_size += sz;
                match_count += 1;
            }
        }
        if match_count == 1 {
            d.size_bytes = matched_size;
        } else if match_count > 1 {
            // 平摊或取单份代表性尺寸，避免除以0
            d.size_bytes = matched_size / (match_count as u64);
        }
    }

    // 2. 按 (original_name, class_name) 分组，寻找最新版本与废弃版本
    let mut group_indices: HashMap<(String, String), Vec<usize>> = HashMap::new();
    for (i, d) in drivers.iter().enumerate() {
        let key = (d.original_name.to_lowercase(), d.class_name.to_lowercase());
        group_indices.entry(key).or_default().push(i);
    }

    for (_, indices) in group_indices {
        if indices.len() <= 1 {
            // 单独驱动，保持最新状态
            if let Some(&idx) = indices.first() {
                drivers[idx].is_latest = true;
                drivers[idx].is_outdated = false;
            }
            continue;
        }

        // 寻找版本最大的索引
        let mut best_idx = indices[0];
        for &idx in &indices[1..] {
            let cur = &drivers[idx];
            let best = &drivers[best_idx];
            if compare_driver_versions(
                &cur.driver_version,
                &cur.driver_date,
                &best.driver_version,
                &best.driver_date,
            ) == std::cmp::Ordering::Greater
            {
                best_idx = idx;
            }
        }

        for &idx in &indices {
            if idx == best_idx {
                drivers[idx].is_latest = true;
                drivers[idx].is_outdated = false;
            } else {
                drivers[idx].is_latest = false;
                drivers[idx].is_outdated = true;
            }
        }
    }

    drivers
}

pub fn get_driver_store_audit() -> (Vec<DriverPackageInfo>, u64, u64) {
    let mut cmd = Command::new("pnputil");
    cmd.arg("/enum-drivers");

    #[cfg(windows)]
    cmd.creation_flags(CREATE_NO_WINDOW);

    let output = match cmd.output() {
        Ok(out) => String::from_utf8_lossy(&out.stdout).to_string(),
        Err(_) => String::new(),
    };

    let raw_drivers = parse_pnputil_output(&output);
    let repo_sizes = scan_file_repository_dir_sizes();
    let classified = classify_and_populate_drivers(raw_drivers, &repo_sizes);

    let mut total_bytes = 0;
    let mut outdated_bytes = 0;
    for d in &classified {
        total_bytes += d.size_bytes;
        if d.is_outdated {
            outdated_bytes += d.size_bytes;
        }
    }

    (classified, total_bytes, outdated_bytes)
}

pub fn delete_driver_package(published_name: &str, force: bool) -> Result<String, String> {
    let p_lower = published_name.to_lowercase();
    if !p_lower.starts_with("oem") || !p_lower.ends_with(".inf") {
        return Err("安全防护拦截：驱动包名称必须为合规的 oem*.inf 命名".to_string());
    }

    let mut cmd = Command::new("pnputil");
    cmd.args(["/delete-driver", published_name]);
    if force {
        cmd.arg("/force");
    }

    #[cfg(windows)]
    cmd.creation_flags(CREATE_NO_WINDOW);

    let output = cmd
        .output()
        .map_err(|e| format!("执行 pnputil 失败: {}", e))?;

    let stdout_str = String::from_utf8_lossy(&output.stdout);
    let stderr_str = String::from_utf8_lossy(&output.stderr);

    if output.status.success() {
        Ok(format!("成功移除驱动包 {}: {}", published_name, stdout_str.trim()))
    } else {
        let err_msg = if !stderr_str.trim().is_empty() {
            stderr_str.trim().to_string()
        } else {
            stdout_str.trim().to_string()
        };
        Err(format!("移除驱动包 {} 失败: {}", published_name, err_msg))
    }
}

pub fn get_hibernation_status() -> HibernationStatus {
    let hiber_path = Path::new(r"C:\hiberfil.sys");
    if hiber_path.exists() {
        let sz = fs::metadata(hiber_path).map(|m| m.len()).unwrap_or(0);
        HibernationStatus {
            enabled: true,
            file_path: r"C:\hiberfil.sys".to_string(),
            size_bytes: sz,
            size_formatted: format_size(sz),
            can_reduce: true,
            status_description: format!(
                "休眠文件已激活，当前独占物理磁盘空间 {}。对于固定台式机或长期接电源的设备，可精简或完全关闭。",
                format_size(sz)
            ),
        }
    } else {
        HibernationStatus {
            enabled: false,
            file_path: r"C:\hiberfil.sys".to_string(),
            size_bytes: 0,
            size_formatted: "0 B".to_string(),
            can_reduce: false,
            status_description: "系统休眠处于未激活状态，未占用任何系统磁盘空间。".to_string(),
        }
    }
}

pub fn set_hibernation_mode(mode: &str) -> Result<String, String> {
    let mode_lower = mode.to_lowercase();
    let mut cmd = Command::new("powercfg");

    match mode_lower.as_str() {
        "off" => {
            cmd.args(["/hibernate", "off"]);
        }
        "reduced" => {
            cmd.args(["/hibernate", "/type", "reduced"]);
        }
        "full" => {
            cmd.args(["/hibernate", "/type", "full"]);
        }
        _ => return Err("无效的休眠调优模式，仅支持 off、reduced、full".to_string()),
    }

    #[cfg(windows)]
    cmd.creation_flags(CREATE_NO_WINDOW);

    let output = cmd
        .output()
        .map_err(|e| format!("执行 powercfg 失败: {}", e))?;

    if output.status.success() {
        let action_name = match mode_lower.as_str() {
            "off" => "已彻底关闭休眠并释放 hiberfil.sys 物理占用空间",
            "reduced" => "已切换为精简休眠模式（仅保留快速启动，体积减半）",
            "full" => "已恢复完整休眠模式",
            _ => "已应用模式",
        };
        Ok(action_name.to_string())
    } else {
        let err_msg = String::from_utf8_lossy(&output.stderr);
        Err(format!("调优休眠模式失败: {}", err_msg.trim()))
    }
}

pub fn get_reserved_storage_status() -> ReservedStorageStatus {
    let mut cmd = Command::new("reg");
    cmd.args(["query", r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\ReserveManager"]);

    #[cfg(windows)]
    cmd.creation_flags(CREATE_NO_WINDOW);

    let mut hard_reserve: u64 = 0;
    let mut soft_reserve: u64 = 0;
    let mut shipped_with_reserves = false;

    if let Ok(out) = cmd.output() {
        let text = String::from_utf8_lossy(&out.stdout);
        for line in text.lines() {
            let line_trim = line.trim();
            if line_trim.starts_with("BaseHardReserveSize") {
                if let Some(hex_part) = line_trim.split_whitespace().last() {
                    let cleaned = hex_part.trim_start_matches("0x");
                    hard_reserve = u64::from_str_radix(cleaned, 16).unwrap_or(0);
                }
            } else if line_trim.starts_with("BaseSoftReserveSize") {
                if let Some(hex_part) = line_trim.split_whitespace().last() {
                    let cleaned = hex_part.trim_start_matches("0x");
                    soft_reserve = u64::from_str_radix(cleaned, 16).unwrap_or(0);
                }
            } else if line_trim.starts_with("ShippedWithReserves") {
                if let Some(val_part) = line_trim.split_whitespace().last() {
                    let cleaned = val_part.trim_start_matches("0x");
                    shipped_with_reserves = cleaned == "1";
                }
            }
        }
    }

    let total = hard_reserve + soft_reserve;
    let is_enabled = shipped_with_reserves || total > 0;

    ReservedStorageStatus {
        enabled: is_enabled,
        hard_reserve_bytes: hard_reserve,
        soft_reserve_bytes: soft_reserve,
        total_reserve_bytes: total,
        total_formatted: format_size(total),
        state_description: if is_enabled {
            format!(
                "Windows 保留存储处于启用状态（预留物理空间 {}），用于防止系统更新因磁盘耗尽而失败。",
                format_size(total)
            )
        } else {
            "Windows 保留存储处于未启用状态。".to_string()
        },
        optimization_tip: if is_enabled {
            "若系统盘容量极度吃紧，可在管理员终端运行 dism /online /set-reservedstoragestate /state:disabled 释放约 7GB 预留空间。".to_string()
        } else {
            "保留存储未占用多余磁盘空间。".to_string()
        },
    }
}

pub fn run_system_storage_audit() -> SystemStorageAuditReport {
    let (drivers, total_driver_sz, outdated_driver_sz) = get_driver_store_audit();
    let hibernation = get_hibernation_status();
    let reserved_storage = get_reserved_storage_status();

    let total_reclaimable = outdated_driver_sz + hibernation.size_bytes;

    let total_driver_count = drivers.len();
    let outdated_driver_count = drivers.iter().filter(|d| d.is_outdated).count();

    SystemStorageAuditReport {
        driver_packages: drivers,
        total_driver_count,
        outdated_driver_count,
        total_driver_store_bytes: total_driver_sz,
        outdated_driver_store_bytes: outdated_driver_sz,
        hibernation,
        reserved_storage,
        total_potential_reclaimable_bytes: total_reclaimable,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_pnputil_output_mock() {
        let sample = r#"
Published Name:     oem128.inf
Original Name:      rtkfilter.inf
Provider Name:      Realtek Semiconductor Corp.
Class Name:         Bluetooth
Class GUID:         {e0cbf06c-cd8b-4647-bb8a-263b43f0f974}
Driver Version:     07/01/2022 1.9.1051.3004
Signer Name:        Microsoft Windows Hardware Compatibility Publisher

Published Name:     oem127.inf
Original Name:      rtkfilter.inf
Provider Name:      Realtek Semiconductor Corp.
Class Name:         Bluetooth
Class GUID:         {e0cbf06c-cd8b-4647-bb8a-263b43f0f974}
Driver Version:     06/10/2022 1.9.1051.3002
Signer Name:        Microsoft Windows Hardware Compatibility Publisher
"#;
        let pkgs = parse_pnputil_output(sample);
        assert_eq!(pkgs.len(), 2);
        assert_eq!(pkgs[0].published_name, "oem128.inf");
        assert_eq!(pkgs[0].original_name, "rtkfilter.inf");
        assert_eq!(pkgs[0].driver_version, "1.9.1051.3004");
        assert_eq!(pkgs[0].driver_date, "07/01/2022");
    }

    #[test]
    fn test_compare_driver_versions() {
        let cmp1 = compare_driver_versions(
            "1.9.1051.3004",
            "07/01/2022",
            "1.9.1051.3002",
            "06/10/2022",
        );
        assert_eq!(cmp1, std::cmp::Ordering::Greater);

        let cmp2 = compare_driver_versions(
            "31.0.101.4255",
            "03/16/2023",
            "31.0.101.5333",
            "02/21/2024",
        );
        assert_eq!(cmp2, std::cmp::Ordering::Less);

        let cmp3 = compare_driver_versions(
            "2.0.0",
            "01/01/2023",
            "2.0.0",
            "01/01/2023",
        );
        assert_eq!(cmp3, std::cmp::Ordering::Equal);
    }

    #[test]
    fn test_classify_and_populate_drivers() {
        let sample = r#"
Published Name:     oem128.inf
Original Name:      rtkfilter.inf
Provider Name:      Realtek Semiconductor Corp.
Class Name:         Bluetooth
Driver Version:     07/01/2022 1.9.1051.3004

Published Name:     oem127.inf
Original Name:      rtkfilter.inf
Provider Name:      Realtek Semiconductor Corp.
Class Name:         Bluetooth
Driver Version:     06/10/2022 1.9.1051.3002

Published Name:     oem5.inf
Original Name:      unique.inf
Provider Name:      Vendor
Class Name:         Display
Driver Version:     01/01/2023 1.0.0.0
"#;
        let pkgs = parse_pnputil_output(sample);
        let mut mock_sizes = HashMap::new();
        mock_sizes.insert("rtkfilter.inf_amd64_123".to_string(), 1024 * 1024);
        mock_sizes.insert("unique.inf_amd64_456".to_string(), 2048 * 1024);

        let classified = classify_and_populate_drivers(pkgs, &mock_sizes);
        assert_eq!(classified.len(), 3);

        let oem128 = classified.iter().find(|d| d.published_name == "oem128.inf").unwrap();
        let oem127 = classified.iter().find(|d| d.published_name == "oem127.inf").unwrap();
        let oem5 = classified.iter().find(|d| d.published_name == "oem5.inf").unwrap();

        assert!(oem128.is_latest);
        assert!(!oem128.is_outdated);

        assert!(!oem127.is_latest);
        assert!(oem127.is_outdated);

        assert!(oem5.is_latest);
        assert!(!oem5.is_outdated);
    }

    #[test]
    fn test_delete_driver_package_name_guard() {
        let res = delete_driver_package("malicious; rm -rf /", false);
        assert!(res.is_err());
        assert!(res.unwrap_err().contains("安全防护拦截"));
    }

    #[test]
    fn test_hibernation_and_reserved_storage_status_query() {
        let hib = get_hibernation_status();
        let _ = hib.enabled;
        let _ = hib.size_bytes;

        let res = get_reserved_storage_status();
        let _ = res.enabled;
        let _ = res.total_reserve_bytes;
    }
}
