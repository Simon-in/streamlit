# -*- coding: utf-8 -*-
"""
SQL模板系统 - 提供常用SQL语句模板和代码片段
"""

import streamlit as st
from typing import Dict, List, Any
from utils import UIHelper


class SQLTemplateManager:
    """SQL模板管理器"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """加载SQL模板"""
        return {
            # 基础查询模板
            "basic_queries": {
                "name": "基础查询",
                "templates": {
                    "simple_select": {
                        "name": "简单查询",
                        "description": "基础的SELECT语句",
                        "template": """SELECT {columns}
FROM {table}
WHERE {condition};""",
                        "parameters": ["columns", "table", "condition"],
                        "example": """SELECT id, name, email
FROM users
WHERE status = 'active';"""
                    },
                    "join_query": {
                        "name": "连接查询",
                        "description": "多表连接查询",
                        "template": """SELECT {select_columns}
FROM {main_table} a
{join_type} JOIN {join_table} b ON a.{join_key1} = b.{join_key2}
WHERE {condition};""",
                        "parameters": ["select_columns", "main_table", "join_type", "join_table", "join_key1", "join_key2", "condition"],
                        "example": """SELECT u.name, o.order_date, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';"""
                    },
                    "aggregate_query": {
                        "name": "聚合查询",
                        "description": "分组聚合统计",
                        "template": """SELECT {group_columns}, {aggregate_functions}
FROM {table}
WHERE {condition}
GROUP BY {group_columns}
HAVING {having_condition}
ORDER BY {order_columns};""",
                        "parameters": ["group_columns", "aggregate_functions", "table", "condition", "having_condition", "order_columns"],
                        "example": """SELECT department, COUNT(*) as employee_count, AVG(salary) as avg_salary
FROM employees
WHERE status = 'active'
GROUP BY department
HAVING COUNT(*) > 5
ORDER BY avg_salary DESC;"""
                    }
                }
            },
            
            # 数据操作模板
            "data_operations": {
                "name": "数据操作",
                "templates": {
                    "batch_insert": {
                        "name": "批量插入",
                        "description": "批量插入数据",
                        "template": """INSERT INTO {table} ({columns})
VALUES 
{values};""",
                        "parameters": ["table", "columns", "values"],
                        "example": """INSERT INTO users (name, email, created_at)
VALUES 
    ('John Doe', 'john@example.com', NOW()),
    ('Jane Smith', 'jane@example.com', NOW()),
    ('Bob Johnson', 'bob@example.com', NOW());"""
                    },
                    "conditional_update": {
                        "name": "条件更新",
                        "description": "基于条件的数据更新",
                        "template": """UPDATE {table}
SET {set_clause}
WHERE {condition};""",
                        "parameters": ["table", "set_clause", "condition"],
                        "example": """UPDATE users
SET status = 'inactive', updated_at = NOW()
WHERE last_login < DATE_SUB(NOW(), INTERVAL 1 YEAR);"""
                    },
                    "upsert": {
                        "name": "插入或更新",
                        "description": "存在则更新，不存在则插入",
                        "template": """INSERT INTO {table} ({columns})
VALUES ({values})
ON DUPLICATE KEY UPDATE
{update_clause};""",
                        "parameters": ["table", "columns", "values", "update_clause"],
                        "example": """INSERT INTO user_stats (user_id, login_count, last_login)
VALUES (1, 1, NOW())
ON DUPLICATE KEY UPDATE
login_count = login_count + 1, last_login = NOW();"""
                    }
                }
            },
            
            # 表结构模板
            "table_structures": {
                "name": "表结构",
                "templates": {
                    "user_table": {
                        "name": "用户表",
                        "description": "标准用户表结构",
                        "template": """CREATE TABLE {table_name} (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);""",
                        "parameters": ["table_name"],
                        "example": """CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    -- ... 其他字段
);"""
                    },
                    "audit_table": {
                        "name": "审计日志表",
                        "description": "数据变更审计表",
                        "template": """CREATE TABLE {table_name} (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(100) NOT NULL,
    record_id BIGINT NOT NULL,
    operation ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    old_values JSON,
    new_values JSON,
    user_id BIGINT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_table_record (table_name, record_id),
    INDEX idx_operation (operation),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);""",
                        "parameters": ["table_name"],
                        "example": """CREATE TABLE audit_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(100) NOT NULL,
    -- ... 其他字段
);"""
                    }
                }
            },
            
            # 性能优化模板
            "performance": {
                "name": "性能优化",
                "templates": {
                    "explain_query": {
                        "name": "查询分析",
                        "description": "分析查询执行计划",
                        "template": """EXPLAIN FORMAT=JSON
{your_query};""",
                        "parameters": ["your_query"],
                        "example": """EXPLAIN FORMAT=JSON
SELECT * FROM users WHERE email = 'john@example.com';"""
                    },
                    "index_analysis": {
                        "name": "索引分析",
                        "description": "分析表的索引使用情况",
                        "template": """-- 查看表的索引
SHOW INDEX FROM {table_name};

-- 查看索引使用统计
SELECT * FROM INFORMATION_SCHEMA.STATISTICS 
WHERE TABLE_SCHEMA = '{database_name}' AND TABLE_NAME = '{table_name}';""",
                        "parameters": ["table_name", "database_name"],
                        "example": """SHOW INDEX FROM users;"""
                    },
                    "slow_query_analysis": {
                        "name": "慢查询分析",
                        "description": "分析慢查询日志",
                        "template": """-- 启用慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = {threshold_seconds};

-- 查看慢查询统计
SELECT 
    query_time,
    lock_time,
    rows_sent,
    rows_examined,
    sql_text
FROM performance_schema.events_statements_history_long
WHERE start_time >= DATE_SUB(NOW(), INTERVAL 1 DAY)
ORDER BY query_time DESC
LIMIT 10;""",
                        "parameters": ["threshold_seconds"],
                        "example": """SET GLOBAL long_query_time = 2;"""
                    }
                }
            },
            
            # 数据分析模板
            "data_analysis": {
                "name": "数据分析",
                "templates": {
                    "data_profiling": {
                        "name": "数据概况",
                        "description": "分析数据质量和分布",
                        "template": """-- 数据概况分析
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT {key_column}) as unique_keys,
    COUNT({column}) as non_null_count,
    COUNT(*) - COUNT({column}) as null_count,
    MIN({column}) as min_value,
    MAX({column}) as max_value,
    AVG({column}) as avg_value
FROM {table};""",
                        "parameters": ["table", "key_column", "column"],
                        "example": """SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(email) as valid_emails
FROM users;"""
                    },
                    "time_series_analysis": {
                        "name": "时间序列分析",
                        "description": "按时间维度分析数据趋势",
                        "template": """SELECT 
    DATE({date_column}) as date,
    COUNT(*) as daily_count,
    SUM({value_column}) as daily_sum,
    AVG({value_column}) as daily_avg
FROM {table}
WHERE {date_column} >= DATE_SUB(NOW(), INTERVAL {days} DAY)
GROUP BY DATE({date_column})
ORDER BY date;""",
                        "parameters": ["table", "date_column", "value_column", "days"],
                        "example": """SELECT 
    DATE(created_at) as date,
    COUNT(*) as new_users
FROM users
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY date;"""
                    }
                }
            }
        }
    
    def get_categories(self) -> List[str]:
        """获取所有模板分类"""
        return list(self.templates.keys())
    
    def get_templates_by_category(self, category: str) -> Dict[str, Any]:
        """获取指定分类的模板"""
        return self.templates.get(category, {}).get("templates", {})
    
    def get_template(self, category: str, template_id: str) -> Dict[str, Any]:
        """获取指定模板"""
        return self.get_templates_by_category(category).get(template_id, {})
    
    def render_template(self, template: str, parameters: Dict[str, str]) -> str:
        """渲染模板"""
        try:
            rendered = template
            for key, value in parameters.items():
                placeholder = "{" + key + "}"
                rendered = rendered.replace(placeholder, str(value))
            return rendered
        except Exception as e:
            UIHelper.show_error(f"渲染模板时发生错误: {str(e)}")
            return template


class CommonSQLPatterns:
    """常用SQL模式"""
    
    @staticmethod
    def generate_pagination_query(table: str, page_size: int = 20, page_number: int = 1,
                                 order_column: str = "id", where_clause: str = "") -> str:
        """生成分页查询"""
        offset = (page_number - 1) * page_size
        where_part = f"WHERE {where_clause}" if where_clause else ""
        
        return f"""-- 分页查询 (第{page_number}页，每页{page_size}条)
SELECT *
FROM {table}
{where_part}
ORDER BY {order_column}
LIMIT {page_size} OFFSET {offset};

-- 获取总记录数
SELECT COUNT(*) as total_count
FROM {table}
{where_part};"""
    
    @staticmethod
    def generate_backup_table_query(source_table: str, backup_suffix: str = None) -> str:
        """生成表备份查询"""
        if not backup_suffix:
            from datetime import datetime
            backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        backup_table = f"{source_table}_backup_{backup_suffix}"
        
        return f"""-- 创建表备份
CREATE TABLE {backup_table} AS
SELECT * FROM {source_table};

-- 验证备份
SELECT 
    (SELECT COUNT(*) FROM {source_table}) as original_count,
    (SELECT COUNT(*) FROM {backup_table}) as backup_count;"""
    
    @staticmethod
    def generate_data_migration_query(source_table: str, target_table: str, 
                                    column_mapping: Dict[str, str] = None,
                                    where_condition: str = "") -> str:
        """生成数据迁移查询"""
        if column_mapping:
            source_columns = ", ".join(column_mapping.keys())
            target_columns = ", ".join(column_mapping.values())
        else:
            source_columns = "*"
            target_columns = ""
        
        where_part = f"WHERE {where_condition}" if where_condition else ""
        
        if target_columns:
            insert_part = f"({target_columns})"
        else:
            insert_part = ""
        
        return f"""-- 数据迁移
INSERT INTO {target_table} {insert_part}
SELECT {source_columns}
FROM {source_table}
{where_part};

-- 验证迁移结果
SELECT 
    (SELECT COUNT(*) FROM {source_table} {where_part}) as source_count,
    (SELECT COUNT(*) FROM {target_table}) as target_count;"""
    
    @staticmethod
    def generate_duplicate_detection_query(table: str, columns: List[str]) -> str:
        """生成重复数据检测查询"""
        columns_str = ", ".join(columns)
        
        return f"""-- 检测重复数据
SELECT {columns_str}, COUNT(*) as duplicate_count
FROM {table}
GROUP BY {columns_str}
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;

-- 查看重复记录的详细信息
SELECT t1.*
FROM {table} t1
INNER JOIN (
    SELECT {columns_str}
    FROM {table}
    GROUP BY {columns_str}
    HAVING COUNT(*) > 1
) t2 ON {' AND '.join([f't1.{col} = t2.{col}' for col in columns])}
ORDER BY {columns_str};"""
    
    @staticmethod
    def generate_data_quality_check(table: str, columns: List[str]) -> str:
        """生成数据质量检查查询"""
        checks = []
        
        for column in columns:
            checks.append(f"""
-- {column} 列质量检查
SELECT 
    '{column}' as column_name,
    COUNT(*) as total_count,
    COUNT({column}) as non_null_count,
    COUNT(*) - COUNT({column}) as null_count,
    ROUND((COUNT({column}) / COUNT(*)) * 100, 2) as completeness_percentage
FROM {table}""")
        
        return "\nUNION ALL\n".join(checks) + ";" 