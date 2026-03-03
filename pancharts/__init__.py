#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts - A Python library for generating ECharts visualizations
"""

from .core import Pancharts
from .pandas_charts import k_v, km_nv, k2_nv, k_vm
from .utils import (
    add_quotes_to_keys,
    random_color,
    random_color_list,
    get_index_type,
    get_value_type,
    deep_merge,
    load_city_cnname,
    load_city_lnglat,
    load_countries_info
)
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
    CALENDAR_OPTION
)

__version__ = "0.1.0"
__author__ = "Wang Peng"
__email__ = "wangpeng_621@163.com"

__all__ = [
    "Pancharts",
    "k_v",
    "km_nv",
    "k2_nv",
    "k_vm",
    "add_quotes_to_keys",
    "random_color",
    "random_color_list",
    "get_index_type",
    "get_value_type",
    "deep_merge",
    "load_city_cnname",
    "load_city_lnglat",
    "load_countries_info",
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
    "RADAR_OPTION",
    "CALENDAR_OPTION"
]