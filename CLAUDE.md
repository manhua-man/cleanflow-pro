# CleanFlow Pro 开发者与协作守则 (Protocol & Rules)

本文档定义了 CleanFlow Pro 项目的核心工程法则、决策框架、安全底线与编码约束。所有人类开发者与 AI 协作代理必须严格遵循本守则。

---

## 1. 核心工程哲学

1. **增量推进 (Incremental Progress)**：优先采用小步快跑、随时可测、随时可审查的原子式变更，坚决杜绝高风险的大规模盲目重构。
2. **上下文至上 (Context is King)**：编写任何新代码前，必须先通读现有模块架构、设计模式与调用约定。
3. **清晰优于取巧 (Clarity Over Cleverness)**：代码结构直观、易读，坚决避免晦涩的黑魔法。
4. **如无必要勿增实体 (YAGNI & Simplicity)**：杜绝过早抽象，每个函数与模块只做一件事并做到极致。

---

## 2. 决策优先级框架 (Decision Priority)

当面临多种技术实现方案时，严格按以下优先级排序裁决：

1. **可测性 (Testability)**：方案是否易于编写高可靠的自动化测试？
2. **可读性 (Readability)**：六个月后其他开发者是否能轻松理解？
3. **一致性 (Consistency)**：是否与现有 Rust/Win32 模式保持统一？
4. **简单性 (Simplicity)**：是否是满足需求的最简方案？
5. **可逆性 (Reversibility)**：未来推翻或变更该决策的成本有多大？

---

## 3. 不可逾越的安全与规范底线 (Safety Sentinels)

### 3.1 100% 绝对零 Emoji 铁律 (Strict Zero-Emoji Rule)
- **全局铁律**：严禁在源代码、代码注释、文档、控制台输出、API 响应、UI 界面文本及 Git Commit 信息中出现任何 Emoji 表情字符。
- 界面图标一律采用统一风格的高清矢量 SVG 图标。

### 3.2 资产与系统安全底线 (Safety First)
1. **云端资产绝对安全**：
   - 治理 OneDrive、iCloud、坚果云等按需同步盘时，严禁调用任何物理删除指令（如 `fs::remove_file`）；
   - 必须通过微软官方 Cloud Filter 库 (`cldapi.dll`) 执行 `CfDehydratePlaceholder` 原生脱水，本地释放扇区为 0 字节占位符，云端数据 100% 完好。
2. **驱动存储池安全保护**：
   - 严禁对 `C:\Windows\System32\DriverStore\FileRepository` 执行粗暴的物理文件删除；
   - 必须先做多版本归一化比对，验证 `oem*.inf` 命名规范，通过 Windows 官方受保护的 `pnputil /delete-driver` 管道执行卸载。
3. **注册表无损备份底线**：
   - 任何注册表修复或清理前，必须自动生成带高精度时间戳的标准 Windows `.reg` 备份快照文件，支持用户随时双击回滚。
4. **目录搬家无损可逆底线**：
   - 基于 Windows NTFS 原生 Directory Junction 技术与互斥进程锁预检 (`process_lock.rs`)；
   - 搬迁前检测锁闭进程并告警，保持原始物理联接点不变，杜绝应用程序路径失效与文件损坏。
5. **用户数据专清底线**：
   - 严格区分用户数据与离线缓存，坚决不清除 Cookie、登录凭据、聊天记录数据库与浏览器书签。

### 3.3 绿色便携与零常驻侵占
- 坚持单文件便携绿色架构（二进制体积控制在 ~9.6 MB，解压即用）；
- 零外部运行时依赖（无需 Node.js / Python / WebView2 运行时）；
- 托盘常驻与全局热键为完全可配置选项，空闲时 0% CPU 占用与零网络活动；退出时干净彻底释放 Win32 系统资源。

---

## 4. 编码与验证规范

1. **Rust 语言与规范**：遵循 Rust 2021 Edition 惯用规范，通过 Clippy 与 Formatter 静态检查。
2. **测试是硬约束 (Tests are Non-Negotiable)**：
   - 所有新增功能必须配备完备的单元测试；
   - 任何代码变更后，必须执行 `cargo test` 确保全量 90 项测试 100% 全部通过；
   - 若发现测试失败，必须修复代码或测试，严禁直接注释或跳过测试。
3. **单源真值**：系统事实、版本号、模块路径与命令参考见 [AGENTS.md](AGENTS.md)。
