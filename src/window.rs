use std::path::{Path, PathBuf};
use std::process::Command;

pub fn find_edge_path() -> Option<PathBuf> {
    let candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ];

    for path_str in candidates {
        let p = Path::new(path_str);
        if p.exists() {
            return Some(p.to_path_buf());
        }
    }

    if let Ok(output) = Command::new("where").arg("msedge.exe").output() {
        if output.status.success() {
            let out_str = String::from_utf8_lossy(&output.stdout);
            if let Some(first_line) = out_str.lines().next() {
                let p = PathBuf::from(first_line.trim());
                if p.exists() {
                    return Some(p);
                }
            }
        }
    }

    None
}

pub fn launch_app_window(port: u16) {
    let url = format!("http://127.0.0.1:{}", port);
    let app_arg = format!("--app={}", url);

    if let Some(edge_bin) = find_edge_path() {
        let mut cmd = Command::new(edge_bin);
        cmd.arg(&app_arg)
            .arg("--window-size=1260,820");

        if let Ok(_) = cmd.spawn() {
            return;
        }
    }

    // Fallback: system browser
    let _ = Command::new("cmd")
        .args(["/c", "start", &url])
        .spawn();
}
