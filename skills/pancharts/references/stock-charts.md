# 股票数据可视化 (sk_vm)

## 功能概述

`sk_vm` 类用于可视化股票数据，主要支持 K 线图和移动平均线分析。

**重要：数据结构有严格要求，必须严格遵守。**

## 数据格式要求（严格）

### sk_vm 股票数据格式

```
DataFrame 结构：
├── 索引: 日期字符串（格式：'YYYY-MM-DD'）
└── 前4列（必须按此顺序）:
    ├── 第1列: 开盘价 (open)
    ├── 第2列: 收盘价 (close)
    ├── 第3列: 最低价 (low)
    └── 第4列: 最高价 (high)
```

**示例数据结构：**

```python
# 索引为日期字符串，前四列必须按 open/close/low/high 顺序
stock_data = pd.DataFrame({
    'open':  [34, 35, 38, 33, 36, 40],   # 开盘价
    'close': [36, 38, 36, 35, 40, 42],   # 收盘价
    'low':   [30, 32, 35, 30, 34, 38],   # 最低价
    'high':  [38, 40, 42, 38, 42, 45]    # 最高价
}, index=['2024-01-01', '2024-01-02', '2024-01-03', 
          '2024-01-04', '2024-01-05', '2024-01-08'])

# 注意：列名可以是任意名称，但顺序必须是 open/close/low/high
```

## 主要特性

- 支持标准 K 线图（蜡烛图）展示
- 支持多条移动平均线（MA）
- 自动处理股票数据格式
- 支持自定义配置

## 支持的图表类型

| 方法 | 说明 | 参数 |
|------|------|------|
| `kline(ma, config)` | K线图 | ma: 移动平均线窗口列表，config: 额外配置字典 |

## 使用示例

### 1. 基础 K 线图

```python
from pancharts import sk_vm
import pandas as pd
import numpy as np

# 创建股票数据（索引为日期，前四列为 open/close/low/high）
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=60).strftime('%Y-%m-%d')
stock_data = pd.DataFrame({
    'open':  100 + np.cumsum(np.random.randn(60) * 2),  # 开盘价
    'close': 100 + np.cumsum(np.random.randn(60) * 2),  # 收盘价
    'low':   100 + np.cumsum(np.random.randn(60) * 2) - 5,   # 最低价
    'high':  100 + np.cumsum(np.random.randn(60) * 2) + 5    # 最高价
}, index=dates)

# 创建 K 线图
chart = sk_vm(stock_data).kline()
chart.render(output_dir='./output', filename='kline_basic.html')
```

### 2. 带移动平均线的 K 线图

```python
# 添加 5、10、20 日均线
chart = sk_vm(stock_data).kline(ma=[5, 10, 20])
chart.render()
```

### 3. 多均线 K 线图

```python
# 添加 5、10、20、30、60 日均线
chart = sk_vm(stock_data).kline(ma=[5, 10, 20, 30, 60], config={
    "title": {"text": "股票 K 线图"}
})
chart.render()
```

## 移动平均线配置

移动平均线（MA）是股票分析中常用的技术指标，用于平滑价格数据。

### 常用均线窗口

| 均线 | 说明 |
|------|------|
| MA5 | 5日均线（周线） |
| MA10 | 10日均线 |
| MA20 | 20日均线（月线） |
| MA30 | 30日均线 |
| MA60 | 60日均线（季线） |
| MA120 | 120日均线（半年线） |
| MA250 | 250日均线（年线） |

### 使用示例

```python
# 单均线
chart = sk_vm(stock_data).kline(ma=[20])

# 多均线
chart = sk_vm(stock_data).kline(ma=[5, 10, 20, 60])
```

## K 线图配置选项

```python
{
    "title": {"text": "股票 K 线图", "left": "center"},
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
    "legend": {"data": ["开盘", "收盘", "MA5", "MA10", "MA20"]},
    "grid": [
        {"left": "10%", "right": "8%", "top": "5%", "height": "50%"},
        {"left": "10%", "right": "8%", "top": "62%", "height": "25%"}
    ],
    "xAxis": [
        {"type": "category", "data": [], "gridIndex": 0},
        {"type": "category", "data": [], "gridIndex": 1}
    ],
    "yAxis": [
        {"type": "value", "scale": True, "gridIndex": 0},
        {"type": "value", "scale": True, "gridIndex": 1}
    ]
}
```

## 完整示例

```python
from pancharts import sk_vm
import pandas as pd
import numpy as np

# 生成模拟股票数据
np.random.seed(123)
dates = pd.date_range('2024-01-01', periods=100).strftime('%Y-%m-%d')

base_price = 100
prices = base_price + np.cumsum(np.random.randn(100) * 1.5)

stock_data = pd.DataFrame({
    'open':  prices + np.random.randn(100) * 0.5,
    'close': prices + np.random.randn(100) * 0.5,
    'high':  prices + np.random.rand(100) * 3 + 1,
    'low':   prices - np.random.rand(100) * 3 - 1
}, index=dates)

# 创建 K 线图
chart = sk_vm(stock_data).kline(
    ma=[5, 10, 20, 60],
    config={
        "title": {"text": "某股票 K 线图（2024年）"},
        "series": [{
            "name": "K线",
            "type": "candlestick",
            "data": [],
            "itemStyle": {
                "color": "#ef5350",      # 阳线颜色（收盘 > 开盘）
                "color0": "#26a69a",     # 阴线颜色（收盘 < 开盘）
                "borderColor": "#ef5350",
                "borderColor0": "#26a69a"
            }
        }]
    }
)

chart.render(output_dir='./output', filename='stock_analysis.html')
```

## 使用 akshare 获取真实数据

```python
# 安装 akshare
# pip install --upgrade akshare

import akshare as ak
import pandas as pd

# 获取股票数据
stock_df = ak.stock_zh_a_hist(symbol="000001", start_date="20240101", end_date="20241231")

# 转换数据格式以匹配 sk_vm
# 需要：索引=日期，前4列=open/close/low/high
stock_data = pd.DataFrame({
    'open':  stock_df['开盘'].values,
    'close': stock_df['收盘'].values,
    'low':   stock_df['最低'].values,
    'high':  stock_df['最高'].values
}, index=stock_df['日期'].values)

# 创建 K 线图
chart = sk_vm(stock_data).kline(ma=[5, 10, 20])
chart.render()
```

## 注意事项

1. **索引格式**：索引必须是日期字符串，格式为 'YYYY-MM-DD'
2. **列顺序**：前四列必须按 open/close/low/high 顺序排列
3. **列名灵活**：列名可以是任意名称，但顺序必须正确
4. **数据完整性**：不建议包含成交量列，会影响显示效果
