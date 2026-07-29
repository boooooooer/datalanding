# DataLanding 数达 · 产品总纲

> 本文件是 DataLanding 生态的顶层设计文档。本项目（`D:\Desktop\test\`）承担架构设计、方案制定、决策下达的角色。下游工作站项目负责执行、整改、提交报告。

---

## 一、身份与角色

### 本项目是什么

**DataLanding HQ** — 产品架构与决策层。不是代码仓库，是设计图纸和作战指挥室。

### 角色分工

```
DataLanding HQ (本项目)           下游工作站 (D:\Files\)
──────────────────────────       ──────────────────────────
  架构设计                         代码实现
  方案制定                         单元测试
  决策下达                         问题整改
  报告审阅                         提交报告
  优先级排序                        打包发布
```

### 工作协议

1. **HQ 下达任务** → 在本项目 CLAUDE.md 或 DOCK/ 文档中写入任务
2. **工作站执行** → 在下游项目目录中打开 Claude，读取任务，执行
3. **工作站报告** → 完成后在下游项目 CLAUDE.md 或 CHANGELOG.md 中记录结果
4. **HQ 审阅** → 在本项目中验证报告，更新任务状态，下达下一步

### 决策权限

| 层级 | 权限 | 举例 |
|------|------|------|
| HQ (本项目) | 架构、命名、技术选型、优先级、跨产品协调 | FastHTML vs Streamlit, 产品线划分 |
| 工作站 | 实现方式、代码风格、具体 API 设计 | 函数签名、变量命名、测试用例 |
| HQ 否决权 | 可驳回工作站的实现方案，要求整改 | 不符合设计规范的 UI |

---

## 二、产品全景

> 完整清单见 [DOCK/产品计划.md](./DOCK/产品计划.md)

```
数达 DataLanding — 科研数据的最后一公里

  MolSuite                   tidyproteomics              PhenoAnalysis
  分子信息与互作计算           质谱蛋白质组学数据处理        表型分析
  ├── CQ 化合物查询           ├── TP  R包 (引擎)          └── PhenoECC
  ├── PQ 蛋白查询             ├── TLiP R包
  ├── PP 口袋预测             ├── TTPP R包 (待建)
  ├── ME 分子编辑             ├── ProteoQuant 定量+可视化
  └── MD 对接与动力学          ├── ProteoLiP  LiP-MS
                              └── ProteoTPP  热稳定性
```

**三条产品线独立迭代，共用数达品牌。交叉点：ProteoLiP → MD (LiP-MS 结构解读)。**

---

## 三、技术架构速览

| 决策 | 选择 | 理由 |
|------|------|------|
| UI 框架 | FastHTML + htmx | 冷启动 <1s (Streamlit 5-8s) |
| 蛋白计算 | R Plumber 子进程 | 复用 tidyproteomics, 不改写 R |
| 分子计算 | Python 原生 | RDKit + Meeko + Vina + P2Rank |
| 打包(开发) | PyInstaller --onedir | 分钟级构建 |
| 打包(生产) | Nuitka --standalone | C++ 编译, 杀软友好 |
| 分发 | zip = Python + R-portable + 应用 | 解压即用, U盘分发 |
| 离线 | 默认离线, 有网可选增强 | 国内实验室主流场景 |
| 便携 | `data/` 文件夹检测 | calibre/Tabby 验证模式 |

---

## 四、当前阶段：第一阶段 — 基础设施

> 详细任务拆解见 [DOCK/第一阶段执行计划.md](./DOCK/第一阶段执行计划.md)

### 目标

搭建 DataLanding 的共享底座：组件库、启动器、R 后端。为 ProteoQuant（模板产品）做好准备。

### 四个并行任务

| 编号 | 任务 | 执行位置 | 产出 |
|:--:|------|------|------|
| **T1** | ProteoViz 离线化 | `D:\Desktop\test\proteoviz\` | 内嵌 Plotly.js, 零 CDN |
| **T2** | ProteoCore 组件库 | 本项目 (新建 `proteocore/`) | FT 组件库, pip install -e . |
| **T3** | 统一启动器 | 本项目 (新建模板) | `_launch.py` 模板 |
| **T4** | R-portable + tpplumber | 本项目 (新建 `tpplumber/`) | 5 API 端点 + Python 客户端 |

T1 和 T2 有先后关系（T1 → 抽取 → T2），T3 和 T4 完全独立。

### 完成标准

- ProteoViz 在无网络环境下正常启动并出图
- ProteoCore 包含 ≥5 个可复用组件，有文档
- 启动器模板可被 ProteoQuant 直接复制使用
- R Plumber 5 个端点全部可通过 Python 客户端调用

---

## 五、下游工作站速查

| 工作站 | 路径 | 当前任务 |
|------|------|------|
| MD 母体 | `D:\Files\code_workstation\projects\MD\` | Sprint 3 收尾 (6+3 任务) |
| CQ | `D:\Files\code_workstation\projects\CQ\` | 稳定, 待命 |
| PP | `D:\Files\code_workstation\projects\PP\` | v0.2.0, 待命 |
| ME (MolEdit) | `D:\Files\code_workstation\projects\MolEdit\` | 打包优化待执行 |
| MD (MolInteract) | `D:\Files\code_workstation\projects\MolDock\` | 重构中 |
| MolToolBank | `D:\Files\code_workstation\projects\MolToolBank\` | 维护 |
| tidyproteomics | `D:\Files\RStudio_workstation\R包\tidyproteomics_v2\` | 维护 |
| tidyLiP | `D:\Files\RStudio_workstation\R包\tidyLiP\` | 维护 |
| PhenoECC | `D:\Files\RStudio_workstation\项目们\randomForestExplainer\` | 待命 |
| GP Thermal | `D:\Files\spyder_workstation\项目们\gp\` | 待 ProteoTPP 阶段 |

---

## 六、文档索引

| 文档 | 位置 | 用途 |
|------|------|------|
| 产品计划 | [DOCK/产品计划.md](./DOCK/产品计划.md) | 定位、产品总表、路线图 |
| 产品架构 | [DOCK/产品架构.md](./DOCK/产品架构.md) | 竞品分析、架构决策 |
| 产品地图 | [DOCK/产品地图.md](./DOCK/产品地图.md) | 项目路径、状态、优先级 |
| 技术细节 | [DOCK/技术细节.md](./DOCK/技术细节.md) | 打包、性能、R-Portable |
| 分发策略 | [DOCK/分发策略.md](./DOCK/分发策略.md) | 分发模式、国内适配 |
| 第一阶段计划 | [DOCK/第一阶段执行计划.md](./DOCK/第一阶段执行计划.md) | 当前任务拆解 |
| 绘图参考 | [drawing/CLAUDE.md](./drawing/CLAUDE.md) | 科研 PPT 生成 (独立分支) |

---

## 七、命名速查

| 层级 | 名称 |
|------|------|
| 伞品牌 | **数达** / DataLanding |
| 分子线 | MolSuite — 分子信息与互作计算 |
| 蛋白线 | tidyproteomics — 质谱蛋白质组学数据处理 |
| 表型线 | PhenoAnalysis — 表型分析 |
