# Scientific PPT Generation Principles

> v1.0 — 基于 ppt-master 深度学习的科研演示文稿生成方法论
> 目标：搭配图标素材库，生成现代化、图文丰富、可复现的科研 PPT

---

## 一、技术栈

| 层 | 工具 | 角色 |
|----|------|------|
| 规划 | ppt-master Strategist 流程 | 主题→大纲→配色→页规划→spec_lock |
| 图标 | ppt-master 内置 (11,631) + Bioicons (2,836) | 为每页提供视觉锚点 |
| 图表 | ppt-master 80+ chart templates | 数据可视化骨架 |
| 绑图 | Python matplotlib/drawSvg | 自定义示意图嵌入 SVG |
| SVG 生成 | ppt-master Executor (AI 手写 SVG) | 逐页生成 1280×720 SVG |
| 导出 | ppt-master svg_to_pptx.py | SVG → Native DrawingML PPTX |

---

## 二、图标策略 — 科学 PPT 的核心差异化

### 2.1 内置图标库选择

| 库 | 风格 | 科学适配度 | 推荐场景 |
|----|------|-----------|----------|
| **phosphor-duotone** | 双色调柔和深度 | ⭐⭐⭐⭐⭐ | **首选**：蛋白、细胞、分子等有机形态 → smooth curves + soft depth |
| **tabler-filled** | 圆润填色 | ⭐⭐⭐⭐ | 次选：需要实体感的图标（仪器、设备） |
| **tabler-outline** | 线条简约 | ⭐⭐⭐ | 精致场景、浅色卡片内嵌 |
| **chunk-filled** | 尖锐几何 | ⭐⭐ | 工程/技术路线图 |

**科研 PPT 默认选 `phosphor-duotone`**，其 bezier 曲线自然过渡适合生物学/化学的有机形态，双色调产生柔和的立体感。

### 2.2 与 Bioicons 的混合使用

Bioicons 图标（`D:\Desktop\test\bioicons\`）可通过两种方式嵌入：

1. **外链方式**：在 SVG 中 `<image href="../images/<name>.svg"/>` — 作为独立图片元素
2. **项目图标池**：复制到 `<project>/icons/custom/`，使用 `data-icon="custom/<name>"` 引用

**推荐策略**：Bioicons 用于高度特化的科学元素（细胞培养板、质谱仪、离心机、受体蛋白），ppt-master 内置图标用于通用概念（文档、图表、箭头、数字、齿轮）。

### 2.3 图标同步命令

```bash
# 从 ppt-master 图标库选择图标到项目
python skills/ppt-master/scripts/icon_sync.py <project> \
    phosphor-duotone/flask phosphor-duotone/dna phosphor-duotone/atom \
    phosphor-duotone/brain phosphor-duotone/chart-line phosphor-duotone/leaf

# SVG 中使用（finalize_svg.py 自动嵌入）
<use data-icon="phosphor-duotone/flask" x="100" y="200" width="48" height="48" fill="#2C5282"/>
```

---

## 三、科研配色体系

### 3.1 预设色板

| 场景 | 主色 | 辅助色 | 强调色 | 背景 |
|------|------|--------|--------|------|
| **蛋白组学/生化** | `#2C5282` (深蓝) | `#4A7A8C` (灰蓝) | `#C0784A` (暖棕) | `#F7F4EF` (浅米白) |
| **分子生物学** | `#285E61` (深绿) | `#319795` (青绿) | `#DD6B20` (橙色) | `#FAFAF5` |
| **药物研发** | `#553C9A` (深紫) | `#805AD5` (紫) | `#E53E3E` (红) | `#F7F5FB` |
| **通用学术** | `#1A365D` (海军蓝) | `#2B6CB0` (蓝) | `#C0563A` (锈红) | `#FFFFFF` |

### 3.2 莫兰迪科研色板（推荐）

低饱和度、沉稳、长时间观看不疲劳：

```
Primary:   #7B9BA6 (Morandi Blue)  — 60-70% 视觉权重
Secondary: #8AA79C (Morandi Sage)  — 结构分区
Accent:    #B8956A (Morandi Warm)  — 关键数字/结论
BG:        #F7F4EF (Morandi Cream) — 全局背景
Text:      #2C3E50 (Deep Slate)    — 正文
Muted:     #8899A0 (Dusty Blue)    — 次要信息
```

### 3.3 配色铁律

- 克制的颜色数量：**1 背景 + 1 主色 + 1 辅助色 + 1 强调色**，不超过 4 个语义色
- 所有页面严格复用同一配色，除非分节页使用深色变体
- 禁止彩虹配色、禁止使用超过 3 种卡片颜色在同一页
- 文字与背景对比度 >= 4.5:1（WCAG AA）

---

## 四、科学 PPT 页面类型与布局

### 4.1 页面类型库

| 类型 | ppt-master layout_type | 科学场景 | SVG 特征 |
|------|----------------------|----------|----------|
| 封面 | `title-cover` | 论文解读、技术分享 | 深色背景 + 大标题 + 英文副标题 |
| 原理页 | `process-flow` | 质谱流程、信号通路 | 4-5 步水平箭头 + 底部卡片说明 |
| 对比页 | `comparison` | DDA vs DIA、方法 A vs B | 双列对称 + 表格/列表 |
| 数据页 | `two-column` | 左侧卡片 + 右侧图表 | 图/表占 40-45% 宽度 |
| 平台页 | `architecture-diagram` | 仪器对比、技术矩阵 | 2×2 或 3×1 卡片网格 |
| 总结页 | `conclusion` | 要点回顾 | 编号步骤 + 加粗结论 |
| 指标页 | `big-number` | 关键数据强调 | 40-52pt 大数字 + 标签 |

### 4.2 信息密度原则

- **卡片网格，不要 bullet 列表**：8 张 50 字卡片 >> 2 张 200 字卡片
- **图文比**：每页至少 1 个视觉元素（图标/图表/示意图），纯文字页不可接受
- **边距 40px**：页面和内容边距 >= 40px，文字不贴边
- **标题 y=36-90**：预留垂直空间给标题，主体内容从 y>=110 开始

---

## 五、图表策略

### 5.1 科学 PPT 常用图表

| 需求 | ppt-master 模板 | 推荐方式 |
|------|----------------|---------|
| 蛋白差异火山图 | `scatter_chart` | Shape-first（保留数据标识） |
| 热图聚类 | `heatmap_chart` | Shape-first |
| 通路富集柱状 | `column_chart` / `horizontal_bar_chart` | Native chart replacement |
| 质谱流程 | `process_flow` / `snake_flow` | Shape-based diagram |
| 时间线 | `timeline` / `gantt_chart` | Shape-based |
| 饼/环图 | `pie_chart` / `donut_chart` | Native replacement |
| Venn 图 | `venn_diagram` | Shape-based |
| 技术对比 | `comparison_table` / `feature_matrix_table` | SVG table |

### 5.2 图表使用规则

- 数据信息**必须在图表卡片中可视化**，不要罗列在文字卡片里
- 优先使用 Shape-first（原生可编辑形状），仅 23 种数据图表可用 Native replacement
- 图表与文字卡片组成网格，确保图文丰富

---

## 六、生成工作流（精简版）

### 6.1 快速启动

```bash
# 1. 初始化项目
cd ppt-master
python skills/ppt-master/scripts/project_manager.py init <name> --format ppt169

# 2. 选择图标（如需要）
python skills/ppt-master/scripts/icon_sync.py projects/<name> \
    phosphor-duotone/flask phosphor-duotone/dna phosphor-duotone/atom \
    phosphor-duotone/chart-line phosphor-duotone/brain

# 3. 写 design_spec.md + spec_lock.md

# 4. 生成 SVG → svg_output/
# （AI 手写，1280×720，用 <use data-icon="..."/> 引用图标）

# 5. 转换
python skills/ppt-master/scripts/svg_to_pptx.py projects/<name>

# 6. 复制到工作目录
cp projects/<name>/exports/*.pptx /d/Desktop/test/ppt/
```

### 6.2 跳过 Confirmation UI

首次快速测试或小型 PPT（<= 8 页）可直接用 chat fallback，跳过 `confirm_ui/server.py` 三步确认流程。大型部署（> 10 页、有品牌约束）按完整 Strategist 流程走。

---

## 七、SVG 编写速查

### 7.1 画布与结构

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720"
     font-family="&quot;Microsoft YaHei&quot;, Arial, sans-serif">
  <!-- 背景 -->
  <g id="bg"><rect x="0" y="0" width="1280" height="720" fill="#F7F4EF"/></g>
  <!-- 标题区 -->
  <g id="title">...</g>
  <!-- 内容区 -->
  <g id="content">...</g>
  <!-- 页脚 -->
  <g id="footer">...</g>
</svg>
```

### 7.2 常用元素

```xml
<!-- 卡片 -->
<rect x="80" y="130" width="370" height="170" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
<!-- 顶部色条 -->
<rect x="80" y="130" width="370" height="4" fill="#2C5282"/>
<!-- 标题文本 -->
<text x="100" y="160" font-size="18" font-weight="700" fill="#1A365D">Title</text>
<!-- 正文 -->
<text x="100" y="190" font-size="13" fill="#4A5568">Body text here</text>
<!-- 图标 -->
<use data-icon="phosphor-duotone/flask" x="100" y="200" width="48" height="48" fill="#2C5282"/>
<!-- 箭头 -->
<line x1="250" y1="180" x2="290" y2="180" stroke="#718096" stroke-width="2"/>
<polygon points="290,175 300,180 290,185" fill="#718096"/>
```

### 7.3 禁止项

- `mask`、`<style>` 标签、external CSS、`<foreignObject>`
- HTML named entities（写原始 Unicode，转义 XML 保留字符）
- `<animate*>`、`<script>`
- Emoji 图标
- http(s) 外链图片 URL（必须上传或用 data-icon 占位符）

---

## 八、科学 PPT 质量标准

### 8.1 每页检查清单

- [ ] 每页至少 1 个视觉元素（图标/图表/图示/大数字）
- [ ] 配色一致：主色/辅助色/强调色/背景色全 deck 统一
- [ ] 边距：主体内容不贴边（>= 40px），卡片内文字不贴边（>= 5px）
- [ ] 文字大小：标题 28-36pt、正文 12-14pt、注释 10-12pt
- [ ] 字体：全篇思源黑体或 Microsoft YaHei，封面可少量衬线体
- [ ] 无 emoji、无无意义装饰线、无贴边窄条
- [ ] 大数字/长文本设置了 wrap 和 autoFit

### 8.2 科研特化标准

- 关键数据标注文献来源（Author, Year, Journal）
- 方法对比页面用并行措辞（parallel wording）
- 示意图用真实图标而非几何形状拼凑
- 图表标题包含 "Figure X:" 编号格式
- 底部可放 source bar 标注页码/章节

---

## 九、与飞书 Slides 的对比

| 维度 | 飞书 Slides | ppt-master |
|------|------------|------------|
| 图片渲染 | 有丢失风险 | 原生矢量形状，可靠 |
| 图标 | 无内置库 | 11,631 个 |
| 图表 | 需手动创建 | 80+ 模板 |
| 输出 | 飞书链接 | .pptx 文件 |
| 编辑 | 飞书内 | PowerPoint / WPS |
| 可复现 | 无 | design_spec + SVG 源文件 |
| 协作 | 实时在线 | 文件分享 |

**结论**：飞书 Slides 适合快速在线展示和协作，ppt-master 适合正式交付的科研 PPT（需要图标、图表、和可编辑的矢量输出）。
