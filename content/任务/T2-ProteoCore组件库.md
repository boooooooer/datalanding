---
type: task
phase: 1
id: T2
name: ProteoCore 组件库
status: 阻塞
priority: high
depends_on: T1
assigned_to: HQ
estimated_hours: 3-4
---

## 任务描述

从 ProteoViz 抽取 FT 组件，建立共享组件库

**执行位置**：本项目 `proteocore/`

### 首批组件（≥5个）
- `upload_page` — 文件上传落地页
- `metric_cards` — 指标卡片行
- `tab_bar` + `tab_panel` — Tab 切换
- `data_table` — 可排序数据表格
- `sidebar_section` — 侧边栏布局

### 验收标准
- [ ] `pip install -e .` 成功，`from proteocore.components.layout import upload_page` 可用
- [ ] ProteoViz 改用 proteocore 组件后功能不变
- [ ] 每个组件有 docstring 说明参数
- [ ] README.md 含使用示例

### 阻塞原因
⬅️ 等待 [[T1-ProteoViz离线化]] 完成后才能抽取组件
