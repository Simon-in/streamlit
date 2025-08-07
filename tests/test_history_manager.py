import os
import sys
import datetime
import json
import uuid
import tempfile

# 将项目根目录添加到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql_generator.utils.history_manager import HistoryManager

def test_history_manager_empty():
    """测试空历史记录初始化"""
    # 使用临时文件作为历史记录文件
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
        temp_path = temp.name
        
    try:
        # 创建一个空的历史记录文件
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write("{}")
        
        # 初始化历史管理器
        manager = HistoryManager(temp_path)
        
        # 测试获取历史记录
        records = manager.get_history_records()
        assert isinstance(records, list), "历史记录应该是一个列表"
        assert len(records) == 0, "历史记录应该为空"
        
        # 测试获取收藏
        favorites = manager.get_favorite_records()
        assert isinstance(favorites, list), "收藏应该是一个列表"
        assert len(favorites) == 0, "收藏应该为空"
        
        # 测试添加记录
        record_id = manager.add_history_record("SELECT", "SELECT * FROM users")
        
        # 验证记录是否被添加
        records = manager.get_history_records()
        assert len(records) == 1, "应该有1条历史记录"
        assert records[0]["id"] == record_id, "记录ID应该匹配"
        assert records[0]["operation_type"] == "SELECT", "操作类型应该是SELECT"
        
        # 测试统计
        stats = manager.get_usage_statistics()
        assert stats["total_stats"]["total_operations"] > 0, "应该有操作统计"
        
        # 测试导出
        json_export = manager.export_history("json")
        assert "records" in json_export, "导出的JSON应该包含records字段"
        
        # 测试删除记录
        manager.delete_record(record_id)
        records = manager.get_history_records()
        assert len(records) == 0, "删除后应该没有记录"
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def test_history_manager_corrupt():
    """测试损坏的历史记录文件"""
    # 使用临时文件作为历史记录文件
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
        temp_path = temp.name
        
    try:
        # 创建一个损坏的历史记录文件（缺少records键）
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write('{"favorites": []}')
        
        # 初始化历史管理器
        manager = HistoryManager(temp_path)
        
        # 测试获取历史记录
        records = manager.get_history_records()
        assert isinstance(records, list), "历史记录应该是一个列表"
        assert len(records) == 0, "历史记录应该为空"
        
        # 测试添加记录
        record_id = manager.add_history_record("INSERT", "INSERT INTO users VALUES (1, 'test')")
        
        # 验证记录是否被添加
        records = manager.get_history_records()
        assert len(records) == 1, "应该有1条历史记录"
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def test_history_manager_favorites():
    """测试收藏功能"""
    # 使用临时文件作为历史记录文件
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
        temp_path = temp.name
        
    try:
        # 创建一个只有records键的历史记录文件（缺少favorites键）
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write('{"records": []}')
        
        # 初始化历史管理器
        manager = HistoryManager(temp_path)
        
        # 测试添加记录
        record_id = manager.add_history_record("UPDATE", "UPDATE users SET name='test' WHERE id=1")
        
        # 测试收藏功能
        result = manager.toggle_favorite(record_id)
        assert result, "切换收藏应该成功"
        
        # 验证收藏是否生效
        favorites = manager.get_favorite_records()
        assert len(favorites) == 1, "应该有1条收藏"
        assert favorites[0]["id"] == record_id, "收藏的记录ID应该匹配"
        
        # 再次切换（取消收藏）
        result = manager.toggle_favorite(record_id)
        assert result, "取消收藏应该成功"
        
        # 验证收藏是否被取消
        favorites = manager.get_favorite_records()
        assert len(favorites) == 0, "收藏应该为空"
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def test_history_manager_search():
    """测试历史记录搜索"""
    # 使用临时文件作为历史记录文件
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
        temp_path = temp.name
        
    try:
        # 创建一个空历史记录文件
        with open(temp_path, 'w') as f:
            f.write("{}")
        
        # 初始化历史管理器
        manager = HistoryManager(temp_path)
        
        # 添加多条记录
        manager.add_history_record("SELECT", "SELECT * FROM users")
        manager.add_history_record("INSERT", "INSERT INTO products VALUES (1, 'apple')")
        manager.add_history_record("UPDATE", "UPDATE users SET name='test' WHERE id=1")
        
        # 测试搜索
        results = manager.search_history("apple")
        assert len(results) == 1, "应该只有1条包含'apple'的记录"
        assert "INSERT" in results[0]["operation_type"], "匹配的记录应该是INSERT操作"
        
        # 测试搜索（无结果）
        results = manager.search_history("banana")
        assert len(results) == 0, "不应该有包含'banana'的记录"
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def run_tests():
    """运行所有测试"""
    print("测试开始...")
    
    test_history_manager_empty()
    print("✅ 测试空历史记录初始化成功")
    
    test_history_manager_corrupt()
    print("✅ 测试损坏的历史记录文件成功")
    
    test_history_manager_favorites()
    print("✅ 测试收藏功能成功")
    
    test_history_manager_search()
    print("✅ 测试历史记录搜索成功")
    
    print("所有测试通过！✨")

if __name__ == "__main__":
    run_tests()
