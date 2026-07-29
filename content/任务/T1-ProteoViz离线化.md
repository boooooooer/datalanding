---
type: task
phase: 1
id: T1
name: ProteoViz 离线化
status: 进行中
priority: high
depends_on: 
assigned_to: HQ
estimated_hours: 1-2
---

## 任务描述

ProteoViz 离线化 — 内嵌 Plotly.js, 零 CDN

**执行位置**：`proteoviz/`

### 验收标准
- [ ] 无网络环境下，`python app.py` → 浏览器打开 → 上传 CSV → 火山图正常渲染
- [ ] 所有 Plotly 图表（volcano, heatmap）均可正常交互
- [ ] 不引入新的外部 CDN 依赖

### 依赖
- T2 需等待此任务完成后启动（组件抽取）

### 关联
- 工作站：[[ProteoViz]]
- 文档：[[DOCK/第一阶段执行计划.md]]
