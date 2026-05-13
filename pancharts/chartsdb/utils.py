#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts数据库管理工具函数
"""

import os
import sqlite3
import subprocess
import sys


def init_pancharts_db(directory: str = None, db_path: str = None) -> str:
    """
    初始化Pancharts的SQLite数据库
    
    参数:
        directory: str - 数据库文件所在的目录路径，兼容Windows和Linux。默认为当前程序文件所在目录
        db_path: str - 直接指定数据库文件路径，如果指定则忽略directory参数和SQLITE_DB_PATH
        
    返回:
        str - 数据库文件的完整路径
        
    说明:
        优先级: db_path > directory > SQLITE_DB_PATH > 默认目录
        1. 如果指定了db_path参数，直接使用
        2. 如果指定了directory参数，在该目录下创建/查找数据库
        3. 如果都未指定，检查SQLITE_DB_PATH配置：
           - 如果不为空，使用SQLITE_DB_PATH作为数据库路径
           - 如果为空，在调用脚本所在目录创建/查找数据库
        如果数据库已存在但缺少某些表，会自动创建缺失的表
        
    数据表 pancharts_options 表结构:
        id: INTEGER PRIMARY KEY AUTOINCREMENT - 记录ID，自增主键
        insert_time: TEXT NOT NULL - 数据插入时间
        option: TEXT NOT NULL - 保存Pancharts对象的option配置
        data_option: TEXT NOT NULL - 保存数据配置项
        file_path: TEXT NOT NULL - 创建该记录时程序所在的文件路径
        tag0: TEXT - 自定义标签0
        tag1: TEXT - 自定义标签1
        data_desc: TEXT - 数据描述，可为空
        data_insight: TEXT - 数据洞察，可为空
        
    数据表 data_desc 表结构:
        id: INTEGER PRIMARY KEY AUTOINCREMENT - 记录ID，自增主键
        file_path: TEXT NOT NULL - 数据的完整路径
        file_suffix: TEXT NOT NULL - 文件后缀（csv, xlsx, txt等）
        read_config: BLOB NOT NULL - pandas读取配置，pickle打包的字典
        desc: TEXT - 数据描述，可为空
        insert_time: TEXT NOT NULL - 数据插入时间
    """
    # 1. 如果指定了db_path参数，直接使用
    if db_path:
        pass
    # 2. 如果指定了directory参数，在该目录下创建/查找数据库
    elif directory:
        db_path = os.path.join(directory, "pancharts_option.db")
    # 3. 如果都未指定，检查SQLITE_DB_PATH配置
    else:
        try:
            from pancharts.chart_config import SQLITE_DB_PATH
            if SQLITE_DB_PATH and SQLITE_DB_PATH.strip():
                db_path = SQLITE_DB_PATH
            else:
                # SQLITE_DB_PATH为空，使用默认逻辑
                if hasattr(sys.modules['__main__'], '__file__'):
                    directory = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
                else:
                    directory = os.getcwd()
                db_path = os.path.join(directory, "pancharts_option.db")
        except ImportError:
            # 无法导入chart_config，使用默认逻辑
            if hasattr(sys.modules['__main__'], '__file__'):
                directory = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
            else:
                directory = os.getcwd()
            db_path = os.path.join(directory, "pancharts_option.db")
    
    # 创建数据库和表
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建 pancharts_options 表（如果不存在）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pancharts_options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insert_time TEXT NOT NULL,
            option TEXT NOT NULL,
            data_option TEXT NOT NULL,
            file_path TEXT NOT NULL,
            tag0 TEXT,
            tag1 TEXT,
            data_desc TEXT,
            data_insight TEXT
        )
    ''')
    
    # 如果表已存在，尝试添加缺失的列
    try:
        cursor.execute('ALTER TABLE pancharts_options ADD COLUMN data_desc TEXT')
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute('ALTER TABLE pancharts_options ADD COLUMN data_insight TEXT')
    except sqlite3.OperationalError:
        pass
    
    # 创建 data_desc 表（如果不存在）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_desc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            file_suffix TEXT NOT NULL,
            read_config BLOB NOT NULL,
            desc TEXT,
            insert_time TEXT NOT NULL
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
