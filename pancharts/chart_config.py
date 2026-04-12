#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts配置模块
包含图表的基础配置信息和AI模型配置
"""

# AI模型默认配置
DEFAULT_AI_API_KEY = ""
DEFAULT_AI_BASE_URL = ""
DEFAULT_AI_MODEL_NAME = ""

# node_modules文件夹的绝对地址,通过设置此路径使用本地的echarts库
NODE_MODULES_PATH = None

# 全局默认配置，优先级最低
# https://echarts.apache.org/zh/theme-builder.html
GLOBAL_DEFAULT_CONFIG = {
    "init": {
        "echarts_source": "online",
        "width": "60%",
        "height": "400px",
        "renderer": "canvas",
        "theme": ""
    }
}

# 柱状图配置
BAR_OPTION = {
    "legend": {"bottom": 0, "left": "center"},
    "grid": {"show": True},
    'series': [{'type': 'bar'}]
}

# 折线图配置
LINE_OPTION = {
    "legend": {"bottom": 0, "left": "center"},
    "grid": {"show": True},
    'series': [{'type': 'line'}]
}

# 散点图配置
SCATTER_OPTION = {
    "legend": {"bottom": 0, "left": "center"},
    "grid": {"show": True},
    'series': [{'type': 'scatter'}]
}

# 特效散点图配置
ESCATTER_OPTION = {
    "legend": {"bottom": 0, "left": "center"},
    "grid": {"show": True},
    'series': [{'type': "effectScatter"}]
}

# 饼图配置
PIE_OPTION = {
    "legend": {
        "orient": 'vertical',
        "left": 'left'
    },
    "title": {
        "left": 'center'
    },
    "tooltip": {
        "trigger": 'item'
    },
    'series': [{'type': "pie"}]
}

# 漏斗图配置
FUNNEL_OPTION = {
    "legend": {
        "bottom": 0,
        "left": "center"
    },
    "title": {
        "left": 'center'
    },
    "tooltip": {
        "trigger": 'item'
    },
    'series': [{'type': "funnel"}]
}

# 词云图配置
WORDCLOUD_OPTION = {
    "title": {
        "left": 'center'
    },
    'series': [{'type': "wordCloud"}]
}

# 太阳图配置
SUNBURST_OPTION = {
    "title": {
        "left": "center"
    },
    "tooltip": {},
    "legend": {},
    'series': [{'type': "sunburst", "radius": [0, '90%'], "label": {"rotate": 'radial'}}]
}

# 树图配置
TREEMAP_OPTION = {
    'series': [{'type': "treemap"}]
}

# 树状图配置
TREE_OPTION = {
    'series': [{'type': "tree"}]
}

# 3D柱状图配置
BAR3D_OPTION = {
    'grid3D': {'boxWidth': 200, 'boxDepth': 80},
    'xAxis3D': {},
    'yAxis3D': {},
    'zAxis3D': {},
    'title': {'left': 'center'},
    'series': [{'type': "bar3D"}]
}

# 关系图配置
GRAPH_OPTION = {
    'series': [{
        'type': "graph", 
        'layout': 'force', 
        "symbolSize": 10, 
        "roam": True, 
        "label": {"show": True},
    }]
}

# 桑基图配置
SANKEY_OPTION = {
    'series': [{
        'type': "sankey", 
        'layout': 'none', 
        "emphasis": {"focus": 'adjacency'},
    }]
}

# 热力图配置
HEATMAP_OPTION = {
    "grid": {"height": '50%', "top": '10%'},
    "xAxis": {},
    "yAxis": {},
    "visualMap": {"calculable": True, "orient": 'horizontal', "left": 'center', "bottom": '15%'},
    'series': [{"type": "heatmap", "label": {"show": True}, "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowColor": 'rgba(0, 0, 0, 0.5)'}}}]
}

# 平行坐标图配置
PARALLEL_OPTION = {
    "series": [{"type": "parallel", "lineStyle": {"width": 4}}]
}

# 雷达图配置
RADAR_OPTION = {
    "series": [{"type": "radar"}]
}

# 日历热图配置
CALENDAR_OPTION = {
    "legend": {},
    "tooltip": {},
    "visualMap": {"show": True, "type": 'piecewise', "orient": 'horizontal', "left": 'center', "top": 65},
    "calendar": {"cellSize": ['auto', 15], "top": 120},
    "series": [{"type": 'heatmap', "coordinateSystem": 'calendar'}]
}

# 地图配置
MAP_OPTION = {
    "tooltip": {"trigger": "item"},
    "legend": {},
    "visualMap": {
        "type": "continuous",
        "calculable": True,
        "inRange": {
            "color": ['#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695']
        },
        "textStyle": {"color": "#333"}
    },
    "series": [
        {
            "type": "map",
            "name": "数据",
            "label": {"show": True, "margin": 8},
            "roam": True,
            "aspectScale": 0.75,
            "zoom": 1
        }
    ]
}
