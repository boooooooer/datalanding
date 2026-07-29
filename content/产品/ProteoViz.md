---
type: product
name: ProteoViz
product_line: tidyproteomics
status: 🔴 原型
version: ""
path: D:\Desktop\test\proteoviz\
current_task: T1 离线化
last_updated: 2026-07-26
priority: high
has_screenshot: false
has_online_demo: true
has_download: false
---

# ProteoViz — 蛋白质组学可视化原型

> FastHTML 交互式火山图、热力图——ProteoQuant 的前身与组件来源。

---

## 🖼️ 界面预览

<!-- ![[产品截图/ProteoViz.png]] -->

> 📸 预览图待生成

---

## ✨ 功能特性

- CSV 上传 → 火山图
- 交互式热力图（Plotly.js）
- 差异表达蛋白高亮与标注
- 可作为 ProteoQuant 的功能预览

---

## 🔗 试用 & 下载

- [x] 🌐 本地启动：`cd proteoviz/ && python app.py`（需要 FastHTML）
- [ ] 📦 下载离线版 — 待第一阶段完成

---

## 技术信息

| 项目 | 内容 |
|------|------|
| 框架 | FastHTML + uvicorn + htmx |
| 图表 | Plotly.js（本地内嵌，零 CDN） |
| 意义 | ProteoCore 组件库的源材料 |
