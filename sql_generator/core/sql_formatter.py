# -*- coding: utf-8 -*-
"""
SQL格式化和验证工具 - 负责SQL语法检查、格式化和分析
"""

import re
import sqlparse
from typing import Dict, List, Any, Optional, Tuple, Union

class SQLFormatter:
    """SQL格式化和验证工具类"""
    
    @staticmethod
    def validate_sql_syntax(sql: str) -> Dict[str, Any]:
        """
        验证SQL语法是否有效
        
        Args:
            sql: 待验证的SQL语句
            
        Returns:
            包含验证结果的字典，格式为：
            {
                'is_valid': bool,  # SQL是否有效
                'errors': List[str],  # 错误列表
                'statement_count': int,  # SQL语句数量
                'statements': List[Dict],  # SQL语句列表，包含类型、文本等信息
                'warnings': List[str]  # 警告列表
            }
        """
        if not sql or not sql.strip():
            return {
                'is_valid': False,
                'errors': ["SQL语句为空"],
                'statement_count': 0,
                'statements': [],
                'warnings': []
            }
        
        # 使用sqlparse解析SQL
        try:
            parsed_statements = sqlparse.parse(sql)
            statements = []
            warnings = []
            
            # 检查基本语法
            for stmt in parsed_statements:
                stmt_type = SQLFormatter._get_statement_type(stmt)
                stmt_dict = {
                    'type': stmt_type,
                    'text': str(stmt)
                }
                statements.append(stmt_dict)
                
                # 对特定语句类型进行验证
                stmt_warnings = SQLFormatter._validate_statement(stmt, stmt_type)
                warnings.extend(stmt_warnings)
            
            # 检查是否存在严重问题
            errors = SQLFormatter._check_syntax_errors(sql)
            
            return {
                'is_valid': len(errors) == 0,
                'errors': errors,
                'statement_count': len(statements),
                'statements': statements,
                'warnings': warnings
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'errors': [f"SQL解析错误: {str(e)}"],
                'statement_count': 0,
                'statements': [],
                'warnings': []
            }
    
    @staticmethod
    def _get_statement_type(stmt: Any) -> str:
        """
        获取SQL语句类型
        
        Args:
            stmt: sqlparse解析后的语句对象
            
        Returns:
            语句类型，如SELECT, INSERT, UPDATE等
        """
        stmt_type = "UNKNOWN"
        
        # 提取第一个token的类型
        if stmt.tokens:
            first_token = None
            for token in stmt.tokens:
                if not token.is_whitespace:
                    first_token = token
                    break
            
            if first_token:
                if hasattr(first_token, 'ttype') and first_token.ttype:
                    # 直接从token获取类型
                    token_value = str(first_token).strip().upper()
                    if token_value in ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", 
                                     "DROP", "TRUNCATE", "MERGE", "WITH"]:
                        stmt_type = token_value
                        
                        # 特殊处理WITH语句（可能是CTE）
                        if stmt_type == "WITH":
                            # 寻找后续的SELECT/INSERT等
                            for token in stmt.tokens:
                                if hasattr(token, 'ttype') and token.ttype:
                                    token_value = str(token).strip().upper()
                                    if token_value in ["SELECT", "INSERT", "UPDATE", "DELETE"]:
                                        stmt_type = f"WITH {token_value}"
                                        break
                else:
                    # 尝试从字符串中识别类型
                    stmt_str = str(stmt).strip().upper()
                    for stmt_type_candidate in ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", 
                                             "ALTER", "DROP", "TRUNCATE", "MERGE", "WITH"]:
                        if stmt_str.startswith(stmt_type_candidate):
                            stmt_type = stmt_type_candidate
                            break
        
        return stmt_type
    
    @staticmethod
    def _validate_statement(stmt: Any, stmt_type: str) -> List[str]:
        """
        验证特定SQL语句
        
        Args:
            stmt: sqlparse解析后的语句对象
            stmt_type: 语句类型
            
        Returns:
            警告列表
        """
        warnings = []
        stmt_str = str(stmt).upper()
        
        # SELECT语句特有的验证
        if stmt_type == "SELECT":
            # 检查是否缺少WHERE子句（可能导致全表扫描）
            has_limit = False
            if "LIMIT" in stmt_str:
                limit_match = re.search(r"LIMIT\s+(\d+)", stmt_str)
                if limit_match and int(limit_match.group(1)) < 1000:
                    has_limit = True
            
            if "WHERE" not in stmt_str and not has_limit:
                warnings.append("SELECT语句缺少WHERE条件，可能会导致全表扫描")
            
            # 检查是否使用了SELECT *
            if "SELECT *" in stmt_str or "SELECT\n*" in stmt_str or "SELECT\t*" in stmt_str:
                warnings.append("使用了SELECT *，建议明确指定需要的列")
        
        # INSERT语句特有的验证
        elif stmt_type == "INSERT":
            # 检查是否指定了列名
            if "INSERT INTO" in stmt_str and "(" not in stmt_str:
                warnings.append("INSERT语句未显式指定列名")
        
        # UPDATE语句特有的验证
        elif stmt_type == "UPDATE":
            # 检查是否缺少WHERE子句
            if "WHERE" not in stmt_str:
                warnings.append("UPDATE语句缺少WHERE条件，将更新整个表")
        
        # DELETE语句特有的验证
        elif stmt_type == "DELETE":
            # 检查是否缺少WHERE子句
            if "WHERE" not in stmt_str:
                warnings.append("DELETE语句缺少WHERE条件，将删除整个表")
        
        return warnings
    
    @staticmethod
    def _check_syntax_errors(sql: str) -> List[str]:
        """
        检查SQL语法错误
        
        Args:
            sql: SQL语句
            
        Returns:
            错误列表
        """
        errors = []
        
        # 检查括号匹配
        if sql.count('(') != sql.count(')'):
            errors.append("括号不匹配: '(' 和 ')' 的数量不一致")
        
        # 检查引号匹配
        single_quotes = sql.count("'") - sql.count("''")  # 考虑转义的单引号
        if single_quotes % 2 != 0:
            errors.append("单引号不匹配: 单引号数量不成对")
        
        double_quotes = sql.count('"') - sql.count('""')  # 考虑转义的双引号
        if double_quotes % 2 != 0:
            errors.append("双引号不匹配: 双引号数量不成对")
        
        # 检查常见的语法错误模式
        if re.search(r"FROM\s+WHERE", sql, re.IGNORECASE):
            errors.append("FROM子句后直接接WHERE，缺少表名")
        
        if re.search(r"WHERE\s+ORDER", sql, re.IGNORECASE):
            errors.append("WHERE子句后直接接ORDER BY，缺少条件表达式")
        
        if re.search(r"SELECT\s+FROM", sql, re.IGNORECASE):
            errors.append("SELECT子句后直接接FROM，缺少列名")
        
        # 检查JOIN语法
        join_without_on = re.search(r"JOIN\s+\w+(?:\.\w+)?\s+(?!ON|USING)", sql, re.IGNORECASE)
        if join_without_on:
            errors.append("JOIN语句后缺少ON或USING子句")
        
        # 检查分号
        if ";" in sql[:-1]:  # 分号不在最后
            stmt_count = len(sqlparse.parse(sql))
            if stmt_count == 1:  # 只有一条语句但中间有分号
                errors.append("SQL语句中间有多余的分号")
        
        return errors
    
    @staticmethod
    def format_sql(sql: str, indent_width: int = 4) -> str:
        """
        格式化SQL语句
        
        Args:
            sql: 待格式化的SQL语句
            indent_width: 缩进宽度，默认为4
            
        Returns:
            格式化后的SQL语句
        """
        try:
            return sqlparse.format(
                sql,
                reindent=True,
                keyword_case='upper',
                identifier_case='lower',
                indent_width=indent_width
            )
        except Exception:
            # 如果格式化失败，返回原始SQL
            return sql
    
    @staticmethod
    def beautify_sql(sql: str) -> str:
        """
        美化SQL语句，使其更易读
        
        Args:
            sql: 原始SQL语句
            
        Returns:
            格式化后的SQL语句
        """
        try:
            # 使用sqlparse进行基本格式化
            formatted_sql = sqlparse.format(
                sql,
                reindent=True,
                keyword_case='upper',
                identifier_case='lower',
                indent_width=4,
                strip_comments=False
            )
            
            # 进一步美化处理
            lines = formatted_sql.split('\n')
            result_lines = []
            
            # 处理每一行
            for line in lines:
                # 保留原始行
                result_lines.append(line)
                
                # 在主要子句后添加空行，增加可读性
                strip_line = line.strip().upper()
                if (strip_line.startswith(('SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 
                                         'ORDER BY', 'LIMIT')) and 
                    not strip_line.endswith((',', 'AND', 'OR'))):
                    result_lines.append('')
            
            return '\n'.join(result_lines)
        except Exception:
            # 如果格式化失败，返回原始SQL
            return sql
    
    @staticmethod
    def get_formatting_suggestions(sql: str) -> List[str]:
        """
        获取SQL格式化建议
        
        Args:
            sql: SQL语句
            
        Returns:
            格式化建议列表
        """
        suggestions = []
        
        # 检查SQL是否已格式化
        if sql.count('\n') < 2:
            suggestions.append("将关键字放在单独行，提高可读性")
        
        # 检查关键字大小写
        if re.search(r'\b(select|from|where|join|and|or|group by|order by)\b', sql, re.IGNORECASE):
            if not re.search(r'\b(SELECT|FROM|WHERE|JOIN|AND|OR|GROUP BY|ORDER BY)\b', sql):
                suggestions.append("将SQL关键字大写以突出显示")
        
        # 检查是否有注释
        if not re.search(r'(--|\/*)', sql):
            suggestions.append("为复杂查询添加注释，解释其目的和逻辑")
        
        # 检查表别名
        tables = re.findall(r'\bFROM\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?', sql, re.IGNORECASE)
        has_alias = all(len(match) > 1 and match[1] for match in tables) if tables else False
        if not has_alias and len(tables) > 0:
            suggestions.append("为表添加有意义的别名，尤其是在复杂查询中")
        
        # 检查缩进
        if re.search(r'\bSELECT\b.*\bFROM\b', sql, re.IGNORECASE | re.DOTALL):
            if not re.search(r'\bSELECT\b.*\n\s+\w+', sql, re.IGNORECASE | re.DOTALL):
                suggestions.append("为列名添加适当的缩进")
        
        # 没有建议时的反馈
        if not suggestions:
            suggestions.append("SQL格式良好，无需额外建议")
        
        return suggestions

    @staticmethod
    def analyze_sql_complexity(sql: str) -> Dict[str, Any]:
        """
        分析SQL复杂度
        
        Args:
            sql: SQL语句
            
        Returns:
            复杂度分析结果字典
        """
        result = {
            'complexity_score': 0,  # 0-100分，越高越复杂
            'join_count': 0,
            'table_count': 0,
            'condition_count': 0,
            'subquery_count': 0,
            'complexity_level': 'simple',  # simple, moderate, complex
            'suggestions': []
        }
        
        # 解析SQL
        try:
            parsed = sqlparse.parse(sql)[0]
            
            # 分析各种复杂度指标
            sql_upper = sql.upper()
            
            # 计算JOIN数量
            result['join_count'] = (
                sql_upper.count(" JOIN ") + 
                sql_upper.count(" INNER JOIN ") + 
                sql_upper.count(" LEFT JOIN ") + 
                sql_upper.count(" RIGHT JOIN ") + 
                sql_upper.count(" FULL JOIN ") + 
                sql_upper.count(" CROSS JOIN ")
            )
            
            # 计算FROM子句中的表数量
            from_clause_match = re.search(r"FROM\s+(.*?)(?:WHERE|GROUP BY|HAVING|ORDER BY|LIMIT|$)", 
                                        sql_upper, re.DOTALL)
            if from_clause_match:
                from_clause = from_clause_match.group(1)
                # 计算逗号分隔的表数量（老式JOIN）
                result['table_count'] = len(re.findall(r",", from_clause)) + 1
                # 加上JOIN语法中的表数量
                result['table_count'] += result['join_count']
            
            # 计算WHERE条件数量
            where_clause_match = re.search(r"WHERE\s+(.*?)(?:GROUP BY|HAVING|ORDER BY|LIMIT|$)", 
                                        sql_upper, re.DOTALL)
            if where_clause_match:
                where_clause = where_clause_match.group(1)
                result['condition_count'] = (
                    where_clause.count(" AND ") + 
                    where_clause.count(" OR ")
                ) + 1  # +1 为基础条件
            
            # 计算子查询数量
            result['subquery_count'] = sql.count("(SELECT") + sql.count("( SELECT")
            
            # 计算复杂度得分
            result['complexity_score'] = min(100, (
                result['table_count'] * 10 +
                result['join_count'] * 15 +
                result['condition_count'] * 5 +
                result['subquery_count'] * 20
            ))
            
            # 确定复杂度级别
            if result['complexity_score'] < 30:
                result['complexity_level'] = 'simple'
            elif result['complexity_score'] < 70:
                result['complexity_level'] = 'moderate'
            else:
                result['complexity_level'] = 'complex'
            
            # 根据复杂度提供建议
            if result['complexity_score'] > 50:
                if result['join_count'] > 3:
                    result['suggestions'].append("查询包含多个JOIN，考虑拆分为更小的查询")
                if result['subquery_count'] > 2:
                    result['suggestions'].append("查询包含多个子查询，考虑使用临时表或CTE简化")
                if result['condition_count'] > 5:
                    result['suggestions'].append("WHERE条件较复杂，考虑重构或使用索引")
            
        except Exception as e:
            # 分析失败时返回基本结果
            result['error'] = str(e)
            
        return result
