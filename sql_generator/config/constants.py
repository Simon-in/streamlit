# -*- coding: utf-8 -*-
"""
配置常量模块
"""

# 页面配置
MAIN_PAGES = ["SQL生成", "高级功能", "模板中心", "历史记录", "数据分析", "streamlit_example"]

SQL_SUB_PAGES = ["主页", "CREATE", "SELECT", "INSERT", "UPDATE", "MERGE", "DELETE", "TRUNCATE"]

ADVANCED_SUB_PAGES = ["视图管理", "索引优化", "存储过程", "触发器", "函数管理", "约束管理"]

TEMPLATE_SUB_PAGES = ["基础查询", "数据操作", "表结构", "性能优化", "数据分析", "自定义模板"]

HISTORY_SUB_PAGES = ["最近记录", "收藏夹", "搜索历史", "使用统计", "导出数据"]

ANALYSIS_SUB_PAGES = ["数据概况", "SQL格式化", "语法检查"]

EXAMPLE_SUB_PAGES = ["主页", "button", "write", "slider", "line_chart", "selectbox"]

# Excel配置
EXCEL_SHEETS = {
    'select': 'select',
    'create': 'create',
    'insert': 'insert',
    'merge': 'merge',
    'delete': 'delete',
    'truncate': 'truncate'
}

# MIME类型
MIME_TYPES = {
    'sql': 'text/plain',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'csv': 'text/csv',
    'json': 'application/json',
    'txt': 'text/plain'
}

# 支持的文件类型
SUPPORTED_FILE_TYPES = ['xlsx', 'csv', 'sql']

# 应用配置
APP_CONFIG = {
    'page_title': 'SQL生成工具',
    'page_icon': '🔧',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# 安全配置
SECURITY_CONFIG = {
    'max_file_size_mb': 5,
    'allowed_file_types': ['xlsx', 'csv', 'sql'],
    'sql_blacklist': [
        'DROP', 'TRUNCATE', 'DELETE', 'UPDATE', 'ALTER', 'INSERT', 
        'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK', 'EXECUTE'
    ]
}
