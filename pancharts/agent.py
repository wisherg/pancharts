#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts Agent模块
包含AI Agent相关的工具函数
"""

import json
from openai import OpenAI


def call_openai_api(system_prompt, user_prompt, temperature=0.7, max_tokens=2000):
    """
    调用OpenAI API，包含客户端创建和API调用逻辑
    配置信息只从chart_config获取，不接受参数输入
    
    参数：
        system_prompt: str - 系统提示词
        user_prompt: str - 用户提示词
        temperature: float - 温度参数，控制输出随机性，默认0.7
        max_tokens: int - 最大token数，默认2000
        
    返回：
        str - API返回的原始内容，如果调用失败返回空字符串
    """
    from .chart_config import DEFAULT_AI_API_KEY, DEFAULT_AI_BASE_URL, DEFAULT_AI_MODEL_NAME
    
    try:
        # 创建客户端（配置信息只从配置文件获取）
        client = OpenAI(
            api_key=DEFAULT_AI_API_KEY,
            base_url=DEFAULT_AI_BASE_URL,
        )
        
        # 调用AI API
        response = client.chat.completions.create(
            model=DEFAULT_AI_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        # 提取回复内容
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        # 如果API调用失败，打印错误信息并返回空字符串
        print(f"API调用失败: {str(e)}")
        return ""


def parse_json_response(response_content, verbose=False):
    """
    解析JSON响应，处理Markdown代码块标记
    
    参数：
        response_content: str - API返回的原始内容
        verbose: bool - 是否打印返回结果，默认False
        
    返回：
        dict - 解析后的字典，如果解析失败返回空字典
    """
    # 移除Markdown代码块标记
    if response_content.startswith('```json'):
        response_content = response_content[7:]
    if response_content.endswith('```'):
        response_content = response_content[:-3]
    response_content = response_content.strip()
    
    # 打印大模型返回结果（如果verbose为True）
    if verbose:
        print("AI Model Response:")
        print(response_content)
        print()
    
    try:
        # 解析JSON
        result = json.loads(response_content)
        
        # 确保返回的是字典
        return result if isinstance(result, dict) else {}
        
    except json.JSONDecodeError:
        # 如果JSON解析失败，返回空字典（始终打印错误信息）
        print("JSON解析失败")
        print(f"原始输出: {response_content}")
        return {}


def pchat(question: str) -> None:
    """
    基于pancharts项目文档回答用户问题
    
    参数：
        question: str - 用户的问题
        
    返回：
        None - 通过print输出结果，不返回任何内容
    """
    import os
    
    # 获取文档路径
    doc_path = os.path.join(os.path.dirname(__file__), 'datasets', 'document_cn.md')
    doc_path = os.path.abspath(doc_path)
    
    # 读取文档内容
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            document_content = f.read()
    except FileNotFoundError:
        print(f"文档文件未找到: {doc_path}")
        print("抱歉，无法找到文档文件。")
        return
    
    # 系统提示词
    system_prompt = """
    你是一个专业的Pancharts文档助手。
    请根据提供的文档内容，用中文回答用户的问题。
    如果文档中没有相关信息，请明确说明。
    回答要简洁明了，直接针对问题给出答案。
    """
    
    # 用户提示词
    user_prompt = f"""
    文档内容:
    {document_content}
    
    用户问题: {question}
    
    请根据文档内容回答上述问题，不需要输出JSON格式。
    """
    
    # 调用AI API并打印结果
    response = call_openai_api(system_prompt, user_prompt, temperature=0.3, max_tokens=2000)
    print(response)


def echat(question: str) -> None:
    """
    回答与ECharts图表配置相关的问题，返回可直接用于Pancharts的option
    
    参数：
        question: str - 用户关于ECharts配置的问题
        
    返回：
        None - 通过print输出结果，不返回任何内容
        
    示例：
        echat("如何设置柱状图的标题颜色为红色？")
        # 输出: {"title": {"text": "标题", "textStyle": {"color": "red"}}}
    """
    # 系统提示词
    system_prompt = """
    你是一个专业的ECharts配置助手。
    请根据用户的问题，生成可以直接用于Pancharts的ECharts option配置。
    
    注意事项：
    1. 所有字符串必须使用双引号
    2. 输出的配置部分必须是有效的JSON格式
    3. 当需要使用JavaScript函数时，必须将函数代码用"JsCode:"前缀包裹
       例如：{"formatter": "JsCode:function(params) { return params.name + ': ' + params.value; }"}
    4. 只返回option配置，option内部不要包含其他解释文字，外部可以有适当的解释
    5. 如果用户的问题需要完整的图表配置，生成完整的option；如果只是部分配置，生成部分配置
    """
    
    # 用户提示词
    user_prompt = f"""
    用户问题: {question}
    
    请根据问题生成对应的ECharts option配置，注意：
    - 使用双引号
    - JavaScript函数需要添加"JsCode:"前缀
    - 只返回JSON格式的option，不要包含其他内容
    """
    
    # 调用AI API
    response = call_openai_api(system_prompt, user_prompt, temperature=0.3, max_tokens=2000)
    
    # 打印结果
    print(response)
