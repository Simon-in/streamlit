# -*- coding: utf-8 -*-
"""
SQL生成器 - 负责生成各种SQL语句
"""

import pandas as pd
import streamlit as st
import re
import sqlparse
from typing import Optional, List, Union, Dict, Any
from sql_generator.utils.file_utils import FileHandler
from sql_generator.utils.ui_utils import UIHelper
from sql_generator.config.constants import EXCEL_SHEETS, MIME_TYPES


class SQLGenerator:
    """SQL语句生成器类"""
    
    def __init__(self, path: Optional[str] = None):
        """
        初始化SQL生成器
        
        Args:
            path: Excel文件路径，可选
        """
        self.path = path

    def bulk_select(self, uploaded_file: Optional[Any] = None, table: Optional[str] = None, 
                   column: Optional[Union[str, List[str]]] = None) -> Union[str, List[str]]:
        """
        生成SELECT语句
        
        Args:
            uploaded_file: 上传的文件
            table: 表名
            column: 列名或列名列表
            
        Returns:
            SELECT语句或语句列表
        """
        try:
            if uploaded_file is None and table and column:
                # 单表模式
                if isinstance(column, list):
                    column_str = ', '.join(column)
                else:
                    column_str = column
                select_statement = f"SELECT {column_str} FROM {table};"
                return select_statement
            elif uploaded_file is not None:
                # 批量模式
                df = FileHandler.read_excel_safely(uploaded_file, EXCEL_SHEETS['select'])
                if df is None:
                    return []
                    
                se_list = []
                for index, row in df.iterrows():
                    target_table = row[0]
                    fields = row[1]
                    select_statements = f"SELECT {fields} FROM {target_table};"
                    se_list.append(select_statements)
                return se_list
            else:
                UIHelper.show_error("请提供表名和列名，或上传包含SELECT配置的文件")
                return []
        except Exception as e:
            UIHelper.show_error(f"生成SELECT语句时发生错误: {str(e)}")
            return []
            
    def bulk_create(self, uploaded_file: Optional[Any] = None) -> Union[str, List[str]]:
        """
        生成CREATE TABLE语句
        
        Args:
            uploaded_file: 上传的文件
            
        Returns:
            CREATE语句或语句列表
        """
        try:
            if uploaded_file is not None:
                # 批量模式
                df = FileHandler.read_excel_safely(uploaded_file, EXCEL_SHEETS['create'])
                if df is None:
                    return []
                
                create_list = []
                # 检查必要的列是否存在
                if '表名' in df.columns:
                    table_col = '表名'
                elif df.columns[0].lower() in ['table', 'table_name', 'tablename']:
                    table_col = df.columns[0]
                else:
                    # 假设第一列为表名
                    table_col = df.columns[0]
                    
                for index, row in df.iterrows():
                    table_name = row[table_col]
                    if not pd.notna(table_name) or not table_name:
                        continue
                    
                    columns = []
                    # 跳过表名列，处理其他列
                    for col_name in df.columns:
                        if col_name == table_col:
                            continue
                        
                        col_def = row[col_name]
                        if pd.notna(col_def) and col_def:
                            columns.append(f"    {col_name} {col_def}")
                    
                    if columns:
                        create_statement = f"CREATE TABLE {table_name} (\n"
                        create_statement += ",\n".join(columns)
                        create_statement += "\n);"
                        create_list.append(create_statement)
                
                return create_list
            else:
                UIHelper.show_error("请上传包含CREATE配置的文件")
                return []
        except Exception as e:
            UIHelper.show_error(f"生成CREATE语句时发生错误: {str(e)}")
            return []
            
    def sql_formatted(self, sql_list: List[str]) -> str:
        """
        格式化SQL语句列表为一个字符串
        
        Args:
            sql_list: SQL语句列表
            
        Returns:
            格式化后的SQL字符串
        """
        if not sql_list:
            return ""
            
        try:
            # 使用sqlparse格式化每条SQL语句
            formatted_sqls = []
            for sql in sql_list:
                # 格式化SQL语句
                formatted_sql = sqlparse.format(
                    sql,
                    reindent=True,
                    keyword_case='upper'
                )
                formatted_sqls.append(formatted_sql)
                
            # 合并所有SQL语句，每条语句间加空行
            return "\n\n".join(formatted_sqls)
        except Exception as e:
            UIHelper.show_error(f"格式化SQL语句时发生错误: {str(e)}")
            return "\n\n".join(sql_list)  # 如果格式化失败，则返回原始SQL列表
            
    def bulk_insert(self, uploaded_file: Optional[Any] = None) -> List[str]:
        """
        根据上传的Excel文件生成INSERT语句
        
        Args:
            uploaded_file: 上传的Excel文件
            
        Returns:
            INSERT语句列表
        """
        try:
            if uploaded_file is None:
                UIHelper.show_error("请上传包含INSERT配置的文件")
                return []
                
            # 读取Excel文件
            df = FileHandler.read_excel_safely(uploaded_file, EXCEL_SHEETS['insert'])
            if df is None:
                return []
                
            insert_list = []
            for index, row in df.iterrows():
                # 假设Excel中的格式为：表名, 列名(逗号分隔), 值(逗号分隔)
                if len(row) >= 3 and pd.notna(row[0]) and pd.notna(row[1]) and pd.notna(row[2]):
                    table_name = row[0]
                    columns = row[1].split(',')
                    values = row[2].split(',')
                    
                    # 确保列名和值的数量一致
                    if len(columns) == len(values):
                        # 格式化列名和值
                        formatted_columns = ", ".join(col.strip() for col in columns)
                        formatted_values = ", ".join(f"'{val.strip()}'" for val in values)
                        
                        # 生成INSERT语句
                        insert_statement = f"INSERT INTO {table_name} ({formatted_columns}) VALUES ({formatted_values});"
                        insert_list.append(insert_statement)
                    else:
                        UIHelper.show_error(f"第 {index+1} 行的列名和值数量不匹配")
                        
            return insert_list
        except Exception as e:
            UIHelper.show_error(f"生成INSERT语句时发生错误: {str(e)}")
            return []
