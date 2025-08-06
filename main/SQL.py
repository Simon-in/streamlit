# -*- coding: utf-8 -*-
"""
SQL生成器 - 负责生成各种SQL语句
"""

import pandas as pd
import streamlit as st
from typing import Optional, List, Union, Dict, Any
from utils import FileHandler, UIHelper
from config import EXCEL_SHEETS, MIME_TYPES


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

    def bulk_insert(self, uploaded_file: Optional[Any] = None) -> List[str]:
        """
        生成INSERT语句
        
        Args:
            uploaded_file: 上传的文件
            
        Returns:
            INSERT语句列表
        """
        try:
            if uploaded_file is None:
                UIHelper.show_error("请上传包含INSERT配置的文件")
                return []
                
            df = FileHandler.read_excel_safely(uploaded_file, EXCEL_SHEETS['insert'])
            if df is None:
                return []
                
            ist_list = [
                f"INSERT INTO {row[0]} ({row[1]}) VALUES ({row[2]});"
                for row in df.itertuples(index=False)
            ]
            return ist_list
        except Exception as e:
            UIHelper.show_error(f"生成INSERT语句时发生错误: {str(e)}")
            return []

    def bulk_delete(self, uploaded_file: Optional[Any] = None, target_table: Optional[str] = None, 
                   column: Optional[str] = None, uniqueid: Optional[str] = None, 
                   source_table: Optional[str] = None) -> Union[str, List[str]]:
        """
        生成DELETE语句
        
        Args:
            uploaded_file: 上传的文件
            target_table: 目标表名
            column: 列名
            uniqueid: 唯一标识字段
            source_table: 源表名
            
        Returns:
            DELETE语句或语句列表
        """
        try:
            if uploaded_file is None and all([target_table, column, uniqueid, source_table]):
                # 单表模式
                del_statement = (
                    f"DELETE FROM {target_table} \n"
                    f"WHERE {uniqueid} IN (\n"
                    f"    SELECT {uniqueid} FROM {source_table}\n"
                    f"); \n"
                    f"INSERT INTO {target_table} ({column}) \n"
                    f"SELECT {column} \n"
                    f"FROM {source_table};"
                )
                return del_statement
            elif uploaded_file is not None:
                # 批量模式
                df = FileHandler.read_excel_safely(uploaded_file, EXCEL_SHEETS['delete'])
                if df is None:
                    return []
                    
                del_list = []
                for index, row in df.iterrows():
                    target_domain = row[0]
                    target_table = row[1]
                    fields = row[2].split(',')
                    increment_field = row[3]
                    source_table = row[4]
                    
                    delete_statement = (
                        f"--------- {target_table} --------- \n"
                        f"DELETE FROM {target_domain}.{target_table} \n"
                        f"WHERE {increment_field} IN (\n"
                        f"    SELECT {increment_field} FROM {source_table}\n"
                        f");"
                    )
                    
                    formatted_fields = ',\n    '.join(fields)
                    insert_statement = (
                        f"INSERT INTO {target_domain}.{target_table} (\n"
                        f"    {formatted_fields}\n"
                        f")\n"
                        f"SELECT \n"
                        f"    {formatted_fields}\n"
                        f"FROM {target_domain}.{source_table};"
                    )
                    
                    del_list.extend([delete_statement, insert_statement])
                return del_list
            else:
                UIHelper.show_error("请提供完整的参数或上传配置文件")
                return []
        except Exception as e:
            UIHelper.show_error(f"生成DELETE语句时发生错误: {str(e)}")
            return []

    def bulk_truncate(self, uploaded_file: Optional[Any] = None, mode: Optional[str] = None, 
                     table_name: Optional[str] = None) -> List[str]:
        """
        生成TRUNCATE语句
        
        Args:
            uploaded_file: 上传的文件
            mode: 模式 ('simple' 或 'with_insert')
            table_name: 表名（单表模式使用）
            
        Returns:
            TRUNCATE语句列表
        """
        try:
            if table_name and not uploaded_file:
                # 单表模式
                if not InputValidator.validate_table_name(table_name):
                    UIHelper.show_error("表名格式不正确")
                    return []
                return [f"TRUNCATE TABLE {table_name};"]
                
            elif uploaded_file is not None:
                df = FileHandler.read_excel_safely(uploaded_file, EXCEL_SHEETS['truncate'])
                if df is None:
                    return []
                
                trunk_list = []
                
                if mode == 'simple':
                    # 简单TRUNCATE模式
                    for index, row in df.iterrows():
                        table = row[0]
                        truncate_statement = f"TRUNCATE TABLE {table};"
                        trunk_list.append(truncate_statement)
                        
                elif mode == 'with_insert':
                    # TRUNCATE + INSERT模式
                    for index, row in df.iterrows():
                        target_table = row[0]
                        target_column = row[1].split(',')
                        source_table = row[2]
                        
                        # 生成 TRUNCATE 语句
                        truncate_statement = (
                            f"--------- {target_table} --------- \n"
                            f"TRUNCATE TABLE {target_table};"
                        )
                        
                        # 生成 INSERT 语句
                        formatted_fields = ',\n    '.join(target_column)
                        insert_statement = (
                            f"INSERT INTO {target_table} (\n"
                            f"    {formatted_fields}\n"
                            f")\n"
                            f"SELECT\n"
                            f"    {formatted_fields}\n"
                            f"FROM {source_table};"
                        )
                        
                        trunk_list.extend([truncate_statement, insert_statement])
                        
                return trunk_list
            else:
                UIHelper.show_error("请提供表名或上传配置文件")
                return []
                
        except Exception as e:
            UIHelper.show_error(f"生成TRUNCATE语句时发生错误: {str(e)}")
            return []

    def bulk_merge(self, uploaded_file: Optional[Any] = None) -> List[str]:
        """
        生成MERGE语句
        
        Args:
            uploaded_file: 上传的文件
            
        Returns:
            MERGE语句列表
        """
        try:
            if uploaded_file is None:
                UIHelper.show_error("请上传包含MERGE配置的文件")
                return []
                
            df = FileHandler.read_excel_safely(uploaded_file, EXCEL_SHEETS['merge'])
            if df is None:
                return []
                
            merge_list = []
            for index, row in df.iterrows():
                target_table = row[0]
                target_column = row[1].split(',')
                uniqueid = row[2]
                source_table = row[3]
                source_column = row[4].split(',')
                
                # 格式化字段
                formatted_fields_target = ',\n    '.join([col.strip() for col in target_column])
                formatted_fields_source = ',\n    '.join([f"SOURCE.{col.strip()}" for col in source_column])
                
                # 生成UPDATE SET子句
                update_set = ',\n    '.join(
                    [f"{target_column[i].strip()} = SOURCE.{source_column[i].strip()}" 
                     for i in range(len(target_column))]
                )
                
                # 处理表名，提取schema和表名
                table_parts = target_table.split('.')
                table_alias = table_parts[-1] if len(table_parts) > 1 else target_table
                
                merge_statement = (
                    f"--------- {target_table} --------- \n"
                    f"MERGE INTO {target_table} \n"
                    f"USING {source_table} AS SOURCE \n"
                    f"ON {table_alias}.{uniqueid} = SOURCE.{uniqueid} \n"
                    f"WHEN MATCHED THEN \n"
                    f"    UPDATE SET \n"
                    f"        {update_set} \n"
                    f"WHEN NOT MATCHED THEN \n"
                    f"    INSERT (\n"
                    f"        {formatted_fields_target}\n"
                    f"    ) \n"
                    f"    VALUES (\n"
                    f"        {formatted_fields_source}\n"
                    f"    );"
                )
                merge_list.append(merge_statement)
            return merge_list
            
        except Exception as e:
            UIHelper.show_error(f"生成MERGE语句时发生错误: {str(e)}")
            return []



    def bulk_create(self, uploaded_file: Optional[Any] = None) -> List[str]:
        """
        生成CREATE TABLE语句
        
        Args:
            uploaded_file: 上传的文件
            
        Returns:
            CREATE TABLE语句列表
        """
        try:
            if uploaded_file is None:
                UIHelper.show_error("请上传包含CREATE配置的文件")
                return []
                
            df = FileHandler.read_excel_safely(uploaded_file, EXCEL_SHEETS['create'])
            if df is None:
                return []
                
            create_statements = {}
            domain = None
            
            for _, row in df.iterrows():
                domain = row[0]
                table = row[1]
                column = row[2]
                data_type = row[3]
                
                if table not in create_statements:
                    create_statements[table] = {'domain': domain, 'columns': []}
                create_statements[table]['columns'].append(f"{column} {data_type}")
            
            sql_statements = []
            for table, info in create_statements.items():
                sql_statements.append(f"--------- {table} --------- ")
                columns_str = ",\n    ".join(info['columns'])
                sql_statements.append(f"CREATE TABLE {info['domain']}.{table} (\n    {columns_str}\n);")
                
            return sql_statements
        except Exception as e:
            UIHelper.show_error(f"生成CREATE语句时发生错误: {str(e)}")
            return []

    def bulk_update(self):
        pass

    def sql_formatted(self, sql_list):
        cleaned_statements = [stmt.strip() for stmt in sql_list if stmt.strip()]
        statement = "\n".join(cleaned_statements)
        return statement
