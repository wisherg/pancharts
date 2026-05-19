#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts工具模块
包含各种辅助函数
"""

import re
import random
import os
import sys
import sqlite3
import json as json_module
from datetime import datetime

import pandas as pd
import numpy as np


def custom_json_serializer(obj):
    """
    自定义JSON序列化函数，处理pandas、numpy等非JSON可序列化对象

    参数：
        obj: object - 要序列化的对象

    返回：
        JSON可序列化对象

    支持的类型：
        - bool: 布尔值
        - pd.Timestamp: pandas时间戳
        - pd.DatetimeIndex: pandas时间索引
        - pd.Series: pandas序列
        - np.number: numpy数值类型
        - np.ndarray: numpy数组
        - datetime.datetime: Python日期时间
        - datetime.date: Python日期
    """
    # 处理布尔值（必须在数值类型之前，因为bool是int的子类）
    if isinstance(obj, bool):
        return obj
    # 处理pandas Timestamp对象
    elif isinstance(obj, pd.Timestamp):
        if obj.hour == 0 and obj.minute == 0 and obj.second == 0 and obj.nanosecond == 0:
            return obj.strftime('%Y-%m-%d')
        else:
            return obj.strftime('%Y-%m-%d %H:%M:%S')
    # 处理pandas DatetimeIndex对象
    elif isinstance(obj, pd.DatetimeIndex):
        return [custom_json_serializer(x) for x in obj]
    # 处理pandas Series对象
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    # 处理数值类型（包括Python内置和numpy数值）
    elif isinstance(obj, (int, float, np.number)):
        if isinstance(obj, float) and np.isnan(obj):
            return 0
        return float(obj)
    # 处理numpy数组
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    # 处理datetime对象
    elif isinstance(obj, datetime):
        if obj.hour == 0 and obj.minute == 0 and obj.second == 0:
            return obj.strftime('%Y-%m-%d')
        else:
            return obj.strftime('%Y-%m-%d %H:%M:%S')
    # 处理date对象
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    # 处理其他类型
    else:
        try:
            json_module.dumps(obj)
            return obj
        except:
            try:
                return str(obj)
            except:
                return ""


# 向后兼容导入 - 从 chartsdb 模块导入
try:
    from .chartsdb.utils import init_pancharts_db, open_db_manager
except ImportError:
    def init_pancharts_db(directory: str = None) -> str:
        """初始化Pancharts数据库（兼容旧版本导入）"""
        raise ImportError("chartsdb模块未找到，请确保chartsdb目录存在")
    
    def open_db_manager(host: str = "0.0.0.0", port: int = 8000):
        """打开数据库管理页面（兼容旧版本导入）"""
        raise ImportError("chartsdb模块未找到，请确保chartsdb目录存在")


def add_quotes_to_keys(json_str):
    """
    将字典字符串中所有的键添加双引号，并将true/false转换为True/False
    
    参数:
        json_str: 类似字典结构的字符串
        
    返回:
        所有键都带有双引号且布尔值正确大写的字典字符串
    """
    # 第一步：为键添加双引号
    pattern = r'(?<=[{,])\s*(\w+)(?=\s*:)'  # noqa: W605
    quoted_str = re.sub(pattern, r' "\1"', json_str)
    
    # 第二步：将true和false转换为True和False
    quoted_str = re.sub(r'\btrue\b', 'True', quoted_str)
    quoted_str = re.sub(r'\bfalse\b', 'False', quoted_str)
    
    return quoted_str

def random_color():
    """
    生成一个随机的颜色代码
    
    返回:
        str - 随机颜色代码
    """
    return f'#{random.randint(0, 0xFFFFFF):06x}'

def random_color_list(n):
    """
    随机生成一个长度为n的颜色代码列表
    
    参数:
        n: int - 列表长度
        
    返回:
        List[str] - 随机颜色代码列表
    """
    return [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in range(n)]

def get_index_type(x):
    """
    判断DataFrame索引类型
    
    参数:
        x: pd.DataFrame - 输入的DataFrame
        
    返回:
        str - 索引类型，可选值为"category"、"time"或"value"
    """
    if pd.api.types.is_object_dtype(x.index.dtype):
        return 'category'
    if pd.api.types.is_string_dtype(x.index.dtype):
        return 'category'
    if pd.api.types.is_datetime64_any_dtype(x.index.dtype):
        return 'time'
    if isinstance(x.index.dtype, pd.CategoricalDtype):
        return 'category'
    return 'value'

def get_value_type(x):
    """
    判断Series值的类型
    
    参数:
        x: pd.Series - 输入的Series
        
    返回:
        str - 值类型，可选值为"category"、"time"或"value"
    """
    dtype = x.dtype
    if pd.api.types.is_object_dtype(dtype):
        return 'category'
    if pd.api.types.is_string_dtype(dtype):
        return 'category'
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return 'time'
    if isinstance(dtype, pd.CategoricalDtype):
        return 'category'
    return 'value'

def get_chart(record_id: int, db_path: str = None) -> dict:
    """
    根据图表记录ID获取图表的各项数据，其中Option配置项已转换为Python字典
    
    参数：
        record_id: int - 图表记录的ID
        db_path: str - 数据库文件路径，可选。如果不指定，将从配置文件读取或使用默认路径
        
    返回：
        dict - 包含图表各项数据的字典，结构如下：
            {
                'id': int - 记录ID,
                'insert_time': str - 插入时间,
                'option': dict - 图表配置（已转换为Python字典）,
                'data_option': dict - 数据配置项（已转换为Python字典）,
                'file_path': str - 创建记录时的文件路径,
                'tag0': str - 自定义标签0,
                'tag1': str - 自定义标签1,
                'data_desc': str - 数据描述,
                'data_insight': str - 数据洞察
            }
            如果查询失败或记录不存在，返回空字典{}
    """
    # 获取数据库路径
    if not db_path:
        try:
            from pancharts.chart_config import SQLITE_DB_PATH
            if SQLITE_DB_PATH and SQLITE_DB_PATH.strip():
                db_path = SQLITE_DB_PATH
            else:
                db_path = os.path.join(os.getcwd(), "pancharts_option.db")
        except ImportError:
            db_path = os.path.join(os.getcwd(), "pancharts_option.db")
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查询记录
        cursor.execute('''
            SELECT id, insert_time, option, data_option, file_path, 
                   tag0, tag1, data_desc, data_insight 
            FROM pancharts_options 
            WHERE id = ?
        ''', (record_id,))
        
        row = cursor.fetchone()
        
        if row:
            # 将JSON字符串转换为Python字典
            try:
                option_dict = json_module.loads(row[2]) if row[2] else {}
            except (json_module.JSONDecodeError, TypeError):
                option_dict = {}
            
            try:
                data_option_dict = json_module.loads(row[3]) if row[3] else {}
            except (json_module.JSONDecodeError, TypeError):
                data_option_dict = {}
            
            result = {
                'id': row[0],
                'insert_time': row[1],
                'option': option_dict,
                'data_option': data_option_dict,
                'file_path': row[4],
                'tag0': row[5],
                'tag1': row[6],
                'data_desc': row[7],
                'data_insight': row[8]
            }
        else:
            result = {}
        
        # 关闭连接
        conn.close()
        
        return result
        
    except Exception as e:
        print(f"查询图表数据失败: {str(e)}")
        return {}


def charts_md(id_list: list = None, tag0: str = None, tag1: str = None, path: str = None, db_path: str = None, output_file: str = "charts_report.md") -> str:
    """
    根据条件从数据库查询图表数据，生成Markdown报告文件
    
    参数：
        id_list: list - 图表ID列表，由整数构成
        tag0: str - 按tag0筛选
        tag1: str - 按tag1筛选
        path: str - 按文件路径筛选
        db_path: str - 数据库文件路径，可选
        output_file: str - 输出的Markdown文件名，默认"charts_report.md"
        
    返回：
        str - 输出文件的完整路径，如果失败返回空字符串
    """
    # 获取数据库路径
    if not db_path:
        try:
            from pancharts.chart_config import SQLITE_DB_PATH
            if SQLITE_DB_PATH and SQLITE_DB_PATH.strip():
                db_path = SQLITE_DB_PATH
            else:
                db_path = os.path.join(os.getcwd(), "pancharts_option.db")
        except ImportError:
            db_path = os.path.join(os.getcwd(), "pancharts_option.db")
    
    # 构建查询条件
    conditions = []
    params = []
    
    if id_list and isinstance(id_list, list) and len(id_list) > 0:
        placeholders = ','.join('?' * len(id_list))
        conditions.append(f'id IN ({placeholders})')
        params.extend(id_list)
    
    if tag0 and tag0.strip():
        conditions.append('tag0 = ?')
        params.append(tag0.strip())
    
    if tag1 and tag1.strip():
        conditions.append('tag1 = ?')
        params.append(tag1.strip())
    
    if path and path.strip():
        conditions.append('file_path = ?')
        params.append(path.strip())
    
    if not conditions:
        print("请至少提供一个筛选条件")
        return ""
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 构建查询语句
        where_clause = ' AND '.join(conditions)
        query = f'''
            SELECT id, insert_time, option, data_option, file_path, 
                   tag0, tag1, data_desc, data_insight 
            FROM pancharts_options 
            WHERE {where_clause}
            ORDER BY id
        '''
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            print("未找到符合条件的图表记录")
            return ""
        
        # 收集所有图表数据
        charts_data = []
        all_dependencies = set()
        
        from pancharts.core import Pancharts
        
        for row in rows:
            record_id = row[0]
            insert_time = row[1]
            option_json = row[2]
            data_option_json = row[3]
            file_path = row[4]
            tag0_val = row[5]
            tag1_val = row[6]
            data_desc = row[7]
            data_insight = row[8]
            
            # 解析JSON
            try:
                option_dict = json_module.loads(option_json) if option_json else {}
            except:
                option_dict = {}
            
            try:
                data_option_dict = json_module.loads(data_option_json) if data_option_json else {}
            except:
                data_option_dict = {}
            
            # 创建Pancharts实例并准备渲染数据
            chart = Pancharts(user_option=option_dict, data_config=data_option_dict)
            render_data = chart.prepare_render_data()
            
            rendered_option = render_data.get('rendered_option', '')
            
            # 如果rendered_option是空字符串或空对象，使用原始option
            if not rendered_option or rendered_option == '{}':
                rendered_option = json_module.dumps(option_dict, ensure_ascii=False, indent=2)
            
            # 收集依赖
            deps = []
            if render_data.get('use_echarts_gl'):
                deps.append(render_data.get('echarts_gl_js_path', ''))
            if render_data.get('use_echarts_wordcloud'):
                deps.append(render_data.get('echarts_wordcloud_js_path', ''))
            if render_data.get('map_url'):
                deps.append(render_data.get('map_url'))
            if render_data.get('is_amap_chart'):
                deps.append(render_data.get('amap_js_path', ''))
                deps.append(render_data.get('amap_map_js_path', ''))
            
            for dep in deps:
                if dep:
                    all_dependencies.add(dep)
            
            charts_data.append({
                'id': record_id,
                'insert_time': insert_time,
                'rendered_option': rendered_option,
                'data_desc': data_desc,
                'data_insight': data_insight,
                'tag0': tag0_val,
                'tag1': tag1_val,
                'file_path': file_path
            })
        
        # 生成Markdown内容
        md_content = []
        
        # 添加依赖部分
        md_content.append("# 图表报告")
        md_content.append("")
        md_content.append("## 引用依赖")
        md_content.append("")
        for dep in sorted(all_dependencies):
            md_content.append(f"- {dep}")
        md_content.append("")
        
        # 添加图表部分
        md_content.append("## 图表列表")
        md_content.append("")
        
        for idx, chart_data in enumerate(charts_data, 1):
            md_content.append(f"---")
            md_content.append(f"")
            md_content.append(f"### 图表 {idx} (ID: {chart_data['id']})")
            md_content.append(f"")
            
            # 基本信息
            if chart_data['tag0']:
                md_content.append(f"- **标签0**: {chart_data['tag0']}")
            if chart_data['tag1']:
                md_content.append(f"- **标签1**: {chart_data['tag1']}")
            if chart_data['file_path']:
                md_content.append(f"- **文件路径**: {chart_data['file_path']}")
            if chart_data['insert_time']:
                md_content.append(f"- **插入时间**: {chart_data['insert_time']}")
            md_content.append(f"")
            
            # 数据描述
            md_content.append(f"#### 数据描述")
            md_content.append(f"{chart_data['data_desc'] or '无'}")
            md_content.append(f"")
            
            # 数据洞察
            md_content.append(f"#### 数据洞察")
            md_content.append(f"{chart_data['data_insight'] or '无'}")
            md_content.append(f"")
            
            # Rendered Option
            md_content.append(f"#### 渲染配置 (rendered_option)")
            md_content.append(f"```json")
            md_content.append(chart_data['rendered_option'])
            md_content.append(f"```")
            md_content.append(f"")
        
        # 写入文件
        output_path = os.path.join(os.getcwd(), output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
        
        print(f"Markdown报告已生成: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"生成图表报告失败: {str(e)}")
        return ""


def get_data(identifier, db_path: str = None) -> dict:
    """
    根据ID或file_path从data_desc表读取数据记录，并加载对应的数据文件
    
    参数：
        identifier: int or str - 如果是整数，作为data_desc表的id查询；
                               如果是字符串，作为file_path查询
        db_path: str - 数据库文件路径，可选
    
    返回：
        dict - 包含以下键的字典：
            'data': DataFrame - 读取的数据框
            'desc': str - 数据描述
            'data_info': str - data.info()的输出内容
            'file_path': str - 文件路径
            'read_config': dict - 使用的读取配置
    """
    # 获取数据库路径
    if not db_path:
        try:
            from pancharts.chart_config import SQLITE_DB_PATH
            if SQLITE_DB_PATH and SQLITE_DB_PATH.strip():
                db_path = SQLITE_DB_PATH
            else:
                db_path = os.path.join(os.getcwd(), "pancharts_option.db")
        except ImportError:
            db_path = os.path.join(os.getcwd(), "pancharts_option.db")
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 根据参数类型构建查询
        if isinstance(identifier, int):
            query = 'SELECT file_path, file_suffix, read_config, desc FROM data_desc WHERE id = ?'
            params = (identifier,)
        elif isinstance(identifier, str):
            query = 'SELECT file_path, file_suffix, read_config, desc FROM data_desc WHERE file_path = ?'
            params = (identifier,)
        else:
            print("参数类型错误，必须是整数或字符串")
            return {}
        
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            print(f"未找到匹配的记录: {identifier}")
            return {}
        
        file_path, file_suffix, read_config_pickle, desc = row
        
        # 反序列化read_config
        import pickle
        try:
            read_config = pickle.loads(read_config_pickle)
        except Exception as e:
            read_config = {}
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return {}
        
        # 解析read_config，提取实际的读取参数
        # read_func是函数类型标识，不是读取参数，需要去掉
        read_func = read_config.get('read_func', 'csv')
        
        # 准备传递给读取函数的参数（参考app.py中的处理方式）
        read_params = {}
        
        # 处理 sep 参数
        if read_config.get('sep'):
            if read_config['sep'] == '\\t':
                read_params['sep'] = '\t'
            else:
                read_params['sep'] = read_config['sep']
        
        # 处理 encoding 参数
        if read_config.get('encoding'):
            read_params['encoding'] = read_config['encoding']
        
        # 处理 header 参数
        if read_config.get('header') is not None:
            header_val = read_config['header']
            if header_val == '-1':
                read_params['header'] = None
            else:
                read_params['header'] = int(header_val)
        
        # 处理 names 参数
        if read_config.get('names'):
            names_list = [n.strip() for n in read_config['names'].split('\n') if n.strip()]
            if names_list:
                read_params['names'] = names_list
        
        # 处理 nrows 参数
        if read_config.get('nrows'):
            read_params['nrows'] = int(read_config['nrows'])
        
        # 处理 skiprows 参数
        if read_config.get('skiprows'):
            read_params['skiprows'] = int(read_config['skiprows'])
        
        # 处理 skipfooter 参数
        if read_config.get('skipfooter'):
            read_params['skipfooter'] = int(read_config['skipfooter'])
        
        # 处理 usecols 参数
        if read_config.get('usecols'):
            read_params['usecols'] = read_config['usecols']
        
        # 处理 index_col 参数
        if read_config.get('index_col'):
            read_params['index_col'] = int(read_config['index_col'])
        
        # 处理 parse_dates 参数
        if read_config.get('parse_dates'):
            read_params['parse_dates'] = read_config['parse_dates']
        
        # 处理 na_values 参数
        if read_config.get('na_values'):
            read_params['na_values'] = read_config['na_values']
        
        # 处理 skip_blank_lines 参数
        if 'skip_blank_lines' in read_config:
            read_params['skip_blank_lines'] = read_config['skip_blank_lines']
        

        
        # 根据read_func或文件后缀选择读取函数
        import pandas as pd
        
        try:
            if read_func == 'csv' or file_suffix.lower() == 'csv':
                df = pd.read_csv(file_path, **read_params)
            elif read_func == 'excel' or file_suffix.lower() in ('xlsx', 'xls'):
                df = pd.read_excel(file_path, **read_params)
            else:
                print(f"不支持的文件格式: {file_suffix} (read_func: {read_func})")
                return {}
        except Exception as e:
            print(f"读取文件失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return {}
        
        # 获取data.info()的输出
        import io
        buffer = io.StringIO()
        df.info(buf=buffer)
        data_info = buffer.getvalue()
        
        # 输出信息
        print("=" * 60)
        print(f"数据描述 (desc):")
        print(desc or "无描述")
        print("\n" + "=" * 60)
        print(f"数据信息 (data.info()):")
        print(data_info)
        print("=" * 60)
        
        return {
            'data': df,
            'desc': desc,
            'data_info': data_info,
            'file_path': file_path,
            'read_config': read_config
        }
        
    except Exception as e:
        print(f"获取数据失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return {}


def deep_merge(dict1, dict2):
    """
    递归地合并两个字典，dict2 中的值将覆盖 dict1 中的值。
    如果遇到列表且列表元素为字典，则按顺序合并对应位置的字典。
    列表长度不同时，仅合并前面能匹配的部分，剩余元素保持原样。
    
    :param dict1: 第一个字典
    :param dict2: 第二个字典，它的值将会覆盖第一个字典的值
    :return: 合并后的字典
    """
    result = dict1.copy()  # 复制第一个字典作为基础
    
    for key, value in dict2.items():
        # 检查键是否在结果中且两个值都是字典
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # 递归合并字典
            result[key] = deep_merge(result[key], value)
        
        # 检查键是否在结果中且两个值都是列表
        elif key in result and isinstance(result[key], list) and isinstance(value, list):
            merged_list = []
            # 遍历两个列表中较短的长度
            min_length = min(len(result[key]), len(value))
            
            # 合并对应位置的元素
            for i in range(min_length):
                item1 = result[key][i]
                item2 = value[i]
                
                # 如果两个元素都是字典，则递归合并
                if isinstance(item1, dict) and isinstance(item2, dict):
                    merged_list.append(deep_merge(item1, item2))
                # 如果其中一个是字典而另一个不是，直接使用dict2的值
                elif isinstance(item2, dict):
                    merged_list.append(item2)
                # 否则直接使用dict2的值（非字典元素）
                else:
                    merged_list.append(item2)
            
            # 如果dict1的列表更长，添加剩余元素
            if len(result[key]) > min_length:
                merged_list.extend(result[key][min_length:])
            # 如果dict2的列表更长，添加剩余元素
            elif len(value) > min_length:
                merged_list.extend(value[min_length:])
            
            result[key] = merged_list
        
        # 其他情况直接覆盖
        else:
            result[key] = value
    
    return result

def get_config_file_path():
    """
    获取chart_config.py文件的绝对路径，方便用户手动修改配置
    
    返回:
        str - chart_config.py文件的绝对路径
    """
    import os
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'chart_config.py'))





def create_visual_map(dataframe, map_types, columns):
    """
    生成ECharts的visualMap映射配置
    
    参数:
        dataframe: pd.DataFrame - 输入的数据框
        map_types: str | List[str] - 映射类型，可选值为 "color", "opacity", "symbolSize", "symbol", "lightness", "saturation"
        columns: int | List[int] - 映射的数据框列索引（基于顺序索引），可以是一列或多列
        
    返回:
        List[dict] - visualMap配置列表，每个元素对应一个visualMap配置
        
    说明:
        - map_types与columns一一对应，第i个列使用第i个映射类型
        - 使用get_value_type判断对应列的类型
        - 如果映射列为value类型，进行连续映射
        - 如果为category类型，使用枚举型映射
        - inRange中的范围会自动设定
        - 如果是枚举型，通过random_color_list生成随机颜色列表
    """
    if isinstance(map_types, str):
        map_types = [map_types]
    if isinstance(columns, int):
        columns = [columns]
    
    if len(map_types) != len(columns):
        raise ValueError("map_types和columns的长度必须相等")
    
    visual_maps = []
    
    for i, col_idx in enumerate(columns):
        if col_idx < 0 or col_idx >= len(dataframe.columns):
            raise ValueError(f"列索引 {col_idx} 超出数据框范围")
        
        map_type = map_types[i]
        col_name = dataframe.columns[col_idx]
        col_data = dataframe[col_name]
        value_type = get_value_type(col_data)
        
        visual_map = {
            "type": "continuous" if value_type == "value" else "piecewise",
            "dimension": col_idx
        }
        
        if value_type == "value":
            visual_map["min"] = float(col_data.min())
            visual_map["max"] = float(col_data.max())
        
        in_range = {}
        if map_type == "color":
            if value_type == "value":
                in_range["color"] = ["#50a3ba", "#eac736", "#d94e5d"]
            else:
                unique_vals = col_data.unique().tolist()
                in_range["color"] = random_color_list(len(unique_vals))
        
        elif map_type == "opacity":
            if value_type == "value":
                in_range["opacity"] = [0.1, 1.0]
            else:
                unique_vals = col_data.unique().tolist()
                in_range["opacity"] = [0.3 + j * 0.7 / len(unique_vals) for j in range(len(unique_vals))]
        
        elif map_type == "symbolSize":
            if value_type == "value":
                in_range["symbolSize"] = [10, 30]
            else:
                unique_vals = col_data.unique().tolist()
                in_range["symbolSize"] = [10 + j * 5 for j in range(len(unique_vals))]
        
        elif map_type == "symbol":
            symbols = ["circle", "rect", "roundRect", "triangle", "diamond", "pin", "arrow", "none"]
            if value_type == "value":
                in_range["symbol"] = [symbols[0], symbols[-2]]
            else:
                unique_vals = col_data.unique().tolist()
                in_range["symbol"] = [symbols[j % len(symbols)] for j in range(len(unique_vals))]
        
        elif map_type == "lightness":
            if value_type == "value":
                in_range["lightness"] = [0.2, 0.8]
            else:
                unique_vals = col_data.unique().tolist()
                in_range["lightness"] = [0.3 + j * 0.5 / len(unique_vals) for j in range(len(unique_vals))]
        
        elif map_type == "saturation":
            if value_type == "value":
                in_range["saturation"] = [0.2, 0.8]
            else:
                unique_vals = col_data.unique().tolist()
                in_range["saturation"] = [0.3 + j * 0.5 / len(unique_vals) for j in range(len(unique_vals))]
        
        else:
            raise ValueError(f"不支持的映射类型: {map_type}")
        
        visual_map["inRange"] = in_range
        
        if value_type == "category":
            unique_vals = col_data.unique().tolist()
            visual_map["pieces"] = [{"value": val} for val in unique_vals]
        
        if i > 0:
            visual_map["show"] = False
        
        visual_maps.append(visual_map)
    
    return {"visualMap": visual_maps}


def geocode_amap(address: str | list, api_key: str = None, retries: int = 3, interval: float = 0.3) -> tuple | list:
    """
    使用高德地图API进行地理编码，将地址转换为经纬度
    
    参数:
        address: str | list - 要编码的地址，或地址列表
        api_key: str, optional - 高德地图API key，默认为None时使用配置文件中的key
        retries: int - 失败重试次数，默认3次
        interval: float - 请求间隔时间（秒），默认0.3秒
        
    返回:
        tuple - 单个地址时返回 (经度, 纬度)
        list - 地址列表时返回 ([经度列表], [纬度列表])
        如果失败返回(None, None)或([None...], [None...])并输出错误信息
        
    示例:
        >>> geocode_amap("北京市朝阳区望京SOHO")
        (116.47366, 39.99924)
        >>> geocode_amap(["北京市", "上海市"])
        ([116.4074, 121.4737], [39.9042, 31.2304])
    """
    import requests
    import time
    
    from .chart_config import AMAP_API_KEY
    
    key = api_key if api_key else AMAP_API_KEY
    
    if not key:
        raise ValueError("请在chart_config.py中配置AMAP_API_KEY，或在调用时传入api_key参数")
    
    is_batch = isinstance(address, list)
    addresses = address if is_batch else [address]
    
    def _single_request(addr: str) -> tuple:
        url = "https://restapi.amap.com/v3/geocode/geo"
        params = {
            "address": addr,
            "key": key,
            "output": "json"
        }
        
        for retry in range(retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                result = response.json()
                
                if result.get("status") == "1" and result.get("geocodes"):
                    location = result["geocodes"][0]["location"]
                    lng, lat = map(float, location.split(","))
                    return (lng, lat)
                else:
                    error_msg = f"高德地图API返回失败: status={result.get('status')}, info={result.get('info', '未知错误')}"
                    print(f"[geocode_amap错误] {error_msg}")
                    if retry < retries - 1:
                        time.sleep(0.5)
                        continue
                    return (None, None)
            except requests.exceptions.RequestException as e:
                print(f"[geocode_amap错误] 网络请求失败: {str(e)}")
                if retry < retries - 1:
                    time.sleep(0.5)
                    continue
                return (None, None)
            except Exception as e:
                print(f"[geocode_amap错误] 解析结果失败: {str(e)}")
                if retry < retries - 1:
                    time.sleep(0.5)
                    continue
                return (None, None)
        return (None, None)
    
    results = []
    for addr in addresses:
        result = _single_request(addr)
        results.append(result)
        if addr != addresses[-1]:
            time.sleep(interval)
    
    if is_batch:
        lngs = [r[0] for r in results]
        lats = [r[1] for r in results]
        return (lngs, lats)
    else:
        return results[0]


def merge_charts(options: list, grid_layout: list) -> dict:
    """
    使用ECharts的grid组件合并多个图表，注意仅仅支持直角坐标系图表
    
    参数:
        options: list - 多个ECharts option配置构成的列表
        grid_layout: list - 每行图表数量的列表，如[2,1]表示第一行2张图，第二行1张图
        
    返回:
        dict - 合并后的ECharts option配置
        
    示例:
        >>> option1 = {...}
        >>> option2 = {...}
        >>> option3 = {...}
        >>> merged_option = merge_charts([option1, option2, option3], [2, 1])
    """
    if not isinstance(options, list) or len(options) == 0:
        raise ValueError("options必须是非空列表")
    if not isinstance(grid_layout, list) or len(grid_layout) == 0:
        raise ValueError("grid_layout必须是非空列表")
    
    total_charts = sum(grid_layout)
    if total_charts != len(options):
        raise ValueError(f"grid_layout元素之和({total_charts})必须等于options长度({len(options)})")
    
    merged_option = {
        "title": [],
        "tooltip": {"trigger": "axis"},
        "legend": [],
        "grid": [],
        "xAxis": [],
        "yAxis": [],
        "series": []
    }
    
    chart_index = 0
    total_rows = len(grid_layout)
    
    top_margin = 3
    bottom_margin = 2
    row_gap = 6
    legend_height = 4
    total_content_height = 100 - top_margin - bottom_margin - (total_rows - 1) * row_gap - total_rows * legend_height
    row_height = total_content_height / total_rows
    
    for row_idx, cols in enumerate(grid_layout):
        col_width = 100 / cols
        col_gap = 1
        
        for col_idx in range(cols):
            if chart_index >= len(options):
                break
            
            option = options[chart_index].copy()
            
            x_start = col_idx * col_width
            y_start = top_margin + row_idx * (row_height + row_gap)
            
            grid_width = col_width - col_gap if col_idx < cols - 1 else col_width - 0.5
            grid_height = row_height - 1
            
            grid_item = {
                "left": f"{x_start + 0.5}%",
                "top": f"{y_start + 3}%",
                "width": f"{grid_width - 0.5}%",
                "height": f"{grid_height - 3}%",
                "containLabel": True
            }
            merged_option["grid"].append(grid_item)
            
            x_axis = option.get("xAxis", {})
            if isinstance(x_axis, dict):
                x_axis = x_axis.copy()
                x_axis["gridIndex"] = chart_index
                merged_option["xAxis"].append(x_axis)
            elif isinstance(x_axis, list):
                for i, ax in enumerate(x_axis):
                    ax_copy = ax.copy()
                    ax_copy["gridIndex"] = chart_index
                    merged_option["xAxis"].append(ax_copy)
            
            y_axis = option.get("yAxis", {})
            if isinstance(y_axis, dict):
                y_axis = y_axis.copy()
                y_axis["gridIndex"] = chart_index
                merged_option["yAxis"].append(y_axis)
            elif isinstance(y_axis, list):
                for i, ax in enumerate(y_axis):
                    ax_copy = ax.copy()
                    ax_copy["gridIndex"] = chart_index
                    merged_option["yAxis"].append(ax_copy)
            
            title = option.get("title")
            if title:
                if isinstance(title, dict):
                    title = title.copy()
                    title["left"] = f"{x_start + col_width/2}%"
                    title["top"] = f"{y_start - 2}%"
                    title["textAlign"] = "center"
                    title["textStyle"] = title.get("textStyle", {})
                    title["textStyle"]["fontSize"] = title["textStyle"].get("fontSize", 14)
                    merged_option["title"].append(title)
                elif isinstance(title, list):
                    for t in title:
                        t_copy = t.copy()
                        t_copy["left"] = f"{x_start + col_width/2}%"
                        t_copy["top"] = f"{y_start - 2}%"
                        t_copy["textAlign"] = "center"
                        t_copy["textStyle"] = t_copy.get("textStyle", {})
                        t_copy["textStyle"]["fontSize"] = t_copy["textStyle"].get("fontSize", 14)
                        merged_option["title"].append(t_copy)
            
            legend = option.get("legend")
            series_names = []
            series_data = option.get("series", [])
            if not isinstance(series_data, list):
                series_data = [series_data]
            for s in series_data:
                if isinstance(s, dict) and "name" in s and s["name"]:
                    series_names.append(s["name"])
            
            if legend or series_names:
                legend_item = {
                    "data": series_names,
                    "left": f"{x_start + 2}%",
                    "top": f"{y_start + row_height + 0.5}%",
                    "textStyle": {"fontSize": 12}
                }
                
                if isinstance(legend, dict):
                    legend_item.update(legend.copy())
                
                merged_option["legend"].append(legend_item)
            
            series = option.get("series", [])
            if not isinstance(series, list):
                series = [series]
            
            for i, s in enumerate(series):
                s_copy = s.copy()
                s_copy["xAxisIndex"] = len(merged_option["xAxis"]) - 1
                s_copy["yAxisIndex"] = len(merged_option["yAxis"]) - 1
                merged_option["series"].append(s_copy)
            
            chart_index += 1
    
    if not merged_option["title"]:
        del merged_option["title"]
    if not merged_option["legend"]:
        del merged_option["legend"]
    
    return merged_option


def geocode_opencage(address: str | list, api_key: str = None, retries: int = 3, interval: float = 0.3) -> tuple | list:
    """
    使用OpenCage API进行地理编码，将地址转换为经纬度
    
    参数:
        address: str | list - 要编码的地址，或地址列表
        api_key: str, optional - OpenCage API key，默认为None时使用配置文件中的key
        retries: int - 失败重试次数，默认3次
        interval: float - 请求间隔时间（秒），默认0.3秒
        
    返回:
        tuple - 单个地址时返回 (经度, 纬度)
        list - 地址列表时返回 ([经度列表], [纬度列表])
        如果失败返回(None, None)或([None...], [None...])并输出错误信息
        
    示例:
        >>> geocode_opencage("Beijing, China")
        (116.397229, 39.9075)
        >>> geocode_opencage(["Beijing, China", "Shanghai, China"])
        ([116.397229, 121.4737], [39.9075, 31.2304])
    """
    import requests
    import time
    
    from .chart_config import OPENCAGE_API_KEY
    
    key = api_key if api_key else OPENCAGE_API_KEY
    
    if not key:
        raise ValueError("请在chart_config.py中配置OPENCAGE_API_KEY，或在调用时传入api_key参数")
    
    is_batch = isinstance(address, list)
    addresses = address if is_batch else [address]
    
    def _single_request(addr: str) -> tuple:
        url = "https://api.opencagedata.com/geocode/v1/json"
        params = {
            "q": addr,
            "key": key
        }
        
        for retry in range(retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                result = response.json()
                
                if result.get("results"):
                    geometry = result["results"][0]["geometry"]
                    return (geometry["lng"], geometry["lat"])
                else:
                    error_msg = f"OpenCage API返回失败: status={result.get('status', {}).get('code', '未知')}, message={result.get('status', {}).get('message', '未知错误')}"
                    print(f"[geocode_opencage错误] {error_msg}")
                    if retry < retries - 1:
                        time.sleep(0.5)
                        continue
                    return (None, None)
            except requests.exceptions.RequestException as e:
                print(f"[geocode_opencage错误] 网络请求失败: {str(e)}")
                if retry < retries - 1:
                    time.sleep(0.5)
                    continue
                return (None, None)
            except Exception as e:
                print(f"[geocode_opencage错误] 解析结果失败: {str(e)}")
                if retry < retries - 1:
                    time.sleep(0.5)
                    continue
                return (None, None)
        return (None, None)
    
    results = []
    for addr in addresses:
        result = _single_request(addr)
        results.append(result)
        if addr != addresses[-1]:
            time.sleep(interval)
    
    if is_batch:
        lngs = [r[0] for r in results]
        lats = [r[1] for r in results]
        return (lngs, lats)
    else:
        return results[0]
