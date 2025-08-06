# -*- coding: utf-8 -*-
"""
安全模块 - 提供文件验证和SQL注入防护功能
"""

import re
import os
from typing import List, Optional, Any
import streamlit as st
from utils import UIHelper

# 尝试导入python-magic，如果失败则使用基础验证
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False


class FileSecurityValidator:
    """文件安全验证器"""
    
    # 允许的文件扩展名
    ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.csv', '.txt'}
    
    # 允许的MIME类型
    ALLOWED_MIME_TYPES = {
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # xlsx
        'application/vnd.ms-excel',  # xls
        'text/csv',  # csv
        'text/plain',  # txt
        'application/csv'  # csv alternative
    }
    
    # 最大文件大小 (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @classmethod
    def validate_file_extension(cls, filename: str) -> bool:
        """
        验证文件扩展名
        
        Args:
            filename: 文件名
            
        Returns:
            是否为允许的扩展名
        """
        if not filename:
            return False
        
        ext = os.path.splitext(filename.lower())[1]
        return ext in cls.ALLOWED_EXTENSIONS
    
    @classmethod
    def validate_file_size(cls, file) -> bool:
        """
        验证文件大小
        
        Args:
            file: 文件对象
            
        Returns:
            文件大小是否在允许范围内
        """
        if not file:
            return False
        
        file.seek(0, 2)  # 移动到文件末尾
        size = file.tell()
        file.seek(0)  # 重置到开头
        
        return size <= cls.MAX_FILE_SIZE
    
    @classmethod
    def validate_file_content(cls, file) -> bool:
        """
        验证文件内容类型
        
        Args:
            file: 文件对象
            
        Returns:
            文件内容是否安全
        """
        try:
            # 检查文件是否为空
            file.seek(0)
            content = file.read(1024)  # 读取前1KB
            file.seek(0)  # 重置
            
            if not content:
                return False
            
            # 检查是否包含恶意内容（简单检查）
            malicious_patterns = [
                b'<script',
                b'javascript:',
                b'vbscript:',
                b'onload=',
                b'onerror='
            ]
            
            content_lower = content.lower()
            for pattern in malicious_patterns:
                if pattern in content_lower:
                    return False
            
            return True
            
        except Exception:
            return False
    
    @classmethod
    def comprehensive_file_validation(cls, file) -> tuple[bool, str]:
        """
        综合文件验证
        
        Args:
            file: 文件对象
            
        Returns:
            (是否通过验证, 错误信息)
        """
        if not file:
            return False, "文件不存在"
        
        # 验证文件扩展名
        if not cls.validate_file_extension(file.name):
            return False, f"不支持的文件类型。支持的格式: {', '.join(cls.ALLOWED_EXTENSIONS)}"
        
        # 验证文件大小
        if not cls.validate_file_size(file):
            max_size_mb = cls.MAX_FILE_SIZE / (1024 * 1024)
            return False, f"文件过大。最大允许大小: {max_size_mb}MB"
        
        # 验证文件内容
        if not cls.validate_file_content(file):
            return False, "文件内容不安全或已损坏"
        
        return True, "文件验证通过"


class SQLSecurityValidator:
    """SQL安全验证器"""
    
    # 危险的SQL关键词
    DANGEROUS_KEYWORDS = {
        'drop', 'delete', 'truncate', 'alter', 'create', 'grant', 'revoke',
        'exec', 'execute', 'sp_', 'xp_', 'union', 'script', 'declare',
        'cursor', 'shutdown', 'backup', 'restore'
    }
    
    # SQL注入模式
    INJECTION_PATTERNS = [
        r"(\b(or|and)\b\s+\d+\s*=\s*\d+)",  # or 1=1, and 1=1
        r"(\b(or|and)\b\s+['\"]\w+['\"]\s*=\s*['\"]\w+['\"])",  # or 'a'='a'
        r"(;\s*(drop|delete|truncate|alter|create|grant|revoke))",  # ; drop table
        r"(union\s+select)",  # union select
        r"(script\s*>)",  # script>
        r"(javascript\s*:)",  # javascript:
        r"(<\s*script)",  # <script
    ]
    
    @classmethod
    def validate_table_name(cls, table_name: str) -> bool:
        """
        验证表名安全性
        
        Args:
            table_name: 表名
            
        Returns:
            表名是否安全
        """
        if not table_name or not table_name.strip():
            return False
        
        # 基本格式检查
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)?$'
        if not re.match(pattern, table_name.strip()):
            return False
        
        # 检查危险关键词
        table_lower = table_name.lower()
        for keyword in cls.DANGEROUS_KEYWORDS:
            if keyword in table_lower:
                return False
        
        return True
    
    @classmethod
    def validate_column_names(cls, column_names: str) -> bool:
        """
        验证列名安全性
        
        Args:
            column_names: 列名字符串（逗号分隔）
            
        Returns:
            列名是否安全
        """
        if not column_names or not column_names.strip():
            return False
        
        columns = [col.strip() for col in column_names.split(',')]
        
        for column in columns:
            if not column:
                continue
            
            # 基本格式检查
            pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
            if not re.match(pattern, column):
                return False
            
            # 检查危险关键词
            column_lower = column.lower()
            for keyword in cls.DANGEROUS_KEYWORDS:
                if keyword in column_lower:
                    return False
        
        return True
    
    @classmethod
    def detect_sql_injection(cls, input_string: str) -> bool:
        """
        检测SQL注入攻击
        
        Args:
            input_string: 输入字符串
            
        Returns:
            是否检测到SQL注入
        """
        if not input_string:
            return False
        
        input_lower = input_string.lower()
        
        # 检查注入模式
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, input_lower, re.IGNORECASE):
                return True
        
        return False
    
    @classmethod
    def sanitize_input(cls, input_string: str) -> str:
        """
        清理输入字符串
        
        Args:
            input_string: 输入字符串
            
        Returns:
            清理后的字符串
        """
        if not input_string:
            return ""
        
        # 移除危险字符
        sanitized = re.sub(r'[<>"\';\\]', '', input_string)
        
        # 限制长度
        if len(sanitized) > 100:
            sanitized = sanitized[:100]
        
        return sanitized.strip()


class SecurityManager:
    """安全管理器"""
    
    @staticmethod
    def validate_upload_file(file) -> bool:
        """
        验证上传文件
        
        Args:
            file: 上传的文件
            
        Returns:
            是否通过验证
        """
        is_valid, message = FileSecurityValidator.comprehensive_file_validation(file)
        
        if not is_valid:
            UIHelper.show_error(f"文件验证失败: {message}")
            return False
        
        UIHelper.show_success("文件验证通过")
        return True
    
    @staticmethod
    def validate_sql_inputs(table_name: str = None, columns: str = None, 
                          where_clause: str = None) -> bool:
        """
        验证SQL输入参数
        
        Args:
            table_name: 表名
            columns: 列名
            where_clause: WHERE子句
            
        Returns:
            是否通过验证
        """
        if table_name:
            if not SQLSecurityValidator.validate_table_name(table_name):
                UIHelper.show_error("表名格式不正确或包含危险字符")
                return False
            
            if SQLSecurityValidator.detect_sql_injection(table_name):
                UIHelper.show_error("检测到潜在的SQL注入攻击")
                return False
        
        if columns:
            if not SQLSecurityValidator.validate_column_names(columns):
                UIHelper.show_error("列名格式不正确或包含危险字符")
                return False
            
            if SQLSecurityValidator.detect_sql_injection(columns):
                UIHelper.show_error("检测到潜在的SQL注入攻击")
                return False
        
        if where_clause:
            if SQLSecurityValidator.detect_sql_injection(where_clause):
                UIHelper.show_error("WHERE子句包含潜在的SQL注入攻击")
                return False
        
        return True
    
    @staticmethod
    def log_security_event(event_type: str, details: str):
        """
        记录安全事件
        
        Args:
            event_type: 事件类型
            details: 事件详情
        """
        # 在实际应用中，这里应该记录到日志文件或安全系统
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        
        # 简单的控制台输出（生产环境中应该使用专业的日志系统）
        print(f"[SECURITY] {timestamp} - {event_type}: {details}")
        
        # 如果是严重的安全事件，可以发送警报
        if event_type in ['SQL_INJECTION_DETECTED', 'MALICIOUS_FILE_UPLOAD']:
            st.error(f"🚨 安全警告: {event_type}") 