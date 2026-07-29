---
type: task
phase: 1
id: T4
name: R-portable + tpplumber
status: 待开始
priority: medium
depends_on: 
assigned_to: HQ
estimated_hours: 4-6
---

## 任务描述

搭建 R Plumber API 端点 + Python PlumberClient

**执行位置**：本项目 `tpplumber/`

### API 端点
| 端点 | 方法 | 功能 |
|------|:--:|------|
| `/read` | POST | 文件上传 → 列检测 |
| `/preprocess` | POST | normalize + impute + censor |
| `/quantify` | POST | 定量计算 |
| `/compare` | POST | FC cutoff + p cutoff |
| `/recommend` | GET | 参数推荐 |

### 验收标准
- [ ] `Rscript api.R` → Plumber 在 :8000 启动
- [ ] Python `PlumberClient().read("sample_data.csv")` 返回正确的 columns + n_rows
- [ ] 5 个端点全部可调通
- [ ] 错误响应格式一致

### 关联
- 文档：[[DOCK/第一阶段执行计划.md]]、[[DOCK/技术细节.md]]
