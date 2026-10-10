// #![cfg_attr(not(test), windows_subsystem = "windows")]

use cleanflow::rules::RuleConfig;
use cleanflow::scanner::scan_all;
use cleanflow::server::start_server;
use cleanflow::window::launch_app_window;
use std::env;
use std::net::TcpStream;
use std::path::Path;
use std::sync::atomic::Ordering;

#[cfg(windows)]
extern "system" {
    fn AttachConsole(dw_process_id: u32) -> i32;
}

fn format_bytes(bytes: u64) -> String {
    if bytes >= 1024 * 1024 * 1024 {
        format!("{:.2} GB", bytes as f64 / (1024.0 * 1024.0 * 1024.0))
    } else if bytes >= 1024 * 1024 {
        format!("{:.1} MB", bytes as f64 / (1024.0 * 1024.0))
    } else if bytes >= 1024 {
        format!("{:.1} KB", bytes as f64 / 1024.0)
    } else {
        format!("{} B", bytes)
    }
}

fn run_cli_scan(config: &RuleConfig, json_output: bool) -> anyhow::Result<()> {
    if json_output {
        let report = scan_all(config);
        println!("{}", serde_json::to_string_pretty(&report)?);
        return Ok(());
    }

    println!("============================================================");
    println!("     CleanFlow (净流) - 高性能 Windows 磁盘空间治理引擎     ");
    println!("             [Rust 核心原生引擎 v{}]                     ", env!("CARGO_PKG_VERSION"));
    println!("============================================================\n");

    println!("正在极速多线程扫描全盘规则资产...\n");
    let start_time = std::time::Instant::now();
    let report = scan_all(config);
    let duration = start_time.elapsed();

    for cat in &report.categories {
        println!("------------------------------------------------------------");
        println!(
            "[{}] {} - 可释放: {} ({} 个文件/目录)",
            cat.risk_level.to_uppercase(),
            cat.name,
            format_bytes(cat.total_size_bytes),
            cat.total_files
        );
        println!("说明: {}", cat.description);
        println!("------------------------------------------------------------");

        for rule in &cat.rules {
            if rule.total_size_bytes > 0 || !rule.matched_paths.is_empty() {
                println!(
                    "  * {:<36} -> {:>9} ({} 处匹配)",
                    rule.name,
                    format_bytes(rule.total_size_bytes),
                    rule.matched_paths.len()
                );
                for p in &rule.matched_paths {
                    println!("      - {} ({})", p.path, format_bytes(p.size_bytes));
                }
            }
        }
        println!();
    }

    println!("============================================================");
    println!(
        "扫描完成! 耗时: {:.2}s | 发现可治理总空间: {}",
        duration.as_secs_f64(),
        format_bytes(report.total_size_bytes)
    );
    println!("============================================================");
    Ok(())
}

fn main() -> anyhow::Result<()> {
    let args: Vec<String> = env::args().collect();

    // CLI mode: version check
    if args.iter().any(|a| a == "--version" || a == "-v" || a == "-V") {
        #[cfg(windows)]
        unsafe {
            AttachConsole(0xFFFFFFFF);
        }
        println!("CleanFlow Pro v{}", env!("CARGO_PKG_VERSION"));
        return Ok(());
    }

    // CLI mode checks
    if args.iter().any(|a| a == "--json" || a == "--cli" || a == "--scan") {
        #[cfg(windows)]
        unsafe {
            // Attach to calling terminal if executed from CLI
            AttachConsole(0xFFFFFFFF);
        }

        let config = load_config()?;
        let json_mode = args.iter().any(|a| a == "--json");
        return run_cli_scan(&config, json_mode);
    }

    let default_port = 23999;
    let is_headless = args.iter().any(|a| a == "--headless" || a == "--server-only" || a == "--daemon");
    let mut target_port = default_port;
    if let Some(pos) = args.iter().position(|a| a == "--port") {
        if let Some(p_str) = args.get(pos + 1) {
            if let Ok(p) = p_str.parse::<u16>() {
                target_port = p;
            }
        }
    }

    // Single Instance Guard:
    // If target port is already listening, another instance is already active!
    // If not headless, simply launch the window to connect to the active instance and exit.
    if TcpStream::connect(format!("127.0.0.1:{}", target_port)).is_ok() {
        if !is_headless {
            launch_app_window(target_port);
        }
        return Ok(());
    }

    // Start background server
    let (port, running) = start_server(target_port);

    // Start Auto-Cleaner Daemon and Global Hotkey services
    let daemon = cleanflow::daemon_service::DaemonService::new();
    daemon.start();

    // Start Windows System Tray Service (Listary 8.2 parity)
    let tray = cleanflow::tray::TrayService::new(port);
    tray.start();

    let hotkey = cleanflow::hotkey_manager::HotkeyService::new();
    hotkey.start(
        || {
            // Alt + Space: Spotlight bring-to-front
            #[cfg(windows)]
            unsafe {
                extern "system" {
                    fn FindWindowW(lpClassName: *const u16, lpWindowName: *const u16) -> isize;
                    fn SetForegroundWindow(hWnd: isize) -> i32;
                    fn ShowWindow(hWnd: isize, nCmdShow: i32) -> i32;
                }
                let title: Vec<u16> = "CleanFlow Pro".encode_utf16().chain(std::iter::once(0)).collect();
                let hwnd = FindWindowW(std::ptr::null(), title.as_ptr());
                if hwnd != 0 {
                    ShowWindow(hwnd, 9); // SW_RESTORE
                    SetForegroundWindow(hwnd);
                }
            }
        },
        || {
            // Ctrl + G: Quick Switch
            if let Ok(user_profile) = std::env::var("USERPROFILE") {
                let _ = cleanflow::quick_switch::execute_quick_switch(&user_profile);
            }
        },
    );

    // Launch GUI App Window if not headless
    if !is_headless {
        launch_app_window(port);
    }

    // Keep server thread alive
    while running.load(Ordering::SeqCst) {
        std::thread::sleep(std::time::Duration::from_millis(500));
    }

    Ok(())
}

fn load_config() -> anyhow::Result<RuleConfig> {
    let rules_path = if Path::new("rules.json").exists() {
        "rules.json"
    } else if Path::new("../rules.json").exists() {
        "../rules.json"
    } else {
        "rules.json"
    };

    match RuleConfig::load_from_file(rules_path) {
        Ok(c) => Ok(c),
        Err(_) => {
            let embedded = include_str!("../rules.json");
            RuleConfig::load_from_str(embedded)
        }
    }
}
