# 层次数据可视化 (km_nv)

## 功能概述

`km_nv` 类用于可视化 pandas 中的多级索引、单列数值型数据的序列（Series），适用于层次化数据的展示。

## 主要特性

- 自动将具有多级索引的 pandas Series 转换为树形数据结构
- 支持通过 config 参数传入额外的图表配置，与默认配置合并
- 提供层次化数据可视化的图表类型
- 自动为不同层级节点生成随机颜色

## 支持的图表类型

| 方法 | 说明 | 参数 |
|------|------|------|
| `sunburst(config)` | 旭日图 | config: 额外配置字典 |
| `treemap(num, config)` | 矩形树图 | num: 可选的根节点索引，config: 额外配置字典 |
| `tree(num, config)` | 树图 | num: 可选的根节点索引，config: 额外配置字典 |

## 使用示例

### 1. 旭日图

```python
from pancharts import km_nv
import pandas as pd

# 创建多级索引数据
index = pd.MultiIndex.from_product([
    ['亚洲', '欧洲', '美洲'],           # 第一级：大洲
    ['中国', '日本', '德国', '法国', '美国', '加拿大'],  # 第二级：国家
], names=['大洲', '国家'])

data = pd.Series([1400, 1200, 800, 700, 3100, 280], index=index)

chart = km_nv(data).sunburst({
    "title": {"text": "各国人口分布（单位：百万）"}
})
chart.render(output_dir='./output', filename='sunburst.html')
```

### 2. 矩形树图

```python
# 创建产品类别层次数据
index = pd.MultiIndex.from_product([
    ['电子产品', '服装', '食品'],
    ['手机', '电脑', 'T恤', '裤子', '零食', '饮料'],
], names=['类别', '商品'])
data = pd.Series([5000, 8000, 3000, 2500, 4000, 2000], index=index)

chart = km_nv(data).treemap({
    "title": {"text": "商品销售占比"}
})
chart.render()
```

### 3. 树图

```python
# 创建组织结构数据
index = pd.MultiIndex.from_tuples([
    ('公司总部', '研发部', '前端组'),
    ('公司总部', '研发部', '后端组'),
    ('公司总部', '市场部', '策划组'),
    ('公司总部', '市场部', '运营组'),
], names=['层级1', '层级2', '层级3'])
data = pd.Series([10, 15, 8, 12], index=index)

chart = km_nv(data).tree({
    "title": {"text": "公司组织结构"}
})
chart.render()
```

### 4. 三层索引数据

```python
# 创建三层索引数据
index = pd.MultiIndex.from_product([
    ['华东', '华南'],      # 第一级：区域
    ['一线城市', '二线城市'],  # 第二级：城市等级
    ['高收入', '低收入']    # 第三级：收入等级
])
data = pd.Series([100, 80, 60, 40, 90, 70, 50, 30], index=index)

# 旭日图 - 展示完整层次结构
chart = km_nv(data).sunburst()
chart.render(output_dir='./output', filename='sunburst_hierarchy.html')
```

## 数据格式要求

```python
# 多级索引 Series
index = pd.MultiIndex.from_product([
    ['一级索引1', '一级索引2'],
    ['二级索引1', '二级索引2']
])
data = pd.Series([值列表], index=index)

# 或使用元组创建
index = pd.MultiIndex.from_tuples([
    ('A', 'a'), ('A', 'b'), ('B', 'a'), ('B', 'b')
])
data = pd.Series([值列表], index=index)
```

## 辅助方法

| 方法 | 说明 |
|------|------|
| `sun_tree()` | 生成旭日图数据结构 |
| `tree_data()` | 生成树图数据结构 |
| `treemap_data()` | 生成矩形树图数据结构 |
| `get_color(key)` | 为节点生成随机颜色 |

## 常见配置选项

### 旭日图配置

```python
{
    "series": [{
        "radius": ["15%", "90%"],
        "center": ["50%", "50%"],
        "sort": None,
        "emphasis": {
            "focus": "ancestor"
        }
    }]
}
```

### 矩形树图配置

```python
{
    "series": [{
        "roam": True,
        "nodeGap": 0,
        "label": {
            "show": True,
            "formatter": "{b}: {c}"
        }
    }]
}
```

### 树图配置

```python
{
    "series": [{
        "layout": "orthogonal",
        "orient": "LR",
        "symbol": "circle",
        "symbolSize": 7
    }]
}
```
