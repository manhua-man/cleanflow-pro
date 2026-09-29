# CleanFlow (净流) Pro - Windows 资产治理桌面引擎

CleanFlow (净流) 是一款基于 Rust 核心打造的高性能、工业级 Windows 磁盘空间资产治理桌面软件。软件采用原生单文件架构分发（~5.6 MB），无外部运行环境依赖（无需 Node.js / Python），并严格遵循 Windows 11 Fluent Design 与 Nordic Mica 深色美学规范。

---

## 核心治理能力

1. **智能安全清理 (100% 零风险)**
   - 专攻 Windows 系统临时缓存、系统更新冗余备份、错误报告、缩略图数据库与办公通讯离线包。
   - 内置底层独占跳过与防呆屏障，确保日常办公与系统运行绝对稳定。

2. **现代开发与构建生态治理**
   - 深度治理现代工程师高频构建工具：npm、Bun、pnpm、uv、Cargo、Gradle、Unity Shader 缓存及历史旧版 AI 运行时。
   - Master-Detail 双栏工作台设计：左侧分类快速检索，右侧物理绝对路径树穿透定位。

3. **大资产空间无感迁移 (NTFS Junction 搬家引擎)**
   - 针对动辄占用 30GB~100GB 的巨型目录（如微信数据、Android SDK/AVD、Ollama 模型、HuggingFace 权重）：
     - 通过多线程异步同步引擎将物理文件迁移至大容量副盘（D/E 盘）。
     - 在 C 盘原位置自动创建 0 字节的透明 NTFS 虚拟联接（Junction），应用程序无感照常读写，瞬间为 C 盘释放巨量空间。
   - **多线程实时流式进度浮层**：实时反馈已迁移容量、文件同步计数、总体百分比与当前传输文件名。

4. **虚拟联接管理中心 (双向生命周期与安全回退)**
   - 集中呈现所有已重定向的系统资产，提供链路健康度检测（正常/断裂）。
   - **一键安全迁回 C 盘 (Undo/Restore)**：支持随时将数据完整迁回原位并解除联接。
   - **回迁容量预飞校验**：执行回迁前自动调用 Win32 API 校验 C 盘剩余空间，杜绝回迁爆盘隐患。

5. **SQLite 核心数据库无损挤水分 (VACUUM)**
   - 专攻 Cursor / VSCode `state.vscdb` 以及各类通讯离线库经年累月产生的高达 95% 空闲碎片页（Freelist）。
   - **零外部环境依赖**：底层直接通过 Win32 API 动态调用 Windows 10/11 系统内置的 `winsqlite3.dll`，执行 `PRAGMA wal_checkpoint(TRUNCATE)` 与 `VACUUM`，保障业务对话记录 0 丢失，直接将数据库从数 GB 压缩至几十兆。

6. **全盘单体超大文件透视分析 (Top 100)**
   - 极速揪出超过 100 MB 的单体超大文件，支持虚拟机镜像、数据库、安装包、AI 模型权重、转储日志等分类筛选，支持在资源管理器中一键高亮定位。

---

## 外部参考与技术借鉴

本项目系统吸收并借鉴了开源领域的优秀设计与实践，详细技术解析请参阅外部参考文档：
- [docs/EXTERNAL_REFERENCES.md](docs/EXTERNAL_REFERENCES.md)

主要参考项目包含：
- **Czkawka**: Rust 顶流并发扫描架构、两阶段校验与系统关键目录安全白名单保护。
- **WizTree & SpaceSniffer**: 空间占比地平线视觉条 (Treemap / Horizon Spectrum) 与全盘大文件透视。
- **SteamMover & FolderMove**: NTFS Junction 目录联接机制、双向生命周期账本与进程锁定探针。
- **BleachBit & Litestream**: SQLite 原子无损压缩、WAL 日志截断与原生系统驱动集成。

---

## 架构与技术栈

- **开发语言**: Rust (2021 Edition, GNU x86_64)
- **网络与服务**: tiny_http (本地极轻量 HTTP 协议桥接)
- **底层系统互操作**: Win32 API (Reparse Point, GetDiskFreeSpaceExW, LoadLibraryA, winsqlite3.dll)
- **界面架构**: Windows 11 Fluent Design / Nordic Mica 暗色深度调色板、Segoe UI Variable / Cascadia Code 字体排印
- **交互规范**: Master-Detail 双栏深度穿透工作台、自适应流式进度浮层
- **交付体积**: ~5.6 MB Release 单一便携式可执行文件 (`cleanflow.exe`)

---

## 快速构建与运行

### 1. 环境准备
- Windows 10 (1809+) 或 Windows 11 (x64)
- Rust 编译器 (`rustc` 1.80+) 与 Cargo

### 2. 编译 Release 版本
```bash
cargo build --release
```
编译产物位于 `target/release/cleanflow.exe`。

### 3. 运行
直接双击 `cleanflow.exe` 或在终端运行：
```bash
# 启动桌面 GUI 界面
./target/release/cleanflow.exe

# 命令行极速体检模式
./target/release/cleanflow.exe --cli

# 输出标准 JSON 格式报告
./target/release/cleanflow.exe --json
```

---

## 开源协议

本项目基于 MIT License 开源，详情参阅 LICENSE 文件。
