---
type: product
name: ProteoQuant
product_line: tidyproteomics
status: 📋 待建
version: ""
path: ""
current_task: 等待第一阶段完成
last_updated: 2026-07-26
priority: high
has_screenshot: false
has_online_demo: false
has_download: false
---

# ProteoQuant — 蛋白质组学数据处理与可视化

> DataLanding 第二阶段核心产品——一站式蛋白质组学定量分析与可视化桌面应用。

---

## 🖼️ 界面预览

🛠️ 开发中 · 等待第一阶段（T1-T4）完成后启动

<!-- ![[产品截图/ProteoQuant.png]] -->

---

## ✨ 功能特性（规划）

- 文件拖拽上传（Spectronaut / MaxQuant / DIA-NN）
- 自动预处理推荐（智能归一化、插补、删失）
- 差异表达分析（火山图、热力图、MA 图）
- MSstats 比较一键出图
- 报告导出（PDF / PNG / CSV）

---

## 🔗 试用 & 下载

- [ ] 🌐 在线试用 — 待开发
- [ ] 📦 下载离线版 — 待开发

---

## 技术信息

| 项目 | 内容 |
|------|------|
| 框架 | FastHTML + uvicorn + htmx |
| 引擎 | R Plumber :8000（tidyproteomics） |
| 组件库 | ProteoCore（从 ProteoViz 抽取） |
| 启动器 | 统一 `_launch.py` 模板 |
