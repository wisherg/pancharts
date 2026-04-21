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

# 高德地图API配置
AMAP_API_KEY = ""

# OpenCage API配置
OPENCAGE_API_KEY = ""

# 百度地图API配置
BAIDU_API_KEY = ""

# node_modules文件夹的绝对地址,通过设置此路径使用本地的echarts库
NODE_MODULES_PATH = None

# 全局默认配置，优先级最低
# https://echarts.apache.org/zh/theme-builder.html
GLOBAL_DEFAULT_CONFIG = {
    "init": {
        "echarts_source": "local",
        "width": "60%",
        "height": "400px",
        "renderer": "canvas",
        "theme": ""
    },
  "color": ["#d87c7c", "#919e8b", "#d7ab82", "#6e7074", "#61a0a8", "#efa18d", "#787464", "#cc7e63", "#724e58", "#4b565b"],
  "backgroundColor": "#fef8ef",
  "textStyle": {},
  "title": {
    "textStyle": {
      "color": "#333"
    },
    "subtextStyle": {
      "color": "#aaa"
    }
  },
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

MAP3D_OPTION = {
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
            "type": "map3d",
            "name": "数据",
            "label": {"show": True, "margin": 8},
            "roam": True,
            "aspectScale": 0.75,
            "zoom": 1,
            "groundPlane": {
                "show": True,
                "color": '#081027',
                "borderColor": '#2f5597',
                "borderWidth": 1
            },
            "shading": 'lambert',
            "boxHeight": 8,
            "itemStyle": {
                "color": '#152949',
                "borderColor": '#2f5597',
                "borderWidth": 1
            }

        }
    ]
}


#geo地理坐标配置
GEO_OPTION = {
    "title": {
        "left": "center"
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "geo": {
        "roam": True,
    },
}

GEO_GRAPH_OPTION = {
    "title": {
        "left": "center"
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "geo": {
        "roam": True,
    },
    "series": [{
        "type": "graph",
        "coordinateSystem": "geo",
        "edgeSymbol": ['none', 'arrow'],
        "edgeSymbolSize": 5,
        "lineStyle": {
            "color": '#718adbff',
            "opacity": 1
        }
    }]
}


#geo3d地理坐标配置
GEO3D_BAR3D_OPTION = {
    "backgroundColor": '#081027',
    "title": {
        "left": "center"
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "geo3D": {
        "shading": 'lambert',
        "boxHeight": 8,
        "itemStyle": {
            "color": '#152949',
            "borderColor": '#2f5597',
            "borderWidth": 1
        }
    },
    "series": [{
        "type": "bar3D",
        "coordinateSystem": "geo3D"
    }]
}

GEO3D_LINES3D_OPTION = {
    "backgroundColor": '#081027',
    "title": {
        "left": "center"
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "geo3D": {
        "shading": 'lambert',
        "boxHeight": 8,
        "itemStyle": {
            "color": '#152949',
            "borderColor": '#2f5597',
            "borderWidth": 1
        }
    },
    "series": [{
        "type": "lines3D",
        "coordinateSystem": "geo3D",
        "effect": {
            "show": True,
            "trailWidth": 1.5,
            "trailOpacity": 0.5,
            "trailLength": 0.2,
            "constantSpeed": 5
        },
        "blendMode": "lighter",
        "lineStyle": {
            "width": 1.5,
            "opacity": 0.25
        }
    }]
}
