# -*- coding: utf-8 -*-
"""
高级SQL功能模块 - 提供视图、索引、存储过程等高级SQL功能
"""

import pandas as pd
import streamlit as st
from typing import Optional, List, Dict, Any, Union
from utils import FileHandler, UIHelper, InputValidator
from config import EXCEL_SHEETS


class AdvancedSQLGenerator:
    """高级SQL生成器"""
    
    def __init__(self):
        pass
    
    def generate_view(self, view_name: str, select_query: str, schema: str = None) -> str:
        """
        生成CREATE VIEW语句
        
        Args:
            view_name: 视图名称
            select_query: SELECT查询语句
            schema: 模式名称
            
        Returns:
            CREATE VIEW语句
        """
        try:
            if not view_name or not select_query:
                UIHelper.show_error("视图名称和查询语句不能为空")
                return ""
            
            # 验证输入
            if not InputValidator.validate_table_name(view_name):
                UIHelper.show_error("视图名称格式不正确")
                return ""
            
            full_view_name = f"{schema}.{view_name}" if schema else view_name
            
            view_sql = f"""-- 创建视图: {view_name}
CREATE VIEW {full_view_name} AS
{select_query};"""
            
            return view_sql
            
        except Exception as e:
            UIHelper.show_error(f"生成视图语句时发生错误: {str(e)}")
            return ""
    
    def generate_index(self, table_name: str, columns: List[str], index_name: str = None, 
                      unique: bool = False, index_type: str = "BTREE") -> str:
        """
        生成CREATE INDEX语句
        
        Args:
            table_name: 表名
            columns: 列名列表
            index_name: 索引名称
            unique: 是否唯一索引
            index_type: 索引类型
            
        Returns:
            CREATE INDEX语句
        """
        try:
            if not table_name or not columns:
                UIHelper.show_error("表名和列名不能为空")
                return ""
            
            # 生成索引名称
            if not index_name:
                index_name = f"idx_{table_name}_{'_'.join(columns)}"
            
            # 构建索引语句
            unique_keyword = "UNIQUE " if unique else ""
            columns_str = ", ".join(columns)
            
            index_sql = f"""-- 创建索引: {index_name}
CREATE {unique_keyword}INDEX {index_name} 
ON {table_name} ({columns_str})
USING {index_type};"""
            
            return index_sql
            
        except Exception as e:
            UIHelper.show_error(f"生成索引语句时发生错误: {str(e)}")
            return ""
    
    def generate_stored_procedure(self, proc_name: str, parameters: List[Dict], 
                                body: str, schema: str = None) -> str:
        """
        生成存储过程
        
        Args:
            proc_name: 存储过程名称
            parameters: 参数列表 [{'name': 'param1', 'type': 'INT', 'direction': 'IN'}]
            body: 存储过程体
            schema: 模式名称
            
        Returns:
            CREATE PROCEDURE语句
        """
        try:
            if not proc_name or not body:
                UIHelper.show_error("存储过程名称和过程体不能为空")
                return ""
            
            full_proc_name = f"{schema}.{proc_name}" if schema else proc_name
            
            # 构建参数列表
            param_list = []
            if parameters:
                for param in parameters:
                    direction = param.get('direction', 'IN')
                    param_str = f"{direction} {param['name']} {param['type']}"
                    param_list.append(param_str)
            
            params_str = ",\n    ".join(param_list) if param_list else ""
            
            proc_sql = f"""-- 创建存储过程: {proc_name}
DELIMITER //
CREATE PROCEDURE {full_proc_name}(
    {params_str}
)
BEGIN
{body}
END //
DELIMITER ;"""
            
            return proc_sql
            
        except Exception as e:
            UIHelper.show_error(f"生成存储过程时发生错误: {str(e)}")
            return ""
    
    def generate_trigger(self, trigger_name: str, table_name: str, timing: str, 
                        event: str, trigger_body: str) -> str:
        """
        生成触发器
        
        Args:
            trigger_name: 触发器名称
            table_name: 表名
            timing: 触发时机 (BEFORE/AFTER)
            event: 触发事件 (INSERT/UPDATE/DELETE)
            trigger_body: 触发器体
            
        Returns:
            CREATE TRIGGER语句
        """
        try:
            if not all([trigger_name, table_name, timing, event, trigger_body]):
                UIHelper.show_error("所有字段都不能为空")
                return ""
            
            trigger_sql = f"""-- 创建触发器: {trigger_name}
DELIMITER //
CREATE TRIGGER {trigger_name}
{timing} {event} ON {table_name}
FOR EACH ROW
BEGIN
{trigger_body}
END //
DELIMITER ;"""
            
            return trigger_sql
            
        except Exception as e:
            UIHelper.show_error(f"生成触发器时发生错误: {str(e)}")
            return ""
    
    def generate_function(self, func_name: str, parameters: List[Dict], 
                         return_type: str, func_body: str, schema: str = None) -> str:
        """
        生成用户定义函数
        
        Args:
            func_name: 函数名称
            parameters: 参数列表
            return_type: 返回类型
            func_body: 函数体
            schema: 模式名称
            
        Returns:
            CREATE FUNCTION语句
        """
        try:
            if not all([func_name, return_type, func_body]):
                UIHelper.show_error("函数名称、返回类型和函数体不能为空")
                return ""
            
            full_func_name = f"{schema}.{func_name}" if schema else func_name
            
            # 构建参数列表
            param_list = []
            if parameters:
                for param in parameters:
                    param_str = f"{param['name']} {param['type']}"
                    param_list.append(param_str)
            
            params_str = ", ".join(param_list) if param_list else ""
            
            func_sql = f"""-- 创建函数: {func_name}
DELIMITER //
CREATE FUNCTION {full_func_name}({params_str})
RETURNS {return_type}
DETERMINISTIC
READS SQL DATA
BEGIN
{func_body}
END //
DELIMITER ;"""
            
            return func_sql
            
        except Exception as e:
            UIHelper.show_error(f"生成函数时发生错误: {str(e)}")
            return ""
    
    def generate_constraint(self, table_name: str, constraint_name: str, 
                          constraint_type: str, columns: List[str], 
                          reference_table: str = None, reference_columns: List[str] = None) -> str:
        """
        生成约束语句
        
        Args:
            table_name: 表名
            constraint_name: 约束名称
            constraint_type: 约束类型 (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK)
            columns: 列名列表
            reference_table: 引用表名 (外键使用)
            reference_columns: 引用列名 (外键使用)
            
        Returns:
            ALTER TABLE语句
        """
        try:
            if not all([table_name, constraint_name, constraint_type, columns]):
                UIHelper.show_error("表名、约束名称、约束类型和列名不能为空")
                return ""
            
            columns_str = ", ".join(columns)
            
            if constraint_type.upper() == "FOREIGN KEY":
                if not reference_table or not reference_columns:
                    UIHelper.show_error("外键约束需要指定引用表和引用列")
                    return ""
                ref_columns_str = ", ".join(reference_columns)
                constraint_sql = f"""-- 添加外键约束: {constraint_name}
ALTER TABLE {table_name}
ADD CONSTRAINT {constraint_name}
FOREIGN KEY ({columns_str})
REFERENCES {reference_table}({ref_columns_str});"""
            else:
                constraint_sql = f"""-- 添加约束: {constraint_name}
ALTER TABLE {table_name}
ADD CONSTRAINT {constraint_name}
{constraint_type} ({columns_str});"""
            
            return constraint_sql
            
        except Exception as e:
            UIHelper.show_error(f"生成约束语句时发生错误: {str(e)}")
            return ""


class DataAnalyzer:
    """数据分析器"""
    
    @staticmethod
    def analyze_excel_structure(uploaded_file) -> Dict[str, Any]:
        """
        分析Excel文件结构
        
        Args:
            uploaded_file: 上传的Excel文件
            
        Returns:
            分析结果字典
        """
        try:
            if uploaded_file is None:
                return {}
            
            # 读取所有工作表
            excel_file = pd.ExcelFile(uploaded_file)
            analysis_result = {
                'sheet_names': excel_file.sheet_names,
                'sheet_info': {},
                'total_sheets': len(excel_file.sheet_names),
                'file_size': len(uploaded_file.getvalue()) if hasattr(uploaded_file, 'getvalue') else 0
            }
            
            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                    analysis_result['sheet_info'][sheet_name] = {
                        'rows': len(df),
                        'columns': len(df.columns),
                        'column_names': df.columns.tolist(),
                        'data_types': df.dtypes.to_dict(),
                        'null_counts': df.isnull().sum().to_dict(),
                        'sample_data': df.head(3).to_dict('records') if len(df) > 0 else []
                    }
                except Exception as e:
                    analysis_result['sheet_info'][sheet_name] = {'error': str(e)}
            
            return analysis_result
            
        except Exception as e:
            UIHelper.show_error(f"分析文件结构时发生错误: {str(e)}")
            return {}
    
    @staticmethod
    def generate_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
        """
        生成数据摘要统计
        
        Args:
            df: DataFrame
            
        Returns:
            统计摘要
        """
        try:
            summary = {
                'basic_info': {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'memory_usage': df.memory_usage(deep=True).sum(),
                    'column_names': df.columns.tolist()
                },
                'data_types': df.dtypes.value_counts().to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'numeric_summary': {},
                'categorical_summary': {}
            }
            
            # 数值型列统计
            numeric_columns = df.select_dtypes(include=['number']).columns
            if len(numeric_columns) > 0:
                summary['numeric_summary'] = df[numeric_columns].describe().to_dict()
            
            # 分类型列统计
            categorical_columns = df.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                summary['categorical_summary'][col] = {
                    'unique_count': df[col].nunique(),
                    'top_values': df[col].value_counts().head(5).to_dict()
                }
            
            return summary
            
        except Exception as e:
            UIHelper.show_error(f"生成数据摘要时发生错误: {str(e)}")
            return {}


class SQLFormatter:
    """SQL格式化器"""
    
    @staticmethod
    def format_sql(sql_text: str, style: str = "standard") -> str:
        """
        格式化SQL语句
        
        Args:
            sql_text: 原始SQL文本
            style: 格式化风格
            
        Returns:
            格式化后的SQL
        """
        try:
            import sqlparse
            
            # 格式化选项
            format_options = {
                'standard': {
                    'reindent': True,
                    'keyword_case': 'upper',
                    'identifier_case': 'lower',
                    'strip_comments': False
                },
                'compact': {
                    'reindent': False,
                    'keyword_case': 'upper',
                    'identifier_case': 'lower',
                    'strip_comments': True
                },
                'pretty': {
                    'reindent': True,
                    'keyword_case': 'upper',
                    'identifier_case': 'lower',
                    'strip_comments': False,
                    'indent_width': 4
                }
            }
            
            options = format_options.get(style, format_options['standard'])
            formatted = sqlparse.format(sql_text, **options)
            
            return formatted
            
        except ImportError:
            # 如果没有安装sqlparse，使用简单格式化
            return SQLFormatter._simple_format(sql_text)
        except Exception as e:
            UIHelper.show_error(f"格式化SQL时发生错误: {str(e)}")
            return sql_text
    
    @staticmethod
    def _simple_format(sql_text: str) -> str:
        """简单的SQL格式化"""
        # 基本的关键词大写和缩进
        keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 
                   'RIGHT JOIN', 'GROUP BY', 'ORDER BY', 'HAVING', 'INSERT', 
                   'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
        
        formatted = sql_text
        for keyword in keywords:
            formatted = formatted.replace(keyword.lower(), keyword)
            formatted = formatted.replace(keyword.title(), keyword)
        
        return formatted
    
    @staticmethod
    def validate_sql_syntax(sql_text: str) -> Dict[str, Any]:
        """
        验证SQL语法
        
        Args:
            sql_text: SQL文本
            
        Returns:
            验证结果
        """
        try:
            import sqlparse
            
            parsed = sqlparse.parse(sql_text)
            
            result = {
                'is_valid': len(parsed) > 0,
                'statement_count': len(parsed),
                'statements': [],
                'warnings': [],
                'errors': []
            }
            
            for stmt in parsed:
                stmt_info = {
                    'type': stmt.get_type(),
                    'tokens': len(list(stmt.flatten())),
                    'text': str(stmt).strip()
                }
                result['statements'].append(stmt_info)
            
            return result
            
        except ImportError:
            return {
                'is_valid': True,
                'statement_count': 1,
                'statements': [{'type': 'UNKNOWN', 'text': sql_text}],
                'warnings': ['sqlparse未安装，无法进行详细语法验证'],
                'errors': []
            }
        except Exception as e:
            return {
                'is_valid': False,
                'statement_count': 0,
                'statements': [],
                'warnings': [],
                'errors': [str(e)]
            } 