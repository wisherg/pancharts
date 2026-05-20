# 矩阵与关系数据 (k2_nv)

## 功能概述

`k2_nv` 类用于可视化 pandas 中的双层索引、单列数值型数据的序列（Series），适用于矩阵型和关系型数据的展示。

## 主要特性

- 自动将具有双层索引的 pandas Series 转换为 ECharts 可接受的数据格式
- 支持通过 config 参数传入额外的图表配置，与默认配置合并
- 提供关系型和三维数据可视化的图表类型
- 支持为图网络数据指定节点分类

## 支持的图表类型

| 方法 | 说明 | 参数 |
|------|------|------|
| `bar3d(config)` | 3D柱状图 | config: 额外配置字典 |
| `graph(config)` | 图网络 | config: 额外配置字典 |
| `sankey(config)` | 桑基图 | config: 额外配置字典 |
| `heatmap(config)` | 热力图 | config: 额外配置字典 |

## 使用示例

### 1. 热力图

```python
from pancharts import k2_nv
import pandas as pd

# 创建双层索引数据（通常由 groupby 产生）
data = pd.Series(
    [15, 25, 35, 45, 20, 30, 25, 35, 10, 15, 30, 40],
    index=pd.MultiIndex.from_product([
        ['产品A', '产品B', '产品C'],
        ['Q1', 'Q2', 'Q3', 'Q4']
    ])
)

chart = k2_nv(data).heatmap({
    "title": {"text": "产品季度销量热力图"},
    "series": [{
        "label": {"show": True}
    }]
})
chart.render(output_dir='./output', filename='heatmap.html')
```

### 2. 3D柱状图

```python
# 3D柱状图展示产品季度销量
data = pd.Series(
    [15, 25, 35, 45, 55, 65, 20, 30],
    index=pd.MultiIndex.from_product([
        ['产品A', '产品B', '产品C', '产品D'],
        ['Q1', 'Q2']
    ])
)

chart = k2_nv(data).bar3d({
    "title": {"text": "产品季度销量 3D 图"},
    "grid3D": {"viewControl": {"autoRotate": True}}
})
chart.render()
```

### 3. 桑基图

```python
# 桑基图展示用户行为流向
data = pd.Series(
    [100, 60, 40, 30, 30, 30, 40],
    index=pd.MultiIndex.from_tuples([
        ('访问', '首页'), ('访问', '商品'), ('访问', '促销'),
        ('首页', '商品'), ('首页', '促销'),
        ('商品', '下单'), ('促销', '下单')
    ])
)

chart = k2_nv(data).sankey({
    "title": {"text": "用户行为流向"},
    "series": [{
        "lineStyle": {"curveness": 0.5}
    }]
})
chart.render()
```

### 4. 关系图

```python
# 关系图展示社交网络
data = pd.Series(
    [10, 20, 15, 25, 30],
    index=['用户A', '用户B', '用户C', '用户D', '用户E']
)

chart = k2_nv(data).graph({
    "title": {"text": "社交网络关系"},
    "series": [{
        "layout": "force",
        "force": {"repulsion": 3000}
    }]
})
chart.render()
```

## 数据格式要求

```python
# 双层索引 Series
data = pd.Series(
    [值列表],
    index=pd.MultiIndex.from_product([
        ['第一层索引1', '第一层索引2'],
        ['第二层索引1', '第二层索引2']
    ])
)

# 示例
data = pd.Series(
    [15, 25, 35, 45],
    index=pd.MultiIndex.from_product([['产品A', '产品B'], ['Q1', 'Q2']])
)
```

## 辅助方法

| 方法 | 说明 |
|------|------|
| `bi_network_data()` | 生成图网络的节点和连接数据 |

## 常见配置选项

### 热力图配置

```python
{
    "xAxis": {"type": "category", "data": ["A", "B", "C"]},
    "yAxis": {"type": "category", "data": ["1", "2", "3"]},
    "visualMap": {
        "min": 0,
        "max": 100,
        "calculable": True,
        "orient": "horizontal",
        "left": "center",
        "bottom": "10%"
    }
}
```

### 桑基图配置

```python
{
    "series": [{
        "layout": "none",
        "emphasis": {
            "focus": "adjacency",
            "lineStyle": {"opacity": 1}
        },
        "lineStyle": {
            "curveness": 0.5,
            "opacity": 0.4
        }
    }]
}
```

### 3D柱状图配置

```python
{
    "grid3D": {
        "viewControl": {"autoRotate": True},
        "light": {
            "main": {"intensity": 1.2},
            "ambient": {"intensity": 0.3}
        }
    }
}
```
