# AI 辅助配置

## 功能概述

Pancharts 支持使用 AI 大模型自动修改和优化图表配置，无需手动编写复杂的 ECharts 配置代码。

## 核心功能

- `patch_option()`: 使用 AI 生成配置补丁并合并到现有配置
- `modify_option()`: 使用 AI 生成完整的修改后配置
- 支持自然语言描述修改要求

## 配置 AI API

### 方法一：修改配置文件

编辑 `chart_config.py` 文件：

```python
# AI 模型配置
DEFAULT_AI_API_KEY = "your-api-key"
DEFAULT_AI_BASE_URL = "https://api.deepseek.com"  # 或其他 API 地址
DEFAULT_AI_MODEL_NAME = "deepseek-chat"  # 或其他模型名称
```


## 使用示例

### 1. 使用 patch_option 生成配置补丁

```python
from pancharts import k_v
import pandas as pd

# 创建图表
data = pd.Series([10, 25, 30, 45, 50], index=['北京', '上海', '广州', '深圳', '杭州'])
chart = k_v(data).bar()

# 使用 AI 修改配置（生成补丁）
chart.patch_option("将标题改为红色，背景改为浅蓝色，添加数据标签")

# 渲染输出
chart.render(output_dir='./output', filename='ai_modified_chart.html')
```

### 2. 使用 modify_option 生成完整配置

```python
from pancharts import Pancharts

# 创建简单配置
option = {
    "title": {"text": "销售数据"},
    "xAxis": {"type": "category", "data": ["A", "B", "C"]},
    "yAxis": {"type": "value"},
    "series": [{"type": "bar", "data": [10, 20, 30]}]
}

chart = Pancharts(option)

# 使用 AI 生成完整配置
chart.modify_option("将图表改为渐变柱状图，添加动画效果，设置主题色为蓝色系")

chart.render()
```

### 3. 复杂修改要求

```python
chart.patch_option("""
1. 将柱状图改为横向柱状图
2. 添加渐变颜色，从蓝色到紫色
3. 添加数据标签显示在柱子右侧
4. 设置背景为浅色渐变
5. 添加图例
""")

chart.render()
```

## AI 修改方法对比

| 方法 | 说明 | 适用场景 |
|------|------|---------|
| `patch_option()` | 生成配置补丁，合并到现有配置 | 小范围修改，保留原有结构 |
| `modify_option()` | 生成完整的修改后配置 | 大幅修改，重新设计图表 |

## 支持的修改类型

### 样式修改

- 颜色和主题
- 字体和字号
- 背景和边框
- 渐变效果

### 布局修改

- 图表大小和位置
- 图例位置
- 坐标轴配置
- 网格和背景

### 数据展示

- 数据标签显示
- 提示框配置
- 动画效果
- 交互行为

### 图表类型转换

- 柱状图 ↔ 折线图
- 散点图 ↔ 气泡图
- 饼图 ↔ 环形图

## AI Agent 功能

### desc_chat - 数据分析描述

```python
from pancharts import agent

# 使用 AI 分析数据并生成洞察
insight = agent.desc_chat(
    user_requirement="分析销售数据趋势和规律",
    data_config={
        "xAxis": "产品类别",
        "yAxis": "销售额",
        "data": [100, 150, 80, 120]
    },
    max_words=200
)

print(insight)
```

### data_chat - 生成并执行统计代码

```python
from pancharts import agent
import pandas as pd

data = pd.DataFrame({
    '产品': ['A', 'B', 'C', 'D'],
    '销量': [100, 150, 80, 120],
    '利润': [20, 35, 15, 25]
})

# 生成统计分析代码并执行
result = agent.data_chat(
    data=data,
    user_requirement="计算各产品的利润率并排序",
    data_desc="产品销售数据"
)

print(result['result'])  # 分析结果
print(result['code'])    # 生成的代码
print(result['desc'])    # 结果描述
```

### pchat - 基于文档回答问题

```python
from pancharts import agent

# 基于文档回答问题
agent.pchat("如何创建一个柱状图？")
```

### echat - 生成 ECharts 配置

```python
from pancharts import agent

# 生成 ECharts 配置
agent.echat("创建一个带有渐变效果的柱状图")
```

## 配置参数说明

### API 配置参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `DEFAULT_AI_API_KEY` | AI API 密钥 | 空 |
| `DEFAULT_AI_BASE_URL` | AI API 地址 | "https://api.deepseek.com" |
| `DEFAULT_AI_MODEL_NAME` | AI 模型名称 | "deepseek-chat" |

### 调用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `prompt` | 修改要求描述 | 必需 |
| `verbose` | 是否打印详细信息 | False |
| `temperature` | 温度参数（0-1） | 0.7 |
| `max_tokens` | 最大输出 token 数 | 2048 |

## 注意事项

1. **API 密钥**: 使用 AI 功能前必须配置有效的 API 密钥
2. **网络连接**: 需要网络连接才能调用 AI API
3. **费用**: AI API 调用可能产生费用，请留意使用量
4. **数据隐私**: 避免将敏感数据发送到外部 API
5. **配置格式**: AI 返回的配置需要符合 ECharts 语法

## 完整示例

```python
from pancharts import k_v, chart_config
import pandas as pd

# 配置 AI API
chart_config.DEFAULT_AI_API_KEY = "your-api-key"
chart_config.DEFAULT_AI_BASE_URL = "https://api.deepseek.com"

# 创建数据
data = pd.Series([120, 200, 150, 80, 70],
                 index=['产品A', '产品B', '产品C', '产品D', '产品E'])

# 创建初始图表
chart = k_v(data).bar({
    "title": {"text": "产品销量"}
})

# 使用 AI 优化配置
chart.patch_option("""
1. 将标题颜色改为深蓝色
2. 添加副标题显示'2024年Q1'
3. 柱子使用渐变色，从左到右由浅蓝到深蓝
4. 添加数据标签显示在柱子顶部
5. 设置背景为淡灰色
6. 添加图例
""")

# 保存到数据库
chart.to_db(
    tag0="AI优化图表",
    tag1="产品分析",
    data_desc="产品销量数据",
    data_insight="AI自动优化后的图表配置"
)

chart.render(output_dir='./output', filename='ai_optimized.html')
```
