# Pancharts 项目教程文档

## 目录
1. [pandas_charts.py - pandas数据可视化模块](#pandas_chartspy)
2. [core.py - 核心模块](#corepy)
3. [utils.py - 工具模块](#utilspy)

---

## pandas_charts.py

pandas_charts.py 是 Pancharts 项目中专门用于基于 pandas 数据结构进行可视化的模块，提供了多个类来处理不同类型的 pandas 数据。

### 1. k_v 类

**功能**：用于可视化 pandas 中的单列索引序列数据（Series）。

**主要特性**：
- 自动将 pandas Series 转换为 ECharts 可接受的数据格式
- 自动判断索引类型（category或value）与数值类型（category或value）
- 支持通过 config 参数传入额外的图表配置，与默认配置合并
- 提供多种常用图表类型的可视化方法

**支持的图表类型**：
- bar: 柱状图
- line: 折线图
- scatter: 散点图
- escatter: 增强散点图
- pie: 饼图
- funnel: 漏斗图
- wordcloud: 词云图
- calendar: 日历热图
- map: 地图可视化

**主要方法**：

| 方法 | 说明 | 参数 |
|------|------|------|
| `bar(config)` | 绘制柱状图 | config: 额外配置字典 |
| `line(config)` | 绘制折线图 | config: 额外配置字典 |
| `scatter(config)` | 绘制散点图 | config: 额外配置字典 |
| `escatter(config)` | 绘制增强散点图 | config: 额外配置字典 |
| `pie(config)` | 绘制饼图 | config: 额外配置字典 |
| `funnel(config)` | 绘制漏斗图 | config: 额外配置字典 |
| `wordcloud(config)` | 绘制词云图 | config: 额外配置字典 |
| `calendar(config)` | 绘制日历热图 | config: 额外配置字典 |
| `map(map_name, config)` | 绘制地图 | map_name: 地图名称，config: 额外配置字典 |

**示例代码**：
```python
from pancharts import k_v
import pandas as pd

# 创建数据
data = pd.Series([10, 25, 30, 45, 50], index=['北京', '上海', '广州', '深圳', '杭州'])

# 创建k_v实例并绘制柱状图
chart = k_v(data).bar()
chart.render()

# 绘制饼图
chart = k_v(data).pie()
chart.render()
```

---

### 2. km_nv 类

**功能**：用于可视化 pandas 中的多列索引、单列数值型数据的序列（Series）。

**主要特性**：
- 自动将具有多级索引的 pandas Series 转换为树形数据结构
- 支持通过 config 参数传入额外的图表配置，与默认配置合并
- 提供层次化数据可视化的图表类型
- 自动为不同层级节点生成随机颜色

**支持的图表类型**：
- sunburst: 旭日图
- treemap: 矩形树图
- tree: 树图

**主要方法**：

| 方法 | 说明 | 参数 |
|------|------|------|
| `sunburst(config)` | 绘制旭日图 | config: 额外配置字典 |
| `treemap(num, config)` | 绘制矩形树图 | num: 可选的根节点索引，config: 额外配置字典 |
| `tree(num, config)` | 绘制树图 | num: 可选的根节点索引，config: 额外配置字典 |

**辅助方法**：
- `sun_tree()`: 生成旭日图数据结构
- `tree_data()`: 生成树图数据结构
- `treemap_data()`: 生成矩形树图数据结构
- `get_color(key)`: 为节点生成随机颜色

**示例代码**：
```python
from pancharts import km_nv
import pandas as pd

# 创建具有多级索引的数据
index = pd.MultiIndex.from_product([['华东', '华南'], ['一线城市', '二线城市'], ['高收入', '中等收入']])
data = pd.Series([100, 80, 60, 40, 90, 70, 50, 30], index=index)

# 绘制旭日图
chart = km_nv(data).sunburst()
chart.render()

# 绘制矩形树图
chart = km_nv(data).treemap()
chart.render()
```

---

### 3. k2_nv 类

**功能**：用于可视化 pandas 中的两层索引、单列数值型数据的序列（Series）。

**主要特性**：
- 自动将具有双层索引的 pandas Series 转换为 ECharts 可接受的数据格式
- 支持通过 config 参数传入额外的图表配置，与默认配置合并
- 提供关系型和三维数据可视化的图表类型
- 支持为图网络数据指定节点分类

**支持的图表类型**：
- bar3d: 3D柱状图
- graph: 图网络
- sankey: 桑基图
- heatmap: 热力图

**主要方法**：

| 方法 | 说明 | 参数 |
|------|------|------|
| `bar3d(config)` | 绘制3D柱状图 | config: 额外配置字典 |
| `graph(config)` | 绘制图网络 | config: 额外配置字典 |
| `sankey(config)` | 绘制桑基图 | config: 额外配置字典 |
| `heatmap(config)` | 绘制热力图 | config: 额外配置字典 |

**辅助方法**：
- `bi_network_data()`: 生成图网络的节点和连接数据

**示例代码**：
```python
from pancharts import k2_nv
import pandas as pd

# 创建具有双层索引的数据（通常由两列groupby产生）
data = pd.Series(
    [15, 25, 35, 45, 55, 65],
    index=pd.MultiIndex.from_product([['产品A', '产品B', '产品C'], ['Q1', 'Q2']])
)

# 绘制热力图
chart = k2_nv(data).heatmap()
chart.render()

# 绘制3D柱状图
chart = k2_nv(data).bar3d()
chart.render()
```

---

### 4. k_vm 类

**功能**：用于可视化 pandas 中的单列索引、多列数值型数据的 DataFrame。

**主要特性**：
- 自动将 pandas DataFrame 转换为 ECharts 可接受的数据格式
- 支持通过 config 参数传入额外的图表配置，与默认配置合并
- 提供多维数据可视化的图表类型
- 支持灵活的数据编码方式（rect_plot方法）
- 支持数据的可视化映射（vmap_size和vmap_color方法）

**支持的图表类型**：
- parallel: 平行坐标图
- radar: 雷达图
- rect_plot: 灵活数据编码方式，支持多种二维图表

**主要方法**：

| 方法 | 说明 | 参数 |
|------|------|------|
| `parallel(config)` | 绘制平行坐标图 | config: 额外配置字典 |
| `radar(config)` | 绘制雷达图 | config: 额外配置字典 |
| `rect_plot(series_type, encode_x, encode_y, config)` | 灵活数据编码绘图 | series_type: 图表类型，encode_x: x轴编码，encode_y: y轴编码，config: 额外配置 |
| `vmap_size(dimension, symbolSize)` | 配置点大小映射 | dimension: 维度索引，symbolSize: 点大小范围 |
| `vmap_color(dimension, color)` | 配置颜色映射 | dimension: 维度索引，color: 颜色范围 |

**辅助方法**：
- `parallel_schema()`: 生成平行坐标图的轴配置
- `radar_schema()`: 生成雷达图的指示器配置
- `radar_data()`: 生成雷达图数据

**示例代码**：
```python
from pancharts import k_vm
import pandas as pd
import numpy as np

# 创建数据
data = pd.DataFrame(
    np.random.rand(10, 5),
    columns=['价格', '销量', '利润', '库存', '评分'],
    index=[f'产品{i}' for i in range(1, 11)]
)

# 绘制雷达图
chart = k_vm(data).radar()
chart.render()

# 使用rect_plot绘制散点图，使用vmap_color进行颜色映射
vm = k_vm(data)
color_map = vm.vmap_color(dimension=2, color=['#ff0000', '#00ff00'])
chart = vm.rect_plot(series_type='scatter', encode_x=0, encode_y=1, config=color_map)
chart.render()
```

---

## core.py

core.py 是 Pancharts 项目的核心模块，包含主要的 Pancharts 类和渲染逻辑。

### Pancharts 类

**功能**：ECharts 可视化生成类，负责配置管理和 HTML 渲染。

**初始化参数**：
- `user_option`: dict, optional - 用户配置选项，优先级最高
- `data_config`: dict, optional - 数据配置项
- `graph_config`: dict, optional - 图形配置项

**主要属性**：

| 属性 | 说明 |
|------|------|
| `option` | 获取或设置 ECharts 配置（property） |
| `echarts_source` | echarts 资源来源，可选 "local" 或 "online" |
| `is_map_chart` | 是否为地图图表 |
| `map_name` | 地图名称 |

**主要方法**：

#### 1. 配置管理方法

| 方法 | 说明 | 参数 |
|------|------|------|
| `option` (property) | 获取合并后的配置 | - |
| `option.setter` | 设置用户配置 | value: 配置字典 |
| `dmerge(dict2)` | 递归合并配置字典 | dict2: 要合并的配置 |
| `modify_option(prompt, api_key, base_url, model_name)` | 使用 AI 修改 option | prompt: 修改要求，其他参数可选 |
| `patch_option(prompt, api_key, base_url, model_name)` | 使用 AI 生成补丁合并 | prompt: 修改要求，其他参数可选 |

#### 2. 渲染方法

| 方法 | 说明 | 参数 |
|------|------|------|
| `render(output_dir, filename)` | 渲染为 HTML 文件 | output_dir: 输出目录，filename: 文件名 |
| `render_notebook()` | 渲染为 Jupyter Notebook 可用内容 | - |

**示例代码**：
```python
from pancharts import Pancharts

# 方式1：创建实例时传入option
option = {
    "title": {"text": "简单示例"},
    "xAxis": {"data": ["A", "B", "C", "D", "E"]},
    "yAxis": {},
    "series": [{"type": "bar", "data": [10, 20, 30, 40, 50]}]
}
chart = Pancharts(option)
chart.render()

# 方式2：通过属性赋值
chart = Pancharts()
chart.option = option
chart.render()

# 使用dmerge合并配置
chart = Pancharts(option)
additional_config = {"title": {"subtext": "副标题"}}
chart.dmerge(additional_config)
chart.render()
```

---

## utils.py

utils.py 是 Pancharts 项目的工具模块，包含各种辅助函数。

### 主要函数

| 函数 | 说明 | 参数 | 返回值 |
|------|------|------|--------|
| `add_quotes_to_keys(json_str)` | 为字典字符串中的键添加双引号 | json_str: 字典字符串 | 处理后的字符串 |
| `random_color()` | 生成随机颜色代码 | - | 十六进制颜色字符串 |
| `random_color_list(n)` | 生成随机颜色列表 | n: 列表长度 | 颜色列表 |
| `get_index_type(x)` | 判断 DataFrame 索引类型 | x: DataFrame | "category", "time" 或 "value" |
| `get_value_type(x)` | 判断 Series 值类型 | x: Series | "category", "time" 或 "value" |
| `deep_merge(dict1, dict2)` | 递归合并两个字典 | dict1, dict2: 要合并的字典 | 合并后的字典 |
| `get_config_file_path()` | 获取配置文件路径 | - | chart_config.py 的绝对路径 |
| `load_city_cnname()` | 加载城市中文名称数据 | - | DataFrame |
| `load_city_lnglat()` | 加载城市经纬度数据 | - | DataFrame |
| `load_countries_info()` | 加载国家信息数据 | - | DataFrame |

**示例代码**：
```python
from pancharts.utils import random_color, random_color_list, deep_merge

# 生成随机颜色
color = random_color()
print(color)  # 例如: #3a7bc8

# 生成颜色列表
colors = random_color_list(5)
print(colors)  # 例如: ['#a1b2c3', '#d4e5f6', ...]

# 深度合并字典
dict1 = {"a": 1, "b": {"c": 2}}
dict2 = {"b": {"d": 3}, "e": 4}
merged = deep_merge(dict1, dict2)
print(merged)  # {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}
```

---

## 快速开始

### 安装

```bash
pip install pancharts
```

### 基本使用流程

1. **导入必要的模块**
```python
from pancharts import k_v, Pancharts
import pandas as pd
```

2. **准备数据**
```python
data = pd.Series([10, 20, 30, 40, 50], index=['A', 'B', 'C', 'D', 'E'])
```

3. **创建图表**
```python
chart = k_v(data).bar()
```

4. **渲染图表**
```python
chart.render(output_dir='./output', filename='my_chart.html')
```

---

## 注意事项

1. 所有图表方法都返回 Pancharts 实例，可以链式调用
2. config 参数会与默认配置合并，优先级最高
3. 地图图表需要指定正确的地图名称
4. AI 功能需要配置 API 密钥（详见 chart_config.py）
