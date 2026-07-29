---
type: adr
id: ADR-002
title: tidyproteomics 既是 R 包名也是产品线名
date: 2026-07-26
status: 已采纳
superseded_by: 
context: tidyproteomics 作为 R 包已有多年积累，桌面产品线需要命名
decision: |
  R 包保持 `library(tidyproteomics)`；桌面套件命名 ProteoQuant / ProteoLiP / ProteoTPP。
  UI 中标注 "Powered by tidyproteomics"。
consequences:
  - R 包名和产品线名一致，降低用户认知成本
  - 桌面产品用 Proteo- 前缀区分具体功能
  - 需在 UI 中标注引擎归属
---

## 决策

- R 包（技术引擎）：保持 `tidyproteomics` / `tidyLiP` / `tidyTPP`
- 桌面应用：`ProteoQuant` / `ProteoLiP` / `ProteoTPP`
- UI 标注：`Powered by tidyproteomics`

## 理由

- tidyproteomics 已有社区知名度，R 包改名成本高
- Proteo- 前缀清晰标识蛋白质组学定位
- 区分引擎层（R 包）和用户界面层（桌面应用）

## 影响

在架构文档和代码中需区分"tidyproteomics（R 包）"和"tidyproteomics（产品线）"。
