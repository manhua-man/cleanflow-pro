use std::path::Path;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use tiny_http::{Header, Method, Response, Server, StatusCode};

use crate::cleaner::{clear_directory_contents, delete_single_file};
use crate::disks::get_disk_drives;
use crate::giant_files::scan_giant_files;
use crate::migrator::{
    get_migration_status, is_junction, list_active_junctions, migrate_to_drive,
    reveal_in_explorer, rollback_junction, start_migration_task,
};
use crate::process_lock::{check_common_locking_processes, kill_process_by_name};
use crate::rules::RuleConfig;
use crate::scanner::scan_all;
use crate::vacuum::vacuum_sqlite_database;

const HTML_CONTENT: &str = include_str!("ui.html");

#[derive(serde::Deserialize)]
struct CleanRequest {
    paths: Vec<String>,
}

#[derive(serde::Deserialize)]
struct MigrateRequest {
    source_path: String,
    target_drive: String,
}

#[derive(serde::Deserialize)]
struct VacuumRequest {
    db_path: String,
}

#[derive(serde::Deserialize)]
struct RollbackRequest {
    source_path: String,
}

#[derive(serde::Deserialize)]
struct RevealRequest {
    path: String,
}

#[derive(serde::Deserialize)]
struct CheckPathRequest {
    path: String,
}

#[derive(serde::Deserialize)]
struct KillProcessRequest {
    name: String,
}

#[derive(serde::Deserialize)]
struct DeleteFileRequest {
    path: String,
}

pub fn start_server(preferred_port: u16) -> (u16, Arc<AtomicBool>) {
    let running = Arc::new(AtomicBool::new(true));
    let running_clone = running.clone();

    // Try preferred port or bind to 0
    let server = match Server::http(format!("127.0.0.1:{}", preferred_port)) {
        Ok(s) => s,
        Err(_) => Server::http("127.0.0.1:0").expect("无法绑定本地端口"),
    };

    let actual_port = server.server_addr().to_ip().map(|a| a.port()).unwrap_or(preferred_port);

    std::thread::spawn(move || {
        while running_clone.load(Ordering::SeqCst) {
            let mut request = match server.recv() {
                Ok(rq) => rq,
                Err(_) => break,
            };

            let method = request.method().clone();
            let url = request.url().to_string();

            // Handle CORS OPTIONS
            if method == Method::Options {
                let mut response = Response::empty(StatusCode(200));
                response.add_header(Header::from_bytes(&b"Access-Control-Allow-Origin"[..], &b"*"[..]).unwrap());
                response.add_header(Header::from_bytes(&b"Access-Control-Allow-Methods"[..], &b"GET, POST, OPTIONS"[..]).unwrap());
                response.add_header(Header::from_bytes(&b"Access-Control-Allow-Headers"[..], &b"Content-Type"[..]).unwrap());
                let _ = request.respond(response);
                continue;
            }

            // Route handling
            if url == "/" || url == "/index.html" {
                let header = Header::from_bytes(&b"Content-Type"[..], &b"text/html; charset=utf-8"[..]).unwrap();
                let response = Response::from_string(HTML_CONTENT).with_header(header);
                let _ = request.respond(response);
            } else if url == "/api/disks" && method == Method::Get {
                let drives = get_disk_drives();
                let json = serde_json::to_string(&drives).unwrap_or_else(|_| "[]".to_string());
                send_json_response(request, json);
            } else if url == "/api/scan" && method == Method::Get {
                let config_res = load_rules();
                match config_res {
                    Ok(cfg) => {
                        let report = scan_all(&cfg);
                        let json = serde_json::to_string(&report).unwrap_or_else(|_| "{}".to_string());
                        send_json_response(request, json);
                    }
                    Err(e) => {
                        let err_json = format!(r#"{{"error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/junctions" && method == Method::Get {
                let records = list_active_junctions();
                let json = serde_json::to_string(&records).unwrap_or_else(|_| "[]".to_string());
                send_json_response(request, json);
            } else if url == "/api/junctions/rollback" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<RollbackRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => match rollback_junction(&req.source_path) {
                        Ok(bytes_restored) => {
                            let res_json = serde_json::json!({
                                "success": true,
                                "bytes_restored": bytes_restored,
                                "source_path": req.source_path
                            })
                            .to_string();
                            send_json_response(request, res_json);
                        }
                        Err(e) => {
                            let err_json = serde_json::json!({
                                "success": false,
                                "error": e.to_string()
                            })
                            .to_string();
                            send_json_response(request, err_json);
                        }
                    },
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/giant-files" && method == Method::Get {
                // Minimum size: 100 MB
                let min_size = 100 * 1024 * 1024;
                let files = scan_giant_files(min_size, 100);
                let json = serde_json::to_string(&files).unwrap_or_else(|_| "[]".to_string());
                send_json_response(request, json);
            } else if url == "/api/reveal" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<RevealRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => {
                        let _ = reveal_in_explorer(&req.path);
                        send_json_response(request, r#"{"success": true}"#.to_string());
                    }
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/check-path" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<CheckPathRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => {
                        let p = Path::new(&req.path);
                        if !p.exists() {
                            let res_json = serde_json::json!({
                                "exists": false,
                                "error": "指定路径不存在"
                            })
                            .to_string();
                            send_json_response(request, res_json);
                            continue;
                        }

                        let is_dir = p.is_dir();
                        let is_junc = is_junction(p);
                        let (size, files) = crate::scanner::calculate_path_stats(p);
                        let locks = check_common_locking_processes(&req.path);

                        let res_json = serde_json::json!({
                            "exists": true,
                            "path": req.path,
                            "is_dir": is_dir,
                            "is_junction": is_junc,
                            "size_bytes": size,
                            "file_count": files,
                            "locking_processes": locks,
                        })
                        .to_string();
                        send_json_response(request, res_json);
                    }
                    Err(e) => {
                        let err_json = format!(r#"{{"exists": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/kill-process" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<KillProcessRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => match kill_process_by_name(&req.name) {
                        Ok(_) => {
                            send_json_response(request, r#"{"success": true}"#.to_string());
                        }
                        Err(e) => {
                            let err_json = serde_json::json!({
                                "success": false,
                                "error": e.to_string()
                            })
                            .to_string();
                            send_json_response(request, err_json);
                        }
                    },
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/delete-file" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<DeleteFileRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => {
                        let p = Path::new(&req.path);
                        let res = delete_single_file(p);
                        let res_json = serde_json::json!({
                            "success": res.errors.is_empty(),
                            "bytes_freed": res.bytes_freed,
                            "errors": res.errors,
                        })
                        .to_string();
                        send_json_response(request, res_json);
                    }
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/clean" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<CleanRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => {
                        let mut total_freed = 0u64;
                        let mut total_files = 0u64;
                        let mut all_errors = Vec::new();

                        for path_str in req.paths {
                            let p = Path::new(&path_str);
                            if !p.exists() {
                                continue;
                            }
                            if p.is_file() {
                                let res = delete_single_file(p);
                                total_freed += res.bytes_freed;
                                total_files += res.files_deleted;
                                all_errors.extend(res.errors);
                            } else if p.is_dir() {
                                let res = clear_directory_contents(p);
                                total_freed += res.bytes_freed;
                                total_files += res.files_deleted;
                                all_errors.extend(res.errors);
                            }
                        }

                        let res_json = serde_json::json!({
                            "success": true,
                            "bytes_freed": total_freed,
                            "files_deleted": total_files,
                            "errors": all_errors,
                        })
                        .to_string();
                        send_json_response(request, res_json);
                    }
                    Err(e) => {
                        let err_json = format!(r#"{{"error": "解析请求失败: {}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/migrate" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<MigrateRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => match migrate_to_drive(&req.source_path, &req.target_drive) {
                        Ok(outcome) => {
                            let res_json = serde_json::json!({
                                "success": true,
                                "source_path": outcome.source_path.to_string_lossy(),
                                "target_path": outcome.target_path.to_string_lossy(),
                                "bytes_moved": outcome.bytes_moved,
                            })
                            .to_string();
                            send_json_response(request, res_json);
                        }
                        Err(e) => {
                            let err_json = serde_json::json!({
                                "success": false,
                                "error": e.to_string()
                            })
                            .to_string();
                            send_json_response(request, err_json);
                        }
                    },
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/migrate-start" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<MigrateRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => match start_migration_task(req.source_path, req.target_drive) {
                        Ok(job_id) => {
                            let res_json = serde_json::json!({
                                "success": true,
                                "job_id": job_id
                            })
                            .to_string();
                            send_json_response(request, res_json);
                        }
                        Err(e) => {
                            let err_json = serde_json::json!({
                                "success": false,
                                "error": e.to_string()
                            })
                            .to_string();
                            send_json_response(request, err_json);
                        }
                    },
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/migrate-status" && method == Method::Get {
                let status = get_migration_status();
                let json = serde_json::to_string(&status).unwrap_or_else(|_| "{}".to_string());
                send_json_response(request, json);
            } else if url == "/api/vacuum" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<VacuumRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => match vacuum_sqlite_database(&req.db_path) {
                        Ok(vac) => {
                            let res_json = serde_json::json!({
                                "success": true,
                                "path": vac.path,
                                "original_size": vac.original_size,
                                "new_size": vac.new_size,
                                "bytes_freed": vac.bytes_freed,
                            })
                            .to_string();
                            send_json_response(request, res_json);
                        }
                        Err(e) => {
                            let err_json = serde_json::json!({
                                "success": false,
                                "error": e.to_string()
                            })
                            .to_string();
                            send_json_response(request, err_json);
                        }
                    },
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/shutdown" && method == Method::Post {
                running_clone.store(false, Ordering::SeqCst);
                let res_json = r#"{"success": true, "message": "已关闭"}"#;
                send_json_response(request, res_json.to_string());
                std::thread::spawn(|| {
                    std::thread::sleep(std::time::Duration::from_millis(300));
                    std::process::exit(0);
                });
            } else {
                let not_found = Response::from_string("Not Found");
                let _ = request.respond(not_found);
            }
        }
    });

    (actual_port, running)
}

fn load_rules() -> Result<RuleConfig, String> {
    // 1. Try relative rules.json
    let p = Path::new("rules.json");
    if p.exists() {
        let content = std::fs::read_to_string(p).map_err(|e| e.to_string())?;
        return serde_json::from_str(&content).map_err(|e| e.to_string());
    }

    // 2. Try adjacent to current exe
    if let Ok(exe) = std::env::current_exe() {
        if let Some(dir) = exe.parent() {
            let p = dir.join("rules.json");
            if p.exists() {
                let content = std::fs::read_to_string(p).map_err(|e| e.to_string())?;
                return serde_json::from_str(&content).map_err(|e| e.to_string());
            }
        }
    }

    // 3. Fallback to embedded rules.json string
    let embedded = include_str!("../rules.json");
    serde_json::from_str(embedded).map_err(|e| e.to_string())
}

fn send_json_response(request: tiny_http::Request, body: String) {
    let header_type = Header::from_bytes(&b"Content-Type"[..], &b"application/json; charset=utf-8"[..]).unwrap();
    let header_cors = Header::from_bytes(&b"Access-Control-Allow-Origin"[..], &b"*"[..]).unwrap();
    let response = Response::from_string(body)
        .with_header(header_type)
        .with_header(header_cors);
    let _ = request.respond(response);
}
