use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::RwLock;
use std::time::{SystemTime, UNIX_EPOCH};

#[cfg(windows)]
extern "system" {
    fn SHQueryUserNotificationState(pquns: *mut u32) -> i32;
    fn GetLastInputInfo(plii: *mut LASTINPUTINFO) -> i32;
    fn GetTickCount() -> u32;
}

#[cfg(windows)]
#[repr(C)]
#[allow(non_snake_case)]
struct LASTINPUTINFO {
    cbSize: u32,
    dwTime: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum UserNotificationContext {
    AcceptsNotifications, // 可正常接收温和提示
    BusyFullScreen,      // 全屏独占 (游戏/视频/全屏放映)，严禁打扰
    PresentationMode,    // 演示放映模式，严禁打扰
    QuietTime,           // 免打扰时段，严禁打扰
    NotPresent,          // 用户不在电脑前
    Other(u32),
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct DiskSample {
    pub timestamp_secs: u64,
    pub free_bytes: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum BurnRateTrend {
    Stable,        // 波动平稳 (< 10 MB/min)
    FillingFast,   // 快速消耗 (> 50 MB/min)
    CriticalSurge, // 突发暴增 (> 300 MB/min)
    Reclaiming,    // 空间释放中 (> 10 MB/min 回收)
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BurnRateForecast {
    pub drive_letter: String,
    pub current_free_bytes: u64,
    pub rate_mb_per_min: f64, // 负数代表减少，正数代表增加
    pub trend: BurnRateTrend,
    pub estimated_minutes_to_exhaustion: Option<u64>,
    pub forecast_warning: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SelfHealingRule {
    pub id: String,
    pub name: String,
    pub description: String,
    pub enabled: bool,
    pub trigger_min_free_gb: u64,
    pub require_idle: bool,
    pub require_dnd_inactive: bool,
    pub action_type: String, // "empty_recycle_bin", "clean_temp_garbage", "evict_cloud_files"
    pub cooldown_seconds: u64,
    pub last_triggered_secs: u64,
    pub total_times_triggered: usize,
    pub total_bytes_saved: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SelfHealingEvent {
    pub timestamp_secs: u64,
    pub rule_id: String,
    pub rule_name: String,
    pub action_executed: String,
    pub bytes_freed: u64,
    pub message: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IntelligentGuardStatus {
    pub notification_state: UserNotificationContext,
    pub notification_state_label: String,
    pub is_dnd_active: bool,
    pub user_idle_seconds: u64,
    pub is_idle_for_background_task: bool,
    pub forecast: BurnRateForecast,
    pub rules: Vec<SelfHealingRule>,
    pub recent_events: Vec<SelfHealingEvent>,
}

pub fn get_user_notification_state() -> (UserNotificationContext, bool) {
    #[cfg(windows)]
    unsafe {
        let mut state: u32 = 0;
        let hr = SHQueryUserNotificationState(&mut state);
        if hr == 0 {
            match state {
                1 => (UserNotificationContext::NotPresent, true),
                2 => (UserNotificationContext::BusyFullScreen, true),
                3 => (UserNotificationContext::BusyFullScreen, true), // QUNS_RUNNING_D3D_FULL_SCREEN
                4 => (UserNotificationContext::PresentationMode, true),
                5 => (UserNotificationContext::AcceptsNotifications, false),
                6 => (UserNotificationContext::QuietTime, true),
                7 => (UserNotificationContext::BusyFullScreen, true), // QUNS_APP
                other => (UserNotificationContext::Other(other), false),
            }
        } else {
            (UserNotificationContext::AcceptsNotifications, false)
        }
    }
    #[cfg(not(windows))]
    {
        (UserNotificationContext::AcceptsNotifications, false)
    }
}

pub fn get_user_idle_seconds() -> u64 {
    #[cfg(windows)]
    unsafe {
        let mut lii = LASTINPUTINFO {
            cbSize: std::mem::size_of::<LASTINPUTINFO>() as u32,
            dwTime: 0,
        };
        if GetLastInputInfo(&mut lii) != 0 {
            let tick = GetTickCount();
            if tick >= lii.dwTime {
                let diff_ms = tick - lii.dwTime;
                return (diff_ms / 1000) as u64;
            }
        }
        0
    }
    #[cfg(not(windows))]
    {
        0
    }
}

pub fn calculate_burn_rate(samples: &[DiskSample]) -> (f64, BurnRateTrend, Option<u64>) {
    if samples.len() < 2 {
        return (0.0, BurnRateTrend::Stable, None);
    }

    let oldest = &samples[0];
    let newest = &samples[samples.len() - 1];

    if newest.timestamp_secs <= oldest.timestamp_secs {
        return (0.0, BurnRateTrend::Stable, None);
    }

    let elapsed_secs = (newest.timestamp_secs - oldest.timestamp_secs) as f64;
    let elapsed_mins = elapsed_secs / 60.0;
    if elapsed_mins < 0.05 {
        return (0.0, BurnRateTrend::Stable, None);
    }

    // 变动量：正数代表增加，负数代表减少（消耗）
    let delta_bytes = newest.free_bytes as f64 - oldest.free_bytes as f64;
    let rate_mb_per_min = (delta_bytes / (1024.0 * 1024.0)) / elapsed_mins;

    let trend = if rate_mb_per_min < -300.0 {
        BurnRateTrend::CriticalSurge
    } else if rate_mb_per_min < -50.0 {
        BurnRateTrend::FillingFast
    } else if rate_mb_per_min > 10.0 {
        BurnRateTrend::Reclaiming
    } else {
        BurnRateTrend::Stable
    };

    let est_minutes = if rate_mb_per_min < -1.0 && newest.free_bytes > 0 {
        let free_mb = (newest.free_bytes as f64) / (1024.0 * 1024.0);
        let mins = (free_mb / (-rate_mb_per_min)).round() as u64;
        Some(mins)
    } else {
        None
    };

    (rate_mb_per_min, trend, est_minutes)
}

pub struct IntelligentGuardManager {
    samples: RwLock<HashMap<String, Vec<DiskSample>>>,
    rules: RwLock<Vec<SelfHealingRule>>,
    events: RwLock<Vec<SelfHealingEvent>>,
}

impl Default for IntelligentGuardManager {
    fn default() -> Self {
        Self::new()
    }
}

impl IntelligentGuardManager {
    pub fn new() -> Self {
        let default_rules = vec![
            SelfHealingRule {
                id: "rule_recycle_bin".to_string(),
                name: "低容量自动清空回收站".to_string(),
                description: "当系统盘 (C:) 剩余空间低于 10GB 时，自动清空全盘回收站累积文件".to_string(),
                enabled: true,
                trigger_min_free_gb: 10,
                require_idle: false,
                require_dnd_inactive: true,
                action_type: "empty_recycle_bin".to_string(),
                cooldown_seconds: 14400, // 4 小时冷却
                last_triggered_secs: 0,
                total_times_triggered: 0,
                total_bytes_saved: 0,
            },
            SelfHealingRule {
                id: "rule_temp_garbage".to_string(),
                name: "空闲期自动收缩临时垃圾".to_string(),
                description: "当系统盘剩余低于 15GB 且用户处于空闲状态时，静默清理 AppData 临时日志与崩溃转储".to_string(),
                enabled: true,
                trigger_min_free_gb: 15,
                require_idle: true,
                require_dnd_inactive: true,
                action_type: "clean_temp_garbage".to_string(),
                cooldown_seconds: 14400,
                last_triggered_secs: 0,
                total_times_triggered: 0,
                total_bytes_saved: 0,
            },
            SelfHealingRule {
                id: "rule_cloud_evict".to_string(),
                name: "云同步盘超期缓存自动脱水".to_string(),
                description: "当系统盘剩余低于 12GB 且空闲时，自动将 OneDrive 超过 30 天未打开的文件转为仅联机占位".to_string(),
                enabled: true,
                trigger_min_free_gb: 12,
                require_idle: true,
                require_dnd_inactive: true,
                action_type: "evict_cloud_files".to_string(),
                cooldown_seconds: 28800, // 8 小时冷却
                last_triggered_secs: 0,
                total_times_triggered: 0,
                total_bytes_saved: 0,
            },
        ];

        Self {
            samples: RwLock::new(HashMap::new()),
            rules: RwLock::new(default_rules),
            events: RwLock::new(Vec::new()),
        }
    }

    pub fn record_sample(&self, drive: &str, free_bytes: u64) -> BurnRateForecast {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_secs())
            .unwrap_or(0);

        let drive_key = drive.to_uppercase();
        let mut map = self.samples.write().unwrap();
        let list = map.entry(drive_key.clone()).or_default();

        list.push(DiskSample {
            timestamp_secs: now,
            free_bytes,
        });

        // 保留最近 1 小时且最多 120 个样本
        if list.len() > 120 {
            list.remove(0);
        }
        if let Some(first) = list.first() {
            if now > first.timestamp_secs + 3600 && list.len() > 2 {
                list.retain(|s| s.timestamp_secs >= now - 3600);
            }
        }

        let (rate, trend, est_minutes) = calculate_burn_rate(list);

        let forecast_warning = match trend {
            BurnRateTrend::CriticalSurge => Some(format!(
                "突发预警：{} 盘正以每分钟 {:.1} MB 剧烈吞噬空间！",
                drive_key, -rate
            )),
            BurnRateTrend::FillingFast => Some(format!(
                "容量提示：{} 盘正以每分钟 {:.1} MB 快速缩减，预计约 {} 分钟耗尽",
                drive_key,
                -rate,
                est_minutes.unwrap_or(0)
            )),
            _ => None,
        };

        BurnRateForecast {
            drive_letter: drive_key,
            current_free_bytes: free_bytes,
            rate_mb_per_min: rate,
            trend,
            estimated_minutes_to_exhaustion: est_minutes,
            forecast_warning,
        }
    }

    pub fn get_status(&self, drive: &str) -> IntelligentGuardStatus {
        let (notif_state, is_dnd) = get_user_notification_state();
        let idle_secs = get_user_idle_seconds();
        let is_idle_for_bg = idle_secs >= 180; // 空闲超过 3 分钟即视为适合作业

        let notif_label = match notif_state {
            UserNotificationContext::AcceptsNotifications => "正常接收通知".to_string(),
            UserNotificationContext::BusyFullScreen => "全屏/游戏专注中 (自动免打扰)".to_string(),
            UserNotificationContext::PresentationMode => "演示放映模式 (自动免打扰)".to_string(),
            UserNotificationContext::QuietTime => "Windows 免打扰时段".to_string(),
            UserNotificationContext::NotPresent => "用户暂离".to_string(),
            UserNotificationContext::Other(_) => "系统守护中".to_string(),
        };

        // 获取当前驱动器最新空间
        let drives = crate::disks::get_disk_drives();
        let clean_target = drive.trim_end_matches('\\').to_uppercase();
        let free_bytes = drives
            .iter()
            .find(|d| d.letter.to_uppercase() == clean_target)
            .map(|d| d.free_bytes)
            .unwrap_or_else(|| {
                drives.first().map(|d| d.free_bytes).unwrap_or(0)
            });

        let forecast = self.record_sample(&clean_target, free_bytes);
        let rules_clone = self.rules.read().unwrap().clone();
        let events_clone = self.events.read().unwrap().clone();

        IntelligentGuardStatus {
            notification_state: notif_state,
            notification_state_label: notif_label,
            is_dnd_active: is_dnd,
            user_idle_seconds: idle_secs,
            is_idle_for_background_task: is_idle_for_bg,
            forecast,
            rules: rules_clone,
            recent_events: events_clone,
        }
    }

    pub fn toggle_rule(&self, rule_id: &str, enabled: bool) -> Result<(), String> {
        let mut rules = self.rules.write().unwrap();
        if let Some(r) = rules.iter_mut().find(|r| r.id == rule_id) {
            r.enabled = enabled;
            Ok(())
        } else {
            Err(format!("未找到规则 ID: {}", rule_id))
        }
    }

    pub fn evaluate_and_run_self_healing(&self, drive: &str) -> Vec<SelfHealingEvent> {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_secs())
            .unwrap_or(0);

        let (_, is_dnd) = get_user_notification_state();
        let idle_secs = get_user_idle_seconds();
        let is_idle = idle_secs >= 180;

        let drives = crate::disks::get_disk_drives();
        let clean_target = drive.trim_end_matches('\\').to_uppercase();
        let free_bytes = drives
            .iter()
            .find(|d| d.letter.to_uppercase() == clean_target)
            .map(|d| d.free_bytes)
            .unwrap_or(0);

        let free_gb = free_bytes / (1024 * 1024 * 1024);

        let mut executed_events = Vec::new();
        let mut rules = self.rules.write().unwrap();

        for rule in rules.iter_mut() {
            if !rule.enabled {
                continue;
            }

            // 冷却判定
            if now < rule.last_triggered_secs + rule.cooldown_seconds {
                continue;
            }

            // 容量触发阈值判定
            if free_gb >= rule.trigger_min_free_gb {
                continue;
            }

            // 场景避让判定
            if rule.require_dnd_inactive && is_dnd {
                continue;
            }
            if rule.require_idle && !is_idle {
                continue;
            }

            // 触发自愈动作
            let mut freed_bytes = 0;
            let mut message = String::new();

            match rule.action_type.as_str() {
                "empty_recycle_bin" => {
                    if let Ok(b) = crate::system_tools::empty_recycle_bin() {
                        freed_bytes = b;
                        message = format!("自愈成功：自动清空回收站腾退 {}", crate::system_storage_audit::format_size(b));
                    }
                }
                "clean_temp_garbage" => {
                    let temp_dir = std::env::var("LOCALAPPDATA").unwrap_or_default() + "\\Temp";
                    let empty_dirs = crate::system_tools::scan_empty_directories(&temp_dir);
                    let (cleaned, _) = crate::system_tools::clean_empty_directories(&empty_dirs);
                    message = format!("自愈成功：静默清除 {} 个空壳临时目录", cleaned);
                }
                "evict_cloud_files" => {
                    let audit = crate::cloud_storage_audit::run_cloud_storage_audit();
                    let paths: Vec<String> = audit.evictable_files.iter().map(|f| f.path.clone()).collect();
                    if !paths.is_empty() {
                        let (count, total_freed, _) = crate::cloud_storage_audit::batch_evict_cloud_files(&paths);
                        freed_bytes = total_freed;
                        message = format!("自愈成功：脱水释放 {} 个云盘长期未用文件，腾退 {}", count, crate::system_storage_audit::format_size(total_freed));
                    }
                }
                _ => {}
            }

            if !message.is_empty() {
                rule.last_triggered_secs = now;
                rule.total_times_triggered += 1;
                rule.total_bytes_saved += freed_bytes;

                let event = SelfHealingEvent {
                    timestamp_secs: now,
                    rule_id: rule.id.clone(),
                    rule_name: rule.name.clone(),
                    action_executed: rule.action_type.clone(),
                    bytes_freed: freed_bytes,
                    message,
                };
                executed_events.push(event);
            }
        }

        if !executed_events.is_empty() {
            let mut ev_list = self.events.write().unwrap();
            ev_list.extend(executed_events.clone());
            if ev_list.len() > 50 {
                let excess = ev_list.len() - 50;
                ev_list.drain(0..excess);
            }
        }

        executed_events
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_burn_rate_stable() {
        let samples = vec![
            DiskSample { timestamp_secs: 1000, free_bytes: 100 * 1024 * 1024 * 1024 },
            DiskSample { timestamp_secs: 1060, free_bytes: 100 * 1024 * 1024 * 1024 },
        ];
        let (rate, trend, est) = calculate_burn_rate(&samples);
        assert_eq!(rate, 0.0);
        assert_eq!(trend, BurnRateTrend::Stable);
        assert!(est.is_none());
    }

    #[test]
    fn test_calculate_burn_rate_fast_filling() {
        let samples = vec![
            DiskSample { timestamp_secs: 1000, free_bytes: 10 * 1024 * 1024 * 1024 },
            // 2 分钟后减少了 200MB (速率 100 MB/min)
            DiskSample { timestamp_secs: 1120, free_bytes: 10 * 1024 * 1024 * 1024 - 200 * 1024 * 1024 },
        ];
        let (rate, trend, est) = calculate_burn_rate(&samples);
        assert!(rate < -90.0);
        assert_eq!(trend, BurnRateTrend::FillingFast);
        assert!(est.is_some());
    }

    #[test]
    fn test_guard_manager_lifecycle() {
        let mgr = IntelligentGuardManager::new();
        let fc = mgr.record_sample("C:", 50 * 1024 * 1024 * 1024);
        assert_eq!(fc.drive_letter, "C:");

        let status = mgr.get_status("C:");
        assert_eq!(status.rules.len(), 3);

        let res = mgr.toggle_rule("rule_recycle_bin", false);
        assert!(res.is_ok());

        let status2 = mgr.get_status("C:");
        let r1 = status2.rules.iter().find(|r| r.id == "rule_recycle_bin").unwrap();
        assert!(!r1.enabled);
    }
}
