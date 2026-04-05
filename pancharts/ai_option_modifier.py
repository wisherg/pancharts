#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Option 修改器模块
用于通过各种AI大模型修改Pancharts的option对象
"""

import json
from openai import OpenAI

class AIOptionModifier:
    """
    使用AI大模型修改ECharts option的通用类
    支持DeepSeek、ChatGPT、千问等多种大模型
    """
    
    def __init__(self, api_key: str = None, base_url: str = None, model_name: str = None):
        """
        初始化AIOptionModifier
        
        参数：
            api_key: str - API密钥，默认为配置文件中的DEFAULT_AI_API_KEY
            base_url: str - API基础URL，默认为配置文件中的DEFAULT_AI_BASE_URL
            model_name: str - 模型名称，默认为配置文件中的DEFAULT_AI_MODEL_NAME
        """
        from .chart_config import DEFAULT_AI_API_KEY, DEFAULT_AI_BASE_URL, DEFAULT_AI_MODEL_NAME
        
        self.client = OpenAI(
            api_key=api_key or DEFAULT_AI_API_KEY,
            base_url=base_url or DEFAULT_AI_BASE_URL,
        )
        self.model_name = model_name or DEFAULT_AI_MODEL_NAME
    
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
        # 系统提示词，确保模型只返回JSON
        system_prompt = """
        你是一个专业的ECharts配置修改助手。
        请根据用户的要求修改提供的option对象，但只能修改样式属性，不能修改数据部分。
        你的输出必须是纯JSON格式的option字典，不能包含任何其他解释或说明文字。
        确保JSON格式正确，可直接被json.loads()解析。
        """
        
        # 用户提示词，包含当前option和修改要求
        user_prompt = f"""
        原始option: {json.dumps(current_option, ensure_ascii=False)}
        
        修改要求: {prompt}
        
        请只返回修改后的option JSON，不要包含其他内容。
        """
        
        try:
            # 调用AI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            
            # 提取回复内容
            response_content = response.choices[0].message.content.strip()
            
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
            
            # 解析JSON
            new_option = json.loads(response_content)
            
            # 确保数据部分未被修改
            return new_option
            
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回原始option
            return current_option
        except Exception:
            # 如果API调用失败，返回原始option
            return current_option
    
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
        # 系统提示词，确保模型只返回修改处的键值对
        system_prompt = """
        你是一个专业的ECharts配置修改助手。
        请根据用户的要求修改提供的option对象，但只能修改样式属性，不能修改数据部分。
        你的输出必须是纯JSON格式，只包含需要修改的键值对，不能包含完整的option。
        例如，如果只需要修改title的textStyle，只返回{"title": {"textStyle": {"color": "red"}}}即可。
        确保JSON格式正确，可直接被json.loads()解析。
        """
        
        # 用户提示词，包含当前option和修改要求
        user_prompt = f"""
        原始option: {json.dumps(current_option, ensure_ascii=False)}
        
        修改要求: {prompt}
        
        请只返回需要修改的键值对的JSON，不要包含完整的option，也不要包含其他内容。
        """
        
        try:
            # 调用AI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
            )
            
            # 提取回复内容
            response_content = response.choices[0].message.content.strip()
            
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
            
            # 解析JSON
            patch = json.loads(response_content)
            
            # 确保返回的是字典
            return patch if isinstance(patch, dict) else {}
            
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回空字典
            return {}
        except Exception:
            # 如果API调用失败，返回空字典
            return {}
