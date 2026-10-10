# CleanFlow 大众化高频易用性专项研发计划与技术规范书
(Consumer Experience & Usability Blueprint)

---

## 1. 背景与核心目标

在吸收 Listary 与 fsearch 核心特性的过程中，我们明确了 CleanFlow 的终极定位：**面向普通大众用户的原生桌面中枢**。
普通大众用户不具备开发者和极客的命令行思维，存在三大不可逾越的体验痛点：
1. **拼音缩写依赖**：普通用户在中文 Windows 下寻找软件或文件时，习惯敲键盘打声母缩写（例如输入 `jsq` 找计算器、输入 `wz` 找王者或微信），纯字符匹配直接搜中文属于严重体验硬伤；
2. **拒绝记忆语法**：普通用户不会也不可能去记忆 `type:dir`、`ext:png` 或 `size:>100mb` 这类极客前缀，必须通过直观的可视化药丸按钮一键点击过滤；
3. **高频资产回溯**：用户经常需要重新打开 5 分钟前找过的文件，或重复上一次的搜索词，需要开箱即用的历史记忆。

本计划书定义了针对上述痛点的落地实现方案与排期。

---

## 2. 核心特性详细技术方案

### 2.1 汉字拼音与声母全拼检索引擎 (Pinyin Search Engine)

#### 技术方案选型
- **选型考量**：不依赖百兆级庞大外部数据文件，采用轻量紧凑的 Unicode 汉字转拼音映射表（内存占用控制在 `< 600KB`）。
- **数据结构与索引增强**：
  为每个 MFT 文件条目建立多维度匹配影子：
  ```rust
  pub struct PinyinNameShadow {
      pub original_name: String,      // 例如: "计算器.exe"
      pub pinyin_initials: String,     // 例如: "jsq.exe"
      pub pinyin_full: String,         // 例如: "jisuanqi.exe"
  }
  ```
- **匹配执行逻辑**：
  在 [src/fuzzy_matcher.rs](file:///C:/Users/EDY/.gemini/antigravity/scratch/devcleaner/src/fuzzy_matcher.rs) 中：
  1. 优先执行原始名称字符匹配；
  2. 若未命中且输入为全 ASCII 字母，则在 `pinyin_initials`（声母缩写）与 `pinyin_full`（全拼）上并行跑模糊匹配；
  3. 声母精确对齐赋予额外加权得分，确保输入 `jsq` 时 `计算器.exe` 稳居第一位。

---

### 2.2 可视化类型过滤药丸 (Visual Filter Chips)

#### 分类定义与扩展名宏映射表
后端在 [src/search_engine.rs](file:///C:/Users/EDY/.gemini/antigravity/scratch/devcleaner/src/search_engine.rs) 建立工业级扩展名映射表：

| 药丸标识 (Chip Key) | 中文标签 | 判定逻辑 / 涵盖扩展名集合 |
| :--- | :--- | :--- |
| `all` | 全部 | 不限类型 (默认状态) |
| `folder` | 文件夹 | 仅限目录 (`entry.is_dir == true`) |
| `doc` | 文档 | `doc, docx, pdf, txt, xlsx, xls, pptx, ppt, md, csv, rtf, epub` |
| `pic` | 图片 | `png, jpg, jpeg, gif, bmp, webp, svg, ico, psd, ai, tiff, raw` |
| `video` | 视频 | `mp4, mkv, avi, mov, wmv, flv, rmvb, webm, m4v` |
| `audio` | 音乐 | `mp3, wav, flac, aac, m4a, ogg, wma` |
| `archive` | 压缩包 | `zip, rar, 7z, tar, gz, bz2, iso, 7-zip` |
| `app` | 应用 | `exe, lnk, bat, cmd, msi` |

#### 前端交互与 Fluent UI 规范
- **布局位置**：在主界面搜索栏正下方、以及 Spotlight 悬浮窗输入框正下方，紧凑横向排布；
- **视觉风格**：采用 Windows 11 Fluent 药丸胶囊风格，未选中时半透明灰色边框，选中时 Fluent 主题色高亮（如 `#0078d4` 背景）；
- **响应机制**：用户点击任意药丸，无需重新向后端请求全量数据，前端直接联动或在下一次按键时带上 `category` 参数；
- **键盘快捷切换**：支持快捷键快速切换分类（如按 `Ctrl+1` 到 `Ctrl+8` 快速切换）。

---

### 2.3 历史记录与查询记忆流 (History & Query Memory)

#### 最近打开文件历史 (Recent Files)
- **持久化设计**：采用本地轻量 JSON 文件存储（位于工作区同级 `data/recent_files.json`）；
- **容量与淘汰策略**：免费版保留最近 30 项，Pro 版无限制，采用 LRU 淘汰机制；
- **空输入回退体验**：当用户刚打开 Spotlight 悬浮框且尚未输入任何文字时，列表默认不展示空白，而是直接展示最近打开的文件列表，支持一键回车直达。

#### 搜索词历史记忆 (Query Memory)
- **触发机制**：在搜索输入框为空时，用户按键盘 `Up Arrow` (上方向键) 自动填入最近一次搜索词，再次按键翻看历史搜索词，按 `Down Arrow` (下方向键) 向后回退。

---

### 2.4 Pro 版资产管理与高级配置 GUI

#### 目录收藏夹管理与短别名 (Favorites & Aliases)
- 在搜索结果卡片中提供加星标按钮，点击即可加入“常用收藏夹”；
- 允许用户为收藏目录指定 2-4 位简短别名（例如为 `D:\Code\Frontend\CleanFlow` 绑定别名 `cf`）；
- 用户在搜索框输入 `cf` 直接回车，即可瞬间在资源管理器或 VS Code 中打开该目录。

#### 自定义动作与排除规则可视化配置表单
- 在“设置”界面中提供专门的图形化列表；
- 用户无需修改任何配置文件，直接通过界面点击“添加动作”，输入动作名称、浏览选择 `.exe` 路径、选择适用文件类型；
- 提供一键添加排除目录按钮，直接在文件夹选择器中选取要屏蔽的路径。

---

## 3. 落地实施路线图与里程碑 (Roadmap Milestones)

```
================================================================================
                    CleanFlow 大众易用性落地推进甘特图
================================================================================

[Phase 2.1: 核心大众化体验冲刺] (即刻实施)
  Step 1: 引入轻量级拼音转换模块，升级 fuzzy_matcher.rs 支持声母与全拼检索
  Step 2: search_engine.rs 增加 Category Macro 映射，前端实现 Filter Chips 药丸栏
  Step 3: 实现搜索框上下键翻看历史检索词与最近打开文件持久化
  Step 4: cargo test 单元测试与端到端编译验证

[Phase 2.2: Pro 版资产管理与高级设置]
  Step 5: 目录收藏夹与短别名快速直达系统
  Step 6: 自定义动作与排除规则 GUI 可视化表单
  Step 7: 7 天试用流转体验链路闭环

[Phase 2.3: 商业化封装与发布]
  Step 8: Inno Setup 自动化打包制作独立离线安装程序
================================================================================
```
