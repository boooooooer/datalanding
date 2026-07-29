# CLAUDE.md — Scientific PPT Generation Quick Reference

> 完整细节见 `docs/SCIENTIFIC_PPT_PRINCIPLES.md`
> 依赖：ppt-master (github.com/hugohe3/ppt-master) + scidraw conda env

## 快速启动

```bash
# 环境
conda activate scidraw
cd ppt-master

# 建项目
python skills/ppt-master/scripts/project_manager.py init <name> --format ppt169

# 选图标（科研默认 phosphor-duotone）
python skills/ppt-master/scripts/icon_sync.py projects/<name> \
    phosphor-duotone/flask phosphor-duotone/dna phosphor-duotone/atom \
    phosphor-duotone/chart-line phosphor-duotone/brain phosphor-duotone/leaf

# 生成 PPTX
python skills/ppt-master/scripts/svg_to_pptx.py projects/<name>

# 输出到 ppt/
cp projects/<name>/exports/*.pptx ppt/
```

## 图标资源

| 来源 | 数量 | 科学适用 | 用法 |
|------|------|---------|------|
| ppt-master phosphor-duotone | 1,200+ | ⭐⭐⭐⭐⭐ | `<use data-icon="phosphor-duotone/name" x="..." y="..." width="48" height="48" fill="..."/>` |
| ppt-master tabler-outline | 5,000+ | ⭐⭐⭐ | 线条简约，卡片内嵌 |
| ppt-master tabler-filled | 1,000+ | ⭐⭐⭐⭐ | 实体感强，仪器设备 |
| Bioicons (本地) | 20 下载 | ⭐⭐⭐⭐⭐ | `<image href="../bioicons/name.svg"/>` 或拷入 `icons/custom/` |
| ppt-master 图表 | 80+ | - | `executor-chart.md` 按需加载 |

**科研 PPT 默认图标库 = phosphor-duotone**（双色调柔和立体感，适合生物学/化学有机形态）

## 配色

| 场景 | 主色 | 强调 | 背景 |
|------|------|------|------|
| 蛋白组学 | `#2C5282` | `#C0784A` | `#F7F4EF` |
| 分子生物 | `#285E61` | `#DD6B20` | `#FAFAF5` |
| 莫兰迪通用 | `#7B9BA6` | `#B8956A` | `#F7F4EF` |

铁律：1 背景 + 1 主色 + 1 辅助 + 1 强调 = 4 个语义色，全局一致。

## SVG 规范

- 画布：`viewBox="0 0 1280 720"`
- 字体：`Microsoft YaHei`, Arial, sans-serif
- 标题 28-36pt / 正文 12-14pt / 注释 10-12pt
- 边距 >= 40px（卡片内 >= 5px）
- 禁止：emoji、`<style>`、`<foreignObject>`、外链图片 URL、无意义装饰线

## 科学 PPT 质量铁律

1. **必须有图**：每页 >= 1 个视觉元素（图标/图表/图示/大数字），纯文字页不可交付
2. **卡片网格**：8 张 50 字卡片 >> 2 张 200 字卡片
3. **真实图标**：用图标库的 SVG 图标，不要用几何形状拼凑生物概念
4. **配色统一**：全 deck 同一个配色体系
5. **文献标注**：关键数据标注来源 (Author, Year, Journal)

## 图表决策

| 需求 | 推荐 |
|------|------|
| 常规数据 | Shape-first SVG（可编辑形状） |
| 柱/饼/线/散点 | Native chart replacement（23 种支持） |
| 流程/时间线/韦恩 | Shape-based 模板 |
