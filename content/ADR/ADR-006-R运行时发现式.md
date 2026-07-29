---
type: adr
id: ADR-006
title: R 运行时发现式
date: 2026-07-26
status: 已采纳
superseded_by: 
context: 桌面应用依赖 R（tidyproteomics/tidyLiP），需要决定 R 的获取和发现策略
decision: |
  启动顺序：
  1. 扫描系统 PATH 中的 R
  2. 兜底使用捆绑的 R-portable
  3. 以上均不可用 → 友好提示安装指引
consequences:
  - 有系统 R 的用户优先使用（性能更好，版本可控）
  - 无 R 的用户也能开箱即用（R-portable 兜底）
  - 捆绑 R-portable 增加分发体积 ~60MB
---

## 决策

**发现式 R 运行时**：系统 R → R-portable → 安装指引。

## 理由

- 生物信息学用户通常已安装 R，应优先使用
- 实验人员（目标用户）可能没有 R，需要零配置方案
- 参考 RStudio 的 `RSTUDIO_WHICH_R` 环境变量策略

## 影响

启动器需实现 R 检测逻辑（Windows 下查注册表 + PATH）。
R-portable 需随应用分发，打包脚本需包含 R 环境构建步骤。
