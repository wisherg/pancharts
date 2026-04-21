#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts - A Python library for generating ECharts visualizations
"""

from .core import Pancharts
from .pandas_charts import k_v, km_nv, k2_nv, k_vm, gk_vm
from .utils import (
    add_quotes_to_keys,
    random_color,
    random_color_list,
    get_index_type,
    get_value_type,
    deep_merge,
    load_city_cnname,
    load_city_lnglat,
    load_countries_info,
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
    GEO3D_LINES3D_OPTION
)

__version__ = "0.1.4.1"
__author__ = "wang peng"
__email__ = "wangpeng_621@163.com"

__all__ = [
    "Pancharts",
    "k_v",
    "km_nv",
    "k2_nv",
    "k_vm",
    "gk_vm",
    "add_quotes_to_keys",
    "random_color",
    "random_color_list",
    "get_index_type",
    "get_value_type",
    "deep_merge",
    "load_city_cnname",
    "load_city_lnglat",
    "load_countries_info",
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
    "GEO3D_LINES3D_OPTION"
]
