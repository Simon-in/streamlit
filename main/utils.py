# -*- coding: utf-8 -*-
"""
工具模块 - 提供通用功能和辅助函数
"""

import streamlit as st
import pandas as pd
import os
from typing import Optional, List, Dict, Any
from config import MIME_TYPES, SUPPORTED_FILE_TYPES
from security import SecurityManager


class FileHandler:
    """文件处理类"""
    
    @staticmethod
    def validate_file_type(file, allowed_types: List[str] = None) -> bool:
        """验证文件类型（包含安全验证）"""
        if file is None:
            return False
        
        # 基本类型验证
        if allowed_types is None:
            allowed_types = SUPPORTED_FILE_TYPES
            
        file_extension = file.name.split('.')[-1].lower()
        basic_validation = file_extension in allowed_types
        
        if not basic_validation:
            return False
        
        # 安全验证
        return SecurityManager.validate_upload_file(file)
    
    @staticmethod
    def read_excel_safely(file_path: str, sheet_name: str) -> Optional[pd.DataFrame]:
        """安全读取Excel文件"""
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        except FileNotFoundError:
            st.error(f"文件未找到: {file_path}")
            return None
        except ValueError as e:
            st.error(f"工作表 '{sheet_name}' 不存在: {e}")
            return None
        except Exception as e:
            st.error(f"读取文件时发生错误: {e}")
            return None
    
    @staticmethod
    def create_download_button(button_name: str, file_path: str, file_type: str) -> bool:
        """创建下载按钮"""
        if not os.path.exists(file_path):
            st.error(f"文件不存在: {file_path}")
            return False
        
        try:
            with open(file_path, "rb") as file:
                file_bytes = file.read()
            
            mime_type = MIME_TYPES.get(file_type, "text/plain")
            
            if mime_type == "text/plain":
                st.warning(f"不支持的文件类型: {file_type}")
                return False
            
            st.download_button(
                label=button_name,
                data=file_bytes,
                file_name=os.path.basename(file_path),
                mime=mime_type
            )
            return True
            
        except Exception as e:
            st.error(f"创建下载按钮时发生错误: {e}")
            return False


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
        return SecurityManager.validate_sql_inputs(table_name=table_name.strip())
    
    @staticmethod
    def validate_column_list(column_list: str) -> bool:
        """验证列名列表（包含安全验证）"""
        if not column_list or not column_list.strip():
            return False
        
        # 使用安全验证器
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
        st.divider()
    
    @staticmethod
    def display_sql_with_download(sql_content: str, filename: str, title: str = "生成的SQL语句"):
        """显示SQL内容并提供下载按钮"""
        st.subheader(title)
        st.code(sql_content, language='sql')
        
        st.download_button(
            label="📥 下载SQL文件",
            data=sql_content,
            file_name=filename,
            mime=MIME_TYPES['sql'],
            type="primary"
        ) 