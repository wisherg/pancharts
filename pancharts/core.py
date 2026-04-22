#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts核心模块
包含核心Pancharts类和渲染逻辑
"""

import json
import os
import random
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from .chart_config import GLOBAL_DEFAULT_CONFIG


class JsCode:
    """
    用于标记JavaScript代码的特殊类
    当option中包含 "JsCode:function..." 格式的字符串时，会被转换为此类实例
    在渲染时会被正确处理为JavaScript代码
    """
    def __init__(self, code):
        self.code = code


class Pancharts:
    """
    ECharts可视化生成类
    
    用法示例：
        from pancharts import Pancharts
        
        # 创建实例时传入option
        chart = Pancharts(option={...})
        
        # 或通过属性赋值
        chart = Pancharts()
        chart.option = {...}
        
        # 渲染HTML到当前目录
        chart.render()
        
        # 渲染HTML到指定目录
        chart.render(output_dir='/path/to/output')
    """
    
    def __init__(self, user_option=None, data_config=None, graph_config=None):
        """
        初始化Pancharts实例

        参数：
            user_option: dict, optional - 用户配置选项，优先级最高
            data_config: dict, optional - 数据配置项
            graph_config: dict, optional - 图形配置项
        """
        self._user_option = user_option or {}
        self._data_config = data_config or {}
        self._graph_config = graph_config or {}
        self._template_dir = Path(__file__).parent / "templates"
        
        # 初始化默认属性，在_prepare_render_data中会重新设置
        self._init = {}
        # 从全局配置中获取默认值
        self.echarts_source = GLOBAL_DEFAULT_CONFIG.get("init", {}).get("echarts_source", "local")
        self._width = GLOBAL_DEFAULT_CONFIG.get("init", {}).get("width", "50%")
        self._height = GLOBAL_DEFAULT_CONFIG.get("init", {}).get("height", "600px")
        self._renderer = GLOBAL_DEFAULT_CONFIG.get("init", {}).get("renderer", "canvas")
        self._theme = GLOBAL_DEFAULT_CONFIG.get("init", {}).get("theme", "")
        
        # 初始化地图相关属性，在_prepare_render_data中会重新检测和设置
        self._map_filename_dict = {}
        self.is_map_chart = False
        self.map_name = "china"
        self.echarts_map_name = "china"
    
    @property
    def option(self):
        """获取ECharts配置"""
        # 合并所有配置项，优先级：user_option > data_config > graph_config > GLOBAL_DEFAULT_CONFIG
        from .utils import deep_merge
        merged = GLOBAL_DEFAULT_CONFIG.copy()
        merged = deep_merge(merged, self._graph_config)
        merged = deep_merge(merged, self._data_config)
        merged = deep_merge(merged, self._user_option)
        return merged
    
    @option.setter
    def option(self, value):
        """设置ECharts配置"""
        if not isinstance(value, dict):
            raise TypeError("option must be a dictionary")
        self._user_option = value
    
    def dmerge(self, dict2):
        """
        使用deep_merge将外部配置字典递归合并到user_option中
        
        参数：
            dict2: dict - 要合并的配置字典
            
        返回：
            self - 返回自身，支持链式调用
        """
        from .utils import deep_merge
        self._user_option = deep_merge(self._user_option, dict2)
        return self
    
    def modify_option(self, prompt: str, verbose: bool = False) -> "Pancharts":
        """
        使用AI大模型修改option样式
        支持DeepSeek、ChatGPT、千问等多种大模型
        
        参数：
            prompt: str - 修改要求
            verbose: bool - 是否打印大模型的返回结果，默认为False
            
        返回：
            self - 支持链式调用
            
        注意：API配置（api_key、base_url、model_name）现在只能通过chart_config.py配置文件设置
        """
        from .ai_option_modifier import AIOptionModifier
        
        # 获取当前option
        current_option = self.option
        
        # 创建修改器实例（配置从chart_config获取）
        modifier = AIOptionModifier()
        
        # 获取修改后的option
        new_option = modifier.modify_option(current_option, prompt, verbose=verbose)
        
        # 更新user_option，只保留样式修改
        self._user_option = new_option
        
        return self
    
    def patch_option(self, prompt: str, verbose: bool = False) -> "Pancharts":
        """
        使用AI大模型生成只包含修改处的补丁字典，然后通过deep_merge合并到原始option中
        支持DeepSeek、ChatGPT、千问等多种大模型
        
        参数：
            prompt: str - 修改要求
            verbose: bool - 是否打印大模型的返回结果，默认为False
            
        返回：
            self - 支持链式调用
            
        注意：API配置（api_key、base_url、model_name）现在只能通过chart_config.py配置文件设置
        """
        from .ai_option_modifier import AIOptionModifier
        from .utils import deep_merge
        
        # 获取当前option
        current_option = self.option
        
        # 创建修改器实例（配置从chart_config获取）
        modifier = AIOptionModifier()
        
        # 获取修改补丁
        patch = modifier.generate_patch(current_option, prompt, verbose=verbose)
        
        # 通过deep_merge将补丁合并到user_option中
        self._user_option = deep_merge(self._user_option, patch)
        
        return self
    
    def _process_jscode_in_json(self, json_str):
        """
        处理JSON字符串中的__jscode__标记，将其转换为实际的JavaScript代码
        
        参数：
            json_str: str - JSON字符串
            
        返回：
            str - 处理后的字符串，__jscode__标记已被转换为JavaScript代码
        """
        import re
        
        # 匹配 {"__jscode__": "..."} 模式并替换为实际的JavaScript代码
        # 注意：这里需要处理转义的引号
        pattern = r'\{"__jscode__":\s*"([^"]*)"\}'
        
        def replace_jscode(match):
            # 获取JavaScript代码（需要处理转义字符）
            js_code = match.group(1)
            # 还原转义的引号
            js_code = js_code.replace('\\"', '"')
            js_code = js_code.replace("\\'", "'")
            return js_code
        
        result = re.sub(pattern, replace_jscode, json_str)
        return result
    
    def _custom_json_serializer(self, obj):
        """
        自定义JSON序列化函数，处理非JSON可序列化对象
        
        参数：
            obj: object - 要序列化的对象
            
        返回：
            JSON可序列化对象
        """
        import pandas as pd
        import numpy as np
        import datetime
        
        # 处理布尔值（必须在数值类型之前，因为bool是int的子类）
        if isinstance(obj, bool):
            return obj
        # 处理pandas Timestamp对象
        elif isinstance(obj, pd.Timestamp):
            # 如果只有日期部分（时间为00:00:00），只输出日期
            if obj.hour == 0 and obj.minute == 0 and obj.second == 0 and obj.nanosecond == 0:
                return obj.strftime('%Y-%m-%d')
            else:
                return obj.strftime('%Y-%m-%d %H:%M:%S')
        # 处理pandas DatetimeIndex对象
        elif isinstance(obj, pd.DatetimeIndex):
            return [self._custom_json_serializer(x) for x in obj]
        # 处理pandas Series对象
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        # 处理数值类型（包括Python内置和numpy数值）
        elif isinstance(obj, (int, float, np.number)):
            # 处理numpy nan
            if isinstance(obj, float) and np.isnan(obj):
                return 0
            return float(obj)
        # 处理numpy数组
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        # 处理datetime对象
        elif isinstance(obj, datetime.datetime):
            # 如果只有日期部分（时间为00:00:00），只输出日期
            if obj.hour == 0 and obj.minute == 0 and obj.second == 0:
                return obj.strftime('%Y-%m-%d')
            else:
                return obj.strftime('%Y-%m-%d %H:%M:%S')
        # 处理其他类型
        else:
            try:
                # 尝试JSON序列化
                import json
                json.dumps(obj)
                return obj
            except:
                try:
                    # 尝试使用str()转换
                    return str(obj)
                except:
                    # 无法转换，返回空字符串
                    return ""
    
    def _prepare_render_data(self):
        """
        准备渲染所需的共享数据

        返回：
            dict - 包含渲染所需的所有数据
        """
        # 获取合并后的配置
        merged_option = self.option
        
        # 处理init配置，只从merged_option的init键获取
        self._init = {}
        
        # 从merged_option中的init键获取初始化配置
        if isinstance(merged_option, dict) and "init" in merged_option:
            self._init.update(merged_option["init"])
        
        # 处理echarts_source，从init字典中获取，默认值为"local"
        self.echarts_source = self._init.get("echarts_source", "local")
        
        # 设置默认值
        self._width = self._init.get("width", "100%")
        self._height = self._init.get("height", "600px")
        self._renderer = self._init.get("renderer", "canvas")
        self._theme = self._init.get("theme", "")
        
        # 检查echarts_source是否有效
        if self.echarts_source not in ["local", "online"]:
            raise ValueError("echarts_source must be 'local' or 'online'")
        
        # 检查renderer是否有效
        if self._renderer not in ["canvas", "svg"]:
            raise ValueError("renderer must be 'canvas' or 'svg'")
        
        # 加载地图文件名映射
        if not self._map_filename_dict:
            map_filename_path = Path(__file__).parent / "datasets" / "map_filename.json"
            if map_filename_path.exists():
                with open(map_filename_path, "r", encoding="utf-8") as f:
                    self._map_filename_dict = json.load(f)
        
        # 检测是否包含地图系列或geo组件
        self.is_map_chart = False
        self.map_name = "china"  # 默认地图名称
        self.echarts_map_name = "china"  # ECharts使用的实际地图名称
        
        # 先检查是否有geo组件
        if merged_option.get("geo"):
            geo_option = merged_option.get("geo")
            if isinstance(geo_option, dict) and geo_option.get("map"):
                self.is_map_chart = True
                self.map_name = geo_option.get("map", "china")
        
        # 再检查是否有map系列，如果有，会覆盖geo组件的地图名称
        if merged_option.get("series") and not self.is_map_chart:
            for series in merged_option.get("series", []):
                if isinstance(series, dict) and series.get("type") == "map":
                    self.is_map_chart = True
                    self.map_name = series.get("map", "china")
                    break
        
        # 检查是否有反向映射（英文名称到中文名称）
        if self.is_map_chart:
            # 默认使用原始地图名称
            self.echarts_map_name = self.map_name
            
            # 检查是否有直接匹配（中文名称直接匹配）
            if self.map_name in self._map_filename_dict:
                self.echarts_map_name = self.map_name
            else:
                # 检查反向映射（英文名称到中文名称）
                for name, info in self._map_filename_dict.items():
                    if info[0] == f"maps/{self.map_name}":
                        self.echarts_map_name = name
                        break
                    # 也检查文件名部分是否匹配
                    if info[0].replace("maps/", "") == self.map_name:
                        self.echarts_map_name = name
                        break
        
        # 选择echarts引入路径
        from .chart_config import NODE_MODULES_PATH
        
        if self.echarts_source == "local":
            # 优先使用配置的node_modules绝对路径
            if NODE_MODULES_PATH:
                custom_echarts_path = Path(NODE_MODULES_PATH) / "echarts/dist/echarts.min.js"
                custom_echarts_gl_path = Path(NODE_MODULES_PATH) / "echarts-gl/dist/echarts-gl.min.js"
                custom_echarts_wordcloud_path = Path(NODE_MODULES_PATH) / "echarts-wordcloud/dist/echarts-wordcloud.min.js"
                
                if custom_echarts_path.exists():
                    echarts_js_path = str(custom_echarts_path)
                else:
                    # 配置的绝对路径文件不存在，直接使用在线资源
                    echarts_js_path = "https://assets.pyecharts.org/assets/v5/echarts.min.js"
                
                if custom_echarts_gl_path.exists():
                    echarts_gl_js_path = str(custom_echarts_gl_path)
                else:
                    echarts_gl_js_path = "https://assets.pyecharts.org/assets/v5/echarts-gl.min.js"
                
                if custom_echarts_wordcloud_path.exists():
                    echarts_wordcloud_js_path = str(custom_echarts_wordcloud_path)
                else:
                    echarts_wordcloud_js_path = "https://assets.pyecharts.org/assets/v5/echarts-wordcloud.min.js"
            else:
                # 没有配置绝对路径，直接使用在线资源
                echarts_js_path = "https://assets.pyecharts.org/assets/v5/echarts.min.js"
                echarts_gl_js_path = "https://assets.pyecharts.org/assets/v5/echarts-gl.min.js"
                echarts_wordcloud_js_path = "https://assets.pyecharts.org/assets/v5/echarts-wordcloud.min.js"
        else:
            # 在线版使用pyecharts的在线资源
            echarts_js_path = "https://assets.pyecharts.org/assets/v5/echarts.min.js"
            echarts_gl_js_path = "https://assets.pyecharts.org/assets/v5/echarts-gl.min.js"
            echarts_wordcloud_js_path = "https://assets.pyecharts.org/assets/v5/echarts-wordcloud.min.js"
        
        # 判断是否需要引入echarts-gl（用于3D图表）
        use_echarts_gl = False
        if merged_option.get("series"):
            for series in merged_option.get("series", []):
                if isinstance(series, dict):
                    series_type = series.get("type")
                    # 检查所有需要echarts-gl的3D图类型
                    if series_type in ["bar3D", "line3D", "scatter3D", "surface", "map3D", "grid3D", "graphGL", "lines3D"]:
                        use_echarts_gl = True
                        break
        
        # 判断是否需要引入echarts-wordcloud（用于词云图）
        use_echarts_wordcloud = False
        if merged_option.get("series"):
            for series in merged_option.get("series", []):
                if isinstance(series, dict) and series.get("type") == "wordCloud":
                    use_echarts_wordcloud = True
                    break
        
        # 处理地图数据路径
        map_url = None
        if self.is_map_chart:
            # 检查是否有本地地图数据文件
            map_filename = self.map_name
            if self.map_name in self._map_filename_dict:
                map_filename = self._map_filename_dict[self.map_name][0].replace("maps/", "")
            
            # 检查本地资源（仅当echarts_source为local时）
            if self.echarts_source == "local":
                # 优先使用配置的node_modules绝对路径
                if NODE_MODULES_PATH:
                    custom_map_path = Path(NODE_MODULES_PATH) / "echarts/map/js" / (map_filename + ".js")
                    if custom_map_path.exists():
                        map_url = str(custom_map_path)
            
            # 如果本地没有地图数据文件或使用在线资源，使用pyecharts在线地图数据源
            if not map_url:
                map_url = "https://assets.pyecharts.org/assets/v5/maps/" + map_filename + ".js"
        
        # 复制option并替换地图名称为正确的注册名称
        rendered_option = merged_option.copy()
        if self.is_map_chart:
            # 深拷贝option以避免修改原始数据
            import copy
            rendered_option = copy.deepcopy(merged_option)
            
            # 替换geo组件的map属性为正确的注册名称
            if rendered_option.get("geo") and isinstance(rendered_option["geo"], dict):
                rendered_option["geo"]["map"] = self.echarts_map_name
            
            # 替换所有地图系列的map属性为正确的注册名称
            for series in rendered_option.get("series", []):
                if isinstance(series, dict) and series.get("type") == "map":
                    series["map"] = self.echarts_map_name
        
        # 移除init键，因为它只是本包的设定，不应该出现在最终渲染的HTML中
        if isinstance(rendered_option, dict) and "init" in rendered_option:
            del rendered_option["init"]
        
        # 递归处理rendered_option中的非JSON可序列化对象
        def recursive_serialize(obj):
            """递归序列化对象"""
            if isinstance(obj, dict):
                return {k: recursive_serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [recursive_serialize(item) for item in obj]
            elif isinstance(obj, tuple):
                return [recursive_serialize(item) for item in obj]
            elif isinstance(obj, str) and obj.startswith("JsCode:"):
                # 识别并处理JavaScript代码
                return JsCode(obj[7:])  # 去掉"JsCode:"前缀
            else:
                return self._custom_json_serializer(obj)
        
        # 序列化option
        rendered_option = recursive_serialize(rendered_option)
        
        # 自定义JSON编码器，处理JsCode对象
        class JsCodeEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, JsCode):
                    return {'__jscode__': obj.code}
                return super().default(obj)
        
        # 使用自定义编码器序列化option
        rendered_option = json.dumps(rendered_option, cls=JsCodeEncoder, ensure_ascii=False)
        
        # 处理JSON字符串中的__jscode__标记，将其转换为实际的JavaScript代码
        rendered_option = self._process_jscode_in_json(rendered_option)
        
        return {
            "echarts_js_path": echarts_js_path,
            "echarts_gl_js_path": echarts_gl_js_path,
            "use_echarts_gl": use_echarts_gl,
            "echarts_wordcloud_js_path": echarts_wordcloud_js_path,
            "use_echarts_wordcloud": use_echarts_wordcloud,
            "map_url": map_url,
            "rendered_option": rendered_option
        }
    
    def render(self, filename="index.html", output_dir="."):
        """
        渲染HTML文件

        参数：
            filename: str - 输出文件名，默认index.html
            output_dir: str - 输出目录，默认当前目录

        返回：
            str - 生成的HTML文件路径
        """
        # 确保输出目录存在
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 设置模板环境
        env = Environment(loader=FileSystemLoader(str(self._template_dir)))
        template = env.get_template('template.html')
        
        # 生成随机ID
        random_id = random.randint(100, 999)
        
        # 准备渲染数据
        render_data = self._prepare_render_data()
        
        # 渲染模板
        html_content = template.render(
            echarts_js_path=render_data["echarts_js_path"],
            echarts_gl_js_path=render_data["echarts_gl_js_path"],
            use_echarts_gl=render_data["use_echarts_gl"],
            echarts_wordcloud_js_path=render_data["echarts_wordcloud_js_path"],
            use_echarts_wordcloud=render_data["use_echarts_wordcloud"],
            option=render_data["rendered_option"],
            random_id=random_id,
            width=self._width,
            height=self._height,
            renderer=self._renderer,
            theme=self._theme,
            is_map_chart=self.is_map_chart,
            map_name=self.map_name if self.is_map_chart else "",
            map_url=render_data["map_url"]
        )
        
        # 保存生成的HTML文件
        html_file_path = output_path / filename
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file_path)
    
    def render_notebook(self):
        """
        渲染为Jupyter Notebook可用的HTML内容

        返回：
            str - 生成的HTML字符串，可直接在Jupyter Notebook中显示
        """
        # 设置模板环境
        env = Environment(loader=FileSystemLoader(str(self._template_dir)))
        template = env.get_template('nb_jupyter_notebook.html')
        
        # 生成随机ID
        import uuid
        chart_id = uuid.uuid4().hex
        
        # 准备渲染数据（支持本地资源优先）
        render_data = self._prepare_render_data()
        
        # 渲染模板
        html_content = template.render(
            echarts_js_path=render_data["echarts_js_path"],
            echarts_gl_js_path=render_data["echarts_gl_js_path"],
            use_echarts_gl=render_data["use_echarts_gl"],
            echarts_wordcloud_js_path=render_data["echarts_wordcloud_js_path"],
            use_echarts_wordcloud=render_data["use_echarts_wordcloud"],
            option=render_data["rendered_option"],
            chart_id=chart_id,
            width=self._width,
            height=self._height,
            renderer=self._renderer,
            theme=self._theme,
            map_url=render_data["map_url"],
            map_name=self.map_name  # 添加map_name参数，用于模板中生成正确的地图引用
        )
        
        # 返回HTML内容，与pyecharts兼容，直接显示在Jupyter Notebook中
        from IPython.display import HTML
        return HTML(html_content)
        
    def to_pyecharts(self):
        """
        将Pancharts配置转换为pyecharts的Chart实例
        
        返回：
            pyecharts.charts.chart.Chart - pyecharts的Chart实例，已设置好option
            
        说明：
            1. 自动移除pancharts特有的init配置键
            2. 将pancharts的"JsCode:..."字符串格式转换为pyecharts的JsCode类
            3. 递归处理所有嵌套的JsCode标记
            
        示例：
            from pancharts import Pancharts
            chart = Pancharts(option={...})
            pe_chart = chart.to_pyecharts()
            pe_chart.render("output.html")
        """
        import copy
        
        # 获取合并后的option
        merged_option = self.option
        
        # 深拷贝以避免修改原始数据
        option_for_pyecharts = copy.deepcopy(merged_option)
        
        # 移除pancharts特有的init配置
        if "init" in option_for_pyecharts:
            del option_for_pyecharts["init"]
        
        # 递归处理JsCode标记，转换为pyecharts的JsCode类
        def convert_jscode(obj):
            if isinstance(obj, dict):
                return {k: convert_jscode(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_jscode(item) for item in obj]
            elif isinstance(obj, str) and obj.startswith("JsCode:"):
                # 转换为pyecharts的JsCode类
                from pyecharts.utils import JsCode
                return JsCode(obj[7:])  # 去掉"JsCode:"前缀
            else:
                return obj
        
        # 转换option中的JsCode标记
        option_for_pyecharts = convert_jscode(option_for_pyecharts)
        
        # 创建pyecharts的Chart实例
        from pyecharts.charts.chart import Chart
        pe_chart = Chart()
        pe_chart.set_global_opts()
        pe_chart.options = option_for_pyecharts
        
        return pe_chart
    
    def to_nicegui(self):
        """
        将Pancharts配置转换为nicegui兼容的ECharts配置字典
        
        返回：
            dict - 符合nicegui要求的ECharts配置字典
            
        说明：
            1. 自动移除pancharts特有的init配置键
            2. 将pancharts的"JsCode:..."字符串格式转换为nicegui的":property"格式
               nicegui中使用冒号前缀表示该属性值为JavaScript表达式
            3. 递归处理所有嵌套的JsCode标记
            
        nicegui的JsCode处理方式：
            使用冒号":"前缀属性名来表示值是JavaScript表达式
            例如: ':formatter': r'(val, idx) => `group ${val}`'
            
        示例：
            from pancharts import Pancharts
            from nicegui import ui
            
            chart = Pancharts(option={...})
            config = chart.to_nicegui()
            
            ui.echart(config).classes('w-full h-96')
            ui.run()
        """
        import copy
        
        # 获取合并后的option
        merged_option = self.option
        
        # 深拷贝以避免修改原始数据
        option_for_nicegui = copy.deepcopy(merged_option)
        
        # 移除pancharts特有的init配置
        if "init" in option_for_nicegui:
            del option_for_nicegui["init"]
        
        # 递归处理JsCode标记，转换为nicegui的":property"格式
        def convert_jscode(obj):
            if isinstance(obj, dict):
                result = {}
                for k, v in obj.items():
                    # 检查值是否为JsCode标记
                    if isinstance(v, str) and v.startswith("JsCode:"):
                        # 使用冒号前缀表示JavaScript表达式
                        result[f":{k}"] = v[7:]  # 去掉"JsCode:"前缀
                    else:
                        result[k] = convert_jscode(v)
                return result
            elif isinstance(obj, list):
                return [convert_jscode(item) for item in obj]
            else:
                return obj
        
        # 转换option中的JsCode标记
        option_for_nicegui = convert_jscode(option_for_nicegui)
        
        return option_for_nicegui

