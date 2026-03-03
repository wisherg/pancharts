#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts pandas可视化模块
包含基于pandas的数据可视化类
"""

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
    CALENDAR_OPTION,
    MAP_OPTION
)
from pancharts.utils import get_index_type, get_value_type, random_color,deep_merge
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
        for i in data.sort_values(ascending=False).items():
            self.base_data.append({"name": i[0], "value": i[1]})
        try:
            self.legend = data.index.name
        except:
            self.legend = ""

        self.rect_data_config = {
            'xAxis': {
                'type': self.xaxis_type
            },
            'yAxis': {
                'type': self.yaxis_type
            },
            'series': [
                {
                    'data': self.rect_data, "name": self.legend
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
        self.xtype = get_value_type(self.df_data.iloc[:, 0])
        self.ytype = get_value_type(self.df_data.iloc[:, 1])
        self.ztype = get_value_type(self.df_data.iloc[:, 2])

        self.bar3d_data_option = {
            'xAxis3D': {'type': self.xtype},
            'yAxis3D': {'type': self.ytype},
            'zAxis3D': {'type': self.ztype},
            'series': [{"data": self.bar3d_data}]
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
        schema = []
        n = 0
        for i in self.data:
            if self.data[i].dtype.str[0] == '|':
                schema.append({"dim": n, "name": i, "type": "category", "data": self.data[i].unique().tolist()})
            elif self.data[i].dtype.str[0] == '<':
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
