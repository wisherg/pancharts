#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts pandas可视化模块
包含基于pandas的数据可视化类
"""

import pandas as pd

from pancharts.chart_config import (
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
    GLOBE_SCATTER_OPTION,
    GLOBE_BAR3D_OPTION,
    GLOBE_LINES3D_OPTION,
    KLINE_OPTION
)
from pancharts.utils import get_index_type, get_value_type, random_color, deep_merge, create_visual_map
from pancharts.core import Pancharts


class k_v:
    """
    用于可视化pandas中的单列索引序列数据（Series）。
    
    主要功能：
        - 自动将pandas Series转换为ECharts可接受的数据格式
        - 自动判断索引类型（category或value）与数值类型（category或value）
        - 支持通过config参数传入额外的图表配置，与默认配置合并
        - 提供多种常用图表类型的可视化方法
    
    支持的图表类型：
        - bar: 柱状图
        - line: 折线图
        - scatter: 散点图
        - escatter: 增强散点图
        - pie: 饼图
        - funnel: 漏斗图
        - wordcloud: 词云图
        - calendar: 日历热图
        - map: 地图可视化
    
    参数：
        data: pandas Series - 要可视化的数据
    
    用法示例：
        from pancharts import k_v
        import pandas as pd
        
        data = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
        chart = k_v(data).bar()
        chart.render()
    """
    def __init__(self, data):
        self.rect_data = list(data.items())
        self.xaxis_type = get_index_type(data)
        self.yaxis_type = get_value_type(data)
        self.base_data = []
        self.xdata = []
        for i in data.items():
            self.base_data.append({"name": i[0], "value": i[1]})
            self.xdata.append(i[0])
        
        # 按照优先级：data.index.name > data.name > ""
        self.legend = ""
        if data.index.name:
            self.legend = data.index.name
        elif data.name:
            self.legend = data.name

        self.rect_data_config = {
            'xAxis': {
                'type': self.xaxis_type,
                'data': self.xdata
            },
            'yAxis': {
                'type': self.yaxis_type
            },
            'series': [
                {
                    'data': self.base_data, "name": self.legend
                }
            ]
        }
        self.base_data_config = {
            "title": {
                "text": self.legend
            },
            "series": [{"data": self.base_data}]
        }
        
        # 日历热图配置
        self.calendar_data_config = {
            "visualMap": {"min": int(data.values.min()), "max": int(data.values.max())},
            "calendar": {"range": [data.index.min(), data.index.max()]},
            "series": [{"data": self.rect_data}]
        }
        
        # 地图配置
        self.map_data_config = {
            "visualMap": {"min": int(data.values.min()), "max": int(data.values.max())},
            "series": [{"data": self.base_data}]
        }

    def bar(self, config: dict | None = {}):
        return Pancharts(graph_config=BAR_OPTION, data_config=self.rect_data_config, user_option=config)
    
    def line(self, config: dict | None = {}):
        return Pancharts(graph_config=LINE_OPTION, data_config=self.rect_data_config, user_option=config)
    
    def scatter(self, config: dict | None = {}):
        return Pancharts(graph_config=SCATTER_OPTION, data_config=self.rect_data_config, user_option=config)
    
    def escatter(self, config: dict | None = {}):
        return Pancharts(graph_config=ESCATTER_OPTION, data_config=self.rect_data_config, user_option=config)
    
    def pie(self, config: dict | None = {}):
        return Pancharts(graph_config=PIE_OPTION, data_config=self.base_data_config, user_option=config)
    
    def funnel(self, config: dict | None = {}):
        return Pancharts(graph_config=FUNNEL_OPTION, data_config=self.base_data_config, user_option=config)
    
    def wordcloud(self, config: dict | None = {}):
        return Pancharts(graph_config=WORDCLOUD_OPTION, data_config=self.base_data_config, user_option=config)
    
    def calendar(self, config: dict | None = {}):
        return Pancharts(graph_config=CALENDAR_OPTION, data_config=self.calendar_data_config, user_option=config)
    
    def map(self, map_name: str, config: dict | None = {}):
        """
        地图可视化
        
        参数：
            map_name: str - 地图名称，如"中国"、"美国"等
            config: dict | None - 额外的配置项
            
        返回：
            Pancharts - 图表实例
        """
        # 创建地图特定配置
        map_specific_config = {
            "series": [
                {
                    "map": map_name
                }
            ]
        }
        # 合并地图特定配置到数据配置中
        map_data_config = deep_merge(self.map_data_config, map_specific_config)
        return Pancharts(graph_config=MAP_OPTION, data_config=map_data_config, user_option=config)


class km_nv:
    """
    用于可视化pandas中的多列索引、单列数值型数据的序列（Series）。
    
    主要功能：
        - 自动将具有多级索引的pandas Series转换为树形数据结构
        - 支持通过config参数传入额外的图表配置，与默认配置合并
        - 提供层次化数据可视化的图表类型
        - 自动为不同层级节点生成随机颜色
    
    支持的图表类型：
        - sunburst: 旭日图
        - treemap: 矩形树图
        - tree: 树图
    
    参数：
        data: pandas Series - 要可视化的数据，需具有多级索引
    
    用法示例：
        from pancharts import km_nv
        import pandas as pd
        
        # 创建具有多级索引的数据
        index = pd.MultiIndex.from_product([['A', 'B'], ['x', 'y']])
        data = pd.Series([10, 20, 30, 40], index=index)
        chart = km_nv(data).sunburst()
        chart.render()
    """
    def __init__(self, data):
        self.data = data.sort_index(level=list(range(data.index.nlevels)))
        self.n = data.index.nlevels
        self.color_code = {}
    
    def get_color(self, key):
        """生成一个随机的颜色代码"""
        try:
            color = self.color_code[key]
        except:
            self.color_code[key] = random_color()
            color = self.color_code[key]
        return color

    def sun_tree(self):
        bank_list = ["" for i in range(self.n)]
        index_list_tem = ["" for i in range(self.n)]
        sun_tree = []
        for i, j in self.data.items():
            sun_tree_tem = sun_tree
            for k in range(0, self.n - 1):
                if i[k] != index_list_tem[k]:
                    sun_tree_tem.append({"name": i[k], "itemStyle": {"color": self.get_color(i[k])}, "children": [], })
                    index_list_tem[k:] = [i[k]] + bank_list[k + 1:]
                sun_tree_tem = sun_tree_tem[-1]["children"]
            sun_tree_tem.append({"name": i[-1], "itemStyle": {"color": self.get_color(i[-1])}, "value": j, })
        return {"series": [{"data": sun_tree}]}
    
    def tree_data(self):
        bank_list = ["" for i in range(self.n)]
        index_list_tem = ["" for i in range(self.n)]
        sun_tree = []
        for i, j in self.data.items():
            sun_tree_tem = sun_tree
            for k in range(0, self.n - 1):
                if i[k] != index_list_tem[k]:
                    sun_tree_tem.append({"name": i[k], "children": [], })
                    index_list_tem[k:] = [i[k]] + bank_list[k + 1:]
                sun_tree_tem = sun_tree_tem[-1]["children"]
            sun_tree_tem.append({"name": i[-1], "value": j, })
        return sun_tree
    
    def treemap_data(self):
        bank_list = ["" for i in range(self.n)]
        index_list_tem = ["" for i in range(self.n)]
        sun_tree = []
        for i, j in self.data.items():
            sun_tree_tem = sun_tree
            for k in range(0, self.n - 1):
                if i[k] != index_list_tem[k]:
                    sun_tree_tem.append({"name": i[k], "value": j, "children": []})
                    index_list_tem[k:] = [i[k]] + bank_list[k + 1:]
                else:
                    sun_tree_tem[-1]["value"] = sun_tree_tem[-1]["value"] + j
                sun_tree_tem = sun_tree_tem[-1]["children"]
            sun_tree_tem.append({"name": i[-1], "value": j})
        return sun_tree
    
    def sunburst(self, config: dict | None = {}):
        return Pancharts(graph_config=SUNBURST_OPTION, data_config=self.sun_tree(), user_option=config)
    
    def treemap(self, num: int = None, config: dict | None = {}):
        if num is None:
            data_config = {"series": [{"data": self.treemap_data()}]}
        elif num >= 0:
            data_config = {"series": [{"data": [self.treemap_data()[num]]}]}
        return Pancharts(graph_config=TREEMAP_OPTION, data_config=data_config, user_option=config)
    
    def tree(self, num: int = None, config: dict | None = {}):
        if num is None:
            data_config = {"series": [{"data": self.tree_data()[0]}]}
        elif num >= 0:
            data_config = {"series": [{"data": [self.tree_data()[num]]}]}
        return Pancharts(graph_config=TREE_OPTION, data_config=data_config, user_option=config)


class k2_nv:
    """
    用于可视化pandas中的两层索引、单列数值型数据的序列（Series）。
    
    主要功能：
        - 自动将具有双层索引的pandas Series转换为ECharts可接受的数据格式
        - 支持通过config参数传入额外的图表配置，与默认配置合并
        - 提供关系型和三维数据可视化的图表类型
        - 支持为图网络数据指定节点分类
    
    支持的图表类型：
        - bar3d: 3D柱状图
        - graph: 图网络
        - sankey: 桑基图
        - heatmap: 热力图
    
    参数：
        data: pandas Series - 要可视化的数据，需具有双层索引结构
        cate: list, optional - 图网络节点分类，长度为2的列表
    
    用法示例：
        from pancharts import k2_nv
        import pandas as pd
        
        # 创建具有双层索引的数据（通常由两列groupby产生）
        data = pd.Series(
            [10, 20, 30, 40],
            index=pd.MultiIndex.from_product([['A', 'B'], ['x', 'y']])
        )
        chart = k2_nv(data).heatmap()
        chart.render()
    """

    _NOT_PROVIDED = object()

    def __init__(self, data, cate=_NOT_PROVIDED):
        """
        初始化k2_nv实例
        
        参数：
            data: pandas Series - 要可视化的数据，需具有双层索引结构，通常是两列groupby产生的
            cate: list, optional - 图网络节点分类，长度为2的列表
        """
        
        if cate is self._NOT_PROVIDED:
            self.cate0 = []
        else:
            self.cate0 = cate
        
        self.data = data
        self.df_data = self.data.reset_index()
        self.bar3d_data = self.df_data.values.tolist()
        self.bar3d_data_object=[{"value":i} for i in self.bar3d_data]
        self.xtype = get_value_type(self.df_data.iloc[:, 0])
        self.ytype = get_value_type(self.df_data.iloc[:, 1])
        self.ztype = get_value_type(self.df_data.iloc[:, 2])

        self.bar3d_data_option = {
            'xAxis3D': {'type': self.xtype},
            'yAxis3D': {'type': self.ytype},
            'zAxis3D': {'type': self.ztype},
            'series': [{"data": self.bar3d_data_object}]
        }
        self.nodes, self.links = self.bi_network_data()
        self.graph_data_option = {
            "series": [{
            "data": self.nodes,
            "links": self.links
            }]
        }

        self.sankey_data_option = self.graph_data_option

        self.heatmap_data_option = {
            "xAxis": {'type': self.xtype},
            "yAxis": {'type': self.ytype},
            "visualMap": {"max": max(self.df_data.iloc[:, 2]), "min": min((self.df_data.iloc[:, 2]))},
            "series": [{"data": self.bar3d_data}]
        }

    def bi_network_data(self):
        links = []
        index0 = set([])
        index1 = set([])
        for i in self.data.items():
            links.append({"source": str(i[0][0]), "target": str(i[0][1]), "value": i[1]})
            index0.add(str(i[0][0]))
            index1.add(str(i[0][1]))
        nodes = []
        for i in index0:
            nodes.append({"name": i, "category": 0})
        
        if len(self.cate0) == 2:
            for i in index1:
                nodes.append({"name": i, "category": 1})
        elif len(self.cate0) != 2:
            for i in index1:
                nodes.append({"name": i, "category": 0})
        return nodes, links

    def bar3d(self, config: dict | None = {}):
        return Pancharts(graph_config=BAR3D_OPTION, data_config=self.bar3d_data_option, user_option=config)

    def graph(self, config: dict | None = {}):
        return Pancharts(graph_config=GRAPH_OPTION, data_config=self.graph_data_option, user_option=config)
    
    def sankey(self, config: dict | None = {}):
        return Pancharts(graph_config=SANKEY_OPTION, data_config=self.sankey_data_option, user_option=config)
    
    def heatmap(self, config: dict | None = {}):
        return Pancharts(graph_config=HEATMAP_OPTION, data_config=self.heatmap_data_option, user_option=config)


class k_vm:
    """
    用于可视化pandas中的单列索引、多列数值型数据的DataFrame。
    
    主要功能：
        - 自动将pandas DataFrame转换为ECharts可接受的数据格式
        - 支持通过config参数传入额外的图表配置，与默认配置合并
        - 提供多维数据可视化的图表类型
        - 支持灵活的数据编码方式（rect_plot方法）
        - 支持数据的可视化映射（vmap_size和vmap_color方法）
    
    支持的图表类型：
        - parallel: 平行坐标图
        - radar: 雷达图
        - rect_plot: 灵活数据编码方式，支持多种二维图表
    
    参数：
        data: pandas DataFrame - 要可视化的数据，需具有单列索引和多列数值
    
    用法示例：
        from pancharts import k_vm
        import pandas as pd
        import numpy as np
        
        # 创建数据
        data = pd.DataFrame(
            np.random.rand(5, 4),
            columns=['a', 'b', 'c', 'd'],
            index=['x', 'y', 'z', 'w', 'v']
        )
        chart = k_vm(data).parallel()
        chart.render()
    """
    def __init__(self, data):
        self.data = data
        self.parallel_data = self.data.values.tolist()
        
        # dataset相关配置
        self.dataset = self.data.reset_index()
        self.dataset_value = self.dataset.values.tolist()
        self.dimensions = self.dataset.columns.tolist()
        self.column_type = [get_value_type(self.dataset[i]) for i in self.dataset]

        self.parallel_data_option = {
            "parallelAxis": self.parallel_schema(),
            "series": [{"data": self.parallel_data}]
        }

        self.radar_data_option = {
            "legend": {"data": self.data.index.tolist()},
            "radar": {"indicator": self.radar_schema()},
            "series": [{"data": self.radar_data()}]
        }
        
        # dataset方式配置图表
        self.dataset_option = {
            "dataset": {
                "dimensions": self.dimensions,
                "source": self.dataset_value
            }
        }
    
    def parallel_schema(self):
        from .utils import get_value_type
        
        schema = []
        n = 0
        for i in self.data:
            value_type = get_value_type(self.data[i])
            if value_type == 'category':
                schema.append({"dim": n, "name": i, "type": "category", "data": self.data[i].unique().tolist()})
            else:
                schema.append({"dim": n, "name": i, "type": "value"})
            n = n + 1
        return schema
    
    def radar_schema(self):
        """雷达图只接受数值型数据"""
        schema = []
        for i in self.data:
            schema.append({"name": i, "max": self.data[i].max(), "min": self.data[i].min()})
        return schema
    
    def radar_data(self):
        radar_data = []
        for i in self.data.iterrows():
            radar_data.append({"name": i[0], "value": i[1].values.tolist()})
        return radar_data
    
    def vmap_size(self, dimension: int, symbolSize: list | None = [5, 60]):
        """
        配置根据维度大小映射点大小
        
        参数：
            dimension: int - 维度索引
            symbolSize: list - 点大小范围
        
        返回：
            dict - 可视化映射配置
        """
        return {
            "visualMap": {
                "dimension": dimension,
                "min": self.dataset[self.dimensions[dimension]].min(),
                "max": self.dataset[self.dimensions[dimension]].max(),
                "inRange": {
                    "symbolSize": symbolSize
                }
            }
        }
    
    def vmap_color(self, dimension: int, color: list | None = ['#f2c31a', '#24b7f2']):
        """
        配置根据维度大小映射颜色
        
        参数：
            dimension: int - 维度索引
            color: list - 颜色范围
        
        返回：
            dict - 可视化映射配置
        """
        return {
            "visualMap": {
                "dimension": dimension,
                "min": self.dataset[self.dimensions[dimension]].min(),
                "max": self.dataset[self.dimensions[dimension]].max(),
                "inRange": {
                    "color": color
                }
            }
        }
    
    def parallel(self, config: dict | None = {}):
        return Pancharts(graph_config=PARALLEL_OPTION, data_config=self.parallel_data_option, user_option=config)
    
    def radar(self, config: dict | None = {}):
        return Pancharts(graph_config=RADAR_OPTION, data_config=self.radar_data_option, user_option=config)
    
    def rect_plot(self, series_type: str, encode_x: int | list, encode_y: int | list, config: dict | None = {}):
        """
        灵活的数据编码方式绘制图表
        
        参数：
            series_type: str - 图表类型
            encode_x: int | list - x轴编码
            encode_y: int | list - y轴编码
            config: dict - 额外配置
        
        返回：
            Pancharts - 图表实例
        """
        # 检查encode_x与encode_y是否同时为列表
        if isinstance(encode_x, list) and isinstance(encode_y, list):
            raise ValueError("encode_x与encode_y不能同时为列表")
        
        # 当三个参数：series_type为字符串，encode_x与encode_y为整数时
        if isinstance(encode_x, int) and isinstance(encode_y, int) and isinstance(series_type, str):
            option_z = {
                "legend": {},
                "xAxis": {"type": self.column_type[encode_x]},
                "yAxis": {"type": self.column_type[encode_y]},
                "series": [
                    {
                        "type": series_type,
                        "name": self.dataset.columns[encode_x],
                        "encode": {
                            "x": encode_x,
                            "y": encode_y,
                        }
                    }
                ]
            }
        # 当series_type为字符串，encode_x为列表，encode_y为整数时
        elif isinstance(series_type, str) and isinstance(encode_x, list) and isinstance(encode_y, int):
            series_option = []
            for i in encode_x:
                series_option.append({
                    "type": series_type,
                    "name": self.dataset.columns[i],
                    "encode": {
                        "x": i,
                        "y": encode_y,
                    }
                })
            option_z = {
                "legend": {},
                "xAxis": {"type": self.column_type[encode_x[0]]},
                "yAxis": {"type": self.column_type[encode_y]},
                "series": series_option
            }
        # 当series_type为字符串，encode_x为整数，encode_y为列表时
        elif isinstance(series_type, str) and isinstance(encode_x, int) and isinstance(encode_y, list):
            series_option = []
            for i in encode_y:
                series_option.append({
                    "type": series_type,
                    "name": self.dataset.columns[i],
                    "encode": {
                        "x": encode_x,
                        "y": i,
                    }
                })
            option_z = {
                "legend": {},
                "xAxis": {"type": self.column_type[encode_x]},
                "yAxis": {"type": self.column_type[encode_y[0]]},
                "series": series_option
            }
        # 当series_type为列表，encode_x为列表，encode_y为整数时
        elif isinstance(series_type, list) and isinstance(encode_x, list) and isinstance(encode_y, int):
            # 判断series_type与encode_x的长度是否相同
            if len(series_type) != len(encode_x):
                raise ValueError("series_type与encode_x的长度必须相同")
            series_option = []
            for i in range(len(series_type)):
                series_option.append({
                    "type": series_type[i],
                    "name": self.dataset.columns[encode_x[i]],
                    "encode": {
                        "x": encode_x[i],
                        "y": encode_y,
                    }
                })
            option_z = {
                "legend": {},
                "xAxis": {"type": self.column_type[encode_x[0]]},
                "yAxis": {"type": self.column_type[encode_y]},
                "series": series_option
            }
        # 当series_type为列表，encode_x为整数，encode_y为列表时
        elif isinstance(series_type, list) and isinstance(encode_x, int) and isinstance(encode_y, list):
            # 判断series_type与encode_y的长度是否相同
            if len(series_type) != len(encode_y):
                raise ValueError("series_type与encode_y的长度必须相同")
            series_option = []
            for i in range(len(series_type)):
                series_option.append({
                    "type": series_type[i],
                    "name": self.dataset.columns[encode_y[i]],
                    "encode": {
                        "x": encode_x,
                        "y": encode_y[i],
                    }
                })
            option_z = {
                "legend": {},
                "xAxis": {"type": self.column_type[encode_x]},
                "yAxis": {"type": self.column_type[encode_y[0]]},
                "series": series_option
            }
        else:
            raise ValueError("参数类型不匹配")
        
        return Pancharts(
            graph_config=option_z,
            data_config=self.dataset_option,
            user_option=config
        )

class gk_vm:
    """
    地理数据可视化类，用于可视化pandas中表示地理信息的数据。
    
    主要功能：
        - 支持基于地理坐标的数据可视化
        - 自动将DataFrame转换为ECharts地理图表可接受的数据格式
        - 支持多种地理图表类型，包括2D和3D图表
        - 支持数据可视化映射（颜色、大小等）
    
    数据格式要求：
        - DataFrame的索引为地理位置名称
        - 默认前两列数据为经纬度（longitude, latitude）
        - 后续列可以是其他数值型数据，用于可视化映射
    
    支持的图表类型：
        - scatter: 地理散点图
        - escatter: 地理特效散点图
        - heatmap: 地理热力图
        - graph: 地理关系图（节点-边）
        - bar3d: 3D柱状图（基于geo3D）
        - line3d: 3D飞线图（基于geo3D）
    
    参数：
        data: pandas DataFrame - 地理数据，索引为位置名称，前两列为经纬度
        map_type: str - 地图类型，如"china"、"world"等
    
    用法示例：
        from pancharts import gk_vm
        import pandas as pd
        
        # 创建地理数据（索引为城市名，前两列为经纬度）
        data = pd.DataFrame({
            'lng': [116.4074, 121.4737, 104.0668],
            'lat': [39.9042, 31.2304, 30.5728],
            'value': [100, 200, 150]
        }, index=['北京', '上海', '成都'])
        
        # 创建地理可视化实例
        geo_chart = gk_vm(data, map_type='china')
        
        # 绘制散点图
        chart = geo_chart.scatter(dimension=2, visual_type='color')
        chart.render()
    """
    def __init__(self,data,map_type:str):
        self.data = data
        self.map_type = map_type
        self.geo_data=[]
        for i in self.data.iterrows():
            self.geo_data.append({
                'name':i[0],
                'value':i[1].tolist()
            })
        self.geo_map={"geo":{"map":self.map_type}}
        self.geo3d_map={"geo3D":{"map":self.map_type}}
        

    def scatter(self, dimension: int | list = 2, visual_type: str | list = "color", config: dict | None = {}):
      
        geo_data_option = {
            "series": [{
                "type": "scatter",
                "coordinateSystem": "geo",
                "data": self.geo_data}]
        }
        geo_data_option.update(self.geo_map)
        geo_data_option.update(create_visual_map(self.data, visual_type, dimension))
        return Pancharts(graph_config=GEO_OPTION, data_config=geo_data_option, user_option=config)

    def escatter(self, dimension: int | list = 2, visual_type: str | list = "color", config: dict | None = {}):
      
        geo_data_option = {
            "series": [{
                "type": "effectScatter",
                "coordinateSystem": "geo",
                "data": self.geo_data}]
        }
        geo_data_option.update(self.geo_map)
        geo_data_option.update(create_visual_map(self.data, visual_type, dimension))
        return Pancharts(graph_config=GEO_OPTION, data_config=geo_data_option, user_option=config)
    
    def heatmap(self, dimension: int | list = 2, visual_type: str | list = "color", config: dict | None = {}):
      
        geo_data_option = {
            "series": [{
                "type": "heatmap",
                "coordinateSystem": "geo",
                "data": self.geo_data}]
        }
        geo_data_option.update(self.geo_map)
        geo_data_option.update(create_visual_map(self.data, visual_type, dimension))
        return Pancharts(graph_config=GEO_OPTION, data_config=geo_data_option, user_option=config)
    
    def graph(self, edges: list, config: dict | None = None):
        if config is None:
            config = {}
        
        edges_data = []
        for i in edges:
            edges_data.append({
                'source': i[0],
                'target': i[1]
            })
      
        geo_data_option = {
            "series": [{
                "nodes": self.geo_data,
                "edges": edges_data
            }]
        }
        geo_data_option.update(self.geo_map)
        return Pancharts(graph_config=GEO_GRAPH_OPTION, data_config=geo_data_option, user_option=config)
    
    def bar3d(self, dimension: int | list = 2, visual_type: str | list = "color", config: dict | None = None):
        if config is None:
            config = {}
        
        geo_data_option = {
            "series": [{
                "data": self.geo_data
            }]
        }
        geo_data_option.update(self.geo3d_map)
        geo_data_option.update(create_visual_map(self.data, visual_type, dimension))
        return Pancharts(graph_config=GEO3D_BAR3D_OPTION, data_config=geo_data_option, user_option=config)
    
    def line3d(self, coords: list, config: dict | None = None):
        if config is None:
            config = {}
        
        coords_data = []
        for i in coords:
            coords_data.append({
                'coords': [self.data.loc[i[0]].tolist()[0:2], self.data.loc[i[1]].tolist()[0:2]]
            })
      
        geo_data_option = {
            "series": [{
                "data": coords_data
            }]
        }
        geo_data_option.update(self.geo3d_map)
        return Pancharts(graph_config=GEO3D_LINES3D_OPTION, data_config=geo_data_option, user_option=config)


class gk_vm_amap:
    """
    高德地图地理数据可视化类，用于通过高德地图API进行地理信息可视化。
    
    主要功能：
        - 支持基于高德地图的地理坐标数据可视化
        - 自动通过高德地图API获取地图中心点
        - 支持多种地理图表类型
        - 支持数据可视化映射（颜色、大小等）
    
    数据格式要求：
        - DataFrame的索引为地理位置名称
        - 默认前两列数据为经纬度（longitude, latitude）
        - 后续列可以是其他数值型数据，用于可视化映射
    
    支持的图表类型：
        - scatter: 散点图
        - effectScatter: 涟漪高亮散点图
        - heatmap: 热力图
        - graph: 关系网络图
        - lines: 飞线图/迁徙图
    
    参数：
        data: pandas DataFrame - 地理数据，索引为位置名称，前两列为经纬度
        map_type: str - 地址名称，用于获取地图中心点（如"北京市"、"上海市"等）
    
    用法示例：
        from pancharts import gk_vm_amap
        import pandas as pd
        
        # 创建地理数据（索引为城市名，前两列为经纬度）
        data = pd.DataFrame({
            'lng': [116.4074, 121.4737, 104.0668],
            'lat': [39.9042, 31.2304, 30.5728],
            'value': [100, 200, 150]
        }, index=['北京', '上海', '成都'])
        
        # 创建高德地图可视化实例（以"北京市"为中心）
        amap_chart = gk_vm_amap(data, map_type='北京市')
        
        # 绘制散点图
        chart = amap_chart.scatter(dimension=2, visual_type='color')
        chart.render()
    """
    
    def __init__(self, data, map_type: str = None):
        """
        初始化gk_vm_amap实例
        
        参数：
            data: pandas DataFrame - 地理数据，索引为位置名称，前两列为经纬度
            map_type: str, optional - 地址名称，用于获取地图中心点。默认为None，此时使用数据的平均经纬度作为中心
        """
        from pancharts.utils import geocode_amap
        
        self.data = data
        self.map_type = map_type
        
        # 构建地理数据格式
        self.geo_data = []
        for i in self.data.iterrows():
            self.geo_data.append({
                'name': i[0],
                'value': i[1].tolist()
            })
        
        # 计算数据的平均经纬度作为默认中心
        avg_lng = self.data.iloc[:, 0].mean()
        avg_lat = self.data.iloc[:, 1].mean()
        self.center = (avg_lng, avg_lat)
        
        # 如果提供了map_type，尝试通过高德地图API获取地图中心点
        if map_type:
            api_center = geocode_amap(map_type)
            if api_center != (None, None):
                self.center = api_center
        
        # 构建amap配置
        self.amap_map = {
            "amap": {
                "center": list(self.center),
                "viewMode": "3D",
                "resizeEnable": True,
                "renderOnMoving": True,
                "echartsLayerInteractive": True
            }
        }
    
    def scatter(self, dimension: int | list = 2, visual_type: str | list = "color", config: dict | None = {}):
        """
        创建高德地图散点图
        
        参数：
            dimension: int | list - 要映射的列索引，默认为第2列（索引从0开始）
            visual_type: str | list - 映射类型，可选值为 "color", "opacity", "symbolSize" 等
            config: dict - 额外的配置项
        
        返回：
            Pancharts - 图表实例
        """
        if config is None:
            config = {}
        
        amap_data_option = {
            "series": [{
                "type": "scatter",
                "coordinateSystem": "amap",
                "data": self.geo_data
            }]
        }
        amap_data_option.update(self.amap_map)
        amap_data_option.update(create_visual_map(self.data, visual_type, dimension))
        return Pancharts(graph_config=AMAP_OPTION, data_config=amap_data_option, user_option=config)
    
    def escatter(self, dimension: int | list = 2, visual_type: str | list = "color", config: dict | None = {}):
        """
        创建高德地图涟漪高亮散点图
        
        参数：
            dimension: int | list - 要映射的列索引，默认为第2列（索引从0开始）
            visual_type: str | list - 映射类型，可选值为 "color", "opacity", "symbolSize" 等
            config: dict - 额外的配置项
        
        返回：
            Pancharts - 图表实例
        """
        if config is None:
            config = {}
        
        amap_data_option = {
            "series": [{
                "type": "effectScatter",
                "coordinateSystem": "amap",
                "data": self.geo_data,
                "effect": {
                    "show": True,
                    "scale": 2,
                    "period": 3
                }
            }]
        }
        amap_data_option.update(self.amap_map)
        amap_data_option.update(create_visual_map(self.data, visual_type, dimension))
        return Pancharts(graph_config=AMAP_OPTION, data_config=amap_data_option, user_option=config)
    
    def heatmap(self, dimension: int | list = 2, visual_type: str | list = "color", config: dict | None = {}):
        """
        创建高德地图热力图
        
        参数：
            dimension: int | list - 要映射的列索引，默认为第2列（索引从0开始）
            visual_type: str | list - 映射类型，可选值为 "color", "opacity", "symbolSize" 等
            config: dict - 额外的配置项
        
        返回：
            Pancharts - 图表实例
        """
        if config is None:
            config = {}
        
        amap_data_option = {
            "series": [{
                "type": "heatmap",
                "coordinateSystem": "amap",
                "data": self.geo_data
            }]
        }
        amap_data_option.update(self.amap_map)
        amap_data_option.update(create_visual_map(self.data, visual_type, dimension))
        return Pancharts(graph_config=AMAP_HEATMAP_OPTION, data_config=amap_data_option, user_option=config)
    
    def graph(self, edges: list, config: dict | None = None):
        """
        创建高德地图关系网络图
        
        参数：
            edges: list - 边的列表，每个元素为(source, target)元组
            config: dict - 额外的配置项
        
        返回：
            Pancharts - 图表实例
        """
        if config is None:
            config = {}
        
        edges_data = []
        for i in edges:
            edges_data.append({
                'source': i[0],
                'target': i[1]
            })
        
        amap_data_option = {
            "series": [{
                "nodes": self.geo_data,
                "edges": edges_data
            }]
        }
        amap_data_option.update(self.amap_map)
        return Pancharts(graph_config=AMAP_GRAPH_OPTION, data_config=amap_data_option, user_option=config)
    
    def lines(self, coords: list, config: dict | None = None):
        """
        创建高德地图飞线图/迁徙图
        
        参数：
            coords: list - 飞线路径列表，每个元素为(start, end)元组，表示从start到end的飞线
            config: dict - 额外的配置项
        
        返回：
            Pancharts - 图表实例
        """
        if config is None:
            config = {}
        
        coords_data = []
        for i in coords:
            coords_data.append({
                'coords': [self.data.loc[i[0]].tolist()[0:2], self.data.loc[i[1]].tolist()[0:2]]
            })
        
        amap_data_option = {
            "series": [{
                "data": coords_data
            }]
        }
        amap_data_option.update(self.amap_map)
        return Pancharts(graph_config=AMAP_LINES_OPTION, data_config=amap_data_option, user_option=config)


class gk_vm_globe:
    """
    Globe 地球可视化类，用于在三维地球表面上进行数据可视化。
    
    主要功能：
        - 支持基于ECharts Globe组件的全球地理数据可视化
        - 提供多种地球渲染风格（基础、夜景、真实感、地形）
        - 支持数据可视化映射（颜色、大小等）
    
    数据格式要求：
        - DataFrame的索引为地理位置名称
        - 前两列为经纬度（longitude, latitude）
        - 后续列可以是其他数值型数据，用于可视化映射
    
    支持的globe类型：
        - 'basic': 基础地球配置，使用lambert着色
        - 'night': 带高度纹理和夜景图层的地球
        - 'realistic': 真实感渲染地球，使用PBR材质
        - 'terrain': 地形渲染地球，显示地形起伏
    
    支持的图表类型：
        - scatter: 3D散点图
        - bar3d: 3D柱状图
        - lines3d: 3D飞线图/迁徙图
    
    参数：
        data: pandas DataFrame - 地理数据，索引为位置名称，前两列为经纬度
        globe_type: str, optional - 地球类型，可选值为 'basic', 'night', 'realistic', 'terrain'，默认为 'basic'
    
    用法示例：
        from pancharts import gk_vm_globe
        import pandas as pd
        
        # 创建地理数据（索引为城市名，前两列为经纬度）
        data = pd.DataFrame({
            'lng': [116.4074, 121.4737, 104.0668, -73.9857],
            'lat': [39.9042, 31.2304, 30.5728, 40.7484],
            'value': [100, 200, 150, 180]
        }, index=['北京', '上海', '成都', '纽约'])
        
        # 创建Globe可视化实例（使用夜景模式）
        globe_chart = gk_vm_globe(data, globe_type='night')
        
        # 绘制散点图
        chart = globe_chart.scatter(dimension=2, visual_type='color')
        chart.render()
    """
    
    def __init__(self, data, globe_type: str = 'basic'):
        """
        初始化gk_vm_globe实例
        
        参数：
            data: pandas DataFrame - 地理数据，索引为位置名称，前两列为经纬度
            globe_type: str - 地球类型，可选值为 'basic', 'night', 'realistic', 'terrain'
        """
        self.data = data
        self.globe_type = globe_type
        
        # 构建地理数据格式
        # Globe的scatter3D数据格式为 [经度, 纬度, 数据值]
        # visualMap使用第三个维度(数据值)进行映射
        self.geo_data = []
        for i in self.data.iterrows():
            row_data = i[1].tolist()
            self.geo_data.append({
                'name': i[0],
                'value': row_data[:3]
            })
        
        # 根据globe_type设置对应的地球配置
        self._setup_globe_config()
    
    def _setup_globe_config(self):
        """根据globe_type设置地球配置"""
        import copy
        from pancharts.chart_config import (
            GLOBE_BASIC_OPTION,
            GLOBE_NIGHT_OPTION,
            GLOBE_REALISTIC_OPTION,
            GLOBE_TERRAIN_OPTION
        )
        
        globe_configs = {
            'basic': GLOBE_BASIC_OPTION,
            'night': GLOBE_NIGHT_OPTION,
            'realistic': GLOBE_REALISTIC_OPTION,
            'terrain': GLOBE_TERRAIN_OPTION
        }
        
        # 获取对应配置，如果类型不存在则使用basic
        # 深拷贝配置以避免修改原始配置
        self.globe_config = copy.deepcopy(globe_configs.get(self.globe_type, GLOBE_BASIC_OPTION))
    
    def scatter(self, dimension: int | list = 2, visual_type: str | list = "color", config: dict | None = {}):
        """
        创建Globe 3D散点图
        
        参数：
            dimension: int | list - 要映射的列索引，默认为第2列（索引从0开始）
            visual_type: str | list - 映射类型，可选值为 "color", "opacity", "symbolSize" 等
            config: dict - 额外的配置项
        
        返回：
            Pancharts - 图表实例
        """
        if config is None:
            config = {}
        
        # 先合并基础globe配置和图表特有配置
        globe_data_option = deep_merge(self.globe_config, GLOBE_SCATTER_OPTION)
        
        # 添加数据
        globe_data_option["series"][0]["data"] = self.geo_data
        
        # 添加visualMap配置
        globe_data_option.update(create_visual_map(self.data, visual_type, dimension))
        
        return Pancharts(graph_config={}, data_config=globe_data_option, user_option=config)
    
    def bar3d(self, dimension: int | list = 2, visual_type: str | list = "color", config: dict | None = {}):
        """
        创建Globe 3D柱状图
        
        参数：
            dimension: int | list - 要映射的列索引，默认为第2列（索引从0开始）
            visual_type: str | list - 映射类型，可选值为 "color", "opacity", "symbolSize" 等
            config: dict - 额外的配置项
        
        返回：
            Pancharts - 图表实例
        """
        if config is None:
            config = {}
        
        # 先合并基础globe配置和图表特有配置
        globe_data_option = deep_merge(self.globe_config, GLOBE_BAR3D_OPTION)
        
        # 添加数据
        globe_data_option["series"][0]["data"] = self.geo_data
        
        # 添加visualMap配置
        globe_data_option.update(create_visual_map(self.data, visual_type, dimension))
        
        return Pancharts(graph_config={}, data_config=globe_data_option, user_option=config)
    
    def lines3d(self, coords: list, config: dict | None = None):
        """
        创建Globe 3D飞线图/迁徙图
        
        参数：
            coords: list - 飞线路径列表，每个元素为(start, end)元组，表示从start到end的飞线
            config: dict - 额外的配置项
        
        返回：
            Pancharts - 图表实例
        """
        if config is None:
            config = {}
        
        coords_data = []
        for i in coords:
            coords_data.append({
                'coords': [self.data.loc[i[0]].tolist()[0:2], self.data.loc[i[1]].tolist()[0:2]]
            })
        
        # 先合并基础globe配置和图表特有配置
        globe_data_option = deep_merge(self.globe_config, GLOBE_LINES3D_OPTION)
        
        # 添加数据
        globe_data_option["series"][0]["data"] = coords_data
        
        return Pancharts(graph_config={}, data_config=globe_data_option, user_option=config)


class sk_vm:
    """
    股票K线图可视化类
    
    参数：
        data: pandas DataFrame - 股票数据，索引为日期字符串
            前四列依次为：开盘价、最高价、最低价、收盘价
    
    支持的图表类型：
        - kline: K线图，支持移动平均线
    """
    
    def __init__(self, data):
        """
        初始化sk_vm实例
        
        参数：
            data: pandas DataFrame - 股票数据，索引为日期字符串
                前四列依次为：开盘价、最高价、最低价、收盘价
        """
        self.data = data
    
    def kline(self, ma: int | list = None, config: dict | None = None):
        """
        绘制K线图
        
        参数：
            ma: int | list - 移动平均线窗口大小，如5表示5日均线，[5, 20]表示5日和20日均线
            config: dict - 自定义配置
        
        返回：
            Pancharts - 图表实例
        """
        if config is None:
            config = {}
        
        # 准备K线数据 [开盘, 收盘, 最低, 最高]
        kline_data = []
        dates = []
        for date, row in self.data.iterrows():
            dates.append(date)
            kline_data.append([row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3]])
        
        # 构建数据配置
        kline_option = deep_merge(KLINE_OPTION.copy(), {
            "xAxis": {"data": dates},
            "series": [{
                "data": kline_data
            }]
        })
        
        # 添加移动平均线
        if ma is not None:
            if isinstance(ma, int):
                ma = [ma]
            
            close_prices = self.data.iloc[:, 1]
            colors = ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de", "#3ba272"]
            
            for i, window in enumerate(ma):
                ma_data = close_prices.rolling(window=window).mean()
                # 将 NaN 值替换为 None，ECharts 会自动跳过这些点
                ma_data = [None if pd.isna(val) else val for val in ma_data]
                kline_option["series"].append({
                    "name": f"MA{window}",
                    "type": "line",
                    "data": ma_data,
                    "smooth": True,
                    "lineStyle": {
                        "color": colors[i % len(colors)],
                        "opacity": 0.8
                    }
                })
        
        return Pancharts(graph_config={}, data_config=kline_option, user_option=config)
    
