#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能演示脚本 - 展示Streamlit SQL生成工具的新增功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径，以便导入sql_generator包
sys.path.append(str(Path(__file__).parent.parent))


def demo_advanced_sql():
    """演示高级SQL功能"""
    print("🚀 高级SQL功能演示")
    print("=" * 50)

    from sql_generator.core.advanced_sql import AdvancedSQLGenerator

    advanced_sql = AdvancedSQLGenerator()

    # 演示视图创建
    print("\n👁️ 视图创建演示:")
    view_sql = advanced_sql.generate_view(
        view_name="active_users",
        select_query="SELECT id, username, email, created_at FROM users WHERE status = 'active'",
        schema="public"
    )
    print(view_sql)

    # 演示索引创建
    print("\n🚀 索引创建演示:")
    index_sql = advanced_sql.generate_index(
        table_name="users",
        columns=["email", "status"],
        index_name="idx_users_email_status",
        unique=False,
        index_type="BTREE"
    )
    print(index_sql)

    # 演示存储过程创建
    print("\n⚙️ 存储过程演示:")
    proc_sql = advanced_sql.generate_stored_procedure(
        proc_name="GetUserCount",
        parameters=[
            {"name": "status_filter", "type": "VARCHAR(20)", "direction": "IN"},
            {"name": "user_count", "type": "INT", "direction": "OUT"}
        ],
        body="    SELECT COUNT(*) INTO user_count FROM users WHERE status = status_filter;",
        schema="public"
    )
    print(proc_sql)


def demo_sql_templates():
    """演示SQL模板功能"""
    print("\n📚 SQL模板功能演示")
    print("=" * 50)

    from sql_generator.templates.sql_patterns import SQLTemplateManager, CommonSQLPatterns

    template_manager = SQLTemplateManager()

    # 展示可用的模板分类
    print("\n📋 可用模板分类:")
    categories = template_manager.get_categories()
    for i, category in enumerate(categories, 1):
        category_info = template_manager.templates[category]
        print(f"{i}. {category_info['name']} ({category})")

    # 演示基础查询模板
    print("\n🔍 基础查询模板演示:")
    basic_templates = template_manager.get_templates_by_category("basic_queries")

    # 使用简单查询模板
    simple_template = basic_templates["simple_select"]
    print(f"模板: {simple_template['name']}")
    print(f"描述: {simple_template['description']}")

    # 渲染模板
    parameters = {
        "columns": "id, name, email",
        "table": "users",
        "condition": "status = 'active' AND created_at > '2024-01-01'"
    }

    rendered_sql = template_manager.render_template(simple_template['template'], parameters)
    print(f"生成的SQL:\n{rendered_sql}")

    # 演示常用SQL模式
    print("\n📊 常用SQL模式演示:")

    # 分页查询
    pagination_sql = CommonSQLPatterns.generate_pagination_query(
        table="users",
        page_size=20,
        page_number=2,
        order_column="created_at",
        where_clause="status = 'active'"
    )
    print("分页查询:")
    print(pagination_sql)

    # 重复数据检测
    duplicate_sql = CommonSQLPatterns.generate_duplicate_detection_query(
        table="users",
        columns=["email", "phone"]
    )
    print("\n重复数据检测:")
    print(duplicate_sql)


def demo_data_analysis():
    """演示数据分析功能"""
    print("\n📊 数据分析功能演示")
    print("=" * 50)

    from sql_generator.core.sql_formatter import SQLFormatter

    # 演示SQL格式化
    print("\n✨ SQL格式化演示:")

    messy_sql = "select u.id,u.name,o.total from users u inner join orders o on u.id=o.user_id where u.status='active' and o.created_at>='2024-01-01' group by u.id,u.name having count(*)>5 order by o.total desc"

    print("原始SQL:")
    print(messy_sql)

    formatted_sql = SQLFormatter.format_sql(messy_sql, "pretty")
    print("\n格式化后的SQL:")
    print(formatted_sql)

    # 演示SQL语法验证
    print("\n🔍 SQL语法验证演示:")

    test_sqls = [
        "SELECT * FROM users WHERE id = 1",
        "SELECT * FROM users WHERE",  # 语法错误
        "INSERT INTO users (name, email) VALUES ('John', 'john@example.com')"
    ]

    for sql in test_sqls:
        validation_result = SQLFormatter.validate_sql_syntax(sql)
        status = "✅ 有效" if validation_result['is_valid'] else "❌ 无效"
        print(f"{status}: {sql}")
        if validation_result['errors']:
            for error in validation_result['errors']:
                print(f"  错误: {error}")


def demo_history_manager():
    """演示历史记录管理"""
    print("\n📚 历史记录管理演示")
    print("=" * 50)

    from sql_generator.utils.history_manager import HistoryManager

    # 创建历史记录管理器
    history_manager = HistoryManager("demo_history.json")

    # 添加示例记录
    print("\n📝 添加历史记录:")

    sample_records = [
        {
            "operation_type": "SELECT",
            "sql_content": "SELECT * FROM users WHERE status = 'active'",
            "file_name": "user_query.sql",
            "user_notes": "查询活跃用户",
            "tags": ["用户", "查询", "活跃"]
        },
        {
            "operation_type": "CREATE",
            "sql_content": "CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(100))",
            "file_name": "create_products.sql",
            "user_notes": "创建产品表",
            "tags": ["产品", "创建表"]
        }
    ]

    for record in sample_records:
        record_id = history_manager.add_history_record(**record)
        print(f"添加记录 ID: {record_id}")

    # 获取历史记录
    print("\n📖 获取历史记录:")
    records = history_manager.get_history_records(limit=10)

    for record in records:
        print(f"ID: {record['id']}, 类型: {record['operation_type']}, 时间: {record['created_at']}")
        print(f"SQL: {record['sql_content'][:50]}...")
        if record['user_notes']:
            print(f"备注: {record['user_notes']}")
        print("-" * 40)

    # 搜索记录
    print("\n🔍 搜索历史记录:")
    search_results = history_manager.search_history("用户")
    print(f"搜索 '用户' 找到 {len(search_results)} 条记录")

    # 获取使用统计
    print("\n📊 使用统计:")
    stats = history_manager.get_usage_statistics(days=30)
    if stats:
        print(f"总操作数: {stats['total_stats']['total_operations']}")
        print(f"操作类型数: {stats['total_stats']['operation_types']}")
        print(f"活跃天数: {stats['total_stats']['active_days']}")
        print(f"收藏数量: {stats['favorite_count']}")


def main():
    """主演示函数"""
    print("🎉 Streamlit SQL生成工具 - 功能演示")
    print("=" * 60)

    try:
        # 演示各个功能模块
        demo_advanced_sql()
        demo_sql_templates()
        demo_data_analysis()
        demo_history_manager()

        print("\n" + "=" * 60)
        print("✅ 功能演示完成！")
        print("=" * 60)

        print("\n🚀 启动完整应用:")
        print("   streamlit run app.py")

        print("\n📖 更多信息:")
        print("   查看 README.md 文件了解详细使用说明")

    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保已安装所有依赖包:")
        print("   pip install -r requirements.txt")

    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        print("请检查项目文件是否完整")


if __name__ == "__main__":
    main()
