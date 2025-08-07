# -*- coding: utf-8 -*-
"""
文件处理工具模块
"""

import streamlit as st
import pandas as pd
import os
from typing import Optional, List, Dict, Any
from sql_generator.config.constants import MIME_TYPES, SUPPORTED_FILE_TYPES
from sql_generator.utils.security import SecurityManager


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
