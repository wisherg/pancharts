# 基础图表 (k_v)

## 功能概述

`k_v` 类用于可视化 pandas 中的单列索引序列数据（Series），支持多种常用图表类型。

## 主要特性

- 自动将 pandas Series 转换为 ECharts 可接受的数据格式
- 自动判断索引类型（category 或 value）与数值类型（category 或 value）
- 支持通过 config 参数传入额外的图表配置，与默认配置合并
- 提供多种常用图表类型的可视化方法

## 支持的图表类型

| 方法 | 说明 | 参数 |
|------|------|------|
| `bar(config)` | 柱状图 | config: 额外配置字典 |
| `line(config)` | 折线图 | config: 额外配置字典 |
| `scatter(config)` | 散点图 | config: 额外配置字典 |
| `escatter(config)` | 特效散点图 | config: 额外配置字典 |
| `pie(config)` | 饼图 | config: 额外配置字典 |
| `funnel(config)` | 漏斗图 | config: 额外配置字典 |
| `wordcloud(config)` | 词云图 | config: 额外配置字典 |
| `calendar(config)` | 日历热图 | config: 额外配置字典 |
| `map(map_name, config)` | 地图可视化 | map_name: 地图名称，config: 额外配置字典 |

## 使用示例

### 1. 柱状图

```python
from pancharts import k_v
import pandas as pd

# 创建数据
data = pd.Series([10, 25, 30, 45, 50], index=['北京', '上海', '广州', '深圳', '杭州'])

# 创建柱状图
chart = k_v(data).bar()
chart.render(output_dir='./output', filename='bar_chart.html')

# 带配置的柱状图
chart = k_v(data).bar({
    "title": {"text": "城市销量"},
    "series": [{
        "itemStyle": {"color": "#5470C6"}
    }]
})
chart.render()
```

### 2. 折线图

```python
data = pd.Series([120, 200, 150, 80, 70, 110, 130],
                 index=['周一', '周二', '周三', '周四', '周五', '周六', '周日'])

# 带面积填充和平滑曲线的折线图
chart = k_v(data).line({
    "title": {"text": "销售趋势"},
    "series": [{
        "areaStyle": {},
        "smooth": True
    }]
})
chart.render()
```

### 3. 饼图

```python
data = pd.Series([335, 310, 234, 135, 148, 520],
                 index=['直接访问', '邮件营销', '联盟广告', '视频广告', '搜索引擎', '其他'])

# 环形饼图
chart = k_v(data).pie({
    "title": {"text": "访问来源"},
    "series": [{
        "radius": ["40%", "70%"],
        "label": {"show": True}
    }]
})
chart.render()
```

### 4. 散点图

```python
data = pd.Series([10, 20, 30, 40, 50, 60, 70],
                 index=['A', 'B', 'C', 'D', 'E', 'F', 'G'])

chart = k_v(data).scatter({
    "series": [{
        "symbolSize": 20,
        "itemStyle": {"color": "#5470C6"}
    }]
})
chart.render()
```

### 5. 词云图

```python
data = pd.Series([100, 80, 60, 50, 40, 35, 30, 28, 25, 20],
                 index=['Python', 'JavaScript', 'Java', 'C++', 'Go', 
                        'Rust', 'TypeScript', 'Swift', 'Kotlin', 'Ruby'])

chart = k_v(data).wordcloud({
    "series": [{
        "shape": "cardioid",
        "sizeRange": [15, 80]
    }]
})
chart.render()
```

### 6. 日历热图

```python
import numpy as np
dates = pd.date_range('2024-01-01', periods=365)
values = np.random.randint(0, 100, 365)
data = pd.Series(values, index=dates)

chart = k_v(data).calendar({
    "series": [{
        "visualMap": {
            "min": 0,
            "max": 100,
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": "20%"
        }
    }]
})
chart.render()
```

### 7. 地图可视化

```python
data = pd.Series({
    '北京': 200, '上海': 180, '广东': 300, '浙江': 150,
    '江苏': 160, '四川': 100, '湖北': 90, '湖南': 85
})

chart = k_v(data).map(map_name='china', config={
    "title": {"text": "各省销售额分布"},
    "visualMap": {
        "min": 0, "max": 300,
        "left": "left", "top": "bottom",
        "text": ["高", "低"],
        "calculable": True
    }
})
chart.render()
```

## 数据格式要求

```python
# 单列索引 Series
pd.Series([值列表], index=[索引列表])

# 示例
data = pd.Series([10, 20, 30], index=['A', 'B', 'C'])
```

## 常见配置选项

### 标题配置

```python
{"title": {"text": "图表标题", "subtext": "副标题", "left": "center"}}
```

### 提示框配置

```python
{"tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}}}
```

### 图例配置

```python
{"legend": {"data": ["系列名"], "top": "5%"}}
```

### 系列配置

```python
{
    "series": [{
        "name": "系列名",
        "type": "bar",
        "data": [10, 20, 30],
        "label": {"show": True, "position": "top"}
    }]
}
```
