#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Option 修改器模块
用于通过各种AI大模型修改Pancharts的option对象
"""

import json

from .agent import call_openai_api, parse_json_response


class AIOptionModifier:
    """
    使用AI大模型修改ECharts option的通用类
    支持DeepSeek、ChatGPT、千问等多种大模型
    """
    
    def __init__(self):
        """
        初始化AIOptionModifier
        
        注意：API配置（api_key、base_url、model_name）只能通过chart_config.py配置文件设置
        """
        pass
    
    def modify_option(self, current_option: dict, prompt: str, verbose: bool = False) -> dict:
        """
        通过AI大模型修改option
        
        参数：
            current_option: dict - 当前的ECharts option
            prompt: str - 修改要求
            verbose: bool - 是否打印大模型的返回结果，默认为False
            
        返回：
            dict - 修改后的ECharts option
        """
        system_prompt = """
        你是一个专业的ECharts配置修改助手。
        请根据用户的要求修改提供的option对象，但只能修改样式属性，不能修改数据部分。
        当修改的属性值是JavaScript代码时，需要将该属性值对应的JavaScript代码转换为前缀为"JsCode:"的字符串格式。
        例如："JsCode:function(params) { return params.name + ': ' + params.value; }"
        你的输出必须是纯JSON格式的option字典，不能包含任何其他解释或说明文字。
        确保JSON格式正确，可直接被json.loads()解析。
        """
        
        user_prompt = f"""
        原始option: {json.dumps(current_option, ensure_ascii=False)}
        
        修改要求: {prompt}
        
        请只返回修改后的option JSON，不要包含其他内容。
        """
        
        response_content = call_openai_api(system_prompt, user_prompt, temperature=0.7, max_tokens=2000)
        
        if not response_content:
            return current_option
        
        result = parse_json_response(response_content, verbose)
        
        return result if result else current_option
    
    def generate_patch(self, current_option: dict, prompt: str, verbose: bool = False) -> dict:
        """
        通过AI大模型生成只包含修改处的键值对的补丁字典
        
        参数：
            current_option: dict - 当前的ECharts option
            prompt: str - 修改要求
            verbose: bool - 是否打印大模型的返回结果，默认为False
            
        返回：
            dict - 只包含修改处的键值对的补丁字典
        """
        system_prompt = """
        你是一个专业的ECharts配置修改助手。
        请根据用户的要求修改提供的option对象，但只能修改样式属性，不能修改数据部分。
        你的输出必须是纯JSON格式，只包含需要修改的键值对，不能包含完整的option。
        例如，如果只需要修改title的textStyle，只返回{"title": {"textStyle": {"color": "red"}}}即可。
        当修改的属性值是JavaScript代码时，需要将该属性值对应的JavaScript代码转换为前缀为"JsCode:"的字符串格式。
        例如："JsCode:function(params) { return params.name + ': ' + params.value; }"
        确保JSON格式正确，可直接被json.loads()解析。
        """
        
        user_prompt = f"""
        原始option: {json.dumps(current_option, ensure_ascii=False)}
        
        修改要求: {prompt}
        
        请只返回需要修改的键值对的JSON，不要包含完整的option，也不要包含其他内容。
        """
        
        response_content = call_openai_api(system_prompt, user_prompt, temperature=0.7, max_tokens=1000)
        
        if not response_content:
            return {}
        
        result = parse_json_response(response_content, verbose)
        
        return result if isinstance(result, dict) else {}
