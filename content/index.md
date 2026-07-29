---
created: 2026-07-29
type: home
updated: 2026-07-29
---

# 🏗️ 数达 DataLanding

> **科研数据的最后一公里** —— 仪器数据 → 发表级图表，零代码，完全离线，解压即用。
>
> 伞品牌覆盖：分子信息与互作计算 · 质谱蛋白质组学数据处理 · 表型分析

---

## 🧪 MolSuite — 分子信息与互作计算

```dataview
TABLE
  status as "状态",
  choice(has_screenshot, "📸", "") as "预览",
  choice(has_online_demo, "🌐", "") as "试用",
  choice(has_download, "📦", "") as "下载"
FROM "产品"
WHERE product_line = "molsuite"
SORT priority DESC
```

> 共享依赖：[[产品/MolToolBank|MolToolBank]] Python 库

---

## 🧬 tidyproteomics — 质谱蛋白质组学数据处理

```dataview
TABLE
  status as "状态",
  choice(has_screenshot, "📸", "") as "预览",
  choice(has_online_demo, "🌐", "") as "试用",
  choice(has_download, "📦", "") as "下载"
FROM "产品"
WHERE product_line = "tidyproteomics"
SORT has_download DESC, priority DESC
```

> R 引擎：[[产品/TP|tidyproteomics]] · [[产品/TLiP|tidyLiP]] · [[产品/TTPP|tidyTPP]]

---

## 🔬 PhenoAnalysis — 表型分析

```dataview
TABLE
  status as "状态",
  choice(has_screenshot, "📸", "") as "预览",
  choice(has_online_demo, "🌐", "") as "试用",
  choice(has_download, "📦", "") as "下载"
FROM "产品"
WHERE product_line = "phenoanalysis"
```

---

## 🖼️ 架构全景

![[架构全景.canvas]]

---

## 🔗 快速导航

| 入口 | 说明 |
|------|------|
| [[开发中心.md\|🔧 开发中心]] | 任务追踪、ADR、报告审阅（内部） |
| [[DOCK/产品计划.md\|📋 产品计划]] | 品牌、路线图、项目路径 |
| [[DOCK/产品架构.md\|🏛️ 产品架构]] | 竞品分析、架构决策 |
| [[架构全景.canvas\|🖼️ 架构全景]] | 交互式架构图 |

---

> **核心差异**：完全离线 · 解压即用 · 中文界面 · 零代码 · 免费开源
>
> **三条产品线独立迭代**，通过 Bridge 协议点对点连接
