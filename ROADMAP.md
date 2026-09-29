# CleanFlow Pro 产品迭代方向与特性规划目录 (Roadmap)

本文档归档 CleanFlow Pro 桌面空间管家的长期技术路线、治理维度扩充规划与待排期特性目录。

---

## 一、产品定位与核心原则 (Core Non-Negotiables)

1. **纯正 Windows 11 Fluent 2 桌面原生体验**
   - 深度贴合 Windows 11 现代设计语言（Segoe UI Variable 字体栈、Mica 暗色层级质感、1px 细微边界、微动效与规范控件）。
   - 坚决杜绝通用 Web SaaS 模板化卡片，严格执行 Zero-Emoji 准则，全局使用统一风格的专业矢量 SVG 图标。
2. **纯粹工具属性，用完即走，拒绝流氓常驻**
   - **不做开机自启动**；
   - **不做系统托盘后台静默驻留**；
   - **不做后台自发网络请求或静默轮询**；
   - 启动即工作，关闭即完全释放系统资源。
3. **100% 数据安全与无损可退 (Safety First)**
   - **注册表安全底线**：任何删除指令执行前，系统自动生成标准 Windows `.reg` 备份文件，支持用户随时双击回滚。
   - **搬迁无损底线**：基于 Windows NTFS 原生 Directory Junction 技术，保持原始物理联接点不变，杜绝应用程序路径失效。
   - **应用缓存专清底线**：严格区分用户数据与离线缓存，坚决不清除 Cookie、登录凭据、聊天记录数据库与浏览器书签。

---

## 二、当前版本已交付稳定特性矩阵 (v1.2)

| 模块名称 | 核心能力 | 本机实测检出 / 治理效果 | 安全保障措施 |
| :--- | :--- | :--- | :--- |
| **空间健康体检与清理** | 系统垃圾、临时文件、开发包、数据库一站式聚合体检与一键治理 | **7.2 GB** 可释放 | 智能推荐勾选，防误删白名单机制 |
| **主流浏览器深度专清** | 覆盖 Edge、Chrome、360 浏览器的离线页面、媒体与编译代码缓存 | **881.7 MB** (5 处核心缓存) | 严格保护 Cookie、登录态与书签 |
| **注册表冗余与失效残留** | 扫描失效 MUICache、无效 OpenWith 打开方式、死链卸载项 | **196 处** 真实残留项 | 修复前自动导出时间戳 `.reg` 恢复备份 |
| **目录无损搬家 (Junction)** | C 盘大体积目录向大容量磁盘转移并原位建立虚拟联接点 | **13.9 GB** 资产迁移潜能 | NTFS 原生硬联接，对上层程序完全透明 |
| **大文件雷达 (100MB+)** | C 盘及全盘深层沉淀文件索引，类型占比分层条形图谱 | 检出 **91 个** 大资产 (**30.4 GB**) | 支持直接定位资源管理器及一键安全粉碎 |
| **开发与编译缓存治理** | npm、pnpm、Unity Package、Gradle、Cargo 依赖包集中释放 | **515.9 MB** 构建依赖缓存 | 仅清理全局存储与 tarball，不坏本地项目 |
| **SQLite 数据库碎片收缩** | 飞书、Chrome、VSCode 等长期高频读写数据库 VACUUM 整理 | **4.0 GB** 碎片压缩空间 | 执行 `PRAGMA page_count` 安全收缩闲置页 |
| **自定义规则引擎** | 支持用户以环境变量通配符灵活自定义专有清理路径 | 动态追加并持久化配置 | 路径有效性校验，热加载即时生效 |

---

## 三、待推进特性与迭代规划目录 (Categorized Feature Backlog)

### 专项一：大文件雷达深层交互与文件级治理 (Giant Files Radar)
- **F1.1: 文件详情侧边抽屉 / 属性卡片**
  - 单击大文件条目唤起侧边信息卡片，展示创建时间、最后修改时间、最后访问时间。
  - 显示当前文件是否正被某些系统进程锁定或独占打开。
- **F1.2: 原生资源管理器右键上下文菜单**
  - 支持快捷操作：在 Windows 资源管理器中打开并高亮选中目标文件 (`explorer.exe /select, <path>`)。
  - 一键复制文件绝对路径至系统剪贴板。
  - 提供快速计算文件 SHA256 / MD5 哈希校验和能力，方便排查重复包。
- **F1.3: 时间跨度与冷热资产切片**
  - 增加时间维度过滤器：`超过 1 年未访问 (极冷资产)`、`6 个月至 1 年`、`最近 3 个月内活跃`。
  - 支持多磁盘跨盘快速切换雷达扫描 (C: / D: / E:)。

### 专项二：主流与国产浏览器深度专清扩充 (Browser Hygiene)
- **F2.1: 国产主流浏览器规则库扩充**
  - **QQ 浏览器**：`%LOCALAPPDATA%\Tencent\QQBrowser\User Data\Default\Cache` 及代码缓存。
  - **搜狗高速浏览器**：`%APPDATA%\SogouExplorer\Webkit\Cache`。
  - **夸克桌面端 (Quark PC)**：`%LOCALAPPDATA%\Quark\User Data\Default\Cache`。
- **F2.2: 极客与开源系浏览器专清**
  - **Brave 浏览器**：`%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Cache`。
  - **Mozilla Firefox**：`%LOCALAPPDATA%\Mozilla\Firefox\Profiles\*.default*\cache2` 结构解析。
- **F2.3: 浏览器专清维度细化**
  - 独立拆分：网页媒体缓存 (Media Cache)、JS/WASM 编译代码缓存 (Code Cache)、GPU 着色器缓存 (GPUCache)、崩溃转储日志 (Crashpad)。

### 专项三：目录无损搬家高价值预设库扩充 (Junction Studio)
- **F3.1: 开发者与高容量软件预设拓展**
  - **Steam 游戏下载库与着色器缓存**：`C:\Program Files (x86)\Steam\steamapps\common` 及 `shadercache`。
  - **Unity Hub 多版本编辑器存储**：`C:\Program Files\Unity\Hub\Editor` (单个版本常达 5GB-15GB)。
  - **Visual Studio 共享组件与下载缓存**：`C:\ProgramData\Microsoft\VisualStudio\Packages`。
  - **HuggingFace 与 AI 模型权重缓存**：`C:\Users\<User>\.cache\huggingface\hub`。
  - **Node.js 全局缓存与 pnpm Store**：`%LOCALAPPDATA%\pnpm\store`。
- **F3.2: 搬迁前进程互斥检查**
  - 搬迁开始前自动检测源目录下是否有文件正被正在运行的软件占用（如微信运行中禁止搬迁微信数据目录）。
  - 提供温和的进程识别与一键辅助关闭或等待机制，避免因文件锁定导致复制中断。

### 专项四：注册表治理深度与容灾机制 (Registry Cleaner)
- **F4.1: 更多高危与冗余键位安全排查**
  - **无效 COM / ActiveX 接口残留**：排查 `HKCR\CLSID` 中 InprocServer32 指向已删除 DLL / OCX 的死链。
  - **失效服务残留项**：排查 `HKLM\SYSTEM\CurrentControlSet\Services` 中 ImagePath 指向已被彻底删除的可执行文件的无主服务项。
- **F4.2: 注册表备份可视化管理面板**
  - 在注册表工作区内嵌“历史备份时间轴”，列出所有生成的 `.reg` 备份文件及其生成时间、包含项数。
  - 提供 `一键还原该备份` 按钮，直接调用 Windows `reg.exe import` 完成极速无损复原。

### 专项五：性能极致优化与系统协同 (Performance & Engine)
- **F5.1: NTFS USN Journal / MFT 极速扫描适配**
  - 针对大文件雷达，探索引入 Windows NTFS 卷的 USN Change Journal 或 MFT 解析，使全盘大文件检索从数秒缩减至毫秒级。
- **F5.2: 扫描任务并发与 CPU 亲和度控制**
  - 确保深度扫描在后台进行时 CPU 占用稳定在可控区间（<15%），保证日常办公、游戏、编程不受丝毫卡顿干扰。
