# Pancharts Project Tutorial

## Table of Contents
1. [pandas_charts.py - Pandas Data Visualization Module](#pandas_chartspy)
2. [core.py - Core Module](#corepy)
3. [utils.py - Utility Module](#utilspy)

---

## pandas_charts.py

pandas_charts.py is the module in the Pancharts project specifically designed for visualizing pandas data structures, providing multiple classes to handle different types of pandas data.

### 1. k_v Class

**Function**: Visualizes single-column index series data (Series) in pandas.

**Key Features**:
- Automatically converts pandas Series to ECharts-acceptable data format
- Automatically determines index type (category or value) and value type (category or value)
- Supports passing additional chart configurations via config parameter, merging with default configurations
- Provides visualization methods for various common chart types

**Supported Chart Types**:
- bar: Bar chart
- line: Line chart
- scatter: Scatter chart
- escatter: Enhanced scatter chart
- pie: Pie chart
- funnel: Funnel chart
- wordcloud: Word cloud
- calendar: Calendar heatmap
- map: Map visualization

**Main Methods**:

| Method | Description | Parameters |
|--------|-------------|------------|
| `bar(config)` | Draw bar chart | config: Additional configuration dict |
| `line(config)` | Draw line chart | config: Additional configuration dict |
| `scatter(config)` | Draw scatter chart | config: Additional configuration dict |
| `escatter(config)` | Draw enhanced scatter chart | config: Additional configuration dict |
| `pie(config)` | Draw pie chart | config: Additional configuration dict |
| `funnel(config)` | Draw funnel chart | config: Additional configuration dict |
| `wordcloud(config)` | Draw word cloud | config: Additional configuration dict |
| `calendar(config)` | Draw calendar heatmap | config: Additional configuration dict |
| `map(map_name, config)` | Draw map | map_name: Map name, config: Additional configuration dict |

**Example Code**:
```python
from pancharts import k_v
import pandas as pd

# Create data
data = pd.Series([10, 25, 30, 45, 50], index=['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Hangzhou'])

# Create k_v instance and draw bar chart
chart = k_v(data).bar()
chart.render()

# Draw pie chart
chart = k_v(data).pie()
chart.render()
```

---

### 2. km_nv Class

**Function**: Visualizes multi-column index, single-column numeric data series (Series) in pandas.

**Key Features**:
- Automatically converts pandas Series with multi-level indexes to tree data structures
- Supports passing additional chart configurations via config parameter, merging with default configurations
- Provides hierarchical data visualization chart types
- Automatically generates random colors for different level nodes

**Supported Chart Types**:
- sunburst: Sunburst chart
- treemap: Treemap
- tree: Tree chart

**Main Methods**:

| Method | Description | Parameters |
|--------|-------------|------------|
| `sunburst(config)` | Draw sunburst chart | config: Additional configuration dict |
| `treemap(num, config)` | Draw treemap | num: Optional root node index, config: Additional configuration dict |
| `tree(num, config)` | Draw tree chart | num: Optional root node index, config: Additional configuration dict |

**Helper Methods**:
- `sun_tree()`: Generate sunburst chart data structure
- `tree_data()`: Generate tree chart data structure
- `treemap_data()`: Generate treemap data structure
- `get_color(key)`: Generate random color for node

**Example Code**:
```python
from pancharts import km_nv
import pandas as pd

# Create data with multi-level index
index = pd.MultiIndex.from_product([['East China', 'South China'], ['Tier 1', 'Tier 2'], ['High Income', 'Medium Income']])
data = pd.Series([100, 80, 60, 40, 90, 70, 50, 30], index=index)

# Draw sunburst chart
chart = km_nv(data).sunburst()
chart.render()

# Draw treemap
chart = km_nv(data).treemap()
chart.render()
```

---

### 3. k2_nv Class

**Function**: Visualizes two-level index, single-column numeric data series (Series) in pandas.

**Key Features**:
- Automatically converts pandas Series with two-level indexes to ECharts-acceptable data format
- Supports passing additional chart configurations via config parameter, merging with default configurations
- Provides relational and 3D data visualization chart types
- Supports specifying node categories for graph network data

**Supported Chart Types**:
- bar3d: 3D bar chart
- graph: Graph network
- sankey: Sankey diagram
- heatmap: Heatmap

**Main Methods**:

| Method | Description | Parameters |
|--------|-------------|------------|
| `bar3d(config)` | Draw 3D bar chart | config: Additional configuration dict |
| `graph(config)` | Draw graph network | config: Additional configuration dict |
| `sankey(config)` | Draw Sankey diagram | config: Additional configuration dict |
| `heatmap(config)` | Draw heatmap | config: Additional configuration dict |

**Helper Methods**:
- `bi_network_data()`: Generate nodes and links data for graph network

**Example Code**:
```python
from pancharts import k2_nv
import pandas as pd

# Create data with two-level index (usually generated by two-column groupby)
data = pd.Series(
    [15, 25, 35, 45, 55, 65],
    index=pd.MultiIndex.from_product([['Product A', 'Product B', 'Product C'], ['Q1', 'Q2']])
)

# Draw heatmap
chart = k2_nv(data).heatmap()
chart.render()

# Draw 3D bar chart
chart = k2_nv(data).bar3d()
chart.render()
```

---

### 4. k_vm Class

**Function**: Visualizes single-column index, multi-column numeric DataFrame in pandas.

**Key Features**:
- Automatically converts pandas DataFrame to ECharts-acceptable data format
- Supports passing additional chart configurations via config parameter, merging with default configurations
- Provides multi-dimensional data visualization chart types
- Supports flexible data encoding (rect_plot method)
- Supports data visualization mapping (vmap_size and vmap_color methods)

**Supported Chart Types**:
- parallel: Parallel coordinates
- radar: Radar chart
- rect_plot: Flexible data encoding, supporting various 2D charts

**Main Methods**:

| Method | Description | Parameters |
|--------|-------------|------------|
| `parallel(config)` | Draw parallel coordinates | config: Additional configuration dict |
| `radar(config)` | Draw radar chart | config: Additional configuration dict |
| `rect_plot(series_type, encode_x, encode_y, config)` | Flexible data encoding plotting | series_type: Chart type, encode_x: x-axis encoding, encode_y: y-axis encoding, config: Additional configuration |
| `vmap_size(dimension, symbolSize)` | Configure point size mapping | dimension: Dimension index, symbolSize: Point size range |
| `vmap_color(dimension, color)` | Configure color mapping | dimension: Dimension index, color: Color range |

**Helper Methods**:
- `parallel_schema()`: Generate axis configuration for parallel coordinates
- `radar_schema()`: Generate indicator configuration for radar chart
- `radar_data()`: Generate radar chart data

**Example Code**:
```python
from pancharts import k_vm
import pandas as pd
import numpy as np

# Create data
data = pd.DataFrame(
    np.random.rand(10, 5),
    columns=['Price', 'Sales', 'Profit', 'Inventory', 'Rating'],
    index=[f'Product{i}' for i in range(1, 11)]
)

# Draw radar chart
chart = k_vm(data).radar()
chart.render()

# Use rect_plot to draw scatter chart with vmap_color for color mapping
vm = k_vm(data)
color_map = vm.vmap_color(dimension=2, color=['#ff0000', '#00ff00'])
chart = vm.rect_plot(series_type='scatter', encode_x=0, encode_y=1, config=color_map)
chart.render()
```

---

## core.py

core.py is the core module of the Pancharts project, containing the main Pancharts class and rendering logic.

### Pancharts Class

**Function**: ECharts visualization generation class, responsible for configuration management and HTML rendering.

**Initialization Parameters**:
- `user_option`: dict, optional - User configuration option, highest priority
- `data_config`: dict, optional - Data configuration
- `graph_config`: dict, optional - Graph configuration

**Main Properties**:

| Property | Description |
|----------|-------------|
| `option` | Get or set ECharts configuration (property) |
| `echarts_source` | echarts resource source, "local" or "online" |
| `is_map_chart` | Whether it's a map chart |
| `map_name` | Map name |

**Main Methods**:

#### 1. Configuration Management Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `option` (property) | Get merged configuration | - |
| `option.setter` | Set user configuration | value: Configuration dict |
| `dmerge(dict2)` | Recursively merge configuration dict | dict2: Configuration to merge |
| `modify_option(prompt, api_key, base_url, model_name)` | Use AI to modify option | prompt: Modification requirements, other parameters optional |
| `patch_option(prompt, api_key, base_url, model_name)` | Use AI to generate patch and merge | prompt: Modification requirements, other parameters optional |

#### 2. Rendering Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `render(output_dir, filename)` | Render to HTML file | output_dir: Output directory, filename: File name |
| `render_notebook()` | Render to Jupyter Notebook compatible content | - |

**Example Code**:
```python
from pancharts import Pancharts

# Method 1: Pass option when creating instance
option = {
    "title": {"text": "Simple Example"},
    "xAxis": {"data": ["A", "B", "C", "D", "E"]},
    "yAxis": {},
    "series": [{"type": "bar", "data": [10, 20, 30, 40, 50]}]
}
chart = Pancharts(option)
chart.render()

# Method 2: Assign via property
chart = Pancharts()
chart.option = option
chart.render()

# Use dmerge to merge configurations
chart = Pancharts(option)
additional_config = {"title": {"subtext": "Subtitle"}}
chart.dmerge(additional_config)
chart.render()
```

---

## utils.py

utils.py is the utility module of the Pancharts project, containing various helper functions.

### Main Functions

| Function | Description | Parameters | Return Value |
|----------|-------------|------------|--------------|
| `add_quotes_to_keys(json_str)` | Add double quotes to keys in dict string | json_str: Dict string | Processed string |
| `random_color()` | Generate random color code | - | Hex color string |
| `random_color_list(n)` | Generate random color list | n: List length | Color list |
| `get_index_type(x)` | Determine DataFrame index type | x: DataFrame | "category", "time", or "value" |
| `get_value_type(x)` | Determine Series value type | x: Series | "category", "time", or "value" |
| `deep_merge(dict1, dict2)` | Recursively merge two dicts | dict1, dict2: Dicts to merge | Merged dict |
| `get_config_file_path()` | Get config file path | - | Absolute path of chart_config.py |
| `load_city_cnname()` | Load city Chinese name data | - | DataFrame |
| `load_city_lnglat()` | Load city longitude/latitude data | - | DataFrame |
| `load_countries_info()` | Load country information data | - | DataFrame |

**Example Code**:
```python
from pancharts.utils import random_color, random_color_list, deep_merge

# Generate random color
color = random_color()
print(color)  # Example: #3a7bc8

# Generate color list
colors = random_color_list(5)
print(colors)  # Example: ['#a1b2c3', '#d4e5f6', ...]

# Deep merge dictionaries
dict1 = {"a": 1, "b": {"c": 2}}
dict2 = {"b": {"d": 3}, "e": 4}
merged = deep_merge(dict1, dict2)
print(merged)  # {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}
```

---

## Quick Start

### Installation

```bash
pip install pancharts
```

### Basic Usage Flow

1. **Import necessary modules**
```python
from pancharts import k_v, Pancharts
import pandas as pd
```

2. **Prepare data**
```python
data = pd.Series([10, 20, 30, 40, 50], index=['A', 'B', 'C', 'D', 'E'])
```

3. **Create chart**
```python
chart = k_v(data).bar()
```

4. **Render chart**
```python
chart.render(output_dir='./output', filename='my_chart.html')
```

---

## Notes

1. All chart methods return Pancharts instance, supporting method chaining
2. config parameter merges with default configuration with highest priority
3. Map charts require correct map name
4. AI features require API key configuration (see chart_config.py)
