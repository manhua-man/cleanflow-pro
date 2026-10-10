# CleanFlow Pro 系统事实与模块索引 (Facts & Architecture Map)

本文档为 CleanFlow Pro 系统的单源真值清单 (Single Source of Truth)。供人类开发者与 AI Agent 快速检索系统事实、命令、模块映射与架构边界。协作守则请参阅 [CLAUDE.md](CLAUDE.md)。

---

## 1. 核心系统事实 (Core Facts)

| 事实项 | 当前真值 | 备注 |
| :--- | :--- | :--- |
| **当前版本号** | `v0.4.5` | 单源定义于 `Cargo.toml` 第 3 行 |
| **开发语言与规范** | Rust 2021 Edition | Cargo 构建系统 |
| **操作系统支持** | Windows 10 / Windows 11 (x64) | 深度集成 Win32 原生 API |
| **发布产物形态** | 单文件绿色便携二进制 | `target/release/cleanflow.exe` (~9.67 MB) |
| **外部运行时依赖** | 零依赖 (None) | 无需 Node.js / Python / WebView2 |
| **自动化测试现状** | 90 / 90 项通过 (100% Passing) | 纯本地测试，执行耗时 ~32 秒 |
| **内置 Web UI** | `src/ui.html` | 静态无外部依赖单 HTML，由 `server.rs` 嵌入 |
| **默认监听端口** | 自动嗅探空闲端口 (或 `--port <PORT>`) | 绑定 `127.0.0.1` 纯本地安全回环 |

---

## 2. 关键构建与执行命令

```powershell
# 1. 运行全量 90 项自动化单元测试套件
cargo test

# 2. 编译高度优化的生产级单文件可执行程序
cargo build --release

# 3. 运行 CleanFlow Pro 主程序 (自动呼出浏览器控制台)
.\target\release\cleanflow.exe

# 4. 以后台静默系统托盘模式运行
.\target\release\cleanflow.exe --silent

# 5. 指定绑定端口
.\target\release\cleanflow.exe --port 9090
```

---

## 3. 源码模块地图 (Source Code Map)

核心源码位于 `src/` 目录下，共 43 个文件：

### 3.1 基础与服务宿主
- [src/main.rs](src/main.rs): 应用程序主入口，命令行参数解析与模式分流。
- [src/lib.rs](src/lib.rs): 核心库入口与模块导出定义。
- [src/server.rs](src/server.rs): 基于 `tiny_http` 的高性能本地 HTTP API 服务器与静态 UI 桥接。
- [src/ui.html](src/ui.html): 前端 Fluent Mica 深色单页 UI 资产（HTML+CSS+JS 纯原生无外部依赖）。
- [src/tray.rs](src/tray.rs): Win32 原生系统托盘消息泵与图标纳管。
- [src/window.rs](src/window.rs): Win32 消息循环与窗口工具函数。
- [src/daemon_service.rs](src/daemon_service.rs): 后台守护服务状态与健康度检测。
- [src/licensing.rs](src/licensing.rs): 商业分级、设备指纹与离线授权激活管理。

### 3.2 支柱一：磁盘空间资产治理
- [src/scanner.rs](src/scanner.rs): 多线程目录遍历扫描器。
- [src/cleaner.rs](src/cleaner.rs): 安全清理执行管道，带白名单屏障。
- [src/winapp2_parser.rs](src/winapp2_parser.rs) & [src/winapp2_engine.rs](src/winapp2_engine.rs): WinApp2.ini 规则解析与匹配执行引擎。
- [src/rules.rs](src/rules.rs): 内置系统与应用清理规则集。
- [src/duplicates.rs](src/duplicates.rs): BLAKE3 三级分水岭重复文件智选查重。
- [src/giant_files.rs](src/giant_files.rs): 全盘单体超大文件扫描与分类。
- [src/registry.rs](src/registry.rs): 注册表幽灵死链扫描与标准 `.reg` 自动备份快照。
- [src/apps.rs](src/apps.rs): 软件卸载无主残留扫描。
- [src/startup.rs](src/startup.rs): 系统自启动项纳管。
- [src/system_tools.rs](src/system_tools.rs): 回收站底层清空与空间统计。
- [src/migrator.rs](src/migrator.rs): NTFS Directory Junction 事务型跨盘搬迁向导与还原。
- [src/process_lock.rs](src/process_lock.rs): Win32 互斥进程锁预检与占用进程探测。
- [src/block_clone.rs](src/block_clone.rs): Windows 11 ReFS Dev Drive 写时复制块克隆去重。
- [src/vacuum.rs](src/vacuum.rs): 动态调用 `winsqlite3.dll` 整理 SQLite Freelist 空闲页。
- [src/system_storage_audit.rs](src/system_storage_audit.rs): Windows 驱动存储池 (`DriverStore`) 废弃包治理、休眠文件 (`hiberfil.sys`) 与 Windows 11 保留存储诊断。
- [src/cloud_storage_audit.rs](src/cloud_storage_audit.rs): OneDrive / iCloud 同步盘穿透比对与微软官方 Cloud Filter (`cldapi.dll`) 原生脱水。

### 3.3 支柱二：毫秒级全盘搜索与启动中枢
- [src/mft_scanner.rs](src/mft_scanner.rs): NTFS MFT 底层流式裸盘遍历与路径树重构。
- [src/usn_scanner.rs](src/usn_scanner.rs): USN Journal 增量监听管道与就绪卷探测。
- [src/search_engine.rs](src/search_engine.rs): 全盘检索引擎、类型过滤与排序调度。
- [src/search_index.rs](src/search_index.rs): 卷索引生命周期与缓存管理。
- [src/trigram_indexer.rs](src/trigram_indexer.rs): 3-Gram 字符倒排索引与代码全文 Grep 加速。
- [src/pinyin_matcher.rs](src/pinyin_matcher.rs): 汉字多音字变体与双字母复合声母 (zh/ch/sh) 归一化拼音引擎。
- [src/fuzzy_matcher.rs](src/fuzzy_matcher.rs): 模糊匹配与拼写容错评分器。
- [src/launcher.rs](src/launcher.rs): 命令行快捷启动、系统工具别名与网络直达。
- [src/hotkey_manager.rs](src/hotkey_manager.rs): 双击 Ctrl 底层键盘钩子与 Alt+Space 全局热键唤起。
- [src/quick_switch.rs](src/quick_switch.rs): Win32 打开/另存为对话框 (`#32770`) 嗅探与路径无感穿透注入。
- [src/action_runner.rs](src/action_runner.rs): 智能动作中心、自定义动作持久化与宏参数替换展开。
- [src/exclusions.rs](src/exclusions.rs): 通配符与正则排除黑名单规则管理。
- [src/history.rs](src/history.rs): 最近文件历史与搜索词记忆。
- [src/favorites.rs](src/favorites.rs): 常用目录加星收藏与短别名快速直达。
- [src/icon_extractor.rs](src/icon_extractor.rs): Win32 `SHGetFileInfoW` 原生文件关联图标提取与高 DPI 自适应。

### 3.4 支柱三：智能空间护航与自愈规则引擎
- [src/intelligent_guard.rs](src/intelligent_guard.rs): Win32 `SHQueryUserNotificationState` 全屏/游戏免打扰感知、`GetLastInputInfo` 键鼠空闲调度、时序空间消耗斜率 (Burn-rate) 预测与轻量本地自愈规则引擎。

---

## 4. 关键 HTTP API 端点一览

- 空间清理：`/api/scan`, `/api/clean`, `/api/drives`, `/api/recycle-bin`
- 空间透视：`/api/treemap`, `/api/giant-files`, `/api/duplicates/scan`, `/api/duplicates/clean`
- 残留死链：`/api/registry/scan`, `/api/registry/clean`, `/api/apps/leftovers`
- 极客工具：`/api/migrate`, `/api/migrate/status`, `/api/block-clone/inspect`, `/api/vacuum/run`
- 驱动与系统底层：`/api/system/storage-audit`, `/api/system/storage-audit/cleanup-drivers`, `/api/system/storage-audit/set-hibernation`
- 云盘脱水：`/api/cloud-storage/roots`, `/api/cloud-storage/scan`, `/api/cloud-storage/evict-file`, `/api/cloud-storage/dehydrate-batch`
- 智能护航：`/api/guard/status`, `/api/guard/trigger-self-heal`, `/api/guard/toggle-rule`
- 毫秒检索：`/api/search`, `/api/search/index`, `/api/search/usn-status`, `/api/search/recent`
- 动作与热键：`/api/actions/list`, `/api/actions/execute`, `/api/quick-switch/check`
- 收藏与排除：`/api/favorites`, `/api/exclusions`

---

## 5. 数据与配置文件规范

- `rules.json`: 内置规则配置定义。
- `winapp2_default.ini`: WinApp2 经典清理规则子集。
- `junctions.json`: NTFS Junction 搬迁历史生命周期注册表（运行期生成）。
- `cleanflow_history.json`: 搜索历史与最近文件记录（运行期生成）。
- `custom_actions.json`: 用户自定义动作配置（运行期生成）。
- `exclusions.json`: 用户自定义排除项规则（运行期生成）。
- `favorites.json`: 目录收藏夹数据（运行期生成）。
- `license.json`: 商业授权许可与设备指纹状态（运行期生成）。
