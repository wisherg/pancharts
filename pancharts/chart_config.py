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

# 高德地图地址查询API配置 https://lbs.amap.com/
AMAP_API_KEY = ""

#高德地图显示API配置
AMAP_MAP_API_KEY = ""

# OpenCage API配置 https://opencagedata.com/
OPENCAGE_API_KEY = ""


# node_modules文件夹的绝对地址
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


# 高德地图基础配置
AMAP_OPTION = {
    "title": {
        "left": "center"
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "amap": {
        "resizeEnable": True,
        "renderOnMoving": True,
        "echartsLayerInteractive": True
    }
}

AMAP_HEATMAP_OPTION = {
    "title": {
        "left": "center"
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "amap": {
        "resizeEnable": True,
        "renderOnMoving": True,
        "echartsLayerInteractive": True
    },
    "visualMap": {
        "show": True,
        "calculable": True,
        "inRange": {
            "color": ["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8"]
        }
    }
}

AMAP_GRAPH_OPTION = {
    "title": {
        "left": "center"
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "amap": {
        "resizeEnable": True,
        "renderOnMoving": True,
        "echartsLayerInteractive": True
    },
    "series": [{
        "type": "graph",
        "coordinateSystem": "amap",
        "edgeSymbol": ['none', 'arrow'],
        "edgeSymbolSize": 5,
        "lineStyle": {
            "color": '#718adbff',
            "opacity": 1
        }
    }]
}

AMAP_LINES_OPTION = {
    "title": {
        "left": "center"
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "amap": {
        "resizeEnable": True,
        "renderOnMoving": True,
        "echartsLayerInteractive": True
    },
    "series": [{
        "type": "lines",
        "coordinateSystem": "amap",
        "effect": {
            "show": True,
            "trailWidth": 1.5,
            "trailOpacity": 0.5,
            "trailLength": 0.2,
            "constantSpeed": 30
        },
        "blendMode": "lighter",
        "lineStyle": {
            "width": 1.5,
            "opacity": 0.25
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


# Globe 纹理资源在线地址基础路径（使用jsdelivr避免跨域问题）
GLOBE_ASSET_URL = "https://cdn.jsdelivr.net/gh/apache/echarts-website@asf-site/examples/data-gl/asset/"

# Globe 地球配置 - 基础配置
GLOBE_BASIC_OPTION = {
    "backgroundColor": '#000',
    "title": {
        "left": "center",
        "textStyle": {"color": "#fff"}
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "globe": {
        "baseTexture": GLOBE_ASSET_URL + "earth.jpg",
        "normalTexture": GLOBE_ASSET_URL + "earth_normal.jpg",
        "shading": 'realistic',
        "realisticMaterial": {
            "roughness": 0.8,
            "metalness": 0
        },
        "environment": GLOBE_ASSET_URL + "starfield.jpg",
        "atmosphere": {
            "show": True
        },
        "light": {
            "ambient": {
                "intensity": 0.2
            },
            "main": {
                "intensity": 1.5,
                "shadow": True
            },
            "ambientCubemap": {
                "texture": GLOBE_ASSET_URL + "lake.hdr",
                "exposure": 1,
                "diffuseIntensity": 0.5,
                "specularIntensity": 1
            }
        }
    }
}

# Globe 地球配置 - 带高度纹理和夜景
GLOBE_NIGHT_OPTION = {
    "backgroundColor": '#000',
    "title": {
        "left": "center",
        "textStyle": {"color": "#fff"}
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "globe": {
        "baseTexture": GLOBE_ASSET_URL + "earth.jpg",
        "normalTexture": GLOBE_ASSET_URL + "earth_normal.jpg",
        "heightTexture": GLOBE_ASSET_URL + "bathymetry_bw_composite_4k.jpg",
        "displacementScale": 0.1,
        "shading": 'realistic',
        "realisticMaterial": {
            "roughness": 0.8,
            "metalness": 0
        },
        "environment": GLOBE_ASSET_URL + "starfield.jpg",
        "light": {
            "ambient": {
                "intensity": 0.2
            },
            "main": {
                "intensity": 1.5,
                "shadow": True
            },
            "ambientCubemap": {
                "texture": GLOBE_ASSET_URL + "lake.hdr",
                "exposure": 1,
                "diffuseIntensity": 0.5,
                "specularIntensity": 1
            }
        },
        "layers": [
            {
                "type": 'blend',
                "blendTo": 'emission',
                "texture": GLOBE_ASSET_URL + "night.jpg"
            },
            {
                "type": 'overlay',
                "texture": GLOBE_ASSET_URL + "clouds.png",
                "shading": 'lambert',
                "distance": 5
            }
        ]
    }
}

# Globe 地球配置 - 真实感渲染
GLOBE_REALISTIC_OPTION = {
    "backgroundColor": '#000',
    "title": {
        "left": "center",
        "textStyle": {"color": "#fff"}
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "legend": {
        "selectedMode": 'single',
        "left": 'left',
        "orient": 'vertical',
        "textStyle": {
            "color": '#fff'
        }
    },
    "globe": {
        "baseTexture": GLOBE_ASSET_URL + "earth.jpg",
        "normalTexture": GLOBE_ASSET_URL + "earth_normal.jpg",
        "environment": GLOBE_ASSET_URL + "starfield.jpg",
        "heightTexture": GLOBE_ASSET_URL + "bathymetry_bw_composite_4k.jpg",
        "displacementScale": 0.1,
        "displacementQuality": 'high',
        "baseColor": '#000',
        "shading": 'realistic',
        "realisticMaterial": {
            "roughness": 0.2,
            "metalness": 0
        },
        "postEffect": {
            "enable": True,
            "depthOfField": {
                "enable": False,
                "focalDistance": 150
            }
        },
        "temporalSuperSampling": {
            "enable": True
        },
        "light": {
            "ambient": {
                "intensity": 0
            },
            "main": {
                "intensity": 0.1,
                "shadow": False
            },
            "ambientCubemap": {
                "texture": GLOBE_ASSET_URL + "lake.hdr",
                "exposure": 1,
                "diffuseIntensity": 0.5,
                "specularIntensity": 2
            }
        },
        "viewControl": {
            "autoRotate": False
        },
        "silent": True
    }
}

# Globe 地球配置 - 地形渲染
GLOBE_TERRAIN_OPTION = {
    "backgroundColor": '#000',
    "title": {
        "left": "center",
        "textStyle": {"color": "#fff"}
    },
    "tooltip": {
        "trigger": "item",
        'formatter': "JsCode:function(params) { return params.name + '<br/>values:' + params.value; }"
    },
    "globe": {
        "baseTexture": GLOBE_ASSET_URL + "world.topo.bathy.200401.jpg",
        "normalTexture": GLOBE_ASSET_URL + "earth_normal.jpg",
        "heightTexture": GLOBE_ASSET_URL + "world.topo.bathy.200401.jpg",
        "displacementScale": 0.04,
        "shading": 'realistic',
        "environment": GLOBE_ASSET_URL + "starfield.jpg",
        "realisticMaterial": {
            "roughness": 0.9
        },
        "postEffect": {
            "enable": True
        },
        "light": {
            "main": {
                "intensity": 5,
                "shadow": True
            },
            "ambientCubemap": {
                "texture": GLOBE_ASSET_URL + "pisa.hdr",
                "diffuseIntensity": 0.2
            }
        }
    }
}

# Globe 散点图配置（仅包含图表特有配置，基础配置从GLOBE_BASIC_OPTION继承）
# visualMap由create_visual_map函数生成，此处不再重复定义
GLOBE_SCATTER_OPTION = {
    "series": [{
        "type": "scatter3D",
        "coordinateSystem": "globe",
        "symbolSize": 12,
        "label": {
            "show": True,
            "formatter": "{b}"
        }
    }]
}

# Globe 3D柱状图配置（仅包含图表特有配置，基础配置从GLOBE_BASIC_OPTION继承）
# visualMap由create_visual_map函数生成，此处不再重复定义
GLOBE_BAR3D_OPTION = {
    "series": [{
        "type": "bar3D",
        "coordinateSystem": "globe",
        "barSize": 1,
        "label": {
            "show": True,
            "formatter": "{b}"
        }
    }]
}

# Globe 飞线图配置（仅包含图表特有配置，基础配置从GLOBE_BASIC_OPTION继承）
GLOBE_LINES3D_OPTION = {
    "series": [{
        "type": "lines3D",
        "coordinateSystem": "globe",
        "effect": {
            "show": True,
            "trailWidth": 1.5,
            "trailOpacity": 0.5,
            "trailLength": 0.2,
            "constantSpeed": 30
        },
        "blendMode": "lighter",
        "lineStyle": {
            "width": 1.5,
            "opacity": 0.25
        }
    }]
}


# K线图基础配置
KLINE_OPTION = {
    "animation": False,
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {
            "type": "cross"
        },
        "borderWidth": 1,
        "borderColor": "#ccc",
        "padding": 10,
        "textStyle": {
            "color": "#000"
        },
        "formatter": "JsCode:function(params) { var date = params[0].name; var result = date + '<br/>'; for(var i = 0; i < params.length; i++) { var item = params[i]; if(item.seriesName === 'K线') { result += '开盘: ' + item.value[1] + '<br/>'; result += '收盘: ' + item.value[2] + '<br/>'; result += '最低: ' + item.value[3] + '<br/>'; result += '最高: ' + item.value[4] + '<br/>'; } else { result += item.seriesName + ': ' + item.value + '<br/>'; } } return result; }"
    },
    "axisPointer": {
        "label": {
            "backgroundColor": "#777"
        }
    },
    "xAxis": {
        "type": "category",
        "boundaryGap": False,
        "axisLine": {"onZero": False},
        "splitLine": {"show": False},
        "min": "dataMin",
        "max": "dataMax"
    },
    "yAxis": {
        "scale": True,
        "splitArea": {"show": True}
    },
    "dataZoom": [
        {
            "type": "inside"
        },
        {
            "show": True,
            "type": "slider",
            "bottom": "3%"
        }
    ],
    "series": [
        {
            "name": "K线",
            "type": "candlestick",
            "itemStyle": {
                "color": "#ef5350",
                "color0": "#26a69a",
                "borderColor": "#ef5350",
                "borderColor0": "#26a69a"
            }
        }
    ]
}
