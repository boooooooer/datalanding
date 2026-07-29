# 🎯 任务追踪

> HQ 下达的任务列表。每个任务独立笔记，Dataview 自动汇入 Home.md。

## 工作流

```
HQ 下达任务 [任务/*.md]   工作站执行        工作站提交报告          HQ 审阅
    │                        │                    │                  │
    ├─ frontmatter           ├─ 在报告模板/       ├─ 报告放            ├─ 更新 frontmatter
    │  status: 待开始        │  填写报告          审阅记录/            │  verdict: ✅/❌
    │  assigned_to: 工作站   │                    │                  │
    └─ 通知工作站            └─ 开始执行           └─ 通知 HQ           └─ 更新 task status
```

## 字段约定

| 字段 | 取值 | 含义 |
|------|------|------|
| `status` | 待开始 / 进行中 / 阻塞 / 已完成 | 生命周期 |
| `priority` | high / medium / low | 优先级 |
| `depends_on` | [[任务ID]] | 前置依赖 |
| `assigned_to` | HQ / 工作站名 | 执行方 |
