#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts - A Python library for generating ECharts visualizations
"""

from .core import Pancharts
from .pandas_charts import k_v, km_nv, k2_nv, k_vm, gk_vm, gk_vm_amap, gk_vm_globe, sk_vm
from .utils import (
    add_quotes_to_keys,
    random_color,
    random_color_list,
    get_index_type,
    get_value_type,
    deep_merge,
    create_visual_map
)
from .agent import call_openai_api, parse_json_response, pchat, echat
from .chart_config import (
    BAR_OPTION,
    LINE_OPTION,
    SCATTER_OPTION,
    ESCATTER_OPTION,
    PIE_OPTION,
    FUNNEL_OPTION,
    WORDCLOUD_OPTION,
    SUNBURST_OPTION,
    TREEMAP_OPTION,
    TREE_OPTION,
    BAR3D_OPTION,
    GRAPH_OPTION,
    SANKEY_OPTION,
    HEATMAP_OPTION,
    PARALLEL_OPTION,
    RADAR_OPTION,
    MAP_OPTION,
    MAP3D_OPTION,
    CALENDAR_OPTION,
    GEO_OPTION,
    GEO_GRAPH_OPTION,
    GEO3D_BAR3D_OPTION,
    GEO3D_LINES3D_OPTION,
    AMAP_OPTION,
    AMAP_HEATMAP_OPTION,
    AMAP_GRAPH_OPTION,
    AMAP_LINES_OPTION,
    GLOBE_BASIC_OPTION,
    GLOBE_NIGHT_OPTION,
    GLOBE_REALISTIC_OPTION,
    GLOBE_TERRAIN_OPTION,
    GLOBE_SCATTER_OPTION,
    GLOBE_BAR3D_OPTION,
    GLOBE_LINES3D_OPTION,
    KLINE_OPTION
)

__version__ = "0.1.5"
__author__ = "wang peng"
__email__ = "wangpeng_621@163.com"

__all__ = [
    "Pancharts",
    "k_v",
    "km_nv",
    "k2_nv",
    "k_vm",
    "gk_vm",
    "gk_vm_amap",
    "gk_vm_globe",
    "add_quotes_to_keys",
    "random_color",
    "random_color_list",
    "get_index_type",
    "get_value_type",
    "deep_merge",
    "create_visual_map",
    "call_openai_api",
    "parse_json_response",
    "pchat",
    "echat",
    "BAR_OPTION",
    "LINE_OPTION",
    "SCATTER_OPTION",
    "ESCATTER_OPTION",
    "PIE_OPTION",
    "FUNNEL_OPTION",
    "WORDCLOUD_OPTION",
    "SUNBURST_OPTION",
    "TREEMAP_OPTION",
    "TREE_OPTION",
    "BAR3D_OPTION",
    "GRAPH_OPTION",
    "SANKEY_OPTION",
    "HEATMAP_OPTION",
    "PARALLEL_OPTION",
    "MAP_OPTION",
    "MAP3D_OPTION",
    "RADAR_OPTION",
    "CALENDAR_OPTION",
    "GEO_OPTION",
    "GEO_GRAPH_OPTION",
    "GEO3D_BAR3D_OPTION",
    "GEO3D_LINES3D_OPTION",
    "AMAP_OPTION",
    "AMAP_HEATMAP_OPTION",
    "AMAP_GRAPH_OPTION",
    "AMAP_LINES_OPTION",
    "GLOBE_BASIC_OPTION",
    "GLOBE_NIGHT_OPTION",
    "GLOBE_REALISTIC_OPTION",
    "GLOBE_TERRAIN_OPTION",
    "GLOBE_SCATTER_OPTION",
    "GLOBE_BAR3D_OPTION",
    "GLOBE_LINES3D_OPTION",
    "sk_vm",
    "KLINE_OPTION"
]
