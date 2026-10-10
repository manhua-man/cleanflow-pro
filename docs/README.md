# CleanFlow Pro 文档导航总控 (Documentation Hub)

欢迎查阅 CleanFlow Pro (净流) 系统技术与工程文档。本文档遵循工程治理标准，采用“业务域空间正交 + 时间生命周期隔离”的分层结构维护。

AI 协作法则与不可变事实请参阅根目录：
- 协作法则与安全底线：[CLAUDE.md](../CLAUDE.md)
- 系统单源真值与模块地图：[AGENTS.md](../AGENTS.md)
- 根目录发版说明：[README.md](../README.md)

---

## 目录路由与文档导航

```text
docs/
├── README.md                           # 本文件：导航总控与拓扑路由
├── 01-规范标准/                        # 业务设计规范与商业分级标准
│   └── PRODUCT_TIER_SPECIFICATION.md   # 免费社区版与 Pro 专业版功能分级规范书
├── 02-项目架构/                        # 系统拓扑、模块通信与 Win32 原生集成
│   └── ARCHITECTURE.md                 # 双支柱架构总览、数据流与 FFI 接口规范
├── 03-功能模块/                        # 业务与功能特性矩阵 (Feature Matrix)
│   └── FEATURE_MATRIX.md               # 磁盘治理、极速检索与智能护航三大支柱清单
├── 04-开发指南/                        # 编译构建、调试避坑与编码规范
│   └── DEVELOPMENT_GUIDE.md            # Windows 原生环境搭建、构建与测试指令
├── 05-测试与基准/                      # 验证基线、性能实测与吸收审计
│   ├── TEST_BASELINE.md                # 90 项自动化测试基线与物理机实测性能数据
│   └── FEATURE_ABSORPTION_AUDIT_REPORT.md # Listary Pro 与 fsearch 特性 1:1 吸收审计总表
├── 06-复盘与沉淀/                      # 架构经验沉淀、外部借鉴与历史日志
│   ├── EXTERNAL_REFERENCES.md          # 业界标杆项目 (Czkawka/WizTree/Listary/fsearch) 深度借鉴沉淀
│   ├── references/                     # 外部标杆专项架构与算法深度剖析档案
│   │   ├── LISTARY_PRO_ANALYSIS.md     # Listary Pro 架构深度剖析与解包反编译归档
│   │   └── FSEARCH_ANALYSIS.md         # fsearch 核心算法与高吞吐虚拟表格深度剖析
│   ├── CONSUMER_EXPERIENCE_IMPROVEMENT_PLAN.md # 大众化易用性专项研发复盘与方案总结
│   └── RELEASE_NOTES_v0.1.0.md         # v0.1.0 架构收敛历史发布说明
└── 08-迭代方向/                        # 未来演进规划与技术探索
    └── ROADMAP.md                      # v0.5.0 路线图与候选演进技术方案
```

---

## 各目录职责与维护原则

1. **`01-规范标准/`**：定义产品边界与商业化分级。变更需经业务与架构双重评审。
2. **`02-项目架构/`**：描述当前代码库真实存在的系统拓扑，绝不写虚构未落地的设计。
3. **`03-功能模块/`**：按业务支柱收敛维护已落地的功能清单，与代码实现 1:1 锚定。
4. **`04-开发指南/`**：工程人员与 AI 必须遵循的环境配置、测试命令与 Win32 避坑指南。
5. **`05-测试与基准/`**：存放可复现的自动化测试结果、性能基准数据与竞品特性吸收审计报告。
6. **`06-复盘与沉淀/`**：沉淀历史版本的技术演进过程、外部优秀项目解析与工程经验。
7. **`08-迭代方向/`**：记录后续版本的演进候选路线，已交付内容及时收敛至前置目录。
