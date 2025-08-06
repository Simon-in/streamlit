# -*- coding: utf-8 -*-
"""
配置文件 - 管理应用程序的配置项和常量
"""

# 页面配置
MAIN_PAGES = ["SQL生成", "高级功能", "模板中心", "历史记录", "数据分析", "streamlit_example"]

SQL_SUB_PAGES = ["主页", "CREATE", "SELECT", "INSERT", "UPDATE", "MERGE", "DELETE", "TRUNCATE"]

ADVANCED_SUB_PAGES = ["视图管理", "索引优化", "存储过程", "触发器", "函数管理", "约束管理"]

TEMPLATE_SUB_PAGES = ["基础查询", "数据操作", "表结构", "性能优化", "数据分析", "自定义模板"]

HISTORY_SUB_PAGES = ["最近记录", "收藏夹", "搜索历史", "使用统计", "导出数据"]

ANALYSIS_SUB_PAGES = ["文件分析", "数据概况", "SQL格式化", "语法检查", "性能建议"]

EXAMPLE_SUB_PAGES = ["主页", "button", "write", "slider", "line_chart", "selectbox"]

SELECT_SUB_PAGES = ["单张表", "批量生成多表"]

# 文件配置
SUPPORTED_FILE_TYPES = ["csv", "txt", "xlsx"]

SAMPLE_FILE_PATH = "main/static/sql_example.xlsx"

# 图片路径配置
IMAGE_PATHS = {
    "create": "main/image/create.png",
    "select": "main/image/select.png",
    "merge": "main/image/merge.png"
}

# MIME类型配置
MIME_TYPES = {
    'xlsx': "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    'zip': "application/zip",
    'json': "application/json",
    'sql': "application/sql"
}

# Excel工作表名称
EXCEL_SHEETS = {
    'select': 'select',
    'insert': 'insert', 
    'delete': 'delete',
    'truncate': 'truncate',
    'merge': 'merge',
    'create': 'create'
}

# 应用程序设置
APP_CONFIG = {
    'page_title': 'SQL生成工具',
    'page_icon': '🔧',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
} 