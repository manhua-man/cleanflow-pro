use std::path::Path;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use tiny_http::{Header, Method, Response, Server, StatusCode};

use crate::cleaner::{clear_directory_contents, delete_single_file};
use crate::disks::get_disk_drives;
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

#[derive(serde::Deserialize)]
struct DockerPruneRequest {
    target: String,
}

#[derive(serde::Deserialize)]
struct AddCustomRuleRequest {
    name: String,
    path_pattern: String,
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

            if url == "/" || url == "/index.html" {
                let html = if let Ok(s) = std::fs::read_to_string("src/ui.html") {
                    s
                } else if let Ok(s) = std::fs::read_to_string("ui.html") {
                    s
                } else {
                    HTML_CONTENT.to_string()
                };
                let header = Header::from_bytes(&b"Content-Type"[..], &b"text/html; charset=utf-8"[..]).unwrap();
                let response = Response::from_string(html).with_header(header);
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
            } else if url == "/api/usn/status" && method == Method::Get {
                let (elevated, active, journal) = crate::usn_scanner::check_usn_journal_status("C:");
                let res_json = serde_json::json!({
                    "volume": "C:",
                    "is_elevated": elevated,
                    "usn_journal_active": active,
                    "has_journal_data": journal.is_some()
                }).to_string();
                send_json_response(request, res_json);
            } else if url == "/api/giant-files" && method == Method::Get {
                // Minimum size: 100 MB, hybrid scanner with automatic USN acceleration
                let min_size = 100 * 1024 * 1024;
                let scan_res = crate::usn_scanner::scan_giant_files_hybrid(None, min_size, 100);
                let json = serde_json::to_string(&scan_res.files).unwrap_or_else(|_| "[]".to_string());
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
            } else if url == "/api/rules/custom" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<AddCustomRuleRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => match save_custom_rule(req) {
                        Ok(_) => {
                            send_json_response(request, r#"{"success": true, "message": "规则保存成功"}"#.to_string());
                        }
                        Err(e) => {
                            let err_json = serde_json::json!({
                                "success": false,
                                "error": e
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
            } else if url == "/api/registry/scan" && method == Method::Get {
                let issues = crate::registry::scan_registry_issues();
                let json = serde_json::to_string(&issues).unwrap_or_else(|_| "[]".to_string());
                send_json_response(request, json);
            } else if url == "/api/registry/clean" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                #[derive(serde::Deserialize)]
                struct RegistryCleanReq {
                    ids: Vec<String>,
                }

                let req_parsed: Result<RegistryCleanReq, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => {
                        let all_issues = crate::registry::scan_registry_issues();
                        let targets: Vec<_> = all_issues
                            .into_iter()
                            .filter(|i| req.ids.contains(&i.id))
                            .collect();
                        let result = crate::registry::clean_registry_issues(&targets);
                        let json = serde_json::to_string(&result).unwrap_or_else(|_| "{}".to_string());
                        send_json_response(request, json);
                    }
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/registry/backups" && method == Method::Get {
                let records = crate::registry::list_registry_backups();
                let json = serde_json::to_string(&records).unwrap_or_else(|_| "[]".to_string());
                send_json_response(request, json);
            } else if url == "/api/registry/backups/restore" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                #[derive(serde::Deserialize)]
                struct RegistryBackupActionReq {
                    backup_path: String,
                }

                match serde_json::from_str::<RegistryBackupActionReq>(&content) {
                    Ok(req) => match crate::registry::restore_registry_backup(&req.backup_path) {
                        Ok(()) => {
                            send_json_response(request, r#"{"success": true, "message": "注册表快照还原成功"}"#.to_string());
                        }
                        Err(e) => {
                            let err_json = serde_json::json!({
                                "success": false,
                                "error": e.to_string(),
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
            } else if url == "/api/registry/backups/delete" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                #[derive(serde::Deserialize)]
                struct RegistryBackupActionReq {
                    backup_path: String,
                }

                match serde_json::from_str::<RegistryBackupActionReq>(&content) {
                    Ok(req) => match crate::registry::delete_registry_backup(&req.backup_path) {
                        Ok(()) => {
                            send_json_response(request, r#"{"success": true}"#.to_string());
                        }
                        Err(e) => {
                            let err_json = serde_json::json!({
                                "success": false,
                                "error": e.to_string(),
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
            } else if url == "/api/docker/status" && method == Method::Get {
                let status = crate::docker::get_docker_status();
                let json = serde_json::to_string(&status).unwrap_or_else(|_| "{}".to_string());
                send_json_response(request, json);
            } else if url == "/api/docker/prune" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                let req_parsed: Result<DockerPruneRequest, _> = serde_json::from_str(&content);
                match req_parsed {
                    Ok(req) => match crate::docker::prune_docker(&req.target) {
                        Ok(output) => {
                            let res_json = serde_json::json!({
                                "success": true,
                                "output": output,
                            })
                            .to_string();
                            send_json_response(request, res_json);
                        }
                        Err(e) => {
                            let res_json = serde_json::json!({
                                "success": false,
                                "error": e,
                            })
                            .to_string();
                            send_json_response(request, res_json);
                        }
                    },
                    Err(e) => {
                        let res_json = serde_json::json!({
                            "success": false,
                            "error": format!("解析请求失败: {}", e),
                        })
                        .to_string();
                        send_json_response(request, res_json);
                    }
                }
            } else if url == "/api/startup/list" && method == Method::Get {
                let items = crate::startup::get_startup_items();
                let json = serde_json::to_string(&items).unwrap_or_else(|_| "[]".to_string());
                send_json_response(request, json);
            } else if url == "/api/startup/remove" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                #[derive(serde::Deserialize)]
                struct StartupRemoveReq {
                    source: String,
                    name: String,
                    location: String,
                }

                match serde_json::from_str::<StartupRemoveReq>(&content) {
                    Ok(req) => match crate::startup::remove_startup_item(&req.source, &req.name, &req.location) {
                        Ok(_) => {
                            send_json_response(request, r#"{"success": true}"#.to_string());
                        }
                        Err(e) => {
                            let err_json = serde_json::json!({ "success": false, "error": e }).to_string();
                            send_json_response(request, err_json);
                        }
                    },
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/apps/list" && method == Method::Get {
                let apps = crate::apps::get_installed_apps();
                let json = serde_json::to_string(&apps).unwrap_or_else(|_| "[]".to_string());
                send_json_response(request, json);
            } else if url == "/api/apps/leftovers" && method == Method::Get {
                let leftovers = crate::apps::scan_app_leftovers();
                let json = serde_json::to_string(&leftovers).unwrap_or_else(|_| "[]".to_string());
                send_json_response(request, json);
            } else if url == "/api/apps/uninstall" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                #[derive(serde::Deserialize)]
                struct AppUninstallReq {
                    uninstall_string: String,
                }

                match serde_json::from_str::<AppUninstallReq>(&content) {
                    Ok(req) => match crate::apps::launch_uninstaller(&req.uninstall_string) {
                        Ok(_) => {
                            send_json_response(request, r#"{"success": true}"#.to_string());
                        }
                        Err(e) => {
                            let err_json = serde_json::json!({ "success": false, "error": e }).to_string();
                            send_json_response(request, err_json);
                        }
                    },
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/system/maintenance" && method == Method::Get {
                let status = crate::system_tools::get_system_maintenance_status();
                let json = serde_json::to_string(&status).unwrap_or_else(|_| "{}".to_string());
                send_json_response(request, json);
            } else if url == "/api/system/recycle-bin/empty" && method == Method::Post {
                match crate::system_tools::empty_recycle_bin() {
                    Ok(bytes) => {
                        let res_json = serde_json::json!({ "success": true, "bytes_freed": bytes }).to_string();
                        send_json_response(request, res_json);
                    }
                    Err(e) => {
                        let err_json = serde_json::json!({ "success": false, "error": e }).to_string();
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/system/empty-dirs/scan" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                #[derive(serde::Deserialize)]
                struct EmptyDirsScanReq {
                    target_dir: String,
                }

                let target = match serde_json::from_str::<EmptyDirsScanReq>(&content) {
                    Ok(req) => req.target_dir,
                    Err(_) => {
                        let temp = std::env::var("LOCALAPPDATA").unwrap_or_default() + "\\Temp";
                        temp
                    }
                };

                let empty_dirs = crate::system_tools::scan_empty_directories(&target);
                let json = serde_json::to_string(&empty_dirs).unwrap_or_else(|_| "[]".to_string());
                send_json_response(request, json);
            } else if url == "/api/system/empty-dirs/clean" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                #[derive(serde::Deserialize)]
                struct EmptyDirsCleanReq {
                    paths: Vec<String>,
                }

                match serde_json::from_str::<EmptyDirsCleanReq>(&content) {
                    Ok(req) => {
                        let (cleaned, errs) = crate::system_tools::clean_empty_directories(&req.paths);
                        let res_json = serde_json::json!({ "success": true, "cleaned_count": cleaned, "errors": errs }).to_string();
                        send_json_response(request, res_json);
                    }
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/duplicates/scan" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                #[derive(serde::Deserialize)]
                struct DupScanReq {
                    target_dir: String,
                    #[serde(default = "default_min_sz")]
                    min_size_mb: u64,
                }
                fn default_min_sz() -> u64 { 1 }

                match serde_json::from_str::<DupScanReq>(&content) {
                    Ok(req) => {
                        let min_bytes = req.min_size_mb * 1024 * 1024;
                        let groups = crate::duplicates::scan_duplicate_files(&req.target_dir, min_bytes);
                        let json = serde_json::to_string(&groups).unwrap_or_else(|_| "[]".to_string());
                        send_json_response(request, json);
                    }
                    Err(e) => {
                        let err_json = format!(r#"{{"success": false, "error": "{}"}}"#, e);
                        send_json_response(request, err_json);
                    }
                }
            } else if url == "/api/duplicates/volume-status" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                #[derive(serde::Deserialize)]
                struct VolReq {
                    path: Option<String>,
                }

                let p = serde_json::from_str::<VolReq>(&content)
                    .ok()
                    .and_then(|r| r.path)
                    .unwrap_or_else(|| "C:\\".to_string());

                let status = crate::block_clone::check_volume_block_clone_support(&p);
                let res_json = serde_json::to_string(&status).unwrap_or_default();
                send_json_response(request, res_json);
            } else if url == "/api/duplicates/clean" && method == Method::Post {
                let mut content = String::new();
                let _ = request.as_reader().read_to_string(&mut content);

                #[derive(serde::Deserialize)]
                struct DupCleanReq {
                    paths: Vec<String>,
                    mode: Option<String>,
                    master_path: Option<String>,
                }

                match serde_json::from_str::<DupCleanReq>(&content) {
                    Ok(req) => {
                        if req.mode.as_deref() == Some("refs_clone") {
                            if let Some(master) = req.master_path {
                                let mut cloned_bytes = 0u64;
                                let mut count = 0usize;
                                let mut errs = Vec::new();
                                for target in &req.paths {
                                    match crate::block_clone::clone_file_extents(&master, target) {
                                        Ok(b) => {
                                            cloned_bytes += b;
                                            count += 1;
                                        }
                                        Err(e) => {
                                            errs.push(format!("{}: {}", target, e));
                                        }
                                    }
                                }
                                let res_json = serde_json::json!({
                                    "success": true,
                                    "mode": "refs_clone",
                                    "bytes_freed": cloned_bytes,
                                    "files_cloned": count,
                                    "errors": errs
                                }).to_string();
                                send_json_response(request, res_json);
                            } else {
                                let err_json = r#"{"success": false, "error": "ReFS 块克隆模式需要指定 master_path 母本路径"}"#;
                                send_json_response(request, err_json.to_string());
                            }
                        } else {
                            let (freed, count, errs) = crate::duplicates::delete_duplicate_files(&req.paths);
                            let res_json = serde_json::json!({
                                "success": true,
                                "mode": "delete",
                                "bytes_freed": freed,
                                "files_deleted": count,
                                "errors": errs
                            }).to_string();
                            send_json_response(request, res_json);
                        }
                    }
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

fn save_custom_rule(req: AddCustomRuleRequest) -> Result<(), String> {
    let mut config = load_rules()?;

    let rule_id = format!(
        "custom_{}",
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs()
    );

    let new_rule = crate::rules::CleanRule {
        id: rule_id,
        name: req.name,
        path_pattern: req.path_pattern,
        action: "clean_dir".to_string(),
        default_checked: true,
        tag: None,
    };

    if let Some(cat) = config.categories.iter_mut().find(|c| c.id == "custom") {
        cat.rules.push(new_rule);
    } else {
        config.categories.push(crate::rules::RuleCategory {
            id: "custom".to_string(),
            name: "用户自定义扩展".to_string(),
            description: "用户在界面自定义配置的专属巡检清理规则".to_string(),
            risk_level: "safe".to_string(),
            rules: vec![new_rule],
        });
    }

    let json_str = serde_json::to_string_pretty(&config).map_err(|e| e.to_string())?;

    // Save to relative path
    let _ = std::fs::write("rules.json", &json_str);

    // Also save alongside current exe if executable location is different
    if let Ok(exe) = std::env::current_exe() {
        if let Some(dir) = exe.parent() {
            let p = dir.join("rules.json");
            let _ = std::fs::write(p, &json_str);
        }
    }

    Ok(())
}

fn send_json_response(request: tiny_http::Request, body: String) {
    let header_type = Header::from_bytes(&b"Content-Type"[..], &b"application/json; charset=utf-8"[..]).unwrap();
    let header_cors = Header::from_bytes(&b"Access-Control-Allow-Origin"[..], &b"*"[..]).unwrap();
    let response = Response::from_string(body)
        .with_header(header_type)
        .with_header(header_cors);
    let _ = request.respond(response);
}
