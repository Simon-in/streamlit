# -*- coding: utf-8 -*-
"""
SQL模板模块 - 提供常用SQL模板和模式
"""

import os
import json
from typing import Dict, List, Any, Optional


class SQLTemplateManager:
    """SQL模板管理器类"""
    
    def __init__(self, custom_templates_path=None):
        """
        初始化SQL模板管理器
        
        Args:
            custom_templates_path: 自定义模板文件路径（可选）
        """
        self.templates = {
            "basic_queries": {
                "name": "基础查询模板",
                "description": "常用的基础SQL查询模板",
                "templates": {
                    "simple_select": {
                        "name": "简单查询",
                        "description": "基本的SELECT查询",
                        "template": "SELECT {columns} FROM {table} WHERE {condition};"
                    },
                    "join_select": {
                        "name": "JOIN查询",
                        "description": "带JOIN的查询",
                        "template": "SELECT {columns} FROM {table1} JOIN {table2} ON {join_condition} WHERE {condition};"
                    },
                    "group_by": {
                        "name": "分组查询",
                        "description": "带GROUP BY的查询",
                        "template": "SELECT {group_columns}, {agg_function}({agg_column}) FROM {table} GROUP BY {group_columns};"
                    }
                }
            },
            "data_manipulation": {
                "name": "数据操作模板",
                "description": "INSERT, UPDATE, DELETE等模板",
                "templates": {
                    "insert_values": {
                        "name": "插入数据",
                        "description": "基本的INSERT语句",
                        "template": "INSERT INTO {table} ({columns}) VALUES ({values});"
                    },
                    "update_values": {
                        "name": "更新数据",
                        "description": "基本的UPDATE语句",
                        "template": "UPDATE {table} SET {set_clause} WHERE {condition};"
                    },
                    "delete_values": {
                        "name": "删除数据",
                        "description": "基本的DELETE语句",
                        "template": "DELETE FROM {table} WHERE {condition};"
                    }
                }
            },
            "schema_management": {
                "name": "表结构管理模板",
                "description": "创建和修改表结构的模板",
                "templates": {
                    "create_table": {
                        "name": "创建表",
                        "description": "创建表的模板",
                        "template": "CREATE TABLE {table} (\n    {columns}\n);"
                    },
                    "alter_table": {
                        "name": "修改表",
                        "description": "修改表结构的模板",
                        "template": "ALTER TABLE {table} {action};"
                    }
                }
            }
        }
        
        # 加载自定义模板
        if custom_templates_path and os.path.exists(custom_templates_path):
            with open(custom_templates_path, 'r', encoding='utf-8') as file:
                custom_templates = json.load(file)
                self.templates.update(custom_templates)
    
    def get_categories(self) -> List[str]:
        """
        获取所有模板分类
        
        Returns:
            模板分类列表
        """
        return list(self.templates.keys())
    
    def get_templates_by_category(self, category: str) -> Dict[str, Any]:
        """
        按分类获取模板
        
        Args:
            category: 模板分类名
            
        Returns:
            指定分类下的模板字典
        """
        if category in self.templates:
            return self.templates[category].get('templates', {})
        return {}
    
    def render_template(self, template_str: str, params: Dict[str, Any]) -> str:
        """
        渲染模板
        
        Args:
            template_str: 模板字符串
            params: 参数字典
            
        Returns:
            渲染后的SQL语句
        """
        rendered_sql = template_str
        
        # 简单的模板替换
        for key, value in params.items():
            placeholder = "{" + key + "}"
            rendered_sql = rendered_sql.replace(placeholder, str(value))
        
        return rendered_sql
    
    def save_custom_template(self, category: str, template_id: str, template_data: Dict[str, Any]) -> bool:
        """
        保存自定义模板
        
        Args:
            category: 模板分类
            template_id: 模板ID
            template_data: 模板数据
            
        Returns:
            保存是否成功
        """
        if category not in self.templates:
            self.templates[category] = {
                "name": category,
                "description": f"{category}模板集合",
                "templates": {}
            }
        
        self.templates[category]["templates"][template_id] = template_data
        return True
    
    def get_all_templates(self) -> Dict[str, Any]:
        """
        获取所有模板
        
        Returns:
            所有模板字典
        """
        return self.templates


class CommonSQLPatterns:
    """常用SQL模式类"""
    
    @staticmethod
    def generate_trend_analysis_query(table_name: str, time_column: str, metric_column: str, 
                                    group_by: Optional[str] = None, interval: str = 'month') -> str:
        """
        生成趋势分析SQL
        
        Args:
            table_name: 表名
            time_column: 时间列名
            metric_column: 指标列名
            group_by: 分组列名（可选）
            interval: 时间间隔，如 'day', 'week', 'month', 'year'
            
        Returns:
            趋势分析SQL语句
        """
        # 构建时间格式化函数（兼容不同数据库）
        time_format = {
            'day': f"TRUNC({time_column}, 'DD')",  # Oracle语法
            'week': f"TRUNC({time_column}, 'IW')",
            'month': f"TRUNC({time_column}, 'MM')",
            'quarter': f"TRUNC({time_column}, 'Q')",
            'year': f"TRUNC({time_column}, 'YYYY')"
        }.get(interval.lower(), f"TRUNC({time_column}, 'MM')")
        
        # 构建SELECT子句
        select_clause = f"SELECT {time_format} AS time_period"
        
        # 添加分组列
        if group_by:
            select_clause += f", {group_by}"
        
        # 添加聚合指标
        select_clause += f",\n    COUNT(*) AS record_count,\n    "
        select_clause += f"AVG({metric_column}) AS avg_value,\n    "
        select_clause += f"MAX({metric_column}) AS max_value,\n    "
        select_clause += f"MIN({metric_column}) AS min_value,\n    "
        select_clause += f"SUM({metric_column}) AS total_value"
        
        # 构建FROM子句
        from_clause = f"FROM {table_name}"
        
        # 构建GROUP BY和ORDER BY子句
        group_by_clause = f"GROUP BY {time_format}"
        if group_by:
            group_by_clause += f", {group_by}"
        
        order_by_clause = "ORDER BY time_period"
        if group_by:
            order_by_clause += f", {group_by}"
        
        # 组合完整SQL
        sql = f"{select_clause}\n{from_clause}\n{group_by_clause}\n{order_by_clause};"
        
        return sql
    
    @staticmethod
    def generate_schema_analysis_query(table_name: str) -> str:
        """
        生成表结构分析SQL
        
        Args:
            table_name: 表名
            
        Returns:
            表结构分析SQL语句
        """
        sql = f"""-- 表基本信息分析
SELECT
    '{table_name}' AS table_name,
    COUNT(*) AS total_rows,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '{table_name}') AS column_count,
    -- 大小信息可能需要根据不同数据库系统调整
    pg_size_pretty(pg_total_relation_size('{table_name}'::regclass)) AS total_size
FROM {table_name};

-- 列数据分布分析 (需要为每列单独运行)
-- SELECT
--    column_name,
--    COUNT(*) AS total_count,
--    COUNT(DISTINCT column_name) AS distinct_count,
--    COUNT(*) - COUNT(column_name) AS null_count,
--    (COUNT(*) - COUNT(column_name))::float / COUNT(*) * 100 AS null_percentage
-- FROM {table_name}
-- GROUP BY column_name;

-- 索引信息
SELECT
    i.relname AS index_name,
    a.attname AS column_name
FROM
    pg_class t,
    pg_class i,
    pg_index ix,
    pg_attribute a
WHERE
    t.oid = ix.indrelid
    AND i.oid = ix.indexrelid
    AND a.attrelid = t.oid
    AND a.attnum = ANY(ix.indkey)
    AND t.relkind = 'r'
    AND t.relname = '{table_name}'
ORDER BY
    i.relname,
    a.attnum;
"""
        return sql
        
    @staticmethod
    def generate_pagination_query(table: str, page_size: int, page_number: int,
                                order_column: str = "id", where_clause: str = None) -> str:
        """
        生成带分页的查询SQL
        
        Args:
            table: 表名
            page_size: 每页记录数
            page_number: 页码（从1开始）
            order_column: 排序列名
            where_clause: WHERE子句条件（可选）
            
        Returns:
            分页查询SQL语句
        """
        # 计算偏移量
        offset = (page_number - 1) * page_size
        
        # 构建WHERE子句
        where_part = f"WHERE {where_clause}" if where_clause else ""
        
        # 构建完整SQL
        sql = f"""SELECT *
FROM {table}
{where_part}
ORDER BY {order_column}
LIMIT {page_size} OFFSET {offset};"""
        
        return sql
    
    @staticmethod
    def generate_duplicate_detection_query(table: str, columns: List[str]) -> str:
        """
        生成重复数据检测SQL
        
        Args:
            table: 表名
            columns: 用于检测重复的列名列表
            
        Returns:
            重复数据检测SQL语句
        """
        # 构建列名字符串
        columns_str = ", ".join(columns)
        
        # 构建完整SQL
        sql = f"""SELECT {columns_str}, COUNT(*) as duplicate_count
FROM {table}
GROUP BY {columns_str}
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC;"""
        
        return sql
    
    # 可以添加更多模板方法
