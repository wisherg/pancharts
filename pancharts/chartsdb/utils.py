#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts数据库管理工具函数
"""

import os
import sqlite3
import subprocess
import sys


def init_pancharts_db(directory: str = None) -> str:
    """
    初始化Pancharts的SQLite数据库
    
    参数:
        directory: str - 数据库文件所在的目录路径，兼容Windows和Linux。默认为当前程序文件所在目录
        
    返回:
        str - 数据库文件的完整路径
        
    说明:
        如果目录中已存在pancharts_option.db文件，则直接返回该文件路径
        如果不存在，则创建数据库文件并创建数据表
        
    数据表 pancharts_options 表结构:
        id: INTEGER PRIMARY KEY AUTOINCREMENT - 记录ID，自增主键
        insert_time: TEXT NOT NULL - 数据插入时间
        option: TEXT NOT NULL - 保存Pancharts对象的option配置
        data_option: TEXT NOT NULL - 保存数据配置项
        file_path: TEXT NOT NULL - 创建该记录时程序所在的文件路径
        tag0: TEXT - 自定义标签0
        tag1: TEXT - 自定义标签1
    """
    # 如果未指定目录，获取调用脚本所在目录
    if directory is None:
        if hasattr(sys.modules['__main__'], '__file__'):
            directory = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        else:
            directory = os.getcwd()
    
    db_path = os.path.join(directory, "pancharts_option.db")
    
    # 如果已存在，直接返回路径
    if os.path.exists(db_path):
        return db_path
    
    # 创建数据库和表
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建数据表
    cursor.execute('''
        CREATE TABLE pancharts_options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insert_time TEXT NOT NULL,
            option TEXT NOT NULL,
            data_option TEXT NOT NULL,
            file_path TEXT NOT NULL,
            tag0 TEXT,
            tag1 TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    
    return db_path


def open_db_manager(host: str = "0.0.0.0", port: int = 8000):
    """
    启动Pancharts数据管理服务，打开数据管理页面
    
    参数:
        host: str - 服务器绑定地址，默认为0.0.0.0（允许所有IP访问）
        port: int - 服务器端口，默认为8000
    
    说明:
        使用 chart_config.py 中的 SQLITE_DB_PATH 配置来定位数据库
    """
    # 检查 SQLITE_DB_PATH 是否配置
    try:
        from pancharts.chart_config import SQLITE_DB_PATH
        if not SQLITE_DB_PATH:
            print("错误：SQLITE_DB_PATH 未配置！")
            print("请先在 chart_config.py 中配置数据库路径：")
            print("1. 使用 init_pancharts_db(directory) 创建数据库")
            print("2. 在 chart_config.py 中设置 SQLITE_DB_PATH = '数据库文件路径'")
            return
    except ImportError:
        print("错误：无法导入 chart_config 模块")
        return
    
    import webbrowser
    
    print(f"正在启动 Pancharts 数据管理服务...")
    # 如果绑定地址是 0.0.0.0，提示用户使用 localhost 访问
    access_host = "localhost" if host == "0.0.0.0" else host
    print(f"请在浏览器中访问: http://{access_host}:{port}")
    print("按 Ctrl+C 停止服务器")
    
    env = os.environ.copy()
    
    # 使用 subprocess 启动 uvicorn 服务器
    cmd = [
        sys.executable, '-m', 'uvicorn', 
        'pancharts.chartsdb.app:app',
        '--host', host,
        '--port', str(port)
    ]
    
    try:
        subprocess.run(cmd, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"启动失败: {e}")
    except KeyboardInterrupt:
        print("\n服务已停止")
