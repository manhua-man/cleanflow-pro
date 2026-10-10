use serde::{Deserialize, Serialize};
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::{OnceLock, RwLock};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ExclusionRule {
    pub id: String,
    pub pattern: String,
    pub rule_type: String, // "path", "wildcard", "regex"
    pub description: String,
    pub is_enabled: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BuiltinExclusion {
    pub pattern: String,
    pub category: String,
    pub description: String,
}

pub struct ExclusionManager {
    store_path: PathBuf,
    rules: Vec<ExclusionRule>,
}

impl ExclusionManager {
    pub fn new(store_path: PathBuf) -> Self {
        let mut mgr = Self {
            store_path,
            rules: Vec::new(),
        };
        mgr.load();
        mgr
    }

    pub fn load(&mut self) {
        if self.store_path.exists() {
            if let Ok(content) = fs::read_to_string(&self.store_path) {
                if let Ok(rules) = serde_json::from_str::<Vec<ExclusionRule>>(&content) {
                    self.rules = rules;
                    return;
                }
            }
        }
        self.rules = Vec::new();
    }

    pub fn save(&self) -> Result<(), String> {
        let json = serde_json::to_string_pretty(&self.rules)
            .map_err(|e| format!("序列化排除规则失败: {}", e))?;
        fs::write(&self.store_path, json)
            .map_err(|e| format!("写入排除规则文件失败: {}", e))?;
        Ok(())
    }

    pub fn list_rules(&self) -> Vec<ExclusionRule> {
        self.rules.clone()
    }

    pub fn list_builtin_exclusions() -> Vec<BuiltinExclusion> {
        vec![
            BuiltinExclusion {
                pattern: "$Recycle.Bin".to_string(),
                category: "系统保护".to_string(),
                description: "Windows 回收站底层目录，防误删与冗余展示".to_string(),
            },
            BuiltinExclusion {
                pattern: "System Volume Information".to_string(),
                category: "系统保护".to_string(),
                description: "NTFS 系统卷还原点与底层元数据，无权限访问".to_string(),
            },
            BuiltinExclusion {
                pattern: "pagefile.sys / hiberfil.sys".to_string(),
                category: "系统保护".to_string(),
                description: "系统虚拟内存与休眠文件锁定占位符".to_string(),
            },
            BuiltinExclusion {
                pattern: "node_modules".to_string(),
                category: "开发降噪".to_string(),
                description: "数万级深层依赖包文件，降噪盾牌默认屏蔽".to_string(),
            },
            BuiltinExclusion {
                pattern: ".git / .svn".to_string(),
                category: "开发降噪".to_string(),
                description: "版本控制底层对象数据库".to_string(),
            },
            BuiltinExclusion {
                pattern: "target / build / dist".to_string(),
                category: "开发降噪".to_string(),
                description: "Rust / CMake / 前端编译构建输出临时目录".to_string(),
            },
            BuiltinExclusion {
                pattern: "venv / .venv / __pycache__".to_string(),
                category: "开发降噪".to_string(),
                description: "Python 虚拟环境与字节码编译缓存".to_string(),
            },
        ]
    }

    pub fn add_rule(&mut self, rule: ExclusionRule) -> Result<(), String> {
        if rule.pattern.trim().is_empty() {
            return Err("排除模式不能为空".to_string());
        }
        if let Some(pos) = self.rules.iter().position(|r| r.id == rule.id) {
            self.rules[pos] = rule;
        } else {
            self.rules.push(rule);
        }
        self.save()
    }

    pub fn remove_rule(&mut self, id: &str) -> bool {
        let initial_len = self.rules.len();
        self.rules.retain(|r| r.id != id);
        if self.rules.len() != initial_len {
            let _ = self.save();
            true
        } else {
            false
        }
    }

    pub fn toggle_rule(&mut self, id: &str) -> Option<bool> {
        for r in &mut self.rules {
            if r.id == id {
                r.is_enabled = !r.is_enabled;
                let state = r.is_enabled;
                let _ = self.save();
                return Some(state);
            }
        }
        None
    }

    pub fn matches_path(&self, path: &str) -> bool {
        let norm_path = path.replace('/', "\\").to_lowercase();

        for r in &self.rules {
            if !r.is_enabled {
                continue;
            }

            let pattern_lower = r.pattern.trim().replace('/', "\\").to_lowercase();
            if pattern_lower.is_empty() {
                continue;
            }

            match r.rule_type.as_str() {
                "wildcard" => {
                    if matches_wildcard(&norm_path, &pattern_lower) {
                        return true;
                    }
                }
                "regex" => {
                    if let Ok(re) = regex::RegexBuilder::new(&r.pattern).case_insensitive(true).build() {
                        if re.is_match(path) {
                            return true;
                        }
                    }
                }
                _ => {
                    // "path" or prefix rule
                    if norm_path.starts_with(&pattern_lower) 
                        || norm_path.contains(&format!("\\{}\\", pattern_lower.trim_matches('\\')))
                        || norm_path.ends_with(&pattern_lower)
                    {
                        return true;
                    }
                }
            }
        }

        false
    }
}

fn matches_wildcard(text: &str, pattern: &str) -> bool {
    // Fast path for extension wildcard like *.log or *.tmp
    if pattern.starts_with("*.") && !pattern[2..].contains('*') && !pattern[2..].contains('?') {
        let ext = &pattern[1..]; // .log
        return text.ends_with(ext);
    }

    // General wildcard conversion to regex
    let mut regex_str = String::with_capacity(pattern.len() * 2 + 2);
    regex_str.push('^');
    for ch in pattern.chars() {
        match ch {
            '*' => regex_str.push_str(".*"),
            '?' => regex_str.push('.'),
            '.' | '+' | '(' | ')' | '[' | ']' | '{' | '}' | '^' | '$' | '|' | '\\' => {
                regex_str.push('\\');
                regex_str.push(ch);
            }
            _ => regex_str.push(ch),
        }
    }
    regex_str.push('$');

    if let Ok(re) = regex::Regex::new(&regex_str) {
        // Test against full path or file name
        if re.is_match(text) {
            return true;
        }
        if let Some(name) = Path::new(text).file_name().and_then(|n| n.to_str()) {
            if re.is_match(name) {
                return true;
            }
        }
    }

    false
}

static GLOBAL_EXCLUSION_MANAGER: OnceLock<RwLock<ExclusionManager>> = OnceLock::new();

pub fn get_global_exclusion_manager() -> &'static RwLock<ExclusionManager> {
    GLOBAL_EXCLUSION_MANAGER.get_or_init(|| {
        let path = PathBuf::from("cleanflow_exclusions.json");
        RwLock::new(ExclusionManager::new(path))
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_exclusion_manager_lifecycle() {
        let temp_dir = std::env::temp_dir().join(format!("cleanflow_excl_test_{}", std::process::id()));
        let _ = fs::create_dir_all(&temp_dir);
        let store_file = temp_dir.join("exclusions.json");

        let mut mgr = ExclusionManager::new(store_file);

        let rule1 = ExclusionRule {
            id: "ex1".to_string(),
            pattern: "D:\\SecretData".to_string(),
            rule_type: "path".to_string(),
            description: "私密文档目录".to_string(),
            is_enabled: true,
        };
        mgr.add_rule(rule1).unwrap();

        let rule2 = ExclusionRule {
            id: "ex2".to_string(),
            pattern: "*.bak".to_string(),
            rule_type: "wildcard".to_string(),
            description: "备份文件".to_string(),
            is_enabled: true,
        };
        mgr.add_rule(rule2).unwrap();

        assert!(mgr.matches_path("D:\\SecretData\\contract.pdf"));
        assert!(mgr.matches_path("C:\\Projects\\code.bak"));
        assert!(!mgr.matches_path("C:\\Projects\\code.rs"));

        // Toggle rule2 to disabled
        let new_state = mgr.toggle_rule("ex2").unwrap();
        assert!(!new_state);
        assert!(!mgr.matches_path("C:\\Projects\\code.bak"));

        // Remove rule1
        assert!(mgr.remove_rule("ex1"));
        assert!(!mgr.matches_path("D:\\SecretData\\contract.pdf"));

        let _ = fs::remove_dir_all(&temp_dir);
    }

    #[test]
    fn test_builtin_exclusions_list() {
        let builtins = ExclusionManager::list_builtin_exclusions();
        assert!(!builtins.is_empty());
        assert!(builtins.iter().any(|b| b.pattern.contains("node_modules")));
        assert!(builtins.iter().any(|b| b.pattern.contains("$Recycle.Bin")));
    }
}
