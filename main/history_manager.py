# -*- coding: utf-8 -*-
"""
历史记录管理模块 - 管理用户的SQL生成历史和操作记录
"""

import json
import streamlit as st
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from utils import UIHelper


class HistoryManager:
    """历史记录管理器"""
    
    def __init__(self, json_path: str = "data/sql_history.json"):
        self.json_path = json_path
        self._init_storage()
    
    def _init_storage(self):
        """初始化存储"""
        try:
            # 确保数据目录存在
            Path(self.json_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 如果文件不存在，创建空的JSON文件
            if not Path(self.json_path).exists():
                self._save_data({
                    'history': [],
                    'favorites': [],
                    'stats': {}
                })
            
        except Exception as e:
            UIHelper.show_error(f"初始化存储失败: {str(e)}")
    
    def _load_data(self) -> Dict[str, Any]:
        """加载数据"""
        try:
            if Path(self.json_path).exists():
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {'history': [], 'favorites': [], 'stats': {}}
        except Exception as e:
            UIHelper.show_error(f"加载数据失败: {str(e)}")
            return {'history': [], 'favorites': [], 'stats': {}}
    
    def _save_data(self, data: Dict[str, Any]):
        """保存数据"""
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            UIHelper.show_error(f"保存数据失败: {str(e)}")
    
    def add_history_record(self, operation_type: str, sql_content: str, 
                          file_name: str = None, parameters: Dict = None,
                          user_notes: str = None, tags: List[str] = None) -> int:
        """
        添加历史记录
        
        Args:
            operation_type: 操作类型
            sql_content: SQL内容
            file_name: 文件名
            parameters: 参数字典
            user_notes: 用户备注
            tags: 标签列表
            
        Returns:
            记录ID
        """
        try:
            data = self._load_data()
            
            # 获取session ID
            session_id = self._get_session_id()
            
            # 生成记录ID
            record_id = len(data['history']) + 1
            
            # 创建记录
            record = {
                'id': record_id,
                'operation_type': operation_type,
                'sql_content': sql_content,
                'file_name': file_name,
                'parameters': parameters,
                'created_at': datetime.now().isoformat(),
                'session_id': session_id,
                'user_notes': user_notes,
                'tags': tags,
                'favorite': False
            }
            
            data['history'].append(record)
            
            # 更新统计信息
            self._update_usage_stats(data, operation_type)
            
            # 保存数据
            self._save_data(data)
            
            return record_id
            
        except Exception as e:
            UIHelper.show_error(f"添加历史记录失败: {str(e)}")
            return -1
    
    def get_history_records(self, limit: int = 50, operation_type: str = None,
                           start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        获取历史记录
        
        Args:
            limit: 限制条数
            operation_type: 操作类型过滤
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            历史记录列表
        """
        try:
            data = self._load_data()
            records = data['history']
            
            # 过滤记录
            filtered_records = []
            for record in records:
                # 操作类型过滤
                if operation_type and record['operation_type'] != operation_type:
                    continue
                
                # 日期过滤
                if start_date or end_date:
                    record_date = record['created_at'][:10]  # 取日期部分
                    if start_date and record_date < start_date:
                        continue
                    if end_date and record_date > end_date:
                        continue
                
                filtered_records.append(record)
            
            # 按时间倒序排序并限制条数
            filtered_records.sort(key=lambda x: x['created_at'], reverse=True)
            return filtered_records[:limit]
            
        except Exception as e:
            UIHelper.show_error(f"获取历史记录失败: {str(e)}")
            return []
    
    def search_history(self, keyword: str, search_in: List[str] = None) -> List[Dict]:
        """
        搜索历史记录
        
        Args:
            keyword: 搜索关键词
            search_in: 搜索范围 ['sql_content', 'user_notes', 'tags']
            
        Returns:
            搜索结果列表
        """
        try:
            if not search_in:
                search_in = ['sql_content', 'user_notes']
            
            data = self._load_data()
            records = data['history']
            
            # 搜索记录
            search_results = []
            for record in records:
                for field in search_in:
                    if field in record and record[field]:
                        if isinstance(record[field], str) and keyword.lower() in record[field].lower():
                            search_results.append(record)
                            break
                        elif isinstance(record[field], list) and any(keyword.lower() in str(item).lower() for item in record[field]):
                            search_results.append(record)
                            break
            
            # 按时间倒序排序
            search_results.sort(key=lambda x: x['created_at'], reverse=True)
            return search_results[:100]  # 限制搜索结果
            
        except Exception as e:
            UIHelper.show_error(f"搜索历史记录失败: {str(e)}")
            return []
    
    def update_record_notes(self, record_id: int, notes: str, tags: List[str] = None) -> bool:
        """
        更新记录备注和标签
        
        Args:
            record_id: 记录ID
            notes: 备注
            tags: 标签列表
            
        Returns:
            是否成功
        """
        try:
            data = self._load_data()
            
            # 查找并更新记录
            for record in data['history']:
                if record['id'] == record_id:
                    record['user_notes'] = notes
                    record['tags'] = tags
                    self._save_data(data)
                    return True
            
            return False
            
        except Exception as e:
            UIHelper.show_error(f"更新记录失败: {str(e)}")
            return False
    
    def toggle_favorite(self, record_id: int) -> bool:
        """
        切换收藏状态
        
        Args:
            record_id: 记录ID
            
        Returns:
            是否成功
        """
        try:
            data = self._load_data()
            
            # 查找并更新记录
            for record in data['history']:
                if record['id'] == record_id:
                    record['favorite'] = not record.get('favorite', False)
                    self._save_data(data)
                    return True
            
            return False
            
        except Exception as e:
            UIHelper.show_error(f"切换收藏状态失败: {str(e)}")
            return False
    
    def delete_record(self, record_id: int) -> bool:
        """
        删除历史记录
        
        Args:
            record_id: 记录ID
            
        Returns:
            是否成功
        """
        try:
            data = self._load_data()
            
            # 查找并删除记录
            for i, record in enumerate(data['history']):
                if record['id'] == record_id:
                    data['history'].pop(i)
                    self._save_data(data)
                    return True
            
            return False
            
        except Exception as e:
            UIHelper.show_error(f"删除记录失败: {str(e)}")
            return False
    
    def get_usage_statistics(self, days: int = 30) -> Dict[str, Any]:
        """
        获取使用统计
        
        Args:
            days: 统计天数
            
        Returns:
            统计信息
        """
        try:
            data = self._load_data()
            records = data['history']
            
            # 计算日期范围
            from datetime import datetime, timedelta
            cutoff_date = (datetime.now() - timedelta(days=days)).date()
            
            # 过滤最近记录
            recent_records = []
            for record in records:
                record_date = datetime.fromisoformat(record['created_at']).date()
                if record_date >= cutoff_date:
                    recent_records.append(record)
            
            # 计算统计信息
            total_operations = len(recent_records)
            operation_types = set(record['operation_type'] for record in recent_records)
            active_days = set(record['created_at'][:10] for record in recent_records)
            favorite_count = sum(1 for record in records if record.get('favorite', False))
            
            # 按操作类型统计
            operation_stats = {}
            for record in recent_records:
                op_type = record['operation_type']
                operation_stats[op_type] = operation_stats.get(op_type, 0) + 1
            
            # 按日期统计
            daily_stats = {}
            for record in recent_records:
                date = record['created_at'][:10]
                daily_stats[date] = daily_stats.get(date, 0) + 1
            
            return {
                'total_stats': {
                    'total_operations': total_operations,
                    'operation_types': len(operation_types),
                    'active_days': len(active_days)
                },
                'operation_stats': [{'operation_type': k, 'count': v} for k, v in operation_stats.items()],
                'daily_stats': [{'date': k, 'count': v} for k, v in daily_stats.items()],
                'favorite_count': favorite_count
            }
            
        except Exception as e:
            UIHelper.show_error(f"获取统计信息失败: {str(e)}")
            return {}
    
    def export_history(self, format: str = 'json', records: List[Dict] = None) -> str:
        """
        导出历史记录
        
        Args:
            format: 导出格式 ('json', 'csv')
            records: 要导出的记录，为None时导出所有记录
            
        Returns:
            导出的数据字符串
        """
        try:
            if records is None:
                records = self.get_history_records(limit=1000)
            
            if format.lower() == 'json':
                return json.dumps(records, indent=2, ensure_ascii=False, default=str)
            
            elif format.lower() == 'csv':
                import csv
                import io
                
                output = io.StringIO()
                if records:
                    fieldnames = records[0].keys()
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(records)
                
                return output.getvalue()
            
            else:
                raise ValueError(f"不支持的导出格式: {format}")
            
        except Exception as e:
            UIHelper.show_error(f"导出历史记录失败: {str(e)}")
            return ""
    
    def _get_session_id(self) -> str:
        """获取当前session ID"""
        if 'session_id' not in st.session_state:
            import uuid
            st.session_state.session_id = str(uuid.uuid4())
        return st.session_state.session_id
    
    def _update_usage_stats(self, data: Dict[str, Any], operation_type: str):
        """更新使用统计"""
        try:
            today = datetime.now().date().isoformat()
            
            if 'stats' not in data:
                data['stats'] = {}
            
            if 'daily_stats' not in data['stats']:
                data['stats']['daily_stats'] = {}
            
            if today not in data['stats']['daily_stats']:
                data['stats']['daily_stats'][today] = {}
            
            if operation_type not in data['stats']['daily_stats'][today]:
                data['stats']['daily_stats'][today][operation_type] = 0
            
            data['stats']['daily_stats'][today][operation_type] += 1
            
        except Exception as e:
            # 静默处理统计错误，不影响主要功能
            pass
    
    def cleanup_old_records(self, days: int = 90) -> int:
        """
        清理旧记录
        
        Args:
            days: 保留天数
            
        Returns:
            删除的记录数
        """
        try:
            data = self._load_data()
            records = data['history']
            
            # 计算截止日期
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # 过滤保留的记录
            original_count = len(records)
            data['history'] = [
                record for record in records
                if datetime.fromisoformat(record['created_at']) >= cutoff_date or record.get('favorite', False)
            ]
            
            deleted_count = original_count - len(data['history'])
            
            # 保存数据
            self._save_data(data)
            
            return deleted_count
            
        except Exception as e:
            UIHelper.show_error(f"清理旧记录失败: {str(e)}")
            return 0 