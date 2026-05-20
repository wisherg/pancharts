# 多维数据对比 (k_vm)

## 功能概述

`k_vm` 类用于可视化 pandas 中的单列索引、多列数值型数据的 DataFrame，适用于多维度数据的对比分析。

**重要：k_vm 支持 rect_plot 方法进行灵活的数据编码，能够支持多个对象数据的比较。**

## 数据格式要求

### k_vm 数据格式

```
DataFrame 结构：
├── 索引: 单列索引（任意类型）
└── 列: 多列数值型数据
```

**示例数据结构：**

```python
# 单列索引 + 多列数值
data = pd.DataFrame(
    [[1, 2, 3, 'a'], [4, 5, 6, 'b'], [7, 8, 9, 'c']],  # 3行4列
    columns=['x', 'y', 'z', 'w'],  # 列名
    index=['a', 'b', 'c']           # 单列索引
)
```

## 主要特性

- **自动将 pandas DataFrame 转换为 ECharts 可接受的数据格式**
- **支持通过 config 参数传入额外的图表配置，与默认配置合并**
- **提供多维数据可视化的图表类型**
- **支持灵活的数据编码方式（rect_plot 方法）**
- **支持数据的可视化映射（vmap_size 和 vmap_color 方法）**

## 支持的图表类型

| 方法 | 说明 | 参数 |
|------|------|------|
| `parallel(config)` | 平行坐标图 | config: 额外配置字典 |
| `radar(config)` | 雷达图 | config: 额外配置字典 |
| `rect_plot(series_type, encode_x, encode_y, config)` | **灵活数据编码绘图** | series_type: 图表类型，encode_x: x轴编码，encode_y: y轴编码，config: 额外配置 |

## rect_plot 灵活数据编码

`rect_plot` 方法是 k_vm 的核心功能，支持灵活的数据编码方式，能够从 DataFrame 中选择特定的列进行绑图，实现多个对象数据的比较。

### rect_plot 参数说明

```python
rect_plot(series_type, encode_x, encode_y, config)

参数：
- series_type: 图表类型（字符串或列表），如 'scatter', 'bar', 'line', 'effectScatter' 等
               当为列表时，需要与 encode_y 列表长度对应
- encode_x: X轴编码（列索引、列名或列表），指定哪一列作为X轴数据
- encode_y: Y轴编码（列索引、列名或列表），指定哪一列作为Y轴数据
            当为列表时，可在同一坐标系下绘制多个图表进行对比
- config: 额外配置字典
```

**重要特性：参数支持列表形式**

当 `series_type`、`encode_x`、`encode_y` 为列表时，可以在同一坐标系下绘制多个图表进行对比：

```python
# 在同一坐标系下绘制柱状图和折线图
vm.rect_plot(["bar", "line"], 0, [1, 2])

# 在同一坐标系下绘制两个散点图
vm.rect_plot("scatter", 0, [1, 2])

# 在同一坐标系下绘制不同类型的图表
vm.rect_plot(["scatter", "effectScatter"], 0, [1, 2])
```

### rect_plot 使用示例

```python
from pancharts import k_vm
import pandas as pd
import numpy as np

# 创建多维度数据
data = pd.DataFrame(
    np.random.rand(10, 4) * 100,
    columns=['价格', '销量', '满意度', '评分'],
    index=[f'产品{i}' for i in range(1, 11)]
)

vm = k_vm(data)

# 示例1：散点图 - 价格(X) vs 销量(Y)
chart = vm.rect_plot(series_type='scatter', encode_x=0, encode_y=1)
chart.render()

# 示例2：使用列名编码
chart = vm.rect_plot(series_type='scatter', encode_x='价格', encode_y='销量')
chart.render()

# 示例3：柱状图 - 满意度(X) vs 评分(Y)
chart = vm.rect_plot(series_type='bar', encode_x=2, encode_y=3)
chart.render()

# 示例4：同一坐标系下绘制多个图表对比
# 柱状图显示销量，折线图显示满意度
chart = vm.rect_plot(["bar", "line"], 0, [1, 2])
chart.render(output_dir='./output', filename='multi_chart.html')

# 示例5：同一坐标系下绘制两个散点图
chart = vm.rect_plot("scatter", 0, [1, 2])
chart.render()

# 示例6：特效散点图对比
chart = vm.rect_plot("effectScatter", 0, [1, 2])
chart.render()
```

### 列索引编号规则

对于 DataFrame 数据，列索引编号规则如下：
- **索引列**：作为标签显示，不参与数值计算
- **第0列**：DataFrame 的第一列（columns[0]）
- **第1列**：DataFrame 的第二列（columns[1]）
- 以此类推...

```python
# 数据结构示例
data = pd.DataFrame({
    '价格': [100, 200, 300],    # 第0列
    '销量': [50, 80, 120],      # 第1列
    '满意度': [85, 90, 95]       # 第2列
}, index=['产品A', '产品B', '产品C'])  # 索引列

vm = k_vm(data)

# 使用列索引
vm.rect_plot("scatter", 0, 1)  # 价格 vs 销量

# 使用列名
vm.rect_plot("scatter", '价格', '销量')  # 价格 vs 销量
```

## 使用示例

### 1. 雷达图

```python
from pancharts import k_vm
import pandas as pd
import numpy as np

# 创建多维度数据
data = pd.DataFrame(
    np.random.rand(5, 6) * 100,
    columns=['价格', '性能', '外观', '续航', '售后', '口碑'],
    index=['产品A', '产品B', '产品C', '产品D', '产品E']
)

chart = k_vm(data).radar({
    "title": {"text": "产品多维度对比"}
})
chart.render(output_dir='./output', filename='radar.html')
```

### 2. 平行坐标图

```python
# 平行坐标图分析学生成绩
data = pd.DataFrame(
    [[1, 2, 3, 'a'], [4, 5, 6, 'b'], [7, 8, 9, 'c']],  # 最后一列可以是类别型
    columns=['x', 'y', 'z', 'w'],
    index=['a', 'b', 'c']
)

chart = k_vm(data).parallel({
    "title": {"text": "学生成绩分析"}
})
chart.render()
```

### 3. 带颜色映射的散点图

```python
# 使用 rect_plot 绘制散点图
data = pd.DataFrame(
    np.random.rand(50, 4) * 100,
    columns=['价格', '销量', '满意度', '评分'],
    index=[f'产品{i}' for i in range(1, 51)]
)

vm = k_vm(data)

# 颜色映射 - 第3列（满意度）映射到颜色
color_config = vm.vmap_color(dimension=2, color=['#313695', '#fee090', '#f46d43'])
chart = vm.rect_plot(
    series_type='scatter',
    encode_x=0,  # X轴：价格
    encode_y=1,  # Y轴：销量
    config=color_config
)
chart.render()
```

### 4. 带大小映射的散点图

```python
# 大小映射 - 第3列映射到点大小
size_config = vm.vmap_size(dimension=2, symbolSize=[5, 30])
chart = vm.rect_plot(
    series_type='scatter',
    encode_x=0,
    encode_y=1,
    config=size_config
)
chart.render()
```

### 5. 多对象数据比较

```python
# 多个对象的多维度比较
data = pd.DataFrame({
    '数学': [85, 92, 78, 90, 88],
    '语文': [90, 88, 82, 85, 92],
    '英语': [78, 95, 85, 88, 80],
    '物理': [92, 85, 90, 78, 88],
    '化学': [88, 90, 85, 92, 85]
}, index=['学生A', '学生B', '学生C', '学生D', '学生E'])

vm = k_vm(data)

# 比较不同学生的成绩分布
chart = vm.rect_plot(
    series_type='scatter',
    encode_x='数学',
    encode_y='语文',
    config={
        "title": {"text": "学生成绩对比：数学 vs 语文"},
        "series": [{
            "label": {"show": True}
        }]
    }
)
chart.render()
```

## 可视化映射方法

### vmap_size

配置点大小映射：

```python
vm = k_vm(data)
size_map = vm.vmap_size(dimension=2, symbolSize=[5, 20])
chart = vm.rect_plot(series_type='scatter', encode_x=0, encode_y=1, config=size_map)
```

### vmap_color

配置颜色映射：

```python
vm = k_vm(data)
color_map = vm.vmap_color(dimension=2, color=['#ff0000', '#00ff00'])
chart = vm.rect_plot(series_type='scatter', encode_x=0, encode_y=1, config=color_map)
```

## 常见配置选项

### 雷达图配置

```python
{
    "radar": {
        "indicator": [
            {"name": "指标1", "max": 100},
            {"name": "指标2", "max": 100},
            {"name": "指标3", "max": 100}
        ],
        "shape": "polygon",
        "splitNumber": 5
    }
}
```

### 平行坐标图配置

```python
{
    "parallel": {
        "left": "5%",
        "right": "13%",
        "bottom": "10%",
        "top": "10%",
        "parallelAxisDefault": {
            "type": "value",
            "nameLocation": "end",
            "nameGap": 20
        }
    }
}
```

### 散点图配置

```python
{
    "series": [{
        "type": "scatter",
        "symbolSize": 15,
        "itemStyle": {
            "opacity": 0.8
        },
        "label": {
            "show": True,
            "position": "right"
        }
    }]
}
```

## 完整示例

```python
from pancharts import k_vm
import pandas as pd
import numpy as np

# 创建产品对比数据
np.random.seed(42)
data = pd.DataFrame({
    '价格': np.random.randint(100, 1000, 10),
    '销量': np.random.randint(50, 500, 10),
    '满意度': np.random.randint(60, 100, 10),
    '评分': np.random.randint(3, 5, 10) + np.random.rand(10)
}, index=[f'产品{i}' for i in range(1, 11)])

vm = k_vm(data)

# 绘制散点图：价格 vs 销量，颜色映射满意度
color_map = vm.vmap_color(dimension=2, color=['#313695', '#74add1', '#abd9e9', '#fee090', '#f46d43'])
chart = vm.rect_plot(
    series_type='scatter',
    encode_x='价格',
    encode_y='销量',
    config={
        "title": {"text": "产品分析：价格与销量关系"},
        "tooltip": {"trigger": "item"},
        **color_map
    }
)

chart.render(output_dir='./output', filename='product_analysis.html')
```

## 注意事项

1. **数据类型**：DataFrame 的列应该是数值型，最后一列可以是类别型
2. **索引**：单列索引，用于标识不同的数据点或对象
3. **编码灵活**：使用 encode_x 和 encode_y 参数可以选择任意列进行绑图
4. **可视化映射**：vmap_size 和 vmap_color 的 dimension 参数从 0 开始计数
