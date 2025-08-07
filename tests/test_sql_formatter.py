#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试SQL格式化功能
"""

import unittest
from sql_generator.core.sql_formatter import SQLFormatter


class TestSQLFormatter(unittest.TestCase):
    """SQL格式化测试类"""
    
    def test_validate_sql_syntax_valid(self):
        """测试有效SQL的语法验证"""
        sql = "SELECT id, name FROM users WHERE age > 18;"
        result = SQLFormatter.validate_sql_syntax(sql)
        
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['statement_count'], 1)
        self.assertEqual(len(result['errors']), 0)
        
    def test_validate_sql_syntax_invalid(self):
        """测试无效SQL的语法验证"""
        sql = "SELECT FROM users WHERE;"
        result = SQLFormatter.validate_sql_syntax(sql)
        
        self.assertFalse(result['is_valid'])
        self.assertTrue(len(result['errors']) > 0)
    
    def test_format_sql(self):
        """测试SQL格式化"""
        sql = "select id,name from users where age>18"
        formatted = SQLFormatter.format_sql(sql)
        
        # 检查关键字是否已大写
        self.assertIn("SELECT", formatted)
        self.assertIn("FROM", formatted)
        self.assertIn("WHERE", formatted)
        
        # 检查是否包含换行
        self.assertGreater(formatted.count('\n'), 0)
    
    def test_get_formatting_suggestions(self):
        """测试SQL格式化建议"""
        sql = "select * from users"
        suggestions = SQLFormatter.get_formatting_suggestions(sql)
        
        # 至少应该有一个建议（关键字大写）
        self.assertGreater(len(suggestions), 0)


if __name__ == "__main__":
    unittest.main()
