# CleanFlow 外部参考项目与技术演进借鉴文档

本文档系统性梳理并归档了在构建 CleanFlow (净流) 桌面端空间资产治理引擎与全盘极速检索中枢过程中，所参考和借鉴的业界经典开源项目、底层系统机制、逆向反编译资产与设计模式。

---

## 1. 核心参考项目与灵感矩阵

| 参考项目 | 核心技术领域 | 官方/开源参考 | 对 CleanFlow 的关键借鉴与沉淀 | 详细分析档案 |
| :--- | :--- | :--- | :--- | :--- |
| **Czkawka** | Rust 极致性能磁盘清理与重复文件治理 | [qarmin/czkawka](https://github.com/qarmin/czkawka) | 多线程并发遍历架构、两阶段校验初筛、系统关键目录强制白名单安全屏障 (Safety Sentinel) | 本文 2.1 节 |
| **WizTree** / **SpaceSniffer** | Windows 磁盘容量热力与快速索引标杆 | [antibodysoft.com/wiztree](https://antibodysoft.com/wiztree) | 空间占用全景地平线视觉条 (Treemap / Horizon Barometer)、全盘 Top 单体超大文件透视分析 | 本文 2.2 节 |
| **SteamMover** / **FolderMove** | Windows 资产无感软搬迁与目录符号重定向 | [steammove.sourceforge.net](https://steammover.sourceforge.net/) | NTFS Junction 目录联接机制、双向生命周期账本 (注册与一键还原)、搬迁前进程独占探测与解绑 | 本文 2.3 节 |
| **BleachBit** / **Litestream** | SQLite 深度瘦身、WAL 事务截断与无损原子压缩 | [bleachbit/bleachbit](https://github.com/bleachbit/bleachbit) | 基于 VACUUM 的空洞碎片整理、WAL 日志强制检查点截断、无损物理扇区重组 | 本文 2.4 节 |
| **Listary Pro** | Windows 原生交互、对话框穿透与动作启动中枢 | [listary.com](https://www.listary.com/) | 双击 Ctrl 底层键盘钩子、标准文件对话框 (#32770) Quick Switch 自动穿透跳转、动作宏展开流水线、Spotlight 悬浮交互 | [LISTARY_PRO_ANALYSIS.md](references/LISTARY_PRO_ANALYSIS.md) |
| **fsearch** | 紧凑内存拓扑、1-Edit 容错与高吞吐虚拟表格 | [cboxdoerfer/fsearch](https://github.com/cboxdoerfer/fsearch) | 扁平父节点拓扑内存节约、1-Edit Damerau-Levenshtein 拼写容错纠错打分、3-Gram 倒排预过滤、60fps 虚拟视口复用数据网格 | [FSEARCH_ANALYSIS.md](references/FSEARCH_ANALYSIS.md) |

---

## 2. 深度技术解析与 CleanFlow 落地实践

### 2.1 Czkawka (Rust 高性能并发与安全防呆设计)
- **技术原理**：
  - Czkawka 作为 Rust 编写的顶流清理工具，最大特色在于极致的多线程 I/O 并发与内存安全控制。
  - 在大规模目录遍历时，若直接计算全量哈希或进行深度递归，会导致严重的磁盘 I/O 堵塞。Czkawka 采取分级筛选：先快速提取文件元数据（大小）过滤，仅对候选集进行轻量级采样，最后阶段才做完整比对。
  - 同时，针对误删系统关键文件的灾难性风险，Czkawka 在内核层固化了系统目录绝对白名单。
- **CleanFlow 的架构落地**：
  - **Rust 原生安全内核**：使用 Rust 多线程与高效遍历，摒弃传统基于 Shell/Bat 的低效脚本。
  - **防呆安全屏障**：在 `cleaner.rs` 与规则引擎中严格规避 Windows 系统盘核心保护目录（`System32`、`WinSxS`、`ProgramData\Microsoft` 等），即使规则定义宽泛也绝不误伤系统基础组件。
  - **进程锁定主动探针**：在清理与搬迁前，调用 Win32 进程探针，检测微信、Cursor、VSCode 等是否正在持有文件句柄，避免清理半截引发文件损坏。

### 2.2 WizTree & SpaceSniffer (空间占比视觉化与直观治理)
- **技术原理**：
  - 传统清理工具只展示枯燥的列表，用户无法直观感受“我的 C 盘究竟被什么占满了”。
  - WizTree 与 SpaceSniffer 采用矩形树图（Treemap）以及多段条形比例图，让用户在几毫秒内建立空间物理认知。
- **CleanFlow 的架构落地**：
  - **C 盘资产地平线光谱条 (Storage Horizon Spectrum)**：
    - 采用 5 色渐变光谱段直观展示：[系统核心与已占用] / [零风险安全清理] / [开发构建缓存] / [重型大资产迁移] / [当前可用物理空间]。
    - 动态输出治理后预计可用容量与净收益增量（例如 `30.00 GB -> 预计 31.86 GB (+1.86 GB)`），让用户清晰掌握治理成果。
  - **全盘大文件透视分析 (Giant Files Detective)**：
    - 专攻 100 MB 以上的单体超大文件，按虚拟机镜像（.vmdk/.img/.iso）、数据库（.db/.vscdb）、AI 权重（.bin/.safetensors）、转储日志（.dmp）分类呈现，直击空间杀手。

### 2.3 SteamMover & FolderMove (NTFS Junction 资产搬迁与双向生命周期)
- **技术原理**：
  - Windows 系统由于历史原因，许多重型应用（如微信客户端数据、Android SDK/AVD、Gradle 缓存、Ollama 模型权重）默认强制写入 C 盘 `%APPDATA%` 或 `%USERPROFILE%`。
  - SteamMover 最早利用 Windows NTFS 原生目录联接（Reparse Point / `mklink /J`）解决游戏库爆盘问题：将目录实际物理数据移动到大容量副盘（D/E 盘），而在 C 盘原位置创建一个 0 字节的透明符号入口。应用程序、驱动和 Windows 操作系统访问时完全无感。
- **CleanFlow 的架构落地**：
  - **异步多线程迁移与实时进度浮层**：
    - 解决了海量大文件搬迁时界面卡死无反馈的问题。通过后台线程异步执行与多阶段状态机（`SCANNING` -> `COPYING` -> `LINKING` -> `COMPLETED`），前端以 300ms 频率实时获取已拷贝字节数、文件数、吞吐百分比与当前传输文件名。
  - **双向生命周期账本与一键还原 (Undo/Restore)**：
    - 独立维护 `junctions.json` 注册表，记录每笔迁移的原入口、物理存储路径、释放容量与创建时间。
    - 每一处虚拟联接均提供**一键完整无损回退还原至 C 盘**的功能。
  - **回迁容量预飞校验 (Pre-flight Capacity Check)**：
    - 在用户执行还原前，通过 Win32 `GetDiskFreeSpaceExW` 自动校验 C 盘剩余可用物理空间。若 C 盘空间不足，立即安全拦截，彻底杜绝回迁导致爆盘的隐患。

### 2.4 BleachBit & Litestream (SQLite 零依赖原生无损收缩)
- **技术原理**：
  - 现代化桌面应用（如 VSCode / Cursor 的 `state.vscdb`、各类通讯工具离线消息库）普遍采用 SQLite 存储。经过高频写入与删除后，物理文件中充斥着大量空闲碎片页（Freelist），导致文件体积膨胀至数 GB 却无法自动归还物理磁盘。
  - 传统的 `VACUUM` 治理工具多依赖外部环境（如 Python `sqlite3` 模块），在干净的 Windows 客户机上常常因缺少运行环境而崩溃。
  - 现代化最佳实践是调用系统原生 C API，并配合 `PRAGMA wal_checkpoint(TRUNCATE)` 截断 WAL 日志。
- **CleanFlow 的架构落地**：
  - **零环境依赖：Windows 原生 WinSqlite3 驱动**：
    - CleanFlow 不依赖外部 Python 或任何动态解释器，直接通过 Win32 API 动态载入 Windows 10/11 系统内置的 `C:\Windows\System32\winsqlite3.dll`（导出 `sqlite3_open`, `sqlite3_exec`, `sqlite3_close`），做到 100% 单文件开箱即用。
  - **无损物理挤水分与容量预期看板**：
    - 执行序列：`PRAGMA busy_timeout = 8000; PRAGMA wal_checkpoint(TRUNCATE); VACUUM; PRAGMA optimize;`。
    - 前端呈现物理占用与压缩后预期柱状图（如 `4.02 GB -> 38.5 MB，无损挤出 99.1% 水分`），并在执行前后即时刷新驱动器剩余空间。

### 2.5 Listary Pro (Windows 原生桌面交互与文件对话框穿透标杆)
- **技术原理与资产沉淀**：
  - Listary 是 Windows 桌面文件检索与全局工作流效率的绝对标杆，其杀手级体验包括：双击 Ctrl 快速唤醒 Spotlight、Win32 文件对话框（`#32770`）Quick Switch 穿透、动作流水线与宏展开替换引擎。
  - **逆向反编译成果物归档**：
    - 解包与反编译资产完整保存在本地物理路径：`C:\Users\EDY\.gemini\antigravity\scratch\listary_unpack\`；
    - 包含反编译工程 `decompiled/Listary`、`decompiled/Listary.Common`、`decompiled/Listary.Interop`，以及核心组件 `extracted/app/listary_engine.dll`、`extracted/app/cnmatch.bin`；
    - 详见专项技术剖析报告：[LISTARY_PRO_ANALYSIS.md](references/LISTARY_PRO_ANALYSIS.md)。
- **CleanFlow 的架构落地与超越**：
  - **纯 Rust 单一二进制重构**：彻底抛弃 Listary 的 .NET 6/WPF 笨重运行时，将常驻物理内存从 150MB+ 降至 18MB；
  - **MFT 裸卷流式直读**：自研 `src/mft_scanner.rs`，1~3 秒直接流式解码裸盘 NTFS MFT 簇链并重组路径树，超越外置闭源引擎依赖；
  - **Quick Switch 对话框穿透**：自研 `src/quick_switch.rs`，纯 Win32 API 递归寻找 `#32770` 窗口子控件并发送 `WM_SETTEXT`，零 DLL 注入保证系统稳定性；
  - **检索与空间资产治理闭环**：检索结果直接联动跨卷 Junction 搬家、ReFS 零拷贝块克隆去重与进程占用强制解锁。

### 2.6 fsearch (极致紧凑内存拓扑、1-Edit 拼写容错与高吞吐虚拟表格)
- **技术原理与工程沉淀**：
  - fsearch 证明了在海量全盘文件检索中，算法设计与内存组织比盲目多线程并发更加关键：
    1. **扁平父指针拓扑**：仅存父节点整型 ID 而不重复分配完整路径字符串，将节点内存压缩至 24 字节；
    2. **1-Edit Damerau-Levenshtein 容错**：对 $\ge 4$ 字符的输入容忍 1 处击键失误（包括相邻字母对换）；
    3. **Trigram 3-Gram 倒排预过滤**：三元组倒排表瞬间剔除 95% 无关候选；
    4. **虚拟视口复用渲染**：仅复用 25~30 个可见 DOM 节点，保障 10 万条结果 60fps 平滑惯性滚动。
  - 详见专项技术剖析报告：[FSEARCH_ANALYSIS.md](references/FSEARCH_ANALYSIS.md)。
- **CleanFlow 的架构落地与超越**：
  - **自研 1-Edit 拼写容错打分器**：在 `src/fuzzy_matcher.rs` 中完整实现与 fsearch 算法对齐的 Damerau-Levenshtein 拼写容错与边界加权；
  - **千万行源码全文毫秒 Grep**：创新性地将 Trigram 预过滤技术从文件名检索拓展至工程代码全文 Grep 检索（`src/trigram_indexer.rs`）；
  - **Fluent Mica 高级虚拟数据网格**：在 `src/ui.html` 中实现基于双向弹性占位器的虚拟视口，支持按文件名、路径、大小、修改时间与匹配得分进行内存即时多列升降序重排 (< 1ms)。

---

## 3. 功能吸收审计与架构指导原则

关于 CleanFlow 对 Listary（原版 38 项）与 fsearch（原版 26 项）特性的逐项 1 对 1 吸收审计与状态对比，请参阅：
- [FEATURE_ABSORPTION_AUDIT_REPORT.md](../05-测试与基准/FEATURE_ABSORPTION_AUDIT_REPORT.md)

CleanFlow 的核心愿景是打造一款**完全属于 Windows 桌面生态、面向全体客户的工业级独立资产治理与极速检索中枢**：
1. **单一二进制交付**：保持 9.6 MB 独立 Release 单文件分发，无 Node.js、Python、.NET、WebView2 运行环境安装门槛。
2. **严苛安全防呆**：只做 100% 确定性的安全清理；对大资产只搬迁不删除；对软联接提供双向可逆还原保障；对数据库做只挤水分不删业务记录的原生 VACUUM。
3. **沉浸式桌面质感**：严格遵循 Windows 11 Fluent Design / Mica 设计系统与 Master-Detail 双栏工作台，保障现代化桌面端操作手感。
