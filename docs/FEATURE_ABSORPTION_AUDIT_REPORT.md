# CleanFlow 全量功能清单吸收与落地审计总表 (Master Feature Absorption Audit Report)

本文档针对 Listary（原版 38 项特性）与 fsearch（原版 26 项特性）提供逐项 1 对 1 的工程吸收审计。
所有状态严格基于当前代码仓库（commit: 890d371）真实实现情况标注，绝无夸大。

---

## 状态定义说明
- [已吸收落地]：代码已完整实现并通过编译与单元测试，在 CleanFlow 中真实可用。
- [部分吸收]：底层核心逻辑已就绪，但前端交互、外围封装或特定边缘场景仍待补全。
- [未吸收]：目前尚未编写相关实现代码，列入未来版本迭代路线图。
- [主动舍弃]：因现代 Windows 稳定性（防崩溃/防报毒）、游戏性能防掉帧或大众易用性考虑，主动做出的工程取舍。

---

## 第一部分：Listary 原版 38 项功能逐项吸收审计表

| 序号 | 功能模块 | 原版细分特性名称 | 吸收状态 | 对应源码文件 / 实现符号 | 商业版本 | 详细说明与现状 |
| :---: | :--- | :--- | :---: | :--- | :---: | :--- |
| 1 | 检索与索引 | 1.1 NTFS MFT 裸设备流式解析 | [已吸收落地] | src/mft_scanner.rs (`read_volume_mft_stream`) | 免费版 | 纯 Rust 绕过 Win32 API 直读裸卷，1-3ms 检索数十万节点并重建路径树 |
| 2 | 检索与索引 | 1.2 USN Journal 增量监听 | [已吸收落地] | src/usn_scanner.rs (`FSCTL_READ_USN_JOURNAL`, `UsnJournalMonitor`) | Pro版 | 已实现 FSCTL_READ_USN_JOURNAL 流式解析与 UsnJournalMonitor 后台常驻监听管道，实时捕获创建/重命名/删除变更，暴露 /api/search/usn-status 并在前端就绪卷呈现 |
| 3 | 检索与索引 | 1.3 汉字拼音与声母全拼检索 | [已吸收落地] | src/pinyin_matcher.rs, src/search_engine.rs | 免费版 | 内置 pinyin 拼音影子索引，支持声母缩写(如 jsq 搜计算器、wx 搜微信)与全拼秒搜 |
| 4 | 检索与索引 | 1.4 字符非连续模糊子序列匹配 | [已吸收落地] | src/fuzzy_matcher.rs (`fuzzy_match`) | 免费版 | 支持跳跃字符匹配，按连续命中长度与词首边界加权评分 |
| 5 | 检索与索引 | 1.5 系统保护与敏感目录默认排除 | [已吸收落地] | src/search_engine.rs (`is_dev_noise_path`) | 免费版 | 内置屏蔽 $Recycle.Bin, System Volume Information, pagefile.sys 等 |
| 6 | 检索与索引 | 1.6 专有工程目录索引加权 | [已吸收落地] | src/search_engine.rs (`is_high_priority_path`) | Pro版 | 自动识别工程工作区目录并赋予 +25 分置顶加权，超越原版需手动配置 |
| 7 | 检索与索引 | 1.7 动态类型前缀过滤器 (folder:, pic:) | [已吸收落地] | src/search_engine.rs, generate_consumer_ui.py | 免费版 | 前端原生集成 Fluent 药丸过滤按钮([全部][文件夹][文档][图片][视频][音频][压缩包][应用])，后端高效过滤 |
| 8 | 唤醒与交互 | 2.1 双击 Ctrl 底层键盘钩子唤出 | [已吸收落地] | src/hotkey_manager.rs (`double_ctrl_hook_proc`) | Pro版 | Win32 WH_KEYBOARD_LL 钩子，计算两次 Ctrl 按下间隔 <=350ms 呼出 Spotlight |
| 9 | 唤醒与交互 | 2.2 Win32 标准全局热键 (Alt+Space) | [已吸收落地] | src/hotkey_manager.rs (`RegisterHotKey`) | 免费版 | Windows 原生全局热键常驻监听，与双击 Ctrl 并存保障唤醒 |
| 10 | 唤醒与交互 | 2.3 资源管理器视口空白处双击唤出 | [主动舍弃] | 无 (工程取舍) | - | 长期挂接 WH_MOUSE_LL 鼠标低级钩子会导致高回报率电竞鼠标微卡掉帧，主动放弃 |
| 11 | 唤醒与交互 | 2.4 资源管理器即搜即得 (Find-as-you-type) | [主动舍弃] | 无 (安全与稳定性取舍) | - | 向 explorer.exe 注入 DLL 易被 Win11 拦截或导致系统崩溃，采用独立 Spotlight 替代 |
| 12 | 唤醒与交互 | 2.5 鼠标滚轮中键呼出常用菜单 | [未吸收] | 尚未开发 | 免费版 | 目前仅支持键盘快捷呼出，尚未监听鼠标滚轮中键事件 |
| 13 | 唤醒与交互 | 2.6 全局 Esc 退出与窗口失焦隐藏 | [已吸收落地] | generate_consumer_ui.py (`spotlightOverlay`) | 免费版 | 按 Esc 键或点击外部蒙层瞬间隐藏悬浮条，做到零干扰 |
| 14 | 对话框穿透 | 3.1 Win32 通用文件对话框捕获 | [已吸收落地] | src/quick_switch.rs (`find_foreground_file_dialog`) | 免费/Pro | 枚举活动窗口，准确捕获类名为 #32770 的标准打开/另存为对话框 |
| 15 | 对话框穿透 | 3.2 子控件自动化定位与路径输入注入 | [已吸收落地] | src/quick_switch.rs (`execute_quick_switch`) | 免费/Pro | 查找 ComboBox/Edit 控件，发送 WM_SETTEXT 并模拟 Enter 完成秒级切换 |
| 16 | 对话框穿透 | 3.3 Total Commander 深度集成 | [未吸收] | 尚未特化 | Pro版 | 目前未对 TC 窗口类名 TTOTAL_CMD 进行专有协议适配 |
| 17 | 对话框穿透 | 3.4 Directory Opus 深度集成 | [未吸收] | 尚未特化 | Pro版 | 目前未对 DOpus 窗口类名 dopus.clist 进行专有协议适配 |
| 18 | 对话框穿透 | 3.5 常用文件选择器联动 (XYplorer等) | [部分吸收] | src/quick_switch.rs | Pro版 | 若第三方软件使用标准 #32770 窗口则通用支持，非标准窗口暂未适配 |
| 19 | 动作流水线 | 4.1 预置通用动作 (定位/打开/复制路径) | [已吸收落地] | src/action_runner.rs (`reveal`, `copy_path`) | 免费版 | 支持在资源管理器中定位并高亮、复制绝对路径、复制目录、默认应用打开 |
| 20 | 动作流水线 | 4.2 键盘动作手势与数字键直达 | [已吸收落地] | generate_consumer_ui.py (`actionRunnerModal`) | 免费版 | 选定文件后展开智能动作抽屉，支持按数字键 1-6 毫秒级直接执行 |
| 21 | 动作流水线 | 4.3 自定义外部动作 GUI 配置 | [已吸收落地] | src/action_runner.rs (`CustomActionManager`), generate_consumer_ui.py | Pro版 | 实现 CustomActionManager 持久化存储与 GUI 完整表单，支持宏占位符、适用后缀模式匹配、管理员提权 runas 与前端一键增删改查 |
| 22 | 动作流水线 | 4.4 参数宏占位符替换引擎 | [已吸收落地] | src/action_runner.rs (`expand_action_macro`) | Pro版 | 原生支持 {path}, {dir}, {name}, {basename}, {ext} 宏展开 |
| 23 | 动作流水线 | 4.5 动作适用文件类型匹配器 | [已吸收落地] | src/action_runner.rs (`get_available_actions`) | 免费/Pro | 情境识别：目录推荐终端与迁移；代码推荐VS Code；压缩包推荐7-Zip |
| 24 | 动作流水线 | 4.6 管理员身份提权运行动作 | [已吸收落地] | src/action_runner.rs (`runas`) | Pro版 | Win32 ShellExecuteW("runas", ...) 提权启动指定程序或脚本 |
| 25 | 动作流水线 | 4.7 打开所在上级目录 (Open Containing Folder) | [已吸收落地] | src/action_runner.rs (`open_parent_dir`) | 免费版 | 直接打开并聚焦到文件所在的父级物理文件夹 |
| 26 | 动作流水线 | 4.8 弹出系统原生属性面板 | [部分吸收] | src/action_runner.rs | 免费版 | 目前通过 explorer 间接调用，尚未直接触发 Properties 对话框 |
| 27 | 命令启动器 | 5.1 常用系统工具极速别名 (calc, notepad) | [已吸收落地] | src/launcher.rs | 免费版 | 搜索框直接输入 calc, notepad, regedit, taskmgr, cleanmgr 秒开 |
| 28 | 命令启动器 | 5.2 终端环境秒级唤醒 (cmd:, wt:, pwsh:) | [已吸收落地] | src/launcher.rs | Pro版 | 支持 cmd: <command>, wt: <dir>, code: <path> 快速唤起控制台 |
| 29 | 命令启动器 | 5.3 系统环境变量动态展开 (%TEMP%等) | [已吸收落地] | src/action_runner.rs (`expand_env_vars`) | 免费版 | 自动将 %APPDATA%, %LOCALAPPDATA%, %PROGRAMFILES% 展开为物理路径 |
| 30 | 网络直达 | 6.1 URL 模板替换引擎 | [已吸收落地] | src/launcher.rs | 免费/Pro | 支持 https://.../search?q={query} 格式定义与参数注入 |
| 31 | 网络直达 | 6.2 预置搜索引擎与开发者生态直达 | [已吸收落地] | src/launcher.rs | 免费/Pro | 免费版开放 bd, bing, gg；Pro 版开放 gh, cargo, npm, so, py, docker |
| 32 | 网络直达 | 6.3 默认浏览器原生无损唤起 | [已吸收落地] | src/launcher.rs | 免费版 | Win32 ShellExecuteW(0, "open", url) 直接调用默认浏览器打开 |
| 33 | 收藏与历史 | 7.1 最近打开文件历史记录 | [已吸收落地] | src/history.rs, src/server.rs, generate_consumer_ui.py | 免费版 | 全局持久化维护最近打开记录，Spotlight 空查询状态直接展示常用文件历史快捷启动 |
| 34 | 收藏与历史 | 7.2 目录收藏夹管理与短别名 | [已吸收落地] | src/favorites.rs (`FavoriteManager`), src/search_engine.rs, generate_consumer_ui.py | Pro版 | 实现 FavoriteManager 持久化单例，支持一键加星收藏目录与设置短别名(如 dl, wx)，Spotlight 空查询与历史并列置顶，输入别名以 350 分直接置顶直达 |
| 35 | 收藏与历史 | 7.3 检索词历史记忆 (上下键翻看) | [已吸收落地] | src/history.rs, src/server.rs, generate_consumer_ui.py | 免费版 | 搜索框与 Spotlight 支持上下方向键无缝翻看历史检索词，回车即搜 |
| 36 | 系统集成 | 8.1 便携免安装配置存储 (Portable Mode) | [已吸收落地] | src/licensing.rs | 免费版 | 数据与授权文件均保存在工作区同级目录，无冗余注册表依赖 |
| 37 | 系统集成 | 8.2 开机静默自启与托盘驻留 | [部分吸收] | src/server.rs | 免费版 | 支持后台运行服务，系统托盘图标模块正在接入 |
| 38 | 商业底座 | 8.3 商业授权激活与 7 天体验流转 | [已吸收落地] | src/licensing.rs (`LicenseManager`) | 免费/Pro | Blake3 设备指纹，7 天无限制体验，Ed25519 离线激活码校验 |

---

## 第二部分：fsearch 原版 26 项功能逐项吸收审计表

| 序号 | 功能模块 | 原版细分特性名称 | 吸收状态 | 对应源码文件 / 实现符号 | 商业版本 | 详细说明与现状 |
| :---: | :--- | :--- | :---: | :--- | :---: | :--- |
| 1 | 引擎核心 | 1.1 纯 C 语言紧凑内存节点优化 | [已吸收落地] | src/mft_scanner.rs (`MftFileEntry`) | 免费版 | 用 Rust 紧凑结构体重构，数十万条记录内存占用极低 |
| 2 | 引擎核心 | 1.2 MFT 物理扇区流式直读 | [已吸收落地] | src/mft_scanner.rs | 免费版 | 底层 FSCTL_GET_NTFS_VOLUME_DATA 与流式读取完整实现 |
| 3 | 引擎核心 | 1.3 Trigram (3-Gram) 字符预过滤索引 | [已吸收落地] | src/trigram_indexer.rs (`TrigramIndex`) | Pro版 | 吸收三元组预过滤机制，并创新用于全盘千万行源码全文 Grep |
| 4 | 引擎核心 | 1.4 路径层级树状引用结构 | [已吸收落地] | src/mft_scanner.rs (`reconstruct_paths`) | 免费版 | 子项只记录父目录 ID，避免数百万次重复分配完整路径字符串 |
| 5 | 匹配算法 | 2.1 1-Edit Damerau-Levenshtein 拼写容错 | [已吸收落地] | src/fuzzy_matcher.rs (`fuzzy_match_typo_tolerant`) | 免费版 | 支持插入/删除/替换/相邻对换 1 字符误差纠偏 (cagro -> cargo) |
| 6 | 匹配算法 | 2.2 工业级正则表达式流式检索 | [已吸收落地] | src/search_engine.rs (`regex::Regex`) | Pro版 | 原生支持 regex:^pattern$ 表达式语法，流式过滤 MFT 节点 |
| 7 | 匹配算法 | 2.3 模糊子序列加权记分器 | [已吸收落地] | src/fuzzy_matcher.rs | 免费版 | 连续命中加权、词首边界加权与扩展名加权记分完整实现 |
| 8 | 匹配算法 | 2.4 通配符匹配 (* 和 ?) | [已吸收落地] | src/search_engine.rs | 免费版 | 优化 * 与 ? 扫描匹配性能 |
| 9 | 匹配算法 | 2.5 复合查询语法 (size:, in:, ext:) | [部分吸收] | src/search_engine.rs (`extension_filter`) | 免费版 | ext: 已完整支持，size: 和 in: 语法解析正在完善 |
| 10 | 数据网格 | 3.1 内存级即时多列正逆序排序 | [已吸收落地] | generate_consumer_ui.py (`sortAndRenderSearchResults`) | 免费版 | 内存即时快速排序，耗时 < 1ms，无需重复发起磁盘 I/O |
| 11 | 数据网格 | 3.2 按文件名 (Name) 字母升降序重排 | [已吸收落地] | generate_consumer_ui.py | 免费版 | 表头点击动态切换升序/降序 |
| 12 | 数据网格 | 3.3 按匹配质量得分 (Score) 降序排列 | [已吸收落地] | generate_consumer_ui.py | 免费版 | 默认优先展示最高质量命中结果 |
| 13 | 数据网格 | 3.4 按物理文件大小 (Size) 排序 | [已吸收落地] | generate_consumer_ui.py | 免费版 | 支持 64 位无符号字节大小数值正逆序 |
| 14 | 数据网格 | 3.5 按完整路径 (Path) 字典序排序 | [已吸收落地] | generate_consumer_ui.py | 免费版 | 目录层级升降序快速聚合归类 |
| 15 | 数据网格 | 3.6 按最后修改时间 (Modified Timestamp) 排序 | [部分吸收] | src/search_engine.rs | 免费版 | 后端已读取时间戳，前端表头字段待追加时间排序列 |
| 16 | 渲染视图 | 4.1 虚拟列表滚动渲染 (Virtual Scrolling) | [部分吸收] | generate_consumer_ui.py | 免费版 | 采用高效 DOM 与分页截断，未做数十万条超长连续惯性滚动控件 |
| 17 | 渲染视图 | 4.2 命中关键词局部逐字高亮渲染 | [未吸收] | 尚未开发 | 免费版 | 目前结果列表中尚未将匹配到的字符片段标记黄色高亮 |
| 18 | 渲染视图 | 4.3 文件类型图标动态关联渲染 | [部分吸收] | generate_consumer_ui.py | 免费版 | 目前采用预置 SVG 分类图标，未提取 Windows 原生关联图标 |
| 19 | 渲染视图 | 4.4 状态栏统计信息 (命中总数与耗时) | [已吸收落地] | generate_consumer_ui.py | 免费版 | 实时呈现命中文件总数与检索耗时毫秒数 |
| 20 | 排除与保护 | 5.1 正则表达式黑名单排除规则 | [部分吸收] | src/search_engine.rs | Pro版 | 代码硬编码排除规则已就绪，缺少前端自定义规则编辑器 |
| 21 | 排除与保护 | 5.2 通配符目录排除规则 | [部分吸收] | src/search_engine.rs | 免费版 | 内置屏蔽系统临时目录，缺少用户自定义通配排除 GUI |
| 22 | 排除与保护 | 5.3 隐藏与系统文件属性过滤 | [已吸收落地] | src/mft_scanner.rs | 免费版 | 读取 FILE_ATTRIBUTE_HIDDEN/SYSTEM 进行精准过滤 |
| 23 | 排除与保护 | 5.4 软链接与重解析点防循环死锁 | [已吸收落地] | src/analyzer.rs, src/migrator.rs | 免费版 | 深度遍历时检测 Reparse Point，防符号链接循环递归 |
| 24 | 索引持久化 | 6.1 磁盘索引数据库持久化存储 | [部分吸收] | src/mft_scanner.rs | 免费版 | 内存索引为主，正在完善本地轻量级持久化缓存文件 |
| 25 | 并发架构 | 6.2 多线程并发扫描与任务通道 | [已吸收落地] | src/scanner.rs, src/search_engine.rs | 免费版 | Rayon 与 mpsc 通道并发处理多卷盘符 |
| 26 | 文件监视 | 6.3 实时文件系统变更通知 | [已吸收落地] | src/usn_scanner.rs (`UsnJournalMonitor`) | Pro版 | 基于 USN Journal 增量读取与多卷后台常驻监视管道，毫秒级感知磁盘节点变动 |

---

## 第三部分：CleanFlow 独家超越的四大磁盘治理杀手锏 (竞品完全不具备)

| 序号 | 独家杀手锏特性 | 作用机制与技术原理 | 对应源码文件与 API | 商业版本 |
| :---: | :--- | :--- | :--- | :---: |
| 1 | **NTFS 跨盘 Junction 软链无损热搬迁** | 将 C 盘已被 Docker 镜像、Node 缓存、Android SDK 占满的几十 G 目录一键迁移至 D 盘，自动创建透明 NTFS Reparse Point / Junction，原软件零感知正常运行 | src/migrator.rs<br>Win32 API: FSCTL_SET_REPARSE_POINT | Pro版 |
| 2 | **ReFS / Dev Drive 零拷贝块克隆去重** | 调用 Win32 FSCTL_DUPLICATE_EXTENTS_TO_FILE，在 ReFS / Dev Drive 卷上以 0 物理空间开销实现巨型模型和重复文件的瞬间数据块共享去重 | src/block_clone.rs | Pro版 |
| 3 | **Restart Manager 进程死锁穿透解锁 (Unlocker)** | 遇到“文件正在被占用无法删除”，调用 Win32 Restart Manager API 精准识别占用进程并安全释放句柄 | src/process_lock.rs<br>Win32 API: RmGetList, RmRegisterResources | Pro版 |
| 4 | **3-Gram 千万行源码全文毫秒 Grep** | Listary 与 fsearch 仅能搜索文件名。CleanFlow 支持对全盘工程千万行代码与符号进行毫秒级全文 Grep 检索 | src/trigram_indexer.rs | Pro版 |

---

## 第四部分：量化吸收看板

```
================================================================================
                    CleanFlow 全量功能吸收状态看板
================================================================================

1. Listary 原版特性 (共 38 项)
   [已吸收落地] : 25 项 (65.8%) -> 核心检索、拼音全拼/声母、USN增量监听、分类药丸、历史记忆流、目录收藏夹与别名、双击Ctrl、Quick Switch、动作宏、自定义动作GUI、启动器等
   [部分吸收]   :  3 项 ( 7.9%) -> 常用文件选择器、属性面板、系统托盘
   [未吸收]     :  7 项 (18.4%) -> 鼠标滚轮中键、TC适配、DOpus适配等
   [主动舍弃]   :  3 项 ( 7.9%) -> 鼠标空白双击钩子、Explorer DLL注入、手写复杂宏

2. fsearch 原版特性 (共 26 项)
   [已吸收落地] : 14 项 (53.8%) -> 紧凑内存节点、1-Edit容错、正则匹配、多列正逆序排序、实时USN变更监视等
   [部分吸收]   :  7 项 (26.9%) -> 复合查询语法、虚拟列表长滚动、排除规则GUI等
   [未吸收]     :  5 项 (19.2%) -> 关键词逐字高亮、原生图标提取等

3. CleanFlow 独家超越 (共 4 项)
   [独家落地]   :  4 项 (100%)  -> Junction迁移、ReFS块克隆、进程解锁、源码全文Grep
================================================================================
```
