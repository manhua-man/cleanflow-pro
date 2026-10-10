use serde::{Deserialize, Serialize};
use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::{Arc, RwLock};
use std::time::{SystemTime, UNIX_EPOCH};

const PRO_TRIAL_DURATION_SECS: u64 = 7 * 86400; // 7 days

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum LicenseTier {
    Community,
    ProTrial { started_at: u64, expires_at: u64 },
    ProLifetime { licensee: String, license_key: String },
    Enterprise { organization: String, seats: u32, license_key: String },
}

impl Default for LicenseTier {
    fn default() -> Self {
        LicenseTier::Community
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LicenseRecord {
    pub tier: LicenseTier,
    pub activated_at: Option<u64>,
    pub device_fingerprint: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LicenseStatus {
    pub tier: String,
    pub tier_display_name: String,
    pub is_pro: bool,
    pub trial_days_left: Option<u32>,
    pub licensee: Option<String>,
    pub device_fingerprint: String,
    pub activation_message: String,
}

pub struct LicenseManager {
    record: Arc<RwLock<LicenseRecord>>,
    storage_path: PathBuf,
}

impl LicenseManager {
    pub fn new() -> Self {
        Self::with_storage_path(Self::resolve_storage_path())
    }

    pub fn with_storage_path(storage_path: PathBuf) -> Self {
        let fingerprint = Self::generate_device_fingerprint();

        let initial_record = if storage_path.exists() {
            match fs::read_to_string(&storage_path) {
                Ok(content) => match serde_json::from_str::<LicenseRecord>(&content) {
                    Ok(mut rec) => {
                        rec.device_fingerprint = fingerprint.clone();
                        rec
                    }
                    Err(_) => LicenseRecord {
                        tier: LicenseTier::Community,
                        activated_at: None,
                        device_fingerprint: fingerprint.clone(),
                    },
                },
                Err(_) => LicenseRecord {
                    tier: LicenseTier::Community,
                    activated_at: None,
                    device_fingerprint: fingerprint.clone(),
                },
            }
        } else {
            LicenseRecord {
                tier: LicenseTier::Community,
                activated_at: None,
                device_fingerprint: fingerprint.clone(),
            }
        };

        Self {
            record: Arc::new(RwLock::new(initial_record)),
            storage_path,
        }
    }

    fn resolve_storage_path() -> PathBuf {
        if let Ok(appdata) = env::var("APPDATA") {
            let cleanflow_dir = Path::new(&appdata).join("CleanFlow");
            let _ = fs::create_dir_all(&cleanflow_dir);
            cleanflow_dir.join("license.json")
        } else {
            PathBuf::from("cleanflow_license.json")
        }
    }

    pub fn generate_device_fingerprint() -> String {
        let comp_name = env::var("COMPUTERNAME").unwrap_or_else(|_| "UNKNOWN_HOST".to_string());
        let user_name = env::var("USERNAME").unwrap_or_else(|_| "DEFAULT_USER".to_string());
        let arch = env::var("PROCESSOR_ARCHITECTURE").unwrap_or_else(|_| "X64".to_string());

        let raw = format!("{}:{}:{}", comp_name, user_name, arch);
        let hash = blake3::hash(raw.as_bytes());
        let hex_str = hash.to_hex();
        let s = hex_str.as_str();

        // Format as XXXX-XXXX-XXXX-XXXX
        format!(
            "{}-{}-{}-{}",
            &s[0..4].to_uppercase(),
            &s[4..8].to_uppercase(),
            &s[8..12].to_uppercase(),
            &s[12..16].to_uppercase()
        )
    }

    pub fn get_status(&self) -> LicenseStatus {
        let rec = self.record.read().unwrap();
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();

        match &rec.tier {
            LicenseTier::Community => LicenseStatus {
                tier: "community".to_string(),
                tier_display_name: "社区免费版".to_string(),
                is_pro: false,
                trial_days_left: None,
                licensee: None,
                device_fingerprint: rec.device_fingerprint.clone(),
                activation_message: "您正在使用 CleanFlow 社区免费版，核心秒搜与清理永久免费".to_string(),
            },
            LicenseTier::ProTrial { expires_at, .. } => {
                if now < *expires_at {
                    let secs_left = expires_at - now;
                    let days_left = ((secs_left + 86399) / 86400) as u32;
                    LicenseStatus {
                        tier: "pro_trial".to_string(),
                        tier_display_name: format!("PRO 体验版 (剩余 {} 天)", days_left),
                        is_pro: true,
                        trial_days_left: Some(days_left),
                        licensee: Some("PRO 试用用户".to_string()),
                        device_fingerprint: rec.device_fingerprint.clone(),
                        activation_message: format!("PRO 特权体验中，剩余 {} 天", days_left),
                    }
                } else {
                    LicenseStatus {
                        tier: "community".to_string(),
                        tier_display_name: "社区免费版 (体验已结束)".to_string(),
                        is_pro: false,
                        trial_days_left: Some(0),
                        licensee: None,
                        device_fingerprint: rec.device_fingerprint.clone(),
                        activation_message: "您的 7 天 PRO 体验已结束，已无缝转回社区版，可随时输入授权码激活终身版".to_string(),
                    }
                }
            }
            LicenseTier::ProLifetime { licensee, .. } => LicenseStatus {
                tier: "pro_lifetime".to_string(),
                tier_display_name: "PRO 终身专业版".to_string(),
                is_pro: true,
                trial_days_left: None,
                licensee: Some(licensee.clone()),
                device_fingerprint: rec.device_fingerprint.clone(),
                activation_message: format!("已成功授权给: {}，享有全部终身 Pro 特权", licensee),
            },
            LicenseTier::Enterprise { organization, seats, .. } => LicenseStatus {
                tier: "enterprise".to_string(),
                tier_display_name: format!("企业授权版 ({} 席位)", seats),
                is_pro: true,
                trial_days_left: None,
                licensee: Some(organization.clone()),
                device_fingerprint: rec.device_fingerprint.clone(),
                activation_message: format!("企业级批量授权: {} (共 {} 席位)", organization, seats),
            },
        }
    }

    pub fn start_pro_trial(&self) -> Result<LicenseStatus, String> {
        let mut rec = self.record.write().unwrap();
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();

        match &rec.tier {
            LicenseTier::ProLifetime { .. } | LicenseTier::Enterprise { .. } => {
                return Err("当前已经是永久授权或企业版，无需开启体验".to_string());
            }
            LicenseTier::ProTrial { expires_at, .. } => {
                if now < *expires_at {
                    return Err("PRO 体验期仍在生效中".to_string());
                }
            }
            LicenseTier::Community => {}
        }

        rec.tier = LicenseTier::ProTrial {
            started_at: now,
            expires_at: now + PRO_TRIAL_DURATION_SECS,
        };
        rec.activated_at = Some(now);

        let _ = self.save_record(&rec);
        drop(rec);

        Ok(self.get_status())
    }

    pub fn activate_license(&self, licensee: &str, key: &str) -> Result<LicenseStatus, String> {
        let trimmed_key = key.trim().to_uppercase();
        let trimmed_licensee = licensee.trim();

        if trimmed_key.is_empty() {
            return Err("激活码不能为空".to_string());
        }

        let is_valid = Self::verify_key(trimmed_licensee, &trimmed_key);
        if !is_valid {
            return Err("激活码无效，请检查输入或联系授权中心获取正式密钥".to_string());
        }

        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();

        let mut rec = self.record.write().unwrap();
        if trimmed_key.contains("ENT") || trimmed_key.contains("CORP") {
            rec.tier = LicenseTier::Enterprise {
                organization: if trimmed_licensee.is_empty() { "企业团队".to_string() } else { trimmed_licensee.to_string() },
                seats: 50,
                license_key: trimmed_key,
            };
        } else {
            rec.tier = LicenseTier::ProLifetime {
                licensee: if trimmed_licensee.is_empty() { "尊贵 Pro 用户".to_string() } else { trimmed_licensee.to_string() },
                license_key: trimmed_key,
            };
        }
        rec.activated_at = Some(now);

        let _ = self.save_record(&rec);
        drop(rec);

        Ok(self.get_status())
    }

    fn verify_key(licensee: &str, key: &str) -> bool {
        // Built-in universal dev/sponsor keys
        if key == "CFPRO-LIFETIME-2026-DEVMASTER-KEY"
            || key == "CLEANFLOW-PRO-COMMUNITY-SPONSOR"
            || key == "CFENT-CORP-UNLIMITED-2026-VIP"
        {
            return true;
        }

        // Standard algorithm-backed verification:
        // Key format: CFPRO-XXXX-XXXX-XXXX-XXXX
        let parts: Vec<&str> = key.split('-').collect();
        if parts.len() == 5 && parts[0] == "CFPRO" {
            let fp = Self::generate_device_fingerprint();
            let check_data = format!("CLEANFLOW_PRO_SIGN:{}:{}:{}", fp, licensee, parts[1]);
            let hash = blake3::hash(check_data.as_bytes()).to_hex();
            let expected_segment = &hash.as_str()[0..4].to_uppercase();
            return parts[4] == expected_segment;
        }

        false
    }

    fn save_record(&self, record: &LicenseRecord) -> Result<(), std::io::Error> {
        let json = serde_json::to_string_pretty(record)
            .map_err(|e| std::io::Error::new(std::io::ErrorKind::Other, e.to_string()))?;
        fs::write(&self.storage_path, json)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn create_test_manager(name: &str) -> LicenseManager {
        let mut p = std::env::temp_dir();
        p.push(format!("cleanflow_test_lic_{}_{}.json", name, std::process::id()));
        let _ = fs::remove_file(&p);
        LicenseManager::with_storage_path(p)
    }

    #[test]
    fn test_device_fingerprint_generation() {
        let fp = LicenseManager::generate_device_fingerprint();
        assert_eq!(fp.len(), 19);
        assert_eq!(fp.matches('-').count(), 3);
    }

    #[test]
    fn test_default_community_tier() {
        let lm = create_test_manager("default_tier");
        let status = lm.get_status();
        assert_eq!(status.tier, "community");
        assert!(!status.is_pro);
    }

    #[test]
    fn test_pro_trial_activation() {
        let lm = create_test_manager("trial_activation");
        let status = lm.start_pro_trial().unwrap();
        assert_eq!(status.tier, "pro_trial");
        assert!(status.is_pro);
        assert_eq!(status.trial_days_left, Some(7));
    }

    #[test]
    fn test_license_key_activation_valid_and_invalid() {
        let lm = create_test_manager("key_activation");

        // Invalid key
        let err = lm.activate_license("Tester", "INVALID-KEY-12345");
        assert!(err.is_err());

        // Valid dev key
        let ok = lm.activate_license("Senior Engineer", "CFPRO-LIFETIME-2026-DEVMASTER-KEY");
        assert!(ok.is_ok());
        let status = ok.unwrap();
        assert_eq!(status.tier, "pro_lifetime");
        assert!(status.is_pro);
        assert_eq!(status.licensee, Some("Senior Engineer".to_string()));
    }
}
