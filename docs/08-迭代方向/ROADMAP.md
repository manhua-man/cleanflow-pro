# CleanFlow Pro 演进路线图与前沿技术规划 (Roadmap & Evolution)

本文档归档 CleanFlow Pro 的历史版本交付里程碑与下一阶段前沿架构演进路线。根目录 [ROADMAP.md](../../ROADMAP.md) 为其简要事实索引。

---

## 1. 历史版本里程碑总结

### v0.1.0 ~ v0.2.0：空间治理基座与界面收敛
- 完成 11 侧边栏到 4 大工作区的 Fluent Mica 界面收敛；
- 建立 NTFS Junction 跨盘搬迁、ReFS 块克隆去重、SQLite 物理 VACUUM 压缩底座；
- 建立系统临时、开发缓存、微信办公与主流浏览器专清管道。

### v0.4.0：毫秒秒搜中枢与 Listary Pro / fsearch 全面吸收
- 实现 NTFS MFT 裸盘流式直读与 USN Journal 增量监听；
- 建立多音字与双字母复合声母 (zh/ch/sh) 智能拼音检索引擎；
- 交付双击 Ctrl 底层钩子、Alt+Space Spotlight 全局悬浮窗、Quick Switch 对话框穿透跳转与智能动作中枢；
- 建立 78 项单元测试基准与商业授权分级。

### v0.4.5：系统深度存储诊断、云盘脱水与智能护航引擎
- **驱动存储池治理**：`pnputil /enum-drivers` 穿透比对与 `FileRepository` 废弃包安全卸载（实测匹配 1.34 GB+ 冗余驱动）；
- **系统休眠与保留存储**：`hiberfil.sys` 物理空间诊断与 `powercfg` 三档模式向导，Windows 11 保留存储注册表高精度诊断；
- **云端同步盘离线缓存脱水**：多源云盘本地同步根目录自动探测，基于微软官方 `cldapi.dll` 原生脱水本地物理扇区，100% 保持云端资产完好；
- **智能空间护航与自愈**：Win32 `SHQueryUserNotificationState` 全屏/游戏免打扰感知，`GetLastInputInfo` 键鼠空闲调度，时序滑动窗口 Burn-rate 斜率建模与耗尽倒计时预警，三级自愈规则引擎；
- 自动化测试扩充至 90 项（100% 全部通过），二进制大小 9.67 MB。

---

## 2. v0.5.0 及后续前沿演进规划 (Frontier Roadmap)

### 2.1 WSL2 / Hyper-V 虚拟硬盘 (.vhdx) 空间精简 (Virtual Disk Compaction)
- **痛点分析**：开发者长期使用 WSL2 Ubuntu 或 Docker Desktop 后，虚拟磁盘 `ext4.vhdx` 会不断膨胀至数十 GB，即便在 Linux 内删除文件，Windows 物理宿主机上的 `.vhdx` 文件也不会自动缩小。
- **技术突破规划**：
  - 扫描开发者的虚拟磁盘空洞与孤立 `.vhdx` 映射；
  - 集成安全的离线 `Compact-VHD` 物理游离页收缩向导，在保证虚拟镜像完整性的前提下瞬间释放数十 GB 宿主机空间。

### 2.2 高级搜索交互与虚拟数据表格体验 (fsearch 极致对齐)
- **痛点分析**：目前搜索结果列表支持正逆序排序，但在复杂工程检索场景下，用户期望多列任意排序与列宽调整。
- **技术突破规划**：
  - 纯 Rust / 极致轻量的前端虚拟数据表格，支持按多列（名称、路径、扩展名、大小、修改时间）平滑排序；
  - 引入列宽自由拖拽调整与本地持久化记忆；
  - 提供多级高级筛选器浮层（支持同时按大小区间、修改日期区间、属性组合等多维过滤）。
