# 数据库存储与数据读取

## 功能概述

Pancharts 支持将图表配置、数据描述和数据洞察保存到 SQLite 数据库中，并提供查询和导出功能。同时提供强大的数据读取功能，能够获取数据的关键信息。

## 核心功能

### 1. 数据库存储
- 将图表配置（option）保存到数据库
- 存储数据描述（data_desc）和数据洞察（data_insight）
- 支持标签分类（tag0, tag1）
- 提供多种查询方式
- 支持导出为 Markdown 报告

### 2. 数据读取（重要功能）
- 通过 `get_data()` 函数读取数据文件或数据库记录
- 获取数据框（DataFrame）
- 获取数据描述（关键信息）
- 获取数据信息（字段、缺失值、数据类型等）

## 数据库表结构

### pancharts_options 表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER | 记录ID（主键，自增） |
| `insert_time` | TIMESTAMP | 插入时间 |
| `option` | TEXT | ECharts 配置（JSON格式） |
| `data_option` | TEXT | 数据配置（JSON格式） |
| `file_path` | TEXT | 文件路径 |
| `tag0` | TEXT | 自定义标签1 |
| `tag1` | TEXT | 自定义标签2 |
| `data_desc` | TEXT | 数据描述 |
| `data_insight` | TEXT | 数据洞察 |

## 数据读取功能

### get_data 函数

`get_data()` 函数是重要的数据读取功能，支持按ID或文件路径查询数据，并返回数据的关键信息。

#### 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `source` | int 或 str | 数据来源，可以是数据库记录ID（int）或文件路径（str） |

#### 返回值

| 键 | 类型 | 说明 |
|------|------|------|
| `data` | DataFrame | 读取的数据框 |
| `desc` | str | 数据描述，包含数据关键信息 |
| `data_info` | str | 数据信息，包含字段、缺失值、数据类型等 |

### 使用示例

```python
from pancharts.utils import get_data

# 示例1：按ID查询
result = get_data(1)

# 示例2：按文件路径查询
result = get_data(r'E:\trea_project\pancharts00\uploads\shoes.csv')

# 获取数据框
df = result['data']

# 获取数据描述（包含数据关键信息）
desc = result['desc']

# 获取数据信息（包含字段、缺失值、数据类型等）
info = result['data_info']

# 打印结果
print("数据框:", df.head())
print("数据描述:", desc)
print("数据信息:", info)
```

### get_data 使用场景

#### 场景1：从数据库读取已存储的数据

```python
# 读取ID为1的数据记录
result = get_data(1)
df = result['data']

# 基于读取的数据创建图表
from pancharts import k_v
chart = k_v(df['销量']).bar()
chart.render()
```

#### 场景2：从文件读取数据并获取信息

```python
# 从CSV文件读取数据
result = get_data(r'E:\data\sales.csv')

# 获取数据信息用于分析
print("数据信息:")
print(result['data_info'])

# 获取数据描述
print("\n数据描述:")
print(result['desc'])

# 使用数据进行可视化
df = result['data']
```

## 数据库操作函数

### init_pancharts_db

初始化 SQLite 数据库：

```python
from pancharts.chartsdb.utils import init_pancharts_db

# 初始化数据库（如果不存在会自动创建）
init_pancharts_db()

# 或者指定数据库路径
init_pancharts_db(db_path="./data/pancharts.db")
```

### open_db_manager

启动 Web 管理界面：

```python
from pancharts.chartsdb.utils import open_db_manager

# 启动 Web 管理界面
# 访问 http://localhost:8000 查看和管理已保存的图表
open_db_manager(host="0.0.0.0", port=8000)
```

### get_chart

获取单个图表数据：

```python
from pancharts.utils import get_chart

chart_data = get_chart(chart_id)
# 返回包含 option, data_desc, data_insight 等信息的字典
```

### charts_md

导出图表为 Markdown 文件：

```python
from pancharts.utils import charts_md

# 参数说明
# id_list: ID列表，如 [1, 2, 3]
# tag0: 标签1筛选
# tag1: 标签2筛选
# output_file: 输出文件名，默认 "charts_report.md"

charts_md(id_list=[1, 2, 3])
charts_md(tag0="销售数据")
charts_md(tag0="销售数据", tag1="2024年")
charts_md(id_list=[1, 2], output_file="my_report.md")
```

## 使用示例

### 1. 保存图表到数据库

```python
from pancharts import k_v
import pandas as pd

# 创建图表
data = pd.Series([10, 20, 30], index=['A', 'B', 'C'])
chart = k_v(data).bar()

# 保存到数据库
result = chart.to_db(
    tag0="销售数据",          # 第一标签
    tag1="2024年",            # 第二标签
    data_desc="产品A、B、C的销量统计，用于分析各产品市场份额",
    data_insight="产品B销量最高，建议增加产品B的产能；产品C增长趋势明显，可考虑重点推广"
)
```

print(result)  # 返回保存结果
```

### 2. 按ID查询图表

```python
from pancharts.utils import get_chart

# 获取ID为1的图表数据
chart_data = get_chart(1)
print(chart_data)
```

### 3. 按ID列表查询并导出Markdown

```python
from pancharts.utils import charts_md

# 按ID列表查询，并把多个图表结果、数据描述、数据洞察逐一写入Markdown文件
charts_md(id_list=[1, 2, 3])
```

### 4. 按标签查询

```python
# 按tag0查询
charts_md(tag0="销售数据")

# 多条件组合（交集）
charts_md(tag0="销售数据", tag1="2024年")
```

### 5. 指定输出文件名

```python
charts_md(id_list=[1, 2], output_file="my_report.md")
```

## 数据库操作函数

### init_pancharts_db

初始化 SQLite 数据库：

```python
from pancharts.chartsdb.utils import init_pancharts_db

# 初始化数据库（如果不存在会自动创建）
init_pancharts_db()

# 或者指定数据库路径
init_pancharts_db(db_path="./data/pancharts.db")
```

### open_db_manager

启动 Web 管理界面：

```python
from pancharts.chartsdb.utils import open_db_manager

# 启动 Web 管理界面
# 访问 http://localhost:8000 查看和管理已保存的图表
open_db_manager(host="0.0.0.0", port=8000)
```

### get_chart

获取单个图表数据：

```python
from pancharts.utils import get_chart

chart_data = get_chart(chart_id)
# 返回包含 option, data_desc, data_insight 等信息的字典
```

### charts_md

导出图表为 Markdown 文件：

```python
from pancharts.utils import charts_md

# 参数说明
# id_list: ID列表，如 [1, 2, 3]
# tag0: 标签1筛选
# tag1: 标签2筛选
# output_file: 输出文件名，默认 "charts_report.md"

charts_md(id_list=[1, 2, 3])
charts_md(tag0="销售数据")
charts_md(tag0="销售数据", tag1="2024年")
charts_md(id_list=[1, 2], output_file="my_report.md")
```

## 数据描述与洞察

### data_desc（数据描述）

数据描述用于说明图表中各个量的意义，包括：
- 数据来源和采集时间
- 各个字段的含义
- 单位和量纲说明
- 数据预处理步骤

### data_insight（数据洞察）

数据洞察是基于图表数据的分析和商业洞察，包括：
- 数据趋势分析
- 异常值识别
- 业务建议
- 决策支持

## 完整工作流示例

```python
from pancharts import k_v
from pancharts.utils import charts_md

# 准备数据
sales_data = pd.Series(
    [120, 200, 150, 80, 70, 110, 130],
    index=['周一', '周二', '周三', '周四', '周五', '周六', '周日']
)

# 创建图表
chart = k_v(sales_data).bar({
    "title": {"text": "本周销售趋势"}
})

# 保存到数据库
chart.to_db(
    tag0="销售分析",
    tag1="周报",
    data_desc="本周每日销售额统计，反映销售波动情况，单位：万元",
    data_insight="周六和周日销售明显高于工作日（+45%），建议增加周末人手；周五销售最低，可考虑促销活动"
)

# 导出报告
charts_md(tag0="销售分析", output_file="weekly_sales_report.md")
```

## 配置说明

### 修改数据库路径

编辑 `chart_config.py` 文件：

```python
# 在 chart_config.py 中设置
SQLITE_DB_PATH = r"E:\path\to\your\pancharts_option.db"
```

### 数据库文件位置

默认数据库路径为 `./pancharts_option.db`（当前工作目录）。
