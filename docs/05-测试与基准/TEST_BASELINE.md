# CleanFlow Pro 测试基线与性能实测数据 (Test & Benchmark Baseline)

本文档记录 CleanFlow Pro 自动化测试覆盖基线与在实际 Windows 11 x64 开发机上的真实物理性能评测指标。

---

## 1. 自动化测试基线看板

- **测试套件规模**：90 项单元测试
- **通过率**：**100% 全部通过** (90 passed, 0 failed, 0 ignored)
- **执行时间**：~32.05 秒（单机全量并发）
- **覆盖模块分布**：
  - `action_runner`: 7 项 (参数宏展开、命令切分、自定义动作生命周期等)
  - `block_clone`: 3 项 (跨卷校验、支持探测等)
  - `cloud_storage_audit`: 4 项 (同步根探测、物理大小穿透、脱水回退等)
  - `daemon_service`: 2 项 (后台服务状态与磁盘空间)
  - `duplicates`: 3 项 (BLAKE3 哈希、大文件分水岭去重等)
  - `exclusions`: 2 项 (内置规则与排除管理器生命周期)
  - `favorites`: 1 项 (收藏夹单例生命周期)
  - `fuzzy_matcher`: 3 项 (精准/前缀、子序列模糊、拼写容错)
  - `history`: 1 项 (最近文件与搜索词记录)
  - `hotkey_manager`: 2 项 (双击 Ctrl 间隔数学计算、服务初始化)
  - `icon_extractor`: 2 项 (无压缩 PNG 编码、图标缓存生命周期)
  - `intelligent_guard`: 3 项 (Burn-rate 预测斜率、稳态计算、护航引擎生命周期)
  - `launcher`: 4 项 (系统命令检测、网络直达、快速工具、空查询等)
  - `licensing`: 4 项 (设备指纹生成、社区版默认、试用流转、激活码校验)
  - `mft_scanner`: 3 项 (FILETIME 时间戳转换、卷枚举、路径树重建)
  - `migrator`: 3 项 (空闲状态、普通目录判定、Junction 创建与探测)
  - `pinyin_matcher`: 5 项 (拼音影子提取、复合声母归一化、多音字变体、综合评分等)
  - `process_lock`: 2 项 (运行进程映射、常见锁定进程检测)
  - `quick_switch`: 2 项 (前台对话框捕获、宽字符转换)
  - `registry`: 4 项 (问题哈希计算、死链目标提取、并发扫描、注册表备份回滚)
  - `rules`: 2 项 (环境变量路径解析、通配符段解析)
  - `search_engine`: 5 项 (查询解析、高级尺寸语法、引号分词、正则搜索、高优先级加权)
  - `search_index`: 1 项 (卷索引生命周期)
  - `startup`: 1 项 (自启动项枚举)
  - `system_storage_audit`: 5 项 (驱动版本比对、驱动分组归一化、oem*.inf 命名守卫、pnputil 模拟解析、休眠与保留存储状态)
  - `system_tools`: 1 项 (回收站统计)
  - `tray`: 1 项 (开机自启查询)
  - `trigram_indexer`: 2 项 (Trigram 索引生成与内存 Grep)
  - `usn_scanner`: 4 项 (USN 日志状态、设备路径格式化、变更类型与监听生命周期、混合大文件扫描)
  - `winapp2_engine` & `parser`: 6 项 (注册表探测、环境变量展开、规则解析、WinApp2 加载等)
  - `apps` & `docker`: 2 项 (安装应用检测、Docker 状态检测)

---

## 2. 物理机性能实测数据

评测环境：Windows 11 x64 (Core i7 / 32GB RAM / NVMe SSD)。

| 评测维度 | 测试场景与数据规模 | 实测结果 | 行业对比标杆 |
| :--- | :--- | :--- | :--- |
| **全盘 100MB+ 巨型资产遍历** | 1,000,000+ 文件元数据 | 耗时 **0.68 秒** | 优于 WinDirStat (45s+)，比肩 WizTree |
| **全盘首字母拼音检索** | 输入 `jsq` / `zhw` / `cq` | 响应时间 **< 15 毫秒** | 优于传统 Everything 字符子序列模式 |
| **虚拟视口渲染滚动** | 1,000 条搜索结果列表 | **60 fps** 惯性平滑滚动 | 消除传统网页 DOM 膨胀与卡顿 |
| **目录跨盘迁移 (Junction)** | 15.8 GB 真实开发/AI 资产 | 耗时 42 秒（robocopy /MT:16 /J） | 零报错，原应用透明无感访问 |
| **注册表扫描与备份** | 20,000+ 系统注册表键值 | 耗时 0.9 秒，自动生成带时间戳快照 | 100% 原生无损双击回滚 |
| **驱动存储池废弃包诊断** | 扫描 `pnputil` 与 `FileRepository` | 耗时 **0.3 秒**，匹配 1.34 GB+ 历史驱动 | 优于第三方粗暴物理删除 |
| **云盘脱水处理速度** | 微软官方 `cldapi.dll` | 单文件脱水 **< 5 毫秒** | 物理空间瞬时归零，云端资产完整 |
| **单文件发布体积** | Release 二进制 | **9.67 MB**（无须安装，解压即用） | 远小于 Electron 类软件 (150MB+) |
