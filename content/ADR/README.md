# 📐 架构决策记录 (ADR)

> Architecture Decision Records — 记录 DataLanding 的每一个关键决策。

```dataview
TABLE
  id as "编号",
  status as "状态",
  date as "日期"
FROM "ADR"
WHERE type = "adr"
SORT id ASC
```

## 使用约定

- 新决策用模板 `Ctrl+P → 插入模板 → ADR 模板`
- 状态：`已采纳` / `已否决` / `已替代`
- 如果某条 ADR 被替代，填写 `superseded_by` 字段指向新 ADR
- 每条 ADR 独立文件，不改写历史
