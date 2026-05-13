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
    # 查找并提取第一个 { 和最后一个 } 之间的内容
    first_brace = response_content.find('{')
    last_brace = response_content.rfind('}')
    
    if first_brace != -1 and last_brace != -1 and first_brace < last_brace:
        response_content = response_content[first_brace:last_brace + 1]
    else:
        # 如果没有找到完整的 { } 结构，移除Markdown代码块标记并尝试解析
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
    4. 此配置的中布尔需要符合python规范，即需要写成True与False。
    5. 只返回option配置，option内部不要包含其他解释文字，外部可以有适当的解释
    6. 如果用户的问题需要完整的图表配置，生成完整的option；如果只是部分配置，生成部分配置
    """
    
    # 用户提示词
    user_prompt = f"""
    用户问题: {question}
    
    请根据问题生成对应的ECharts option配置
    """
    
    # 调用AI API
    response = call_openai_api(system_prompt, user_prompt, temperature=0.3, max_tokens=2000)
    
    # 打印结果
    print(response)


def desc_chat(user_requirement: str, data_config: str, max_words: int = 200) -> str:
    """
    基于数据配置项和用户要求进行专业数据分析，返回数据特征和统计意义
    
    参数：
        user_requirement: str - 用户的分析要求
        data_config: str - 数据配置项（JSON格式）
        max_words: int - 输出的最大字数，默认200字
        
    返回：
        str - 分析结果文本
    """
    # 系统提示词
    system_prompt = f"""你是一个专业的数据分析师。请根据提供的数据配置和用户要求，进行深入的数据分析。

分析内容应该包括：
1. 数据的整体特征和趋势
2. 关键统计指标（如最大值、最小值、平均值等，根据数据类型而定）
3. 数据所呈现的模式和规律
4. 数据的商业或业务意义
5. 可能的结论和建议

输出要求：
- 使用清晰的中文表达
- 结构合理，条理清晰
- 分析要有深度，不只是简单描述数据
- 保持专业、客观的语气
- 输出为纯文本，不包含JSON格式
- 控制在{max_words}字以内"""  
    
    # 用户提示词
    user_prompt = f"""用户分析要求: {user_requirement}

数据配置项:
{data_config}
"""
    
    # 计算max_tokens，大概1个汉字等于1.5个token，留一些余量
    max_tokens = int(max_words * 3)
    
    # 调用AI API
    response = call_openai_api(system_prompt, user_prompt, temperature=0.5, max_tokens=max_tokens)
    
    return response


def data_chat(data, user_requirement: str, data_desc: str = "") -> dict:
    """
    基于数据和用户需求生成并执行pandas统计代码
    
    参数：
        data: pd.DataFrame 或 pd.Series - 要进行统计的数据
        user_requirement: str - 用户的统计需求
        data_desc: str - 数据描述（可选）
        
    返回：
        dict - 包含统计结果(result)、执行的代码(code)和结果描述(result_desc)
    """
    import pandas as pd
    import io
    
    info_buffer = io.StringIO()
    data.info(buf=info_buffer)
    data_info = info_buffer.getvalue()
    
    system_prompt = """你是一个专业的Python数据分析师。请根据用户的统计需求和数据信息，生成正确的Python代码。

注意事项：
1. 代码必须基于变量 `data` 开始，data 是输入的DataFrame或Series
2. 可以使用 pandas、numpy、scipy、seaborn 等常用数据分析库，但请在代码开头添加 import 语句导入
4. 代码必须是可执行的Python代码
5. 只返回代码，不返回其他解释文字
6. 如果是DataFrame，使用 data 作为变量名；如果是Series，也使用 data 作为变量名
7. 支持单行或多行代码，多行代码时最后一行必须将结果赋值给变量 `result`
8. 返回结果应该是统计计算的结果（DataFrame、Series或标量值）

示例（单行）：
用户需求: 计算各列的均值
代码: data.mean()

示例（多行）：
用户需求: 分组统计后计算均值
代码: 
grouped = data.groupby('category')
result = grouped['value'].mean()

示例（需要导入其他库）：
用户需求: 计算数据的标准差
代码: 
import numpy as np
result = np.std(data['value'])
"""
    
    desc_text = f"\n数据描述: {data_desc}" if data_desc else ""
    
    user_prompt = f"""数据信息:
{data_info}
{desc_text}

用户统计需求: {user_requirement}

请生成对应的pandas统计代码:"""
    
    response = call_openai_api(system_prompt, user_prompt, temperature=0.3, max_tokens=10000)
    raw_response = response
    
    code = response.strip()
    if code.startswith('```python'):
        code = code[10:]
    if code.endswith('```'):
        code = code[:-3]
    code = code.strip()
    
    try:
        import pandas as pd
        
        exec_globals = globals().copy()
        exec_globals['pd'] = pd
        exec_globals['pandas'] = pd
        
        local_vars = {'data': data}
        
        if '\n' in code:
            exec(code, exec_globals, local_vars)
        else:
            exec(f"result = {code}", exec_globals, local_vars)
        
        result = local_vars.get('result')
        
        result_info_buffer = io.StringIO()
        if hasattr(result, 'info'):
            result.info(buf=result_info_buffer)
            result_info = result_info_buffer.getvalue()
        else:
            result_info = f"类型: {type(result).__name__}\n形状: {getattr(result, 'shape', '标量')}"
        
        result_desc_prompt = f"""请对以下统计结果进行简要描述（100字以内）：

原始数据信息:
{data_info}

{desc_text}

统计代码: {code}

统计结果信息:
{result_info}

描述要求：
1. 结果整体意义
2. 索引、值或各列的意义
3. 简洁明了，不超过100字"""
        
        result_desc = call_openai_api("你是一个数据分析师，请用简洁的语言描述统计结果。", result_desc_prompt, temperature=0.3, max_tokens=200)
        result_desc = result_desc.strip()
        
        return {
            'result': result,
            'code': code,
            'raw_response': raw_response,
            'result_desc': result_desc
        }
    except Exception as e:
        print(f"代码执行失败: {str(e)}")
        print(f"生成的代码: {code}")
        return {
            'result': None,
            'code': code,
            'error': str(e),
            'raw_response': raw_response,
            'result_desc': ""
        }
