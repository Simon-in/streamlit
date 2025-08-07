# -*- coding: utf-8 -*-
"""
UI工具模块
"""

import streamlit as st
from typing import Optional, Any
from sql_generator.config.constants import MIME_TYPES


class SessionStateManager:
    """Session State管理类"""
    
    @staticmethod
    def init_session_state():
        """初始化session state"""
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = None
        if 'current_page' not in st.session_state:
            st.session_state.current_page = None
        if 'current_sub_page' not in st.session_state:
            st.session_state.current_sub_page = None
    
    @staticmethod
    def get_uploaded_file():
        """获取上传的文件"""
        return st.session_state.get('uploaded_file', None)
    
    @staticmethod
    def set_uploaded_file(file):
        """设置上传的文件"""
        st.session_state.uploaded_file = file


class InputValidator:
    """输入验证类"""
    
    @staticmethod
    def validate_table_name(table_name: str) -> bool:
        """验证表名（包含安全验证）"""
        if not table_name or not table_name.strip():
            return False
        
        # 使用安全验证器
        from sql_generator.utils.security import SecurityManager
        return SecurityManager.validate_sql_inputs(table_name=table_name.strip())
    
    @staticmethod
    def validate_column_list(column_list: str) -> bool:
        """验证列名列表（包含安全验证）"""
        if not column_list or not column_list.strip():
            return False
        
        # 使用安全验证器
        from sql_generator.utils.security import SecurityManager
        return SecurityManager.validate_sql_inputs(columns=column_list.strip())


class UIHelper:
    """UI辅助类"""
    
    @staticmethod
    def show_error(message: str):
        """显示错误消息"""
        st.error(f"❌ {message}")
    
    @staticmethod
    def show_success(message: str):
        """显示成功消息"""
        st.success(f"✅ {message}")
    
    @staticmethod
    def show_warning(message: str):
        """显示警告消息"""
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def show_info(message: str):
        """显示信息消息"""
        st.info(f"ℹ️ {message}")
    
    @staticmethod
    def create_section_header(title: str, description: str = None):
        """创建节标题"""
        st.header(title)
        if description:
            st.markdown(f"*{description}*")
        st.markdown("---")  # 使用markdown横线替代st.divider()
    
    @staticmethod
    def display_sql_with_download(sql_content: str, filename: str, title: str = "生成的SQL语句"):
        """显示SQL内容并提供下载按钮"""
        st.subheader(title)
        st.code(sql_content, language='sql')
        
        st.download_button(
            label="📥 下载SQL文件",
            data=sql_content,
            file_name=filename,
            mime=MIME_TYPES['sql']
        )
