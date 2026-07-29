---
type: product
name: ProteoLiP
product_line: tidyproteomics
status: 📋 待建
version: ""
path: ""
current_task: 等待第二阶段
last_updated: 2026-07-26
priority: medium
has_screenshot: false
has_online_demo: false
has_download: false
---

# ProteoLiP — LiP-MS 蛋白结构变化检测

> 基于 tidyLiP 引擎的 LiP-MS 专用桌面分析工具——检测蛋白构象变化，连接 MD 结构查看。

---

## 🖼️ 界面预览

🛠️ 开发中

---

## ✨ 功能特性（规划）

- LiP-MS 数据专用导入与预处理
- LiP-only 结构变化检测（tidyLiP 引擎）
- 蛋白覆盖度图谱 + 显著区域标注
- **Bridge → MD**：结构变化区域自动发送到 MolInteract 查看 3D 结构

---

## 🔗 试用 & 下载

- [ ] 🌐 在线试用 — 待开发
- [ ] 📦 下载离线版 — 待开发

---

## 技术信息

| 项目 | 内容 |
|------|------|
| 框架 | FastHTML + uvicorn + htmx |
| 引擎 | R Plumber :8000（tidyLiP） |
| 跨线 | Bridge → MD（3D 结构查看） |
