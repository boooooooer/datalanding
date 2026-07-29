---
type: adr
id: ADR-003
title: FastHTML 替代 Streamlit 作为 UI 框架
date: 2026-07-26
status: 已采纳
superseded_by: 
context: |
  MolSuite 现有产品基于 Streamlit，实测冷启动 5-8s（frozen 模式 8-40s）。
  Streamlit 的 Tornado + WebSocket 架构是结构性瓶颈。
  新桌面产品（tidyproteomics 线）需选择 UI 框架。
decision: 所有新工具使用 FastHTML + htmx + uvicorn。MolSuite 按 CQ → PP → ME → MD 顺序迁移
consequences:
  - 新工具冷启动 < 1s
  - 打包体积小（不含 Streamlit、Tornado、WebSocket 等依赖）
  - 开发体验从 Streamlit 热重载改为 FastHTML 自动刷新
  - MolSuite 需投入迁移工作，分四批完成
  - 需统一 ui-ux-pro-max 风格指南确保视觉一致性
---

## 决策

**新工具**：全部 FastHTML + htmx + uvicorn
**旧工具（MolSuite）**：按 CQ → PP → ME → MD 顺序从 Streamlit 迁移

## 对比

| 指标 | Streamlit | FastHTML |
|------|:--------:|:--------:|
| 冷启动 | 5-8s | < 1s |
| 架构 | Tornado + WebSocket | uvicorn + HTTP |
| 打包体积（含依赖） | ~500MB | ~150MB |
| 前端技术栈 | React (内部) | htmx（无 JS 框架） |
| 迁移成本 | — | 需逐一重写 UI |

## 影响

ProteoQuant / ProteoLiP / ProteoTPP 全部使用 FastHTML。MolSuite 第五批任务为框架迁移。
