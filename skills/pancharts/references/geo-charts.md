# 地理数据可视化 (gk_vm)

## 功能概述

`gk_vm` 类用于可视化地理坐标数据，支持地理散点图、热力图、飞线图等多种地理可视化方式。

**重要：数据结构必须严格匹配，否则无法正确显示。**

## 数据格式要求（严格）

### gk_vm 地理数据格式

```
DataFrame 结构：
├── 索引: 地理位置名称（城市名、省份名等）
├── 第1列: 经度 (longitude)
├── 第2列: 纬度 (latitude)
└── 后续列: 其他特征值（用于可视化映射）
```

**示例数据结构：**

```python
# 索引为地名，前两列必须为经度、纬度
geo_df = pd.DataFrame({
    'lng': [116.46, 121.48, 113.23],  # 第1列：经度
    'lat': [39.92, 31.22, 23.16],     # 第2列：纬度
    '人口': [800, 900, 700],           # 后续列：特征值
    '收入': [90, 70, 50]               # 后续列：特征值
}, index=['北京', '上海', '广州'])

# 可视化时，dimension 参数指定使用哪一列进行视觉映射
# dimension=2 表示使用第3列（人口）
# dimension=3 表示使用第4列（收入）
```

## 主要特性

- 支持多种地理坐标系（ECharts 内置地图、高德地图、Globe 地球）
- 支持数据的视觉映射（点大小、颜色）
- 支持 2D 和 3D 地理可视化
- 提供丰富的地图交互功能

## 支持的图表类型

| 方法 | 说明 | 参数 |
|------|------|------|
| `scatter(dimension, visual_type, config)` | 地理散点图 | dimension: 映射列索引，visual_type: 可视化类型，config: 额外配置 |
| `escatter(dimension, visual_type, config)` | 特效散点图 | dimension: 映射列索引，visual_type: 可视化类型，config: 额外配置 |
| `heatmap(dimension, visual_type, config)` | 地理热力图 | dimension: 映射列索引，visual_type: 可视化类型，config: 额外配置 |
| `graph(edges, config)` | 地理关系图 | edges: 边列表，config: 额外配置 |
| `bar3d(dimension, visual_type, config)` | 3D地理柱状图 | dimension: 映射列索引，visual_type: 可视化类型，config: 额外配置 |
| `line3d(coords, config)` | 3D飞线图 | coords: 坐标列表，config: 额外配置 |

## 使用示例

### 1. 地理散点图

```python
from pancharts import gk_vm
import pandas as pd

# 创建地理数据（索引为城市名，前两列为经纬度）
geo_df = pd.DataFrame({
    'lng': [116.46, 121.48, 113.23, 114.07, 104.06],  # 经度
    'lat': [39.92, 31.22, 23.16, 22.62, 30.67],        # 纬度
    '人口': [800, 900, 700, 600, 500],                    # 第3列
    '收入': [90, 70, 50, 40, 20]                          # 第4列
}, index=['北京', '上海', '广州', '深圳', '成都'])

# 创建地理可视化
chinamap = gk_vm(geo_df, "china")

# dimension=2 使用第3列（人口）进行视觉映射
chart = chinamap.scatter(dimension=2, visual_type='color')
chart.render(output_dir='./output', filename='geo_scatter.html')
```

### 2. 特效散点图

```python
# 特效散点图（涟漪效果）
chart = chinamap.escatter(dimension=3, visual_type='color')  # 使用收入列
chart.render()
```

### 3. 地理热力图

```python
# 地理热力图
chart = chinamap.heatmap(dimension=2, visual_type='heatmap')
chart.render()
```

### 4. 3D飞线图

```python
# 3D飞线图 - 展示航线或迁徙
# coords 格式: [[起点lng, 起点lat, 终点lng, 终点lat], ...]
chart = chinamap.line3d(
    coords=[
        [116.46, 39.92, 121.48, 31.22],  # 北京到上海
        [116.46, 39.92, 113.23, 23.16],  # 北京到广州
        [121.48, 31.22, 113.23, 23.16],  # 上海到广州
    ],
    config={"title": {"text": "航线分布"}}
)
chart.render()
```

## Globe 地球可视化

### Globe 散点图

```python
from pancharts import gk_vm_globe

# Globe 3D散点图
chart = gk_vm_globe(geo_df).scatter(
    dimension=2,
    visual_type='size',
    config={"globe": {"globeType": "realistic"}}
)
chart.render()
```

### Globe 类型

| 类型 | 说明 |
|------|------|
| `basic` | 基础配置 |
| `night` | 夜景模式 |
| `realistic` | 真实感渲染 |
| `terrain` | 地形渲染 |

## 高德地图可视化

```python
from pancharts import gk_vm_amap

# 高德地图散点图
chart = gk_vm_amap(geo_df).scatter(dimension=2, visual_type='size')
chart.render()
```

## 常用配置选项

### 地理坐标系配置

```python
{
    "geo": {
        "map": "china",
        "zoom": 5,
        "center": [104.114129, 37.550339],
        "roam": True,
        "label": {"show": True}
    }
}
```

### 视觉映射配置

```python
{
    "visualMap": {
        "min": 0,
        "max": 100,
        "calculable": True,
        "inRange": {
            "color": ["#313695", "#4575b4", "#74add1", "#abd9e9"]
        }
    }
}
```

## 注意事项

1. **列顺序固定**：前两列必须是经度和纬度，不能颠倒
2. **地名匹配**：索引中的地名必须与地图数据中的名称完全匹配
3. **dimension 参数**：从第3列开始计数（dimension=2 表示第3列）
