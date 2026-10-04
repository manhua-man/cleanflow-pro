use serde::{Deserialize, Serialize};
use std::process::Command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DockerItem {
    pub item_type: String,
    pub total_count: String,
    pub active_count: String,
    pub total_size: String,
    pub reclaimable: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DockerStatus {
    pub available: bool,
    pub running: bool,
    pub items: Vec<DockerItem>,
    pub total_reclaimable_str: String,
    pub error: Option<String>,
}

#[derive(Debug, Deserialize)]
struct DockerDfRaw {
    #[serde(rename = "Type")]
    item_type: Option<String>,
    #[serde(rename = "TotalCount")]
    total_count: Option<String>,
    #[serde(rename = "Active")]
    active: Option<String>,
    #[serde(rename = "Size")]
    size: Option<String>,
    #[serde(rename = "Reclaimable")]
    reclaimable: Option<String>,
}

pub fn get_docker_status() -> DockerStatus {
    let output = match Command::new("docker")
        .args(["system", "df", "--format", "{{json .}}"])
        .output()
    {
        Ok(out) => out,
        Err(e) => {
            return DockerStatus {
                available: false,
                running: false,
                items: Vec::new(),
                total_reclaimable_str: "0 B".to_string(),
                error: Some(format!("未检测到 Docker 或无法执行命令: {}", e)),
            };
        }
    };

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        return DockerStatus {
            available: true,
            running: false,
            items: Vec::new(),
            total_reclaimable_str: "0 B".to_string(),
            error: Some(format!("Docker 守护进程未启动: {}", stderr.trim())),
        };
    }

    let stdout = String::from_utf8_lossy(&output.stdout);
    let mut items = Vec::new();

    for line in stdout.lines() {
        let trimmed = line.trim();
        if trimmed.is_empty() {
            continue;
        }
        if let Ok(raw) = serde_json::from_str::<DockerDfRaw>(trimmed) {
            items.push(DockerItem {
                item_type: raw.item_type.unwrap_or_default(),
                total_count: raw.total_count.unwrap_or_default(),
                active_count: raw.active.unwrap_or_default(),
                total_size: raw.size.unwrap_or_default(),
                reclaimable: raw.reclaimable.unwrap_or_default(),
            });
        }
    }

    // Calculate human-friendly total
    let total_str = if items.is_empty() {
        "0 B".to_string()
    } else {
        // Collect reclaimable strings
        let rec_summary: Vec<String> = items
            .iter()
            .filter(|it| !it.reclaimable.starts_with("0B") && !it.reclaimable.is_empty())
            .map(|it| format!("{}: {}", it.item_type, it.reclaimable))
            .collect();
        if rec_summary.is_empty() {
            "0 B 可回收".to_string()
        } else {
            rec_summary.join(" | ")
        }
    };

    DockerStatus {
        available: true,
        running: true,
        items,
        total_reclaimable_str: total_str,
        error: None,
    }
}

pub fn prune_docker(target: &str) -> Result<String, String> {
    let args = match target {
        "builder" => vec!["builder", "prune", "-f"],
        "images" => vec!["image", "prune", "-f"],
        "volumes" => vec!["volume", "prune", "-f"],
        "all" => vec!["system", "prune", "-f"],
        _ => return Err(format!("不支持的清理目标: {}", target)),
    };

    let output = Command::new("docker")
        .args(&args)
        .output()
        .map_err(|e| format!("执行 docker prune 失败: {}", e))?;

    if output.status.success() {
        let stdout = String::from_utf8_lossy(&output.stdout).to_string();
        Ok(stdout)
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        Err(format!("Docker 清理返回错误: {}", stderr.trim()))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_docker_status_call() {
        let status = get_docker_status();
        // Just verify it returns a valid DockerStatus without crashing
        if status.available && status.running {
            assert!(!status.items.is_empty());
        }
    }
}
