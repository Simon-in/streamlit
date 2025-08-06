# -*- coding: utf-8 -*-
"""
性能优化模块 - 提供缓存和性能优化功能
"""

import streamlit as st
import pandas as pd
import hashlib
from typing import Any, Optional
from functools import wraps


class CacheManager:
    """缓存管理器"""
    
    @staticmethod
    @st.cache_data
    def load_excel_file(file_path: str, sheet_name: str) -> Optional[pd.DataFrame]:
        """
        缓存Excel文件读取
        
        Args:
            file_path: 文件路径
            sheet_name: 工作表名称
            
        Returns:
            DataFrame或None
        """
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception:
            return None
    
    @staticmethod
    @st.cache_data
    def generate_sql_statements(file_content: bytes, operation: str) -> list:
        """
        缓存SQL语句生成
        
        Args:
            file_content: 文件内容（字节）
            operation: 操作类型
            
        Returns:
            SQL语句列表
        """
        # 这里应该调用实际的SQL生成逻辑
        # 为了演示，返回空列表
        return []
    
    @staticmethod
    def get_file_hash(file) -> str:
        """
        获取文件的MD5哈希值
        
        Args:
            file: 文件对象
            
        Returns:
            MD5哈希值
        """
        if file is None:
            return ""
        
        file.seek(0)
        content = file.read()
        file.seek(0)  # 重置文件指针
        
        return hashlib.md5(content).hexdigest()


class PerformanceOptimizer:
    """性能优化器"""
    
    @staticmethod
    def optimize_dataframe_display(df: pd.DataFrame, max_rows: int = 1000) -> pd.DataFrame:
        """
        优化DataFrame显示性能
        
        Args:
            df: 原始DataFrame
            max_rows: 最大显示行数
            
        Returns:
            优化后的DataFrame
        """
        if len(df) > max_rows:
            st.warning(f"数据量较大（{len(df)}行），仅显示前{max_rows}行以提高性能")
            return df.head(max_rows)
        return df
    
    @staticmethod
    def lazy_load_component(component_func):
        """
        延迟加载组件装饰器
        
        Args:
            component_func: 组件函数
            
        Returns:
            装饰后的函数
        """
        @wraps(component_func)
        def wrapper(*args, **kwargs):
            with st.spinner("加载中..."):
                return component_func(*args, **kwargs)
        return wrapper
    
    @staticmethod
    def memory_usage_monitor():
        """内存使用监控"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            
            if memory_mb > 500:  # 如果内存使用超过500MB
                st.warning(f"⚠️ 内存使用较高: {memory_mb:.1f} MB")
        except ImportError:
            pass  # psutil未安装时跳过


class SessionOptimizer:
    """Session状态优化器"""
    
    @staticmethod
    def cleanup_old_session_data():
        """清理过期的session数据"""
        # 清理超过一定时间的session数据
        keys_to_remove = []
        for key in st.session_state.keys():
            if key.startswith('temp_') and hasattr(st.session_state[key], 'timestamp'):
                # 如果是临时数据且超过一定时间，标记为删除
                import time
                if time.time() - st.session_state[key].timestamp > 3600:  # 1小时
                    keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key]
    
    @staticmethod
    def optimize_session_state():
        """优化session state"""
        # 限制session state的大小
        if len(st.session_state) > 50:
            st.warning("Session状态项目较多，可能影响性能")
        
        # 清理过期数据
        SessionOptimizer.cleanup_old_session_data()


# 性能监控装饰器
def performance_monitor(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            if execution_time > 2:  # 如果执行时间超过2秒
                st.info(f"⏱️ 操作完成，耗时: {execution_time:.2f}秒")
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            st.error(f"❌ 操作失败，耗时: {execution_time:.2f}秒，错误: {str(e)}")
            raise
    
    return wrapper 