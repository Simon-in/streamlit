# -*- coding: utf-8 -*-
"""
安全模块 - 负责文件上传和SQL注入防护
"""

import os
from typing import Dict, Optional, Any, Union, Tuple

class SecurityManager:
    """安全管理器，负责处理安全相关功能"""
    
    @staticmethod
    def validate_upload_file(file: Any, max_size_mb: int = 5) -> bool:
        """
        验证上传的文件是否安全
        
        Args:
            file: 上传的文件对象
            max_size_mb: 最大文件大小（MB）
            
        Returns:
            文件是否安全的布尔值
        """
        # 检查文件大小
        file.seek(0, os.SEEK_END)
        file_size_mb = file.tell() / (1024 * 1024)  # 转换为MB
        file.seek(0)  # 重置文件指针
        
        if file_size_mb > max_size_mb:
            return False
            
        # 文件扩展名检查在FileHandler中已完成
        
        # 未来可以添加内容扫描等更多安全检查
        
        return True
        
    @staticmethod
    def validate_sql_inputs(table_name: Optional[str] = None, columns: Optional[str] = None) -> bool:
        """
        验证SQL输入是否安全（防止SQL注入）
        
        Args:
            table_name: 表名
            columns: 列名
            
        Returns:
            输入是否安全的布尔值
        """
        # SQL注入黑名单
        blacklist = [
            'DROP', 'TRUNCATE', 'DELETE', 'UPDATE', 'ALTER', 'INSERT', 
            'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK', 'EXECUTE',
            '--', ';', '/*', '*/'
        ]
        
        # 检查表名
        if table_name:
            table_name_upper = table_name.upper()
            if any(keyword in table_name_upper for keyword in blacklist):
                return False
                
        # 检查列名
        if columns:
            columns_upper = columns.upper()
            if any(keyword in columns_upper for keyword in blacklist):
                return False
                
        return True
