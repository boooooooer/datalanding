---
type: product
name: ME MolEdit
product_line: molsuite
status: 🆕 v0.1.0
version: 0.1.0
path: D:\Files\code_workstation\projects\MolEdit\
current_task: 打包优化待执行
last_updated: 2026-07-26
priority: medium
has_screenshot: false
has_online_demo: false
has_download: false
---

# ME — MolEdit 分子结构编辑

> 浏览器中直接绘制、编辑分子结构，支持多种格式导入导出。

---

## 🖼️ 界面预览

<!-- ![[产品截图/ME.png]] -->

> 📸 预览图待生成

---

## ✨ 功能特性

- Ketcher 内核，浏览器内自由绘制
- SMILES / MOL / SDF 格式互转
- 分子结构清洁（3D 坐标优化）
- 导出高分辨率结构图

---

## 🔗 试用 & 下载

- [ ] 🌐 在线试用 — 待部署
- [ ] 📦 下载离线版 — v0.1.0，启动慢（25-40s），等待第三批打包优化

---

## 技术信息

| 项目 | 内容 |
|------|------|
| 框架 | Streamlit + Ketcher |
| 打包 | PyInstaller --onefile + UPX（待优化） |
| 依赖 | RDKit |
