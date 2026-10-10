# CleanFlow Pro 功能特性全景矩阵 (Feature Matrix)

本文档系统性汇总 CleanFlow Pro 当前已实现并验证的全部功能特性，按三大业务支柱组织。所有特性均经过 90 项自动化单元测试验证。

---

## 支柱一：工业级磁盘空间资产治理 (Storage Governance)

### 1. 极速空间清理 (Clean)
- **环形空间健康度仪表盘**：动态感知系统各盘物理余量、占用比例与可回收规模。
- **多维分类光谱占比条 (Spectrum Bar)**：直观呈现系统冗余、现代开发、办公通讯、浏览器及数据库等维度的色彩编码分布。
- **场景化深度专清管道**：
  - **系统临时垃圾**：用户 `%LOCALAPPDATA%\Temp`、Windows 错误报告、补丁残留及空目录；
  - **现代开发套件缓存**：Cargo、Pip、Gradle、Android Studio、Cursor、Unity 编译缓存；
  - **微信与办公深度专清**：微信 4.0 日志、月度离线多媒体、旧版 XPlugin 与飞书缓存；
  - **主流浏览器专清**：Edge 与 Chrome 离线多媒体缓存与 IndexedDB 冗余；
  - **全盘回收站清空**：底层跨卷清空与容量感知。

### 2. 空间透视与去重 (Analyze)
- **自适应 Treemap 矩形树图**：按物理尺寸动态划分 12 栅格矩阵色块，支持数据库、虚拟机磁盘、安装包高光分类。
- **双层防截断检查条 (Inspector Strip)**：悬停/点击色块时联动呈现物理路径，支持定位目录、复制路径、VACUUM 压缩与搬家。
- **BLAKE3 三级分水岭查重**：体积初筛 -> 16KB 头部特征散列 -> BLAKE3 全量并发树状散列，最早母本标记保留，一键清理冗余副本。

### 3. 残留与死链瘦身 (Purge)
- **软件卸载孤立残留**：深度扫描已卸载软件残留在 `AppData\Local` 与 `AppData\Roaming` 的无主配置与缓存目录。
- **注册表死链与失效自启修复**：扫描并修复 MUICache 失效映射、OpenWith 失效右键打开方式与失效自启动项。
- **自动标准 .reg 备份机制**：清理前自动生成高精度时间戳快照文件，支持双击一键原生合并回滚。

### 4. 深度极客工具箱 (Tools)
- **NTFS Junction 跨盘搬迁向导**：支持 Ollama、HuggingFace、PyTorch、Steam、Unity、VS Packages 一键填入，集成互斥进程安全预检与无损回退。
- **ReFS 块克隆写时复制去重**：调用 Win32 `FSCTL_DUPLICATE_EXTENTS_TO_FILE`，副本物理空间为 0，写时自动触发 CoW。
- **SQLite 物理碎片收缩 (VACUUM)**：动态载入 `winsqlite3.dll` 整理 IDE 数据库中的 Freelist 空闲页与 WAL 截断。
- **Windows 驱动存储池安全清理 (DriverStore)**：`pnputil /enum-drivers` 穿透比对，智能分组识别陈旧冗余旧版本驱动，通过官方受保护管道卸载。
- **系统休眠与保留存储调优**：`hiberfil.sys` 空间诊断与 `powercfg` 三档模式向导；Windows 11 保留存储注册表高精度穿透。
- **云端同步盘离线缓存脱水 (Cloud Storage Dehydration)**：多源云盘本地同步根目录自动探测，基于 `cldapi.dll` 原生脱水本地物理簇，严禁物理删除文件。

---

## 支柱二：毫秒级全盘桌面搜索与启动中枢 (Search & Launcher)

### 1. 底层极速检索内核
- **NTFS MFT 裸盘流式直读**：通过 `DeviceIoControl` 绕过高层 API，1~3ms 枚举百万文件元数据。
- **USN Journal 增量监听**：常驻管道实时捕获文件创建、重命名与删除。
- **Trigram 内存加速器**：万级记录微秒级流式过滤。
- **开发噪声自动屏蔽盾**：默认过滤 `node_modules`、`.git`、`target`、`.venv` 等，支持 `noise:all` 临时解除。

### 2. 智能拼音检索引擎
- **多音字全覆盖 (ToPinyinMulti)**：多音字双向变体索引，输入 `cq` 或 `zq` 均能精确命中 `重庆.pdf`。
- **双字母声母 (zh/ch/sh) 归一化**：输入 `zhw` 自动映射为 `zw`，输入 `chq` 映射为 `cq`，输入 `shj` 映射为 `sj`。

### 3. 大众交互与视觉体验
- **可视化类型过滤药丸 (Filter Chips)**：全部、文件夹、文档、图片、视频、音乐、压缩包、应用一键点选过滤。
- **虚拟视口复用渲染引擎 (Virtual Viewport)**：常驻 DOM 25~30 行，支持万级结果流式滚动，稳定 60fps。
- **Win32 原生官方图标提取**：调用 `SHGetFileInfoW` 提取官方高 DPI 真实图标。

### 4. Windows 原生系统集成
- **原生系统托盘常驻**：Win32 托盘图标泵，右键菜单，退出时彻底清理通知区图标。
- **开机自启动管理**：注册表 `Run` 项一键切换。
- **双击 Ctrl 底层钩子**：Win32 `WH_KEYBOARD_LL` 手势检测，350ms 阈值呼出 Spotlight。
- **Alt + Space Spotlight 悬浮窗**：标准全局热键。
- **Quick Switch 对话框穿透**：嗅探 `#32770` 标准文件对话框，一键将当前路径填充至输入控件。

### 5. 智能动作中枢 (Smart Action Hub)
- 资源管理器定位、复制物理路径、管理员身份打开、VS Code 打开、系统属性查看、BLAKE3 校验码计算。
- 自定义动作 GUI 编辑表单，支持宏替换变量与管理员提权。

---

## 支柱三：原生磁盘恢复与数据救援中枢 (Disk & Data Recovery Hub)

面向 AI 时代的高频数据丢失（代码误清空、模型权重误删、Git 误 reset、构建缓存误伤），提供原生高效的灾难抢救通道：

### 1. NTFS MFT 裸盘软删除秒级抢救 (MFT Undelete)
- 直接复用 `mft_scanner` 的底层裸盘流，解析未分配记录中的 `$FILE_NAME` 与 `$DATA` 属性；
- 1~3 秒内列出最近误删文件并提取物理数据运行簇链 (Data Run)，免漫长全盘扫描。

### 2. Windows 卷影副本快照回溯 (Volume Shadow Copy / VSS)
- 调用 Windows 底层 VSS 接口列出历史快照与系统还原点；
- 将卷影副本挂载为只读符号设备，秒级提取被意外覆盖的文件历史版本。

### 3. AI 与工程特征头签名雕刻 (File Carving)
- 针对跨卷格式化或 MFT 损坏灾难，扫描未分配簇，按 Magic Bytes 雕刻恢复 Python/Notebook/Safetensors/JSON/SQLite/PNG 等核心资产。

### 4. 只读安全挂载屏障
- 恢复全流程强制以 `GENERIC_READ` 模式只读挂接，绝不在源盘写入任何文件，杜绝二次数据覆盖。

---

## 全天候智能空间护航与自愈守护底座 (Intelligent Guard & Daemon)

### 1. 全屏独占与游戏免打扰感知
- 调用 Win32 `SHQueryUserNotificationState`，在用户处于全屏应用、DirectX 独占游戏或 PPT 演示放映时自动静默所有弹窗通知。

### 2. 键鼠空闲调度
- 基于 Win32 `GetLastInputInfo` 毫秒级计算系统空闲时长，仅在用户离席超过 5 分钟后触发后台低优先级治理任务。

### 3. 时序空间消耗斜率预测
- 滑动窗口时序算法实时计算空间消耗速率 (MB/min)，在突发空间吞噬时推算耗尽倒计时并发出预警。

### 4. 轻量本地自愈规则引擎
- 内置紧急低容量回收站清空、空闲时系统临时垃圾收缩、超期云盘缓存自动脱水三级自愈管道，具备冷却时间防御与全屏避让拦截。
