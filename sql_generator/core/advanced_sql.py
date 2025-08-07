# -*- coding: utf-8 -*-
"""
高级SQL功能模块 - 提供视图、索引、存储过程等高级SQL功能
"""

import pandas as pd
from typing import Optional, List, Dict, Any, Union
from sql_generator.utils.file_utils import FileHandler
from sql_generator.utils.ui_utils import UIHelper, InputValidator
from sql_generator.config.constants import EXCEL_SHEETS


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
            schema: 模式名（可选）
            
        Returns:
            CREATE VIEW语句
        """
        full_view_name = f"{schema}.{view_name}" if schema else view_name
        
        return f"CREATE OR REPLACE VIEW {full_view_name} AS\n{select_query};"
    
    def generate_index(self, table_name: str, columns: List[str], index_name: str, 
                       unique: bool = False, index_type: str = "BTREE") -> str:
        """
        生成CREATE INDEX语句
        
        Args:
            table_name: 表名
            columns: 列名列表
            index_name: 索引名称
            unique: 是否是唯一索引
            index_type: 索引类型，默认为BTREE
            
        Returns:
            CREATE INDEX语句
        """
        columns_str = ", ".join(columns)
        unique_str = "UNIQUE " if unique else ""
        using_str = f" USING {index_type}" if index_type else ""
        
        return f"CREATE {unique_str}INDEX {index_name} ON {table_name} ({columns_str}){using_str};"
    
    def generate_stored_procedure(self, proc_name: str, parameters: List[Dict[str, str]],
                                 body: str, schema: str = None) -> str:
        """
        生成CREATE PROCEDURE语句
        
        Args:
            proc_name: 存储过程名称
            parameters: 参数列表，每个参数是包含name、type和direction的字典
            body: 存储过程主体
            schema: 模式名（可选）
            
        Returns:
            CREATE PROCEDURE语句
        """
        full_proc_name = f"{schema}.{proc_name}" if schema else proc_name
        
        # 构建参数字符串
        params = []
        for param in parameters:
            direction = param.get("direction", "IN")
            param_str = f"{direction} {param['name']} {param['type']}"
            params.append(param_str)
        
        params_str = ", ".join(params)
        
        return f"""
CREATE PROCEDURE {full_proc_name}({params_str})
BEGIN
{body}
END;
"""

    def generate_trigger(self, trigger_name: str, table_name: str, timing: str, 
                        event: str, body: str) -> str:
        """
        生成CREATE TRIGGER语句
        
        Args:
            trigger_name: 触发器名称
            table_name: 表名
            timing: 触发时机（BEFORE或AFTER）
            event: 触发事件（INSERT、UPDATE或DELETE）
            body: 触发器主体
            
        Returns:
            CREATE TRIGGER语句
        """
        return f"""
CREATE TRIGGER {trigger_name}
{timing} {event} ON {table_name}
FOR EACH ROW
BEGIN
{body}
END;
"""

    def generate_function(self, func_name: str, parameters: List[Dict[str, str]],
                         returns: str, body: str, deterministic: bool = False,
                         schema: str = None) -> str:
        """
        生成CREATE FUNCTION语句
        
        Args:
            func_name: 函数名称
            parameters: 参数列表，每个参数是包含name和type的字典
            returns: 返回类型
            body: 函数主体
            deterministic: 是否是确定性函数
            schema: 模式名（可选）
            
        Returns:
            CREATE FUNCTION语句
        """
        full_func_name = f"{schema}.{func_name}" if schema else func_name
        
        # 构建参数字符串
        params = []
        for param in parameters:
            param_str = f"{param['name']} {param['type']}"
            params.append(param_str)
        
        params_str = ", ".join(params)
        deterministic_str = "DETERMINISTIC" if deterministic else "NOT DETERMINISTIC"
        
        return f"""
CREATE FUNCTION {full_func_name}({params_str})
RETURNS {returns}
{deterministic_str}
BEGIN
{body}
END;
"""

    def generate_constraint(self, table_name: str, constraint_name: str, constraint_type: str,
                           columns: List[str], **kwargs) -> str:
        """
        生成ALTER TABLE添加约束的语句
        
        Args:
            table_name: 表名
            constraint_name: 约束名称
            constraint_type: 约束类型（PRIMARY KEY、FOREIGN KEY、UNIQUE、CHECK）
            columns: 列名列表
            **kwargs: 其他参数，如外键引用表和列
            
        Returns:
            ALTER TABLE ADD CONSTRAINT语句
        """
        columns_str = ", ".join(columns)
        
        if constraint_type == "PRIMARY KEY":
            return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} PRIMARY KEY ({columns_str});"
        
        elif constraint_type == "FOREIGN KEY":
            ref_table = kwargs.get("ref_table")
            ref_columns = kwargs.get("ref_columns", [])
            ref_columns_str = ", ".join(ref_columns)
            
            return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({columns_str}) REFERENCES {ref_table}({ref_columns_str});"
        
        elif constraint_type == "UNIQUE":
            return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} UNIQUE ({columns_str});"
        
        elif constraint_type == "CHECK":
            condition = kwargs.get("condition", "")
            return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} CHECK ({condition});"
        
        else:
            raise ValueError(f"不支持的约束类型: {constraint_type}")
