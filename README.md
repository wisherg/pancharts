# Pancharts

A Python library for generating beautiful ECharts visualizations with seamless pandas integration.

## Features

- **Seamless Pandas Integration**: Directly visualize pandas Series and DataFrames without manual data transformation
- **Simple Data-to-Chart Mapping**: Intuitive API that maps pandas data structures to appropriate chart types
- **Rich Chart Types**: 20+ chart types including bar, line, scatter, pie, funnel, wordcloud, sunburst, treemap, tree, bar3d, graph, sankey, heatmap, parallel, radar, calendar, and map
- **AI-Powered Configuration**: Use `modify_option()` and `patch_option()` to modify chart configurations with large language models
- **Customizable Chart Options**: Full control over ECharts options with deep merge support
- **Dual Rendering Methods**: 
  - `render()`: Save as standalone HTML file
  - `render_notebook()`: Display directly in Jupyter Notebook
- **Flexible ECharts Sources**: Support for both local and online ECharts CDNs
- **Map Visualization**: Built-in support for map charts with geographic data

## Installation

```bash
pip install pancharts
```

## Quick Start

## Pandas Data Structure to Chart Mapping

Pancharts provides specialized classes that automatically map pandas data structures to appropriate visualizations:

### 1. `k_v`: Single-Column Index Series

Use for pandas Series with a single-level index.

**Supported Chart Types:**
- `bar()` - Bar chart
- `line()` - Line chart
- `scatter()` - Scatter chart
- `escatter()` - Effect scatter chart
- `pie()` - Pie chart
- `funnel()` - Funnel chart
- `wordcloud()` - Word cloud chart
- `calendar()` - Calendar heatmap
- `map(map_name)` - Map chart (requires map_name parameter)

**Example:**

```python
import pandas as pd
from pancharts import k_v

# Create sample data
data = pd.Series(
    [120, 200, 150, 80, 70, 110, 130],
    index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    name='Weekly Sales'
)

# Create a bar chart
chart = k_v(data).bar()
chart.render()

#Displays the chart directly in a Jupyter Notebook cell.
chart.render_notebook()

# Create a pie chart
chart = k_v(data).pie()
chart.render()

# Create a map chart (special parameter requirement)
map_data = pd.Series(
    [100, 200, 150, 180],
    index=['湖南省', '上海市', '江西省', '江苏省']
)
chart = k_v(map_data).map("china")
chart.render()
```

### 2. `km_nv`: Multi-Column Index Series

Use for pandas Series with multi-level (hierarchical) indexes.

**Supported Chart Types:**
- `sunburst()` - Sunburst chart
- `treemap(num=None)` - Treemap chart (optional num parameter to select root)
- `tree(num=None)` - Tree chart (optional num parameter to select root)

**Example:**

```python
import pandas as pd
from pancharts import km_nv

# Create multi-index data
index = pd.MultiIndex.from_product(
    [['Electronics', 'Clothing'], ['Phones', 'Laptops', 'Shirts', 'Pants']]
)
data = pd.Series([500, 800, 300, 400,500, 800, 300, 400], index=index)
chart = km_nv(data).sunburst()
chart.render()

# Create a treemap chart with specific root
chart = km_nv(data).treemap(num=0)
chart.render()
```

### 3. `k2_nv`: Two-Level Index Series

Use for pandas Series with exactly two levels of indexes. Perfect for relationship data.

**Supported Chart Types:**
- `bar3d()` - 3D bar chart
- `graph()` - Graph/network chart
- `sankey()` - Sankey diagram
- `heatmap()` - Heatmap

**Special Parameter for `graph()`:**
The `k2_nv` constructor accepts an optional `cate` parameter (list of length 2) for node categorization.

**Example:**

```python
import pandas as pd
from pancharts import k2_nv

# Create two-level index data (often from groupby)
index = pd.MultiIndex.from_product(
    [['Source A', 'Source B'], ['Target X', 'Target Y', 'Target Z']]
)
data = pd.Series([10, 20, 15, 25, 30, 18], index=index)

# Create a heatmap
chart = k2_nv(data).heatmap()
chart.render()

# Create a graph with node categorization
chart = k2_nv(data, cate=['Sources', 'Targets']).graph()
chart.render()
```

### 4. `k_vm`: Single-Column Index, Multi-Column Values DataFrame

Use for pandas DataFrames with single index and multiple value columns.

**Supported Chart Types:**
- `parallel()` - Parallel coordinates chart
- `radar()` - Radar chart
- `rect_plot(series_type, encode_x, encode_y)` - Flexible encoding chart

**Special Methods for `k_vm`:**
- `vmap_size(dimension, symbolSize)` - Map dimension values to symbol sizes
- `vmap_color(dimension, color)` - Map dimension values to colors

**Example:**

```python
import pandas as pd
import numpy as np
from pancharts import k_vm

# Create DataFrame with multiple columns
data = pd.DataFrame(
    np.random.rand(10, 5),
    columns=['Feature A', 'Feature B', 'Feature C', 'Feature D', 'Feature E'],
    index=[f'Sample {i}' for i in range(1, 11)]
)

# Create a parallel coordinates chart
chart = k_vm(data).parallel()
chart.render()

# Create a flexible encoded chart
chart = k_vm(data).rect_plot('scatter', encode_x=0, encode_y=1)
chart.render()

# Use visual mapping
config = k_vm(data).vmap_size(dimension=2, symbolSize=[5, 50])
chart = k_vm(data).rect_plot('scatter', encode_x=0, encode_y=1, config=config)
chart.render()
```

## AI-Powered Configuration Modification

Pancharts provides two methods to modify chart configurations using large language models:
First, you need to obtain the configuration file path using `get_config_file_path`:

```python
from pancharts.utils import get_config_file_path

config_path = get_config_file_path()
print(config_path)
```

Then modify the following configuration items in the config file:

```python
DEFAULT_AI_API_KEY = ""              # Your LLM API key, e.g. sk-...
DEFAULT_AI_BASE_URL = ""             # LLM API endpoint, e.g. https://api.openai.com/v1
DEFAULT_AI_MODEL_NAME = ""           # LLM model name, e.g. gpt-4o, deepseek-chat
```

### 1. `patch_option()` - Patch-Based Updates (Recommended)

Generates only the changed parts and merges them using deep merge. This is more efficient and preserves existing configuration.

```python
from pancharts import Pancharts
from pancharts import k_v

# Create sample data
data = pd.Series(
    [120, 200, 150, 80, 70, 110, 130],
    index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    name='Weekly Sales'
)

# Create a bar chart
chart = k_v(data).bar()

# Modify the entire configuration using AI
chart.patch_option("Change the color of the pillar to red.")
chart.render()
```
### 2. `modify_option()` - Full Configuration Replacement

Generates and replaces the entire chart option.

```python
from pancharts import Pancharts
from pancharts import k_v

# Create sample data
data = pd.Series(
    [120, 200, 150, 80, 70, 110, 130],
    index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    name='Weekly Sales'
)

# Create a bar chart
chart = k_v(data).bar()

# Modify the entire configuration using AI
chart.modify_option("Change the color of the pillar to red.")
chart.render()
```


## Chart Configuration Options

Pancharts supports the full ECharts configuration API. You can pass custom configurations using the `config` parameter in all chart methods:

```python
from pancharts import k_v
import pandas as pd

data = pd.Series([1, 2, 3, 4, 5])

# Pass custom ECharts options
custom_config = {
    "title": {"text": "Custom Title", "left": "center"},
    "tooltip": {"trigger": "axis"},
    "legend": {"top": "bottom"}
}

chart = k_v(data).bar(config=custom_config)
chart.render()
```

## License

MIT License
