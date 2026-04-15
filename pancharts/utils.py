#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts工具模块
包含各种辅助函数
"""

import re
import random

import pandas as pd


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


def load_city_cnname():
    """
    加载城市中文名称数据文件
    
    返回:
        pd.DataFrame - 包含城市中文名称的数据框
    """
    import os
    file_path = os.path.join(os.path.dirname(__file__), 'datasets', 'city_cnname.csv')
    return pd.read_csv(file_path)


def load_city_lnglat():
    """
    加载城市经纬度数据文件
    
    返回:
        pd.DataFrame - 包含城市经纬度的数据框
    """
    import os
    file_path = os.path.join(os.path.dirname(__file__), 'datasets', 'city_lnglat.csv')
    return pd.read_csv(file_path)


def load_countries_info():
    """
    加载国家信息数据文件
    
    返回:
        pd.DataFrame - 包含国家信息的数据框
    """
    import os
    file_path = os.path.join(os.path.dirname(__file__), 'datasets', 'countries_info.csv')
    return pd.read_csv(file_path)
