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
   - **搬迁无损底线**：基于 Windows NTFS 原生 Directory Junction 技术与事务型暂存重命名，保持原始物理联接点不变，杜绝应用程序路径失效与文件损坏。
   - **应用缓存专清底线**：严格区分用户数据与离线缓存，坚决不清除 Cookie、登录凭据、聊天记录数据库与浏览器书签。

---

## 二、当前版本已交付稳定特性矩阵 (v0.1.1 Delivered Matrix)

| 模块名称 | 核心能力 | 本机实测检出 / 治理效果 | 架构与安全保障措施 |
| :--- | :--- | :--- | :--- |
| **空间健康体检与清理** | 系统垃圾、临时文件、开发包、数据库一站式聚合体检与一键治理 | **15.8 GB** 可治理资产 | 智能推荐勾选，多场景分级标签，防误删白名单机制 |
| **全盘交互式 Treemap 树图** | Windows 11 Fluent 2 亚克力玻璃拟态全盘空间占比拓扑透视 | 实时下钻与悬浮浮层 | 320px 专业视窗，颜色编码语义化绑定，双行属性检视条 |
| **重复文件多核流式查重** | 64 KB 自适应流式缓冲 + Rayon 工作窃取多核流式并行哈希 | 秒级完成海量重复候选归并 | 最短路径智选保留，I/O 系统调用开销锐减 87.5% |
| **注册表并发极速巡检与清理** | 预缓存 App Paths + 递归流式解析 + `std::thread::scope` 五线程并发 | 耗时从 3.27s 降至 **0.90s** (3.6x 提升) | 修复前自动导出时间戳 `.reg` 恢复备份，Rayon 并行批处理 |
| **目录事务型搬家 (Junction)** | C 盘大目录转移至大容量磁盘并建立虚拟联接，支持 1-Click 回滚 | 160MB 实测 2.1s 闭环完成 | 事务型暂存重命名 + 自动无损回滚 + `/J /DCOPY:DAT` 零缓存多线程 |
| **SQLite 数据库碎片收缩** | 飞书、Chrome、Cursor 等高频读写数据库 VACUUM 物理收缩 | 释放 4.05 GB 游离碎片 | 原生 `PRAGMA freelist_count` 与 WAL 日志智能安全避让 |
| **系统极客工具箱** | 开机启动项纳管、Docker 虚拟化专清、系统回收站清理、软件盘点 | 聚合全能系统治理 | 原生 Windows API 与轻量化注册表解析，无第三方运行库依赖 |

---

## 三、v0.2.0 里程碑四大核心支柱规划 (v0.2.0 Architecture Roadmap)

### 支柱 1：AI 开发者与高容量数字资产专属搬迁预设 (AI & High-Value Asset Presets)
- **HuggingFace 权重存储**：`%USERPROFILE%\.cache\huggingface\hub` (动辄 20GB - 100GB 大模型权重)。
- **Ollama 本地模型镜像**：`%USERPROFILE%\.ollama\models` (本地大模型镜像集中存储)。
- **PyTorch / TorchHub 预训练模型**：`%USERPROFILE%\.cache\torch\hub`。
- **Unity Hub 多版本引擎编辑器**：`C:\Program Files\Unity\Hub\Editor` (单个引擎 8GB - 20GB)。
- **Steam 游戏库与着色器缓存**：`C:\Program Files (x86)\Steam\steamapps\common` 与 `shadercache`。

### 支柱 2：注册表备份快照可视化时间轴与一键导入复原 (Registry Snapshot Timeline)
- **备份时间轴面板**：在注册表工作区直观呈现 `%TEMP%\cleanflow_registry_backups\` 下的历史备份列表、创建时间戳与受影响项数。
- **原生 1-Click 复原闭环**：前端点击“恢复该快照”，后端直接调用 `reg.exe import` 秒级完整写回，提供无懈可击的系统容灾体验。
- **资源管理器一键定位**：支持直接打开文件夹选中目标 `.reg` 文件，便于用户手动审核备份内容。

### 支柱 3：搬家前运行中进程互斥主动检测与温和接管 (Pre-Flight Mutual-Exclusion Inspector)
- **进程句柄检测**：在启动搬家前，自动扫描是否有进程正在占用源目录（如微信对应的 `WeChat.exe`, `xwechat.exe`，Android 对应的 `adb.exe`, `qemu-system-x86_64.exe`）。
- **友好交互指引**：主动列出占用进程名与 PID，提供“协助安全关闭进程并继续”或“暂不关闭取消操作”，提升迁移成功率与用户亲和度。

### 支柱 4：应用卸载深层残留猎手 (Residual Trace Hunter)
- **已卸载应用残留目录排查**：排查 `%LOCALAPPDATA%`, `%APPDATA%`, `%PROGRAMDATA%` 中主程序已被彻底删除的陈旧数据孤岛。
- **白名单机制**：内置严格系统服务与驱动级保护列表，确保深度清理零误伤。

---

## 四、实施排期与演进计划 (Phased Implementation Plan)

- **Phase 1 (v0.2.0-alpha)**: 扩展 AI / LLM / Steam 大资产专属搬迁预设与识别引擎。
- **Phase 2 (v0.2.0-beta)**: 落地注册表快照管理时间轴、1-Click 导入恢复 API 与前端视图联动。
- **Phase 3 (v0.2.0-rc)**: 集成搬迁前进程互斥主动检测与一键温和关闭工作流。
- **Phase 4 (v0.2.0-final)**: 全量测试验证、便携包与 Inno Setup 安装向导双轨自动化打包交付。
