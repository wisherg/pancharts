---
name: "\"pancharts\""
description: "\"基于 pandas 数据结构（DataFrame/Series）创建 ECharts 可视化图表，支持渲染为 HTML 并保存图表配置、数据描述和洞察到数据库，还提供数据读取功能获取数据关键信息。Invoke when user wants to visualize data, generate charts, save chart configurations to database, or read data with key information.\""
---

# Pancharts 数据可视化技能

Pancharts 是一个基于 Python 的 ECharts 可视化库，专门用于将 pandas 数据结构（DataFrame 和 Series）转换为交互式的 ECharts 图表，并支持将图表配置、数据描述和数据洞察保存到 SQLite 数据库中。此外，还提供强大的数据读取功能，能够获取数据的关键信息。

---

## 核心功能

### 1. 数据结构与可视化类对应

Pancharts 首先判断 pandas 对象的数据结构，然后选择对应的可视化方案。每个可视化类对数据格式有严格要求：

| 数据结构 | pandas 类型 | 可视化类 | 参考文档 |
|---------|------------|---------|---------|
| **单列索引 + 单列数值** | `Series` | `k_v` | [basic-charts.md](references/basic-charts.md) |
| **多级索引 + 单列数值** | `MultiIndex Series` | `km_nv` | [hierarchical-charts.md](references/hierarchical-charts.md) |
| **双层索引 + 单列数值** | `MultiIndex Series` | `k2_nv` | [matrix-charts.md](references/matrix-charts.md) |
| **单列索引 + 多列数值** | `DataFrame` | `k_vm` | [multi-dimensional-charts.md](references/multi-dimensional-charts.md) |
| **地理坐标数据** | `DataFrame`（索引为地名，前两列为经纬度） | `gk_vm` | [geo-charts.md](references/geo-charts.md) |
| **高德地图数据** | `DataFrame` | `gk_vm_amap` | [geo-charts.md](references/geo-charts.md) |
| **Globe地球数据** | `DataFrame` | `gk_vm_globe` | [geo-charts.md](references/geo-charts.md) |
| **股票数据** | `DataFrame`（索引为日期，前四列为OHLC） | `sk_vm` | [stock-charts.md](references/stock-charts.md) |

### 2. 数据读取功能

**重要功能**：通过 `get_data()` 函数读取数据文件或数据库记录，获取数据的关键信息：

```python
from pancharts.utils import get_data

# 按ID查询
result = get_data(1)

# 按文件路径查询
result = get_data(r'E:\path\to\data.csv')

# 获取数据框
df = result['data']

# 获取数据描述（关键信息）
desc = result['desc']

# 获取数据信息（字段、缺失值、数据类型等）
info = result['data_info']
```

### 3. 数据库存储

- 将图表配置（option）保存到数据库
- 存储数据描述（data_desc）和数据洞察（data_insight）
- 支持标签分类（tag0, tag1）
- 支持导出为 Markdown 报告

### 4. AI 辅助配置

- `patch_option()`: 使用 AI 生成配置补丁并合并
- `modify_option()`: 使用 AI 生成完整配置
- 支持自然语言描述修改要求

### 数据格式严格对应关系

```
┌─────────────────────────────────────────────────────────────────┐
│                    数据结构 → 可视化类                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  k_v ←── Series (单列索引 + 单列数值)                            │
│                                                                 │
│  km_nv ←── Series (多级索引 + 单列数值)                          │
│                                                                 │
│  k2_nv ←── Series (双层索引 + 单列数值)                          │
│                                                                 │
│  k_vm ←── DataFrame (单列索引 + 多列数值)                        │
│           ↑                                                      │
│           └── rect_plot(): 灵活数据编码，支持多个对象比较          │
│                                                                 │
│  gk_vm ←── DataFrame (索引=地名, 第1-2列=经度/纬度, 后续=特征)    │
│                                                                 │
│  sk_vm ←── DataFrame (索引=日期字符串, 前4列=open/close/low/high) │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 快速开始

### 安装

```bash
pip install pancharts
```

### 基本使用流程

```python
from pancharts import k_v, Pancharts
import pandas as pd

# 准备数据
data = pd.Series([10, 20, 30, 40, 50], index=['A', 'B', 'C', 'D', 'E'])

# 创建图表（k_v类会自动判断数据结构）
chart = k_v(data).bar()

# 渲染输出
chart.render(output_dir='./output', filename='my_chart.html')
```

---

## 主要模块

### 1. pandas_charts.py
提供基于 pandas 数据结构的可视化类：
- `k_v`: 单列索引 Series 可视化
- `km_nv`: 多级索引 Series 可视化
- `k2_nv`: 双层索引 Series 可视化
- `k_vm`: DataFrame 可视化（支持 rect_plot 灵活编码）
- `gk_vm`: 地理数据可视化
- `gk_vm_amap`: 高德地图可视化
- `gk_vm_globe`: Globe 地球可视化
- `sk_vm`: 股票 K线图可视化

### 2. core.py
核心模块，包含 `Pancharts` 主类：
- 配置管理和合并
- HTML 渲染输出
- 数据库存储

### 3. chart_config.py
配置管理模块：
- AI API 配置
- 地图 API 配置
- 数据库路径配置
- 图表默认配置常量

### 4. utils.py
工具函数模块：
- JSON 序列化
- 颜色生成
- 数据类型判断
- 地理编码
- 数据库查询和导出

### 5. chartsdb
数据库管理模块：
- SQLite 数据库操作
- Web 管理界面

---

## 渲染输出

```python
# 渲染为 HTML 文件
chart.render(output_dir='./output', filename='chart.html')

# 渲染为 Jupyter Notebook
chart.render_notebook()

# 获取 HTML 嵌入片段
html = chart.render_emb()

# 转换为 pyecharts
py_chart = chart.to_pyecharts()
```

---

## 依赖要求

- Python >= 3.7
- pandas >= 1.0.0
- numpy >= 1.0.0
- jinja2 >= 3.0.0
- openai >= 1.0.0 (用于 AI 功能)
- requests >= 2.25.0

---

## ECharts Option 语法

Pancharts 使用标准的 ECharts 配置语法。示例：

```python
option = {
    "title": {"text": "图表标题"},
    "xAxis": {"type": "category", "data": ["A", "B", "C"]},
    "yAxis": {"type": "value"},
    "series": [{"type": "bar", "data": [10, 20, 30]}]
}
chart = Pancharts(option)
```

---

## 详细参考

请查看 `references/` 目录下的各功能文档：

| Topic | Reference | 触发关键词 |
|-------|-----------|-----------|
| 基础图表 | [basic-charts.md](references/basic-charts.md) | bar, line, scatter, pie, funnel, wordcloud, calendar, map |
| 层次数据可视化 | [hierarchical-charts.md](references/hierarchical-charts.md) | sunburst, treemap, tree |
| 矩阵与关系数据 | [matrix-charts.md](references/matrix-charts.md) | heatmap, sankey, bar3d, graph |
| 多维数据对比 | [multi-dimensional-charts.md](references/multi-dimensional-charts.md) | radar, parallel, rect_plot, vmap_size, vmap_color |
| 地理数据可视化 | [geo-charts.md](references/geo-charts.md) | geo_scatter, geo_heatmap, globe, amap |
| 股票数据可视化 | [stock-charts.md](references/stock-charts.md) | kline |
| 数据库存储与数据读取 | [database-storage.md](references/database-storage.md) | to_db, charts_md, get_chart, get_data |
| AI 辅助配置 | [ai-assistant.md](references/ai-assistant.md) | patch_option, modify_option |
