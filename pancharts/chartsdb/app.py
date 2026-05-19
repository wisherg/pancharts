#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pancharts数据管理API服务
使用FastAPI构建的数据管理页面
"""

import os
import sys
import sqlite3
import json
from datetime import datetime

import pandas as pd
import numpy as np

# 优先从 site-packages 导入 fastapi，避免本地文件名冲突
import importlib.util
spec = importlib.util.find_spec('fastapi')
if spec and 'site-packages' in spec.origin:
    sys.path.insert(0, os.path.dirname(spec.origin))

from fastapi import FastAPI, Request, Form, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

try:
    from ..chart_config import SQLITE_DB_PATH
    from .utils import init_pancharts_db
    from ..core import Pancharts
    from ..agent import desc_chat, data_chat
except ImportError:
    from pancharts.chart_config import SQLITE_DB_PATH
    from pancharts.chartsdb.utils import init_pancharts_db
    from pancharts.core import Pancharts
    from pancharts.agent import desc_chat, data_chat

app = FastAPI(title="Pancharts数据管理", description="管理pancharts_option数据库")

# 设置模板目录
template_dir = os.path.join(os.path.dirname(__file__), "templates")
from jinja2 import Environment, FileSystemLoader
jinja_env = Environment(
    loader=FileSystemLoader(template_dir),
    cache_size=0  # 禁用缓存
)


def get_db_path():
    """获取数据库路径"""
    if not SQLITE_DB_PATH:
        raise FileNotFoundError(
            "SQLITE_DB_PATH 未配置，请先在 chart_config.py 中配置数据库路径。\n"
            "使用方法：\n"
            "1. 使用 init_pancharts_db(directory) 创建数据库\n"
            "2. 在 chart_config.py 中设置 SQLITE_DB_PATH = '数据库文件路径'"
        )
    
    return SQLITE_DB_PATH


def get_db_connection():
    """获取数据库连接"""
    db_path = get_db_path()
    
    # 检查数据库文件是否存在
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"数据库文件不存在: {db_path}\n请先使用 init_pancharts_db() 初始化数据库")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


class Record(BaseModel):
    """记录模型"""
    id: int
    insert_time: str
    option: str
    data_option: str
    file_path: str
    tag0: str
    tag1: str


@app.get("/batch-preview", response_class=HTMLResponse)
async def batch_preview(request: Request, ids: str = ""):
    """批量预览多个图表"""
    if not ids:
        return HTMLResponse(content="<h1>请选择要预览的图表</h1>", status_code=400)
    
    id_list = [int(x.strip()) for x in ids.split(',') if x.strip().isdigit()]
    
    if not id_list:
        return HTMLResponse(content="<h1>无效的图表ID</h1>", status_code=400)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    placeholders = ','.join('?' * len(id_list))
    query = f"SELECT * FROM pancharts_options WHERE id IN ({placeholders})"
    cursor.execute(query, id_list)
    records = cursor.fetchall()
    conn.close()
    
    charts = []
    js_dependencies = set()
    
    for record in records:
        try:
            option_data = json.loads(record["option"])
            
            # 从数据库记录中读取 data_desc 和 data_insight（而不是从 option 中）
            data_desc = record["data_desc"] if record["data_desc"] is not None else ""
            data_insight = record["data_insight"] if record["data_insight"] is not None else ""
            
            # 使用 render_emb 生成完整图表HTML（支持3D图表）
            chart = Pancharts()
            chart.option = option_data
            emb_result = chart.render_emb()
            chart_html = emb_result["html"]
            for js_url in emb_result.get("js_dependencies", []):
                js_dependencies.add(js_url)
            
            chart_info = {
                "id": record["id"],
                "tag0": record["tag0"],
                "tag1": record["tag1"],
                "insert_time": record["insert_time"],
                "random_id": f"batch_{record['id']}",
                "desc": data_desc,
                "insight": data_insight,
                "chart_html": chart_html
            }
            charts.append(chart_info)
                
        except Exception as e:
            print(f"Error processing chart {record['id']}: {e}")
    
    template = jinja_env.get_template("batch_preview.html")
    html_content = template.render({
        "request": request,
        "charts": charts,
        "js_dependencies": list(js_dependencies)
    })
    return HTMLResponse(content=html_content)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, tag0: str = "", tag1: str = "", start_time: str = "", end_time: str = "", file_path: str = ""):
    """首页 - 显示所有记录，支持筛选查询"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 构建查询条件
    where_clauses = []
    params = []
    
    if tag0:
        where_clauses.append("tag0 LIKE ?")
        params.append(f"%{tag0}%")
    
    if tag1:
        where_clauses.append("tag1 LIKE ?")
        params.append(f"%{tag1}%")
    
    if start_time:
        where_clauses.append("insert_time >= ?")
        params.append(start_time)
    
    if end_time:
        where_clauses.append("insert_time <= ?")
        params.append(end_time)
    
    if file_path:
        where_clauses.append("file_path LIKE ?")
        params.append(f"%{file_path}%")
    
    # 构建完整查询
    query = "SELECT * FROM pancharts_options"
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    records = cursor.fetchall()
    conn.close()
    
    db_path = get_db_path()
    
    # 直接使用 Jinja2 渲染模板
    template = jinja_env.get_template("db_manager.html")
    html_content = template.render({
        "request": request,
        "records": records,
        "db_path": db_path,
        "filter_tag0": tag0,
        "filter_tag1": tag1,
        "filter_start_time": start_time,
        "filter_end_time": end_time,
        "filter_file_path": file_path
    })
    return HTMLResponse(content=html_content)


@app.get("/record/{record_id}", response_class=HTMLResponse)
async def view_record(request: Request, record_id: int):
    """查看单条记录详情"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pancharts_options WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    conn.close()
    
    if not record:
        return HTMLResponse(content="<h1>记录不存在</h1>", status_code=404)
    
    # 格式化JSON数据
    try:
        option_formatted = json.dumps(json.loads(record["option"]), ensure_ascii=False, indent=2)
    except:
        option_formatted = record["option"]
    
    data_option_formatted = record["data_option"] or "{}"
    
    # 渲染图表（使用新的render_emb方法）
    chart_html = ""
    chart_js_dependencies = []
    try:
        option_data = json.loads(record["option"])
        chart = Pancharts()
        chart.option = option_data
        emb_result = chart.render_emb()
        chart_html = emb_result["html"]
        chart_js_dependencies = emb_result["js_dependencies"]
    except Exception as e:
        chart_html = f'<div style="color: red; padding: 20px;">渲染图表失败: {str(e)}</div>'
    
    # 直接使用 Jinja2 渲染模板
    template = jinja_env.get_template("record_detail.html")
    html_content = template.render({
        "request": request,
        "record": record,
        "option_formatted": option_formatted,
        "data_option_formatted": data_option_formatted,
        "chart_html": chart_html,
        "chart_js_dependencies": chart_js_dependencies
    })
    return HTMLResponse(content=html_content)


@app.get("/edit/{record_id}", response_class=HTMLResponse)
async def edit_record(request: Request, record_id: int):
    """编辑记录页面"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pancharts_options WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    conn.close()
    
    if not record:
        return HTMLResponse(content="<h1>记录不存在</h1>", status_code=404)
    
    # 格式化JSON数据
    try:
        option_formatted = json.dumps(json.loads(record["option"]), ensure_ascii=False, indent=2)
    except:
        option_formatted = record["option"]
    
    data_option_formatted = record["data_option"] or "{}"
    
    # 渲染图表（使用新的render_emb方法）
    chart_html = ""
    chart_js_dependencies = []
    try:
        option_data = json.loads(record["option"])
        chart = Pancharts()
        chart.option = option_data
        emb_result = chart.render_emb()
        chart_html = emb_result["html"]
        chart_js_dependencies = emb_result["js_dependencies"]
    except Exception as e:
        chart_html = f'<div style="color: red; padding: 20px;">渲染图表失败: {str(e)}</div>'
    
    # 直接使用 Jinja2 渲染模板
    template = jinja_env.get_template("record_edit.html")
    html_content = template.render({
        "request": request,
        "record": record,
        "option_formatted": option_formatted,
        "data_option_formatted": data_option_formatted,
        "chart_html": chart_html,
        "chart_js_dependencies": chart_js_dependencies
    })
    return HTMLResponse(content=html_content)


@app.post("/update/{record_id}")
async def update_record(record_id: int, tag0: str = Form(""), tag1: str = Form(""), 
                       option: str = Form(""), data_option: str = Form(""),
                       data_desc: str = Form(""), data_insight: str = Form("")):
    """更新记录"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 如果提供了 option，验证 JSON 格式
    if option:
        try:
            json.loads(option)
        except json.JSONDecodeError:
            return HTMLResponse(content="<h1>Option 格式错误，请输入有效的JSON</h1>", status_code=400)
    
    # 如果提供了 data_option，验证 JSON 格式
    if data_option:
        try:
            json.loads(data_option)
        except json.JSONDecodeError:
            return HTMLResponse(content="<h1>Data Option 格式错误，请输入有效的JSON</h1>", status_code=400)
    
    # 获取当前记录
    cursor.execute("SELECT * FROM pancharts_options WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    
    if not record:
        conn.close()
        return HTMLResponse(content="<h1>记录不存在</h1>", status_code=404)
    
    # 使用现有值或新值
    new_option = option if option else record["option"]
    new_data_option = data_option if data_option else record["data_option"]
    
    cursor.execute('''
        UPDATE pancharts_options SET tag0 = ?, tag1 = ?, option = ?, data_option = ?, data_desc = ?, data_insight = ? WHERE id = ?
    ''', (tag0, tag1, new_option, new_data_option, data_desc, data_insight, record_id))
    
    conn.commit()
    conn.close()
    
    return RedirectResponse(f"/edit/{record_id}", status_code=303)


@app.post("/delete/{record_id}")
async def delete_record(record_id: int):
    """删除记录"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM pancharts_options WHERE id = ?", (record_id,))
    
    conn.commit()
    conn.close()
    
    return RedirectResponse("/", status_code=303)


@app.get("/api/records")
async def get_records_api():
    """API接口 - 获取所有记录"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pancharts_options ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    
    result = []
    for record in records:
        result.append({
            "id": record["id"],
            "insert_time": record["insert_time"],
            "tag0": record["tag0"],
            "tag1": record["tag1"],
            "file_path": record["file_path"]
        })
    
    return {"records": result}


@app.delete("/api/records/{record_id}")
async def delete_record_api(record_id: int):
    """API接口 - 删除记录"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM pancharts_options WHERE id = ?", (record_id,))
    affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return {"success": affected > 0, "message": "删除成功" if affected > 0 else "记录不存在"}


@app.post("/api/preview")
async def preview_chart(option: str = Form("")):
    """API接口 - 预览图表，使用前端传来的option渲染"""
    if not option:
        return {"success": False, "error": "Option 不能为空"}
    
    try:
        option_data = json.loads(option)
    except json.JSONDecodeError:
        return {"success": False, "error": "Option 格式错误，请输入有效的JSON"}
    
    try:
        chart = Pancharts()
        chart.option = option_data
        emb_result = chart.render_emb()
        return {"success": True, "chart_html": emb_result["html"], "js_dependencies": emb_result["js_dependencies"]}
    except Exception as e:
        return {"success": False, "error": f"渲染图表失败: {str(e)}"}


@app.post("/api/patch_option")
async def patch_option_api(request: Request):
    """API接口 - 使用AI修改Option配置"""
    try:
        data = await request.json()
    except Exception as e:
        return {"success": False, "error": "请求格式错误，请使用JSON格式"}
    
    option = data.get("option", "")
    prompt = data.get("prompt", "")
    
    if not option:
        return {"success": False, "error": "Option 不能为空"}
    
    if not prompt:
        return {"success": False, "error": "修改指令不能为空"}
    
    try:
        option_data = json.loads(option)
    except json.JSONDecodeError:
        return {"success": False, "error": "Option 格式错误，请输入有效的JSON"}
    
    try:
        chart = Pancharts()
        chart.option = option_data
        chart.patch_option(prompt)
        patched_option = json.dumps(chart.option, ensure_ascii=False)
        return {"success": True, "patched_option": patched_option}
    except Exception as e:
        return {"success": False, "error": f"AI 修改失败: {str(e)}"}


@app.post("/api/desc_chat")
async def desc_chat_api(request: Request):
    """API接口 - 使用AI分析数据配置"""
    try:
        data = await request.json()
    except Exception as e:
        return {"success": False, "error": "请求格式错误，请使用JSON格式"}
    
    user_requirement = data.get("user_requirement", "")
    data_config = data.get("data_config", "")
    max_words = data.get("max_words", 200)
    
    if not user_requirement:
        return {"success": False, "error": "分析要求不能为空"}
    
    if not data_config:
        return {"success": False, "error": "数据配置不能为空"}
    
    try:
        result = desc_chat(user_requirement, data_config, max_words)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": f"数据分析失败: {str(e)}"}


@app.get("/data-reader", response_class=HTMLResponse)
async def data_reader(request: Request):
    """数据文件读取页面"""
    template = jinja_env.get_template("data_reader.html")
    html_content = template.render({"request": request})
    return HTMLResponse(content=html_content)


@app.post("/api/stats-data")
async def stats_data_api(request: Request):
    """API接口 - 使用data_chat函数进行数据统计分析"""
    from fastapi.responses import JSONResponse
    import json
    import numpy as np
    
    try:
        import pandas as pd
        from pancharts.agent import data_chat
        
        data = await request.json()
        raw_data = data.get("data", [])
        requirement = data.get("requirement", "")
        data_desc = data.get("data_desc", "")
        
        if not raw_data or not requirement:
            return JSONResponse(content={"success": False, "error": "数据或统计需求不能为空"})
        
        df = pd.DataFrame(raw_data)
        
        result = data_chat(df, requirement, data_desc)
        
        raw_response = str(result.get('raw_response', '')) if result.get('raw_response') else ''
        
        if result.get('error'):
            return JSONResponse(content={
                "success": False, 
                "error": str(result['error']), 
                "code": str(result.get('code', '')), 
                "raw_response": raw_response
            })
        
        stats_result = result.get('result')
        if stats_result is None:
            return JSONResponse(content={
                "success": False, 
                "error": "未生成统计结果", 
                "code": str(result.get('code', '')), 
                "raw_response": raw_response
            })
        
        data_type = 'dataframe'
        
        if isinstance(stats_result, pd.Series):
            df_result = stats_result.to_frame()
            data_type = 'series'
        elif isinstance(stats_result, pd.DataFrame):
            df_result = stats_result
        else:
            df_result = pd.DataFrame([{"result": str(stats_result)}])
            data_type = 'other'
        
        # 统计结果执行reset_index()统一格式
        df_reset = df_result.reset_index()
        result_data = df_reset.replace({np.nan: None, float('nan'): None}).to_dict('records')
        index_info = get_index_info(df_result)
        
        return JSONResponse(content={
            "success": True,
            "code": str(result.get('code', '')),
            "result": result_data,
            "row_count": len(df_result),
            "col_count": len(df_result.columns),
            "data_type": data_type,
            "raw_response": raw_response,
            "result_desc": result.get('result_desc', ''),
            "index_info": index_info
        })
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"统计分析失败: {str(e)}"})


@app.post("/api/stats-data-full")
async def stats_data_full_api(
    file: UploadFile = File(...),
    requirement: str = Form(""),
    data_desc: str = Form(""),
    read_func: str = Form("auto"),
    sep: str = Form(","),
    encoding: str = Form("utf-8"),
    header: str = Form("0"),
    names: str = Form("")
):
    """API接口 - 使用全部数据进行统计分析"""
    from fastapi.responses import JSONResponse
    
    try:
        import pandas as pd
        import io
        from pancharts.agent import data_chat
        
        if not requirement:
            return JSONResponse(content={"success": False, "error": "统计需求不能为空"})
        
        content = await file.read()
        filename = file.filename
        
        read_kwargs = {}
        
        if header == "-1":
            read_kwargs['header'] = None
        else:
            read_kwargs['header'] = int(header)
        
        names_list = [n.strip() for n in names.split('\n') if n.strip()] if names else None
        if names_list:
            read_kwargs['names'] = names_list
        
        if sep == '\\t':
            sep = '\t'
        elif sep == ' ':
            sep = ' '
        read_kwargs['sep'] = sep
        
        read_kwargs['encoding'] = encoding
        
        ext = filename.lower().split('.')[-1] if filename else ''
        use_excel = False
        
        if read_func == 'excel':
            use_excel = True
        elif read_func == 'csv':
            use_excel = False
        else:
            use_excel = (ext in ['xls', 'xlsx'])
        
        if use_excel:
            read_kwargs.pop('sep', None)
            df = pd.read_excel(io.BytesIO(content), **read_kwargs)
        else:
            df = pd.read_csv(io.StringIO(content.decode(encoding)), **read_kwargs)
        
        result = data_chat(df, requirement, data_desc)
        
        raw_response = str(result.get('raw_response', '')) if result.get('raw_response') else ''
        
        if result.get('error'):
            return JSONResponse(content={
                "success": False, 
                "error": str(result['error']), 
                "code": str(result.get('code', '')), 
                "raw_response": raw_response
            })
        
        stats_result = result.get('result')
        if stats_result is None:
            return JSONResponse(content={
                "success": False, 
                "error": "未生成统计结果", 
                "code": str(result.get('code', '')), 
                "raw_response": raw_response
            })
        
        def replace_nan(value):
            if isinstance(value, float) and np.isnan(value):
                return None
            if isinstance(value, list):
                return [replace_nan(v) for v in value]
            if isinstance(value, dict):
                return {k: replace_nan(v) for k, v in value.items()}
            return value
        
        index_info = None
        
        if isinstance(stats_result, pd.DataFrame):
            result_data = stats_result.replace({np.nan: None}).to_dict('records')
            row_count = len(result_data)
            col_count = len(result_data[0]) if result_data else 0
            data_type = 'dataframe'
            index_info = {
                'has_index': not stats_result.index.equals(pd.RangeIndex(len(stats_result))),
                'index_name': stats_result.index.name,
                'index_values': stats_result.index.tolist(),
                'columns': stats_result.columns.tolist(),
                'is_multi_index': isinstance(stats_result.index, pd.MultiIndex),
                'index_levels': stats_result.index.nlevels if isinstance(stats_result.index, pd.MultiIndex) else 1,
                'index_names': list(stats_result.index.names) if isinstance(stats_result.index, pd.MultiIndex) else [stats_result.index.name]
            }
        elif isinstance(stats_result, pd.Series):
            index_data = stats_result.index.tolist()
            if isinstance(stats_result.index, pd.MultiIndex):
                index_data = [list(idx) for idx in stats_result.index]
            
            result_data = {
                'index': index_data,
                'values': replace_nan(stats_result.values.tolist()),
                'name': stats_result.name,
                'is_multi_index': isinstance(stats_result.index, pd.MultiIndex),
                'index_names': list(stats_result.index.names) if isinstance(stats_result.index, pd.MultiIndex) else None
            }
            row_count = len(stats_result)
            col_count = 1
            data_type = 'series'
            # 为Series也添加index_info
            index_info = {
                'has_index': not stats_result.index.equals(pd.RangeIndex(len(stats_result))),
                'index_name': stats_result.index.name,
                'index_values': stats_result.index.tolist(),
                'is_multi_index': isinstance(stats_result.index, pd.MultiIndex),
                'index_levels': stats_result.index.nlevels if isinstance(stats_result.index, pd.MultiIndex) else 1,
                'index_names': list(stats_result.index.names) if isinstance(stats_result.index, pd.MultiIndex) else [stats_result.index.name],
                'series_name': stats_result.name
            }
        else:
            result_data = [{"result": str(stats_result)}]
            row_count = 1
            col_count = 1
            data_type = 'other'
            index_info = None
        
        return JSONResponse(content={
            "success": True,
            "code": str(result.get('code', '')),
            "result": result_data,
            "row_count": row_count,
            "col_count": col_count,
            "data_type": data_type,
            "raw_response": raw_response,
            "result_desc": result.get('result_desc', ''),
            "index_info": index_info
        })
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"统计分析失败: {str(e)}", "raw_response": ""})


def get_index_info(df):
    """
    获取数据的索引信息
    
    参数：
        df: pd.DataFrame - 输入的数据框
    
    返回：
        dict - 索引信息
    """
    has_index = not df.index.equals(pd.RangeIndex(len(df)))
    original_index_columns = []
    if has_index:
        if isinstance(df.index, pd.MultiIndex):
            original_index_columns = [name for name in df.index.names if name is not None]
        elif df.index.name is not None:
            original_index_columns = [df.index.name]
    
    return {
        'has_index': has_index,
        'index_name': df.index.name,
        'index_values': df.index.tolist(),
        'columns': df.columns.tolist(),
        'is_multi_index': isinstance(df.index, pd.MultiIndex),
        'index_levels': df.index.nlevels if isinstance(df.index, pd.MultiIndex) else 1,
        'index_names': list(df.index.names) if isinstance(df.index, pd.MultiIndex) else [df.index.name],
        'original_index_columns': original_index_columns
    }


@app.post("/api/read-data")
async def read_data_api(
    file: UploadFile = File(...),
    read_func: str = Form("auto"),
    sep: str = Form(","),
    encoding: str = Form("utf-8"),
    header: str = Form("0"),
    names: str = Form(""),
    nrows: str = Form(""),
    skiprows: str = Form(""),
    skipfooter: str = Form(""),
    usecols: str = Form(""),
    index_col: str = Form(""),
    parse_dates: str = Form(""),
    na_values: str = Form(""),
    skip_blank_lines: bool = Form(True)
):
    """API接口 - 读取数据文件，支持pandas read_csv/read_excel常用参数"""
    try:
        import pandas as pd
        import numpy as np
        import io
        
        content = await file.read()
        filename = file.filename
        
        upload_dir = os.path.join(os.path.dirname(get_db_path()), "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        server_path = os.path.join(upload_dir, filename)
        with open(server_path, 'wb') as f:
            f.write(content)
        
        read_kwargs = {}
        
        if header == "-1":
            read_kwargs['header'] = None
        else:
            read_kwargs['header'] = int(header)
        
        names_list = [n.strip() for n in names.split('\n') if n.strip()] if names else None
        if names_list:
            read_kwargs['names'] = names_list
        
        if sep == '\\t':
            sep = '\t'
        elif sep == ' ':
            sep = ' '
        read_kwargs['sep'] = sep
        
        read_kwargs['encoding'] = encoding
        
        if nrows.strip():
            read_kwargs['nrows'] = int(nrows)
        
        if skiprows.strip():
            read_kwargs['skiprows'] = int(skiprows)
        
        if skipfooter.strip():
            read_kwargs['skipfooter'] = int(skipfooter)
        
        if usecols.strip():
            read_kwargs['usecols'] = [c.strip() for c in usecols.split(',')]
        
        if index_col.strip():
            read_kwargs['index_col'] = index_col.strip()
        
        if parse_dates.strip():
            read_kwargs['parse_dates'] = [c.strip() for c in parse_dates.split(',')]
        
        if na_values.strip():
            read_kwargs['na_values'] = [v.strip() for v in na_values.split(',')]
        
        read_kwargs['skip_blank_lines'] = skip_blank_lines
        
        ext = filename.lower().split('.')[-1] if filename else ''
        use_excel = False
        
        if read_func == 'excel':
            use_excel = True
        elif read_func == 'csv':
            use_excel = False
        else:
            use_excel = (ext in ['xls', 'xlsx'])
        
        if use_excel:
            read_kwargs.pop('sep', None)
            df = pd.read_excel(io.BytesIO(content), **read_kwargs)
        else:
            df = pd.read_csv(io.StringIO(content.decode(encoding)), **read_kwargs)
        
        result_data = df.replace({np.nan: None, float('nan'): None}).to_dict('records')
        index_info = get_index_info(df)
        
        return JSONResponse(content={
            "success": True,
            "data": result_data,
            "row_count": len(df),
            "col_count": len(df.columns),
            "data_type": "dataframe",
            "index_info": index_info,
            "filename": filename,
            "server_path": server_path
        })
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"读取文件失败: {str(e)}"})


@app.get("/visualization", response_class=HTMLResponse)
async def visualization_page(request: Request):
    """可视化页面"""
    template = jinja_env.get_template("visualization.html")
    html_content = template.render({"request": request})
    return HTMLResponse(content=html_content)


@app.post("/api/get-data-info")
async def get_data_info_api(request: Request):
    """API接口 - 获取数据信息"""
    try:
        import pandas as pd
        import io
        
        data = await request.json()
        raw_data = data.get("data", [])
        data_type = data.get("data_type", "dataframe")
        index_info = data.get("index_info", None)
        
        if not raw_data:
            return JSONResponse(content={"success": False, "error": "数据为空"})
        
        # 检查数据是否已经包含了索引列（统计结果有，数据读取没有）
        has_index_columns_in_data = False
        if index_info and index_info.get('has_index') and index_info.get('original_index_columns'):
            df_check = pd.DataFrame(raw_data)
            original_index_columns = index_info.get('original_index_columns', [])
            has_index_columns_in_data = len(original_index_columns) > 0 and all(col in df_check.columns for col in original_index_columns)
        
        if data_type == 'series':
            if isinstance(raw_data, dict) and 'values' in raw_data and 'index' in raw_data:
                if raw_data.get('is_multi_index') and raw_data.get('index_names'):
                    index_tuples = [tuple(idx) for idx in raw_data.get('index', [])]
                    vis_data = pd.Series(raw_data.get('values', []), index=pd.MultiIndex.from_tuples(index_tuples, names=raw_data.get('index_names')), name=raw_data.get('name'))
                else:
                    vis_data = pd.Series(raw_data.get('values', []), index=raw_data.get('index', []), name=raw_data.get('name'))
            else:
                df = pd.DataFrame(raw_data)
                if len(df.columns) >= 2:
                    if has_index_columns_in_data:
                        # 数据中已经包含索引列
                        if index_info and index_info.get('is_multi_index'):
                            # 多重索引
                            df.set_index(index_info.get('original_index_columns'), inplace=True)
                            vis_data = df.iloc[:, 0]
                        else:
                            # 单重索引
                            df.set_index(index_info.get('original_index_columns'), inplace=True)
                            vis_data = df.iloc[:, 0]
                    elif index_info and index_info.get('is_multi_index') and index_info.get('index_levels') and index_info.get('index_levels') > 1:
                        # 使用index_info中的索引信息
                        index_tuples = [tuple(idx) for idx in index_info.get('index_values')]
                        vis_data = pd.Series(df.iloc[:, -1].values, index=pd.MultiIndex.from_tuples(index_tuples, names=index_info.get('index_names')), name=df.columns[-1])
                    else:
                        # 对于普通情况
                        vis_data = pd.Series(df.iloc[:, 1].values, index=df.iloc[:, 0], name=df.columns[1])
                elif len(df.columns) == 1:
                    vis_data = pd.Series(df.iloc[:, 0].values, name=df.columns[0])
                else:
                    return JSONResponse(content={"success": False, "error": "数据为空"})
            df = vis_data.to_frame()
        else:
            df = pd.DataFrame(raw_data)
            if has_index_columns_in_data and index_info and index_info.get('original_index_columns'):
                # 数据中已经包含索引列，直接设置
                df.set_index(index_info.get('original_index_columns'), inplace=True)
            elif index_info and index_info.get('has_index') and index_info.get('index_values'):
                # 数据中没有索引列，从index_info设置
                if index_info.get('is_multi_index') and index_info.get('index_names'):
                    index_tuples = [tuple(idx) for idx in index_info.get('index_values')]
                    df.index = pd.MultiIndex.from_tuples(index_tuples, names=index_info.get('index_names'))
                else:
                    df.index = pd.Index(index_info.get('index_values'), name=index_info.get('index_name'))
        
        buffer = io.StringIO()
        df.info(buf=buffer)
        data_info = buffer.getvalue()
        
        return JSONResponse(content={
            "success": True,
            "data_info": data_info,
            "row_count": len(df),
            "col_count": len(df.columns),
            "columns": df.columns.tolist()
        })
        
    except Exception as e:
        import traceback
        return JSONResponse(content={"success": False, "error": f"获取数据信息失败: {str(e)}\n{traceback.format_exc()}"})


@app.post("/api/create-visualization")
async def create_visualization_api(request: Request):
    """API接口 - 创建可视化图表"""
    try:
        import pandas as pd
        from pancharts.pandas_charts import k_v, km_nv, k2_nv, k_vm, gk_vm, gk_vm_amap, gk_vm_globe, sk_vm
        
        data = await request.json()
        vis_class = data.get("vis_class")
        method = data.get("method")
        raw_data = data.get("data", [])
        data_type = data.get("data_type", "dataframe")
        reconstruct_type = data.get("reconstruct_type", "dataframe")
        index_columns = data.get("index_columns", [])
        params = data.get("params", {})
        
        if not vis_class or not method or not raw_data:
            return JSONResponse(content={"success": False, "error": "参数不完整"})
        
        class_map = {
            'k_v': k_v,
            'km_nv': km_nv,
            'k2_nv': k2_nv,
            'k_vm': k_vm,
            'gk_vm': gk_vm,
            'gk_vm_amap': gk_vm_amap,
            'gk_vm_globe': gk_vm_globe,
            'sk_vm': sk_vm
        }
        
        if vis_class not in class_map:
            return JSONResponse(content={"success": False, "error": f"未知的可视化类: {vis_class}"})
        
        index_info = data.get("index_info", None)
        drop_columns = data.get("drop_columns", [])
        
        # 数据重构步骤
        # 创建DataFrame
        df = pd.DataFrame(raw_data)
        
        # 删除选择的列
        if drop_columns and len(drop_columns) > 0:
            df = df.drop(columns=[col for col in drop_columns if col in df.columns])
        
        # 检查数据是否已经包含了索引列（统计结果有，数据读取没有）
        has_index_columns_in_data = False
        if index_info and index_info.get('has_index') and index_info.get('original_index_columns'):
            original_index_columns = index_info.get('original_index_columns', [])
            has_index_columns_in_data = len(original_index_columns) > 0 and all(col in df.columns for col in original_index_columns)
        
        # 设置索引
        if index_columns:
            # 检查索引列是否存在于数据中
            missing_columns = []
            for col in index_columns:
                if col not in df.columns:
                    missing_columns.append(col)
            
            if missing_columns:
                # 索引列不在数据中，需要从index_info获取
                if index_info and index_info.get('has_index'):
                    if index_info.get('is_multi_index') and index_info.get('index_names'):
                        # 多重索引
                        index_tuples = [tuple(idx) for idx in index_info.get('index_values')]
                        df.index = pd.MultiIndex.from_tuples(index_tuples, names=index_info.get('index_names'))
                    else:
                        # 单重索引
                        df.index = pd.Index(index_info.get('index_values'), name=index_info.get('index_name'))
                else:
                    return JSONResponse(content={"success": False, "error": f"索引列 '{missing_columns[0]}' 不存在"})
            else:
                # 所有索引列都存在于数据中，直接设置
                df.set_index(index_columns, inplace=True)
        
        # 根据重构类型处理
        if reconstruct_type == "series":
            # 对于Series，使用第一列作为值
            if len(df.columns) == 0:
                return JSONResponse(content={"success": False, "error": "数据框没有列"})
            vis_data = df.iloc[:, 0]
        else:
            # 对于DataFrame，根据可视化类处理
            if vis_class == 'k_v':
                if len(df.columns) == 0:
                    return JSONResponse(content={"success": False, "error": "数据为空"})
                # 确保使用df的索引，而不是重新创建
                vis_data = pd.Series(df.iloc[:, 0].values, index=df.index, name=df.columns[0])
            elif vis_class == 'km_nv':
                if len(df.columns) >= 2:
                    # 处理任意级别的多重索引
                    # 假设前n-1列是索引，最后一列是值
                    if len(df.columns) > 2:
                        # 对于多重索引，使用所有列除了最后一列作为索引
                        index_cols = df.columns[:-1]
                        index_tuples = list(zip(*[df[col] for col in index_cols]))
                        index = pd.MultiIndex.from_tuples(index_tuples)
                        vis_data = pd.Series(df.iloc[:, -1].values, index=index)
                    else:
                        # 对于双重索引，使用前两列作为索引
                        index = pd.MultiIndex.from_tuples(list(zip(df.iloc[:, 0], df.iloc[:, 1])))
                        vis_data = pd.Series([1]*len(df), index=index)
                else:
                    vis_data = df.iloc[:, 0]
            elif vis_class == 'k2_nv':
                if len(df.columns) >= 3:
                    index = pd.MultiIndex.from_tuples(list(zip(df.iloc[:, 0], df.iloc[:, 1])))
                    vis_data = pd.Series(df.iloc[:, 2].values, index=index)
                else:
                    vis_data = df.iloc[:, 0]
            else:
                vis_data = df
        
        vis_instance = class_map[vis_class](vis_data)
        
        if not hasattr(vis_instance, method):
            return JSONResponse(content={"success": False, "error": f"方法 {method} 不存在"})
        
        method_func = getattr(vis_instance, method)
        
        try:
            if params:
                result = method_func(**params)
            else:
                result = method_func()
        except TypeError as e:
            return JSONResponse(content={"success": False, "error": f"调用方法失败: {str(e)}"})
        
        if isinstance(result, Pancharts):
            chart = result
        else:
            chart = Pancharts()
            chart.option = result
        emb_result = chart.render_emb()
        
        import io
        buffer = io.StringIO()
        if isinstance(vis_data, pd.Series):
            buffer.write(f"<class 'pandas.core.series.Series'>\n")
            buffer.write(f"Index: {len(vis_data)} entries, {vis_data.index[0]} to {vis_data.index[-1]}\n" if len(vis_data) > 0 else f"Index: 0 entries\n")
            buffer.write(f"Series name: {vis_data.name}\n")
            buffer.write(f"dtype: {vis_data.dtype}\n")
            buffer.write(f"memory usage: {vis_data.memory_usage()} bytes\n")
        else:
            vis_data.info(buf=buffer)
        data_info = buffer.getvalue()
        
        return JSONResponse(content={
            "success": True,
            "option": chart.option,
            "chart_html": emb_result["html"],
            "js_dependencies": emb_result["js_dependencies"],
            "data_info": data_info,
            "data_config": chart.data_config if hasattr(chart, 'data_config') else {}
        })
        
    except Exception as e:
        import traceback
        return JSONResponse(content={"success": False, "error": f"创建可视化失败: {str(e)}\n{traceback.format_exc()}"})


@app.post("/api/preview")
async def preview_chart_api(request: Request):
    """API接口 - 预览图表"""
    try:
        data = await request.json()
        option_text = data.get("option", "")
        
        if not option_text:
            return JSONResponse(content={"success": False, "error": "Option为空"})
        
        option = json.loads(option_text)
        
        chart = Pancharts()
        chart.option = option
        emb_result = chart.render_emb()
        
        return JSONResponse(content={
            "success": True,
            "chart_html": emb_result["html"],
            "js_dependencies": emb_result["js_dependencies"]
        })
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"预览失败: {str(e)}"})


@app.post("/api/save-chart")
async def save_chart_api(request: Request):
    """API接口 - 保存图表到数据库"""
    try:
        data = await request.json()
        option_text = data.get("option", "")
        data_option_text = data.get("data_option", "")
        tag0 = data.get("tag0", "")
        tag1 = data.get("tag1", "")
        file_path = data.get("file_path", "")
        data_desc = data.get("data_desc", "")
        data_insight = data.get("data_insight", "")
        
        if not option_text:
            return JSONResponse(content={"success": False, "error": "Option为空"})
        
        try:
            json.loads(option_text)
        except json.JSONDecodeError:
            return JSONResponse(content={"success": False, "error": "Option格式错误"})
        
        if data_option_text:
            try:
                json.loads(data_option_text)
            except json.JSONDecodeError:
                return JSONResponse(content={"success": False, "error": "Data Option格式错误"})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO pancharts_options (insert_time, option, data_option, file_path, tag0, tag1, data_desc, data_insight)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (insert_time, option_text, data_option_text, file_path, tag0, tag1, data_desc, data_insight))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return JSONResponse(content={"success": True, "id": record_id})
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"保存失败: {str(e)}"})


@app.post("/api/save-data-desc")
async def save_data_desc_api(request: Request):
    """API接口 - 保存数据配置到data_desc表"""
    import pickle
    
    try:
        data = await request.json()
        file_path = data.get("file_path", "")
        file_suffix = data.get("file_suffix", "")
        read_config = data.get("read_config", {})
        desc = data.get("desc", "")
        
        if not file_path or not file_suffix:
            return JSONResponse(content={"success": False, "error": "文件路径和后缀不能为空"})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM data_desc WHERE file_path = ?', (file_path,))
        existing_record = cursor.fetchone()
        
        if existing_record:
            conn.close()
            return JSONResponse(content={"success": False, "error": "该文件路径已存在记录", "duplicate": True})
        
        read_config_pickle = pickle.dumps(read_config)
        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO data_desc (file_path, file_suffix, read_config, desc, insert_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_path, file_suffix, read_config_pickle, desc, insert_time))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return JSONResponse(content={"success": True, "id": record_id})
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"保存失败: {str(e)}"})


@app.get("/api/get-data-desc-list")
async def get_data_desc_list_api():
    """API接口 - 获取所有数据配置记录"""
    import pickle
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, file_path, file_suffix, read_config, desc, insert_time FROM data_desc ORDER BY insert_time DESC')
        records = cursor.fetchall()
        
        result = []
        for record in records:
            id_, file_path, file_suffix, read_config_pickle, desc, insert_time = record
            try:
                read_config = pickle.loads(read_config_pickle)
            except:
                read_config = {}
            
            result.append({
                "id": id_,
                "file_path": file_path,
                "file_suffix": file_suffix,
                "read_config": read_config,
                "desc": desc,
                "insert_time": insert_time
            })
        
        conn.close()
        
        return JSONResponse(content={"success": True, "data": result})
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"获取失败: {str(e)}"})


@app.get("/api/get-data-desc/{record_id}")
async def get_data_desc_api(record_id: int):
    """API接口 - 获取单个数据配置记录"""
    import pickle
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, file_path, file_suffix, read_config, desc, insert_time FROM data_desc WHERE id = ?', (record_id,))
        record = cursor.fetchone()
        
        if not record:
            return JSONResponse(content={"success": False, "error": "记录不存在"})
        
        id_, file_path, file_suffix, read_config_pickle, desc, insert_time = record
        try:
            read_config = pickle.loads(read_config_pickle)
        except:
            read_config = {}
        
        conn.close()
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "id": id_,
                "file_path": file_path,
                "file_suffix": file_suffix,
                "read_config": read_config,
                "desc": desc,
                "insert_time": insert_time
            }
        })
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"获取失败: {str(e)}"})





@app.post("/api/read-data-by-path")
async def read_data_by_path_api(request: Request):
    """API接口 - 通过文件路径直接读取数据"""
    import pandas as pd
    import numpy as np
    import io
    
    try:
        data = await request.json()
        file_path = data.get("file_path", "")
        file_suffix = data.get("file_suffix", "")
        read_config = data.get("read_config", {})
        
        if not file_path:
            return JSONResponse(content={"success": False, "error": "文件路径不能为空"})
        
        if not os.path.exists(file_path):
            return JSONResponse(content={"success": False, "error": f"文件不存在: {file_path}"})
        
        read_kwargs = {}
        if read_config.get('sep'):
            if read_config['sep'] == '\\t':
                read_kwargs['sep'] = '\t'
            else:
                read_kwargs['sep'] = read_config['sep']
        if read_config.get('encoding'):
            read_kwargs['encoding'] = read_config['encoding']
        if read_config.get('header') is not None:
            header_val = read_config['header']
            if header_val == '-1':
                read_kwargs['header'] = None
            else:
                read_kwargs['header'] = int(header_val)
        if read_config.get('names'):
            names = [n.strip() for n in read_config['names'].split('\n') if n.strip()]
            if names:
                read_kwargs['names'] = names
        if read_config.get('nrows'):
            read_kwargs['nrows'] = int(read_config['nrows'])
        if read_config.get('skiprows'):
            read_kwargs['skiprows'] = int(read_config['skiprows'])
        if read_config.get('skipfooter'):
            read_kwargs['skipfooter'] = int(read_config['skipfooter'])
        if read_config.get('usecols'):
            read_kwargs['usecols'] = [c.strip() for c in read_config['usecols'].split(',') if c.strip()]
        if read_config.get('index_col'):
            read_kwargs['index_col'] = read_config['index_col']
        if read_config.get('parse_dates'):
            read_kwargs['parse_dates'] = [c.strip() for c in read_config['parse_dates'].split(',') if c.strip()]
        if read_config.get('na_values'):
            read_kwargs['na_values'] = [v.strip() for v in read_config['na_values'].split(',') if v.strip()]
        if read_config.get('skip_blank_lines') is not None:
            read_kwargs['skip_blank_lines'] = read_config['skip_blank_lines']
        
        if file_suffix in ['xls', 'xlsx']:
            df = pd.read_excel(file_path, **read_kwargs)
        else:
            df = pd.read_csv(file_path, **read_kwargs)
        
        result_data = df.replace({np.nan: None, float('nan'): None}).to_dict('records')
        index_info = get_index_info(df)
        
        return JSONResponse(content={
            "success": True,
            "data": result_data,
            "row_count": len(df),
            "col_count": len(df.columns),
            "data_type": "dataframe",
            "index_info": index_info,
            "file_name": os.path.basename(file_path)
        })
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"读取失败: {str(e)}"})


@app.get("/api/data-desc-list")
async def get_data_desc_list(
    file_path: str = "",
    file_suffix: str = "",
    desc: str = "",
    start_time: str = "",
    end_time: str = ""
):
    """获取data_desc表记录列表"""
    import pickle
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        where_clauses = []
        params = []
        
        if file_path:
            where_clauses.append("file_path LIKE ?")
            params.append(f"%{file_path}%")
        
        if file_suffix:
            where_clauses.append("file_suffix = ?")
            params.append(file_suffix)
        
        if desc:
            where_clauses.append("desc LIKE ?")
            params.append(f"%{desc}%")
        
        if start_time:
            where_clauses.append("insert_time >= ?")
            params.append(start_time)
        
        if end_time:
            where_clauses.append("insert_time <= ?")
            params.append(end_time)
        
        query = "SELECT * FROM data_desc"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        query += " ORDER BY id DESC"
        
        cursor.execute(query, params)
        records = cursor.fetchall()
        
        result = []
        for record in records:
            try:
                read_config = pickle.loads(record["read_config"])
            except:
                read_config = {}
            
            result.append({
                "id": record["id"],
                "file_path": record["file_path"],
                "file_suffix": record["file_suffix"],
                "read_config": read_config,
                "desc": record["desc"],
                "insert_time": record["insert_time"]
            })
        
        conn.close()
        
        return JSONResponse(content={"success": True, "data": result})
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"获取失败: {str(e)}"})


@app.get("/data-desc-edit/{record_id}", response_class=HTMLResponse)
async def data_desc_edit(request: Request, record_id: int):
    """数据描述编辑页面"""
    template = jinja_env.get_template("data_desc_edit.html")
    html_content = template.render({
        "request": request,
        "record_id": record_id
    })
    return HTMLResponse(content=html_content)


@app.get("/api/data-desc/{record_id}")
async def get_data_desc(record_id: int):
    """获取单个data_desc记录详情"""
    import pickle
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM data_desc WHERE id = ?", (record_id,))
        record = cursor.fetchone()
        
        if not record:
            return JSONResponse(content={"success": False, "error": "记录不存在"})
        
        try:
            read_config = pickle.loads(record["read_config"])
        except:
            read_config = {}
        
        conn.close()
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "id": record["id"],
                "file_path": record["file_path"],
                "file_suffix": record["file_suffix"],
                "read_config": read_config,
                "desc": record["desc"],
                "insert_time": record["insert_time"]
            }
        })
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"获取失败: {str(e)}"})


@app.put("/api/data-desc/{record_id}")
async def update_data_desc(record_id: int, request: Request):
    """更新data_desc记录"""
    try:
        data = await request.json()
        new_desc = data.get("desc", "")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE data_desc SET desc = ? WHERE id = ?", (new_desc, record_id))
        conn.commit()
        conn.close()
        
        return JSONResponse(content={"success": True})
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"更新失败: {str(e)}"})


@app.delete("/api/data-desc/{record_id}")
async def delete_data_desc(record_id: int):
    """删除data_desc记录"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM data_desc WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        
        return JSONResponse(content={"success": True})
        
    except Exception as e:
        return JSONResponse(content={"success": False, "error": f"删除失败: {str(e)}"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
