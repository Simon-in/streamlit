# -*- coding: utf-8 -*-
"""
历史记录管理模块 - 提供SQL历史记录的存储和管理功能
"""

import os
import json
import datetime
import uuid
from typing import List, Dict, Any, Optional, Union


class HistoryManager:
    """SQL历史记录管理类"""
    
    def __init__(self, history_file: str = "sql_history.json"):
        """
        初始化历史记录管理器
        
        Args:
            history_file: 历史记录文件路径
        """
        self.history_file = history_file
        self.history_data = self._load_history()
    
    def _load_history(self) -> Dict[str, Any]:
        """
        从文件加载历史记录
        
        Returns:
            历史记录数据字典
        """
        # 创建默认的空历史记录数据结构
        default_history = {"records": [], "favorites": [], "meta": {"last_updated": ""}}
        
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as file:
                    history_data = json.load(file)
                    
                    # 确保数据包含所有必要的键
                    if "records" not in history_data:
                        history_data["records"] = []
                    if "favorites" not in history_data:
                        history_data["favorites"] = []
                    if "meta" not in history_data:
                        history_data["meta"] = {"last_updated": ""}
                    elif "last_updated" not in history_data["meta"]:
                        history_data["meta"]["last_updated"] = ""
                        
                    return history_data
            except (json.JSONDecodeError, UnicodeDecodeError):
                # 如果文件损坏，返回默认空历史记录
                return default_history
        else:
            # 如果文件不存在，返回默认空历史记录
            return default_history
    
    def _save_history(self) -> bool:
        """
        将历史记录保存到文件
        
        Returns:
            是否保存成功
        """
        try:
            # 更新最后修改时间
            self.history_data["meta"]["last_updated"] = datetime.datetime.now().isoformat()
            
            # 保存到文件
            with open(self.history_file, 'w', encoding='utf-8') as file:
                json.dump(self.history_data, file, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def add_history_record(self, operation_type: str, sql_content: str, file_name: str = "",
                         user_notes: str = "", tags: List[str] = None) -> str:
        """
        添加历史记录
        
        Args:
            operation_type: 操作类型（SELECT, INSERT, UPDATE等）
            sql_content: SQL语句内容
            file_name: 关联文件名（可选）
            user_notes: 用户备注（可选）
            tags: 标签列表（可选）
            
        Returns:
            新记录的ID
        """
        # 确保history_data包含records键
        if "records" not in self.history_data:
            self.history_data["records"] = []
        
        # 生成唯一ID
        record_id = str(uuid.uuid4())
        
        # 创建记录
        record = {
            "id": record_id,
            "operation_type": operation_type,
            "sql_content": sql_content,
            "file_name": file_name,
            "user_notes": user_notes,
            "tags": tags or [],
            "created_at": datetime.datetime.now().isoformat(),
            "is_favorite": False
        }
        
        # 添加到历史记录
        self.history_data["records"].append(record)
        
        # 保存历史记录
        self._save_history()
        
        return record_id
    
    def get_history_records(self, limit: int = 0, offset: int = 0,
                          filter_type: str = None) -> List[Dict[str, Any]]:
        """
        获取历史记录
        
        Args:
            limit: 返回记录数量限制（0表示不限制）
            offset: 起始位置偏移量
            filter_type: 按操作类型筛选（可选）
            
        Returns:
            历史记录列表
        """
        # 确保history_data包含records键
        if "records" not in self.history_data:
            self.history_data["records"] = []
            return []
            
        records = self.history_data["records"]
        
        # 按操作类型筛选
        if filter_type:
            records = [r for r in records if r["operation_type"] == filter_type]
        
        # 按创建时间倒序排序
        records = sorted(records, key=lambda x: x.get("created_at", ""), reverse=True)
        
        # 应用分页
        if limit > 0:
            records = records[offset:offset + limit]
        elif offset > 0:
            records = records[offset:]
        
        return records
    
    def get_favorite_records(self) -> List[Dict[str, Any]]:
        """
        获取收藏的历史记录
        
        Returns:
            收藏的历史记录列表
        """
        # 确保favorites键存在
        if "favorites" not in self.history_data:
            self.history_data["favorites"] = []
            
        return self.history_data["favorites"]
    
    def toggle_favorite(self, record_id: str) -> bool:
        """
        切换记录的收藏状态
        
        Args:
            record_id: 记录ID
            
        Returns:
            操作是否成功
        """
        # 确保必要的键存在
        if "records" not in self.history_data:
            self.history_data["records"] = []
        if "favorites" not in self.history_data:
            self.history_data["favorites"] = []
        
        # 查找记录
        for record in self.history_data["records"]:
            if record["id"] == record_id:
                # 切换收藏状态
                is_favorite = not record.get("is_favorite", False)
                record["is_favorite"] = is_favorite
                
                # 更新收藏夹
                if is_favorite:
                    if record not in self.history_data["favorites"]:
                        self.history_data["favorites"].append(record)
                else:
                    self.history_data["favorites"] = [
                        r for r in self.history_data["favorites"] if r["id"] != record_id
                    ]
                
                # 保存历史记录
                self._save_history()
                return True
        
        return False
    
    def delete_record(self, record_id: str) -> bool:
        """
        删除历史记录
        
        Args:
            record_id: 记录ID
            
        Returns:
            操作是否成功
        """
        # 确保必要的键存在
        if "records" not in self.history_data:
            self.history_data["records"] = []
        if "favorites" not in self.history_data:
            self.history_data["favorites"] = []
            
        # 查找并删除记录
        self.history_data["records"] = [
            r for r in self.history_data["records"] if r["id"] != record_id
        ]
        
        # 同步更新收藏夹
        self.history_data["favorites"] = [
            r for r in self.history_data["favorites"] if r["id"] != record_id
        ]
        
        # 保存历史记录
        return self._save_history()
    
    def search_history(self, query: str) -> List[Dict[str, Any]]:
        """
        搜索历史记录
        
        Args:
            query: 搜索关键词
            
        Returns:
            匹配的记录列表
        """
        if not query:
            return []
        
        # 确保history_data包含records键
        if "records" not in self.history_data:
            self.history_data["records"] = []
            return []
            
        query = query.lower()
        results = []
        
        for record in self.history_data["records"]:
            # 搜索SQL内容
            if query in record.get("sql_content", "").lower():
                results.append(record)
                continue
            
            # 搜索用户备注
            if query in record.get("user_notes", "").lower():
                results.append(record)
                continue
            
            # 搜索标签
            if any(query in tag.lower() for tag in record.get("tags", [])):
                results.append(record)
                continue
        
        return results
    
    def get_usage_statistics(self, days: int = 30) -> Dict[str, Any]:
        """
        获取使用统计
        
        Args:
            days: 统计天数范围
            
        Returns:
            统计信息字典
        """
        # 确保history_data包含records键
        if "records" not in self.history_data:
            self.history_data["records"] = []
            return {
                "total_stats": {
                    "total_operations": 0,
                    "operation_types": 0,
                    "active_days": 0
                },
                "operation_breakdown": {},
                "favorite_count": 0,
                "period_days": days
            }
        
        if not self.history_data["records"]:
            return {
                "total_stats": {
                    "total_operations": 0,
                    "operation_types": 0,
                    "active_days": 0
                },
                "operation_breakdown": {},
                "favorite_count": 0,
                "period_days": days
            }
        
        # 计算统计起始时间
        now = datetime.datetime.now()
        start_date = (now - datetime.timedelta(days=days)).isoformat()
        
        # 筛选时间范围内的记录
        recent_records = [
            r for r in self.history_data["records"]
            if r.get("created_at", "") >= start_date
        ]
        
        # 统计操作类型
        operation_types = {}
        for record in recent_records:
            op_type = record.get("operation_type", "UNKNOWN")
            operation_types[op_type] = operation_types.get(op_type, 0) + 1
        
        # 统计活跃天数
        active_days = set()
        for record in recent_records:
            if "created_at" in record:
                try:
                    date_str = record["created_at"].split("T")[0]
                    active_days.add(date_str)
                except (IndexError, AttributeError):
                    pass
        
        # 确保favorites键存在
        if "favorites" not in self.history_data:
            self.history_data["favorites"] = []
            
        # 汇总统计信息
        stats = {
            "total_stats": {
                "total_operations": len(recent_records),
                "operation_types": len(operation_types),
                "active_days": len(active_days)
            },
            "operation_breakdown": operation_types,
            "favorite_count": len(self.history_data["favorites"]),
            "period_days": days
        }
        
        return stats
    
    def export_history(self, export_format: str = "json") -> Union[str, Dict[str, Any]]:
        """
        导出历史记录
        
        Args:
            export_format: 导出格式（"json", "csv", "sql"）
            
        Returns:
            导出的数据
        """
        # 确保必要的键存在
        if "records" not in self.history_data:
            self.history_data["records"] = []
        if "favorites" not in self.history_data:
            self.history_data["favorites"] = []
            
        if export_format == "json":
            return json.dumps(self.history_data, ensure_ascii=False, indent=2)
        
        elif export_format == "csv":
            # 构建CSV内容
            csv_content = "id,operation_type,sql_content,file_name,user_notes,created_at,is_favorite\n"
            
            for record in self.history_data["records"]:
                # 处理CSV中的引号转义
                sql_content = record.get("sql_content", "").replace('"', '""')
                user_notes = record.get("user_notes", "").replace('"', '""')
                
                row = [
                    record.get("id", ""),
                    record.get("operation_type", ""),
                    f'"{sql_content}"',
                    record.get("file_name", ""),
                    f'"{user_notes}"',
                    record.get("created_at", ""),
                    "TRUE" if record.get("is_favorite", False) else "FALSE"
                ]
                csv_content += ",".join(row) + "\n"
            
            return csv_content
        
        elif export_format == "sql":
            # 构建SQL脚本
            sql_content = "-- SQL历史记录导出\n"
            sql_content += f"-- 导出时间: {datetime.datetime.now().isoformat()}\n\n"
            
            for record in self.history_data["records"]:
                sql_content += f"-- 操作类型: {record.get('operation_type', '')}\n"
                sql_content += f"-- 创建时间: {record.get('created_at', '')}\n"
                if record.get("user_notes"):
                    sql_content += f"-- 备注: {record.get('user_notes', '')}\n"
                sql_content += record.get("sql_content", "") + ";\n\n"
            
            return sql_content
        
        else:
            raise ValueError(f"不支持的导出格式: {export_format}")
