# -*- coding: utf-8 -*-
"""
主应用UI模块 - 负责渲染Streamlit界面
"""

from PIL import Image
import os
import re
import pathlib
import streamlit as st
from sql_generator.core.sql_generator import SQLGenerator
from sql_generator.core.sql_formatter import SQLFormatter
from sql_generator.core.advanced_sql import AdvancedSQLGenerator
from sql_generator.templates.sql_patterns import CommonSQLPatterns
from sql_generator.utils.ui_utils import SessionStateManager, UIHelper, InputValidator
from sql_generator.utils.file_utils import FileHandler
from sql_generator.config.constants import *


def run_app():
    """运行主应用程序"""
    # 配置页面
    st.set_page_config(
        page_title=APP_CONFIG['page_title'],
        page_icon=APP_CONFIG['page_icon'],
        layout=APP_CONFIG['layout'],
        initial_sidebar_state=APP_CONFIG['initial_sidebar_state']
    )
    
    # 初始化session state
    SessionStateManager.init_session_state()
    
    # 设置侧边栏
    set_sidebar()
    
    # 添加主页内容
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        # 🚀 SQL生成工具
        
        ### 提高SQL开发效率的得力助手
        
        本工具可以帮助您快速生成各种SQL语句，支持批量生成和自定义模板。无需手动编写复杂SQL，只需填写必要参数或上传模板文件，即可生成格式规范、语法正确的SQL代码。
        
        **主要功能：**
        
        ✅ **多种SQL语句支持** - 覆盖日常开发中的各类SQL需求
        ✅ **批量生成** - 通过Excel模板批量生成多条SQL语句
        ✅ **语法格式化** - 自动美化SQL代码，提高可读性
        ✅ **一键下载** - 生成的SQL可以直接下载为文件使用
        ✅ **模板中心** - 提供常用SQL模板，可自定义扩展
        """)
    
    with col2:
        st.info("""
        **💡 使用说明**
        
        1. 从左侧菜单选择功能模块
        2. 可下载SQL模板进行批量操作
        3. 选择所需的SQL类型进行生成
        
        如有问题，请查看模板中心的示例。
        """)
        
        st.success("""
        **✨ 新功能**
        
        现在支持导出生成的SQL语句为文件，方便您直接在数据库客户端中使用。
        
        同时新增了SQL语法检查和格式化功能，帮助您编写更规范的SQL代码。
        """)
    
    st.markdown("---")
    
    # 添加模板下载区域
    import os
    import pathlib
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📥 SQL模板文件")
        st.markdown("""
        下载 Excel 模板文件，用于批量生成 SQL 语句。按照模板格式填写后上传，即可批量生成SQL语句。
        
        **模板包含以下工作表：**
        - **create** - 表结构定义模板（表名和字段定义）
        - **select** - 查询语句模板（表名和查询字段）
        - **insert** - 插入数据模板（表名、字段和值）
        - **update** - 更新数据模板（表名、SET子句和WHERE条件）
        - **merge** - 合并数据模板（目标表、源表和匹配条件）
        - **delete** - 删除数据模板（表名和条件）
        - **truncate** - 截断表模板（表名列表）
        """)
    
    with col2:
        # 使用 pathlib 获取当前目录的父目录，然后构建模板文件的路径
        current_dir = pathlib.Path(__file__).parent.parent
        template_path = os.path.join(current_dir, "templates", "sql_example.xlsx")
        
        # 使用FileHandler类创建下载按钮
        FileHandler.create_download_button(
            button_name="📥 下载 SQL 模板文件",
            file_path=template_path,
            file_type="xlsx"
        )
    
    st.markdown("---")
    
    # 根据当前页面渲染内容
    current_page = st.session_state.get('current_page', MAIN_PAGES[0])
    
    if current_page == "SQL生成":
        render_sql_page()
    elif current_page == "高级功能":
        render_advanced_page()
    elif current_page == "模板中心":
        render_template_page()
    elif current_page == "历史记录":
        render_history_page()
    elif current_page == "数据分析":
        render_analysis_page()
    elif current_page == "streamlit_example":
        render_example_page()


def set_sidebar():
    """设置侧边栏"""
    with st.sidebar:
        st.title("SQL生成工具")
        st.markdown("---")
        
        for page in MAIN_PAGES:
            if st.button(page, key=f"btn_{page}"):
                st.session_state.current_page = page
                st.session_state.current_sub_page = None
                st.experimental_rerun()
                
        st.markdown("---")
        st.markdown("© 2025 SQL生成工具")


def render_sql_page():
    """渲染SQL生成页面"""
    UIHelper.create_section_header("SQL语句生成", "生成各种类型的SQL语句")
    
    # 子页面选择
    sub_pages = st.tabs(SQL_SUB_PAGES)
    
    # 创建SQL生成器实例
    sql_gen = SQLGenerator()
    
    # 根据子页面渲染不同内容
    with sub_pages[0]:  # 主页
        st.subheader("SQL语句生成向导")
        
        st.markdown("""
        在本页面中，您可以生成各种常用的SQL语句。请从上方选项卡中选择需要生成的SQL类型：
        
        - **CREATE** - 创建表结构
        - **SELECT** - 查询数据
        - **INSERT** - 插入数据
        - **UPDATE** - 更新数据
        - **MERGE** - 合并数据
        - **DELETE** - 删除数据
        - **TRUNCATE** - 清空表数据
        """)
        
        # 添加操作指南
        with st.expander("� 操作指南"):
            st.markdown("""
            1. 选择需要的SQL类型选项卡
            2. 手动输入参数或上传配置文件
            3. 点击"生成"按钮生成SQL
            4. 下载生成的SQL或直接复制使用
            
            **批量生成SQL**：上传按照模板格式编写的Excel文件，可以一次性生成多条SQL语句。
            """)
    
    with sub_pages[1]:  # CREATE
        st.subheader("生成CREATE TABLE语句")
        
        uploaded_file = st.file_uploader("上传CREATE配置文件", type=["xlsx"], key="create_uploader")
        
        if uploaded_file:
            SessionStateManager.set_uploaded_file(uploaded_file)
            create_list = sql_gen.bulk_create(uploaded_file)
            
            if create_list:
                create_sql = sql_gen.sql_formatted(create_list)
                UIHelper.display_sql_with_download(create_sql, "create_table.sql", "生成的CREATE TABLE语句")
        
        st.image("sql_generator/assets/create.png", width=300)
    
    with sub_pages[2]:  # SELECT
        st.subheader("生成SELECT语句")
        
        st.markdown("选择您的方式生成SELECT语句：")
        select_mode = st.radio("生成方式", ["手动输入", "上传文件"], horizontal=True, key="select_mode")
        
        if select_mode == "手动输入":
            col1, col2 = st.columns(2)
            with col1:
                table_name = st.text_input("表名", key="select_table")
            with col2:
                columns = st.text_input("列名（多列用逗号分隔）", key="select_columns")
            
            if st.button("生成SELECT语句"):
                if table_name and columns:
                    select_sql = sql_gen.bulk_select(table=table_name, column=columns)
                    st.code(select_sql, language="sql")
                    st.download_button(
                        label="下载SQL文件",
                        data=select_sql,
                        file_name="select_query.sql",
                        mime=MIME_TYPES['sql']
                    )
                else:
                    UIHelper.show_error("请输入表名和列名")
        else:
            uploaded_file = st.file_uploader("上传SELECT配置文件", type=["xlsx"], key="select_uploader")
            
            if uploaded_file:
                SessionStateManager.set_uploaded_file(uploaded_file)
                select_list = sql_gen.bulk_select(uploaded_file)
                
                if select_list:
                    select_sql = sql_gen.sql_formatted(select_list)
                    UIHelper.display_sql_with_download(select_sql, "select_query.sql", "生成的SELECT语句")
        
        st.image("sql_generator/assets/select.png", width=300)
    
    with sub_pages[3]:  # INSERT
        st.subheader("生成INSERT语句")
        
        st.markdown("选择您的方式生成INSERT语句：")
        insert_mode = st.radio("生成方式", ["手动输入", "上传文件"], horizontal=True, key="insert_mode")
        
        if insert_mode == "手动输入":
            col1, col2 = st.columns(2)
            with col1:
                table_name = st.text_input("表名", key="insert_table")
                columns = st.text_input("列名（多列用逗号分隔）", key="insert_columns")
            with col2:
                values = st.text_area("值（多行用分号分隔）", height=100, key="insert_values")
            
            if st.button("生成INSERT语句"):
                if table_name and columns and values:
                    # 简单实现INSERT语句生成
                    insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
                    st.code(insert_sql, language="sql")
                    st.download_button(
                        label="下载SQL文件",
                        data=insert_sql,
                        file_name="insert_statement.sql",
                        mime=MIME_TYPES['sql']
                    )
                else:
                    UIHelper.show_error("请输入表名、列名和值")
        else:
            uploaded_file = st.file_uploader("上传INSERT配置文件", type=["xlsx"], key="insert_uploader")
            
            if uploaded_file:
                SessionStateManager.set_uploaded_file(uploaded_file)
                # 假设有bulk_insert方法
                insert_list = sql_gen.bulk_insert(uploaded_file)
                
                if insert_list:
                    insert_sql = sql_gen.sql_formatted(insert_list)
                    UIHelper.display_sql_with_download(insert_sql, "insert_statement.sql", "生成的INSERT语句")
        
        st.image("sql_generator/assets/insert.png", width=300)
    
    with sub_pages[4]:  # UPDATE
        st.subheader("生成UPDATE语句")
        
        col1, col2 = st.columns(2)
        with col1:
            table_name = st.text_input("表名", key="update_table")
            set_clause = st.text_area("SET子句 (例如: column1 = 'value1', column2 = 'value2')", height=100, key="update_set")
        with col2:
            where_clause = st.text_area("WHERE子句 (例如: id = 1 AND status = 'active')", height=100, key="update_where")
        
        if st.button("生成UPDATE语句"):
            if table_name and set_clause:
                # 生成UPDATE语句
                update_sql = f"UPDATE {table_name}\nSET {set_clause}"
                if where_clause:
                    update_sql += f"\nWHERE {where_clause}"
                update_sql += ";"
                
                st.code(update_sql, language="sql")
                st.download_button(
                    label="下载SQL文件",
                    data=update_sql,
                    file_name="update_statement.sql",
                    mime=MIME_TYPES['sql']
                )
            else:
                UIHelper.show_error("请输入表名和SET子句")
    
    with sub_pages[5]:  # MERGE
        st.subheader("生成MERGE语句")
        
        uploaded_file = st.file_uploader("上传MERGE配置文件", type=["xlsx"], key="merge_uploader")
        
        if uploaded_file:
            SessionStateManager.set_uploaded_file(uploaded_file)
            # 假设有bulk_merge方法
            merge_list = sql_gen.bulk_merge(uploaded_file)
            
            if merge_list:
                merge_sql = sql_gen.sql_formatted(merge_list)
                UIHelper.display_sql_with_download(merge_sql, "merge_statement.sql", "生成的MERGE语句")
        
        st.image("sql_generator/assets/merge.png", width=300)
    
    with sub_pages[6]:  # DELETE
        st.subheader("生成DELETE语句")
        
        col1, col2 = st.columns(2)
        with col1:
            table_name = st.text_input("表名", key="delete_table")
        with col2:
            where_clause = st.text_area("WHERE子句 (例如: id = 1 AND status = 'active')", height=100, key="delete_where")
        
        if st.button("生成DELETE语句"):
            if table_name:
                # 生成DELETE语句
                delete_sql = f"DELETE FROM {table_name}"
                if where_clause:
                    delete_sql += f"\nWHERE {where_clause}"
                delete_sql += ";"
                
                st.code(delete_sql, language="sql")
                st.download_button(
                    label="下载SQL文件",
                    data=delete_sql,
                    file_name="delete_statement.sql",
                    mime=MIME_TYPES['sql']
                )
            else:
                UIHelper.show_error("请输入表名")
        
        st.image("sql_generator/assets/delete.png", width=300)
    
    with sub_pages[7]:  # TRUNCATE
        st.subheader("生成TRUNCATE语句")
        
        table_name = st.text_input("表名", key="truncate_table")
        
        if st.button("生成TRUNCATE语句"):
            if table_name:
                # 生成TRUNCATE语句
                truncate_sql = f"TRUNCATE TABLE {table_name};"
                
                st.code(truncate_sql, language="sql")
                st.download_button(
                    label="下载SQL文件",
                    data=truncate_sql,
                    file_name="truncate_statement.sql",
                    mime=MIME_TYPES['sql']
                )
            else:
                UIHelper.show_error("请输入表名")
        
        st.image("sql_generator/assets/truncate.png", width=300)

# 其他页面渲染函数的实现...

def render_analysis_page():
    """渲染数据分析页面"""
    UIHelper.create_section_header("数据分析", "分析SQL和数据结构")
    
    # 子页面选择
    sub_pages = st.tabs(ANALYSIS_SUB_PAGES)
    
    # 根据子页面渲染不同内容
    with sub_pages[0]:  # 数据概况
        st.subheader("数据概况分析")
        
        # 表结构分析
        with st.expander("表结构分析"):
            table_name = st.text_input("输入表名", key="table_structure_name")
            if st.button("生成表结构分析SQL", key="gen_struct_sql"):
                if table_name:
                    sql = CommonSQLPatterns.generate_schema_analysis_query(table_name)
                    st.code(sql, language="sql")
                    st.download_button(
                        label="下载SQL",
                        data=sql,
                        file_name="schema_analysis.sql",
                        mime="text/plain"
                    )
                else:
                    UIHelper.show_error("请输入表名")
        
        # 数据趋势分析
        with st.expander("数据趋势分析"):
            col1, col2 = st.columns(2)
            with col1:
                trend_table = st.text_input("表名", key="trend_table")
                trend_time = st.text_input("时间列", key="trend_time")
            with col2:
                trend_metric = st.text_input("指标列", key="trend_metric")
                trend_group = st.text_input("分组列(可选)", key="trend_group")
            
            trend_interval = st.selectbox("时间间隔", 
                                        options=["day", "week", "month", "quarter", "year"],
                                        index=2)
            
            if st.button("生成趋势分析SQL", key="gen_trend_sql"):
                if trend_table and trend_time and trend_metric:
                    sql = CommonSQLPatterns.generate_trend_analysis_query(
                        trend_table, trend_time, trend_metric, trend_group, trend_interval
                    )
                    st.code(sql, language="sql")
                    st.download_button(
                        label="下载SQL",
                        data=sql,
                        file_name="trend_analysis.sql",
                        mime="text/plain"
                    )
                else:
                    UIHelper.show_error("请填写表名、时间列和指标列")
        
        # 数据质量检查
        with st.expander("数据质量检查"):
            st.markdown("""
            **常用数据质量检查SQL:**
            
            1. **空值检查**
            ```sql
            SELECT 
                COUNT(*) AS total_rows,
                SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) AS null_count,
                SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS null_percentage
            FROM table_name;
            ```
            
            2. **重复值检查**
            ```sql
            SELECT 
                column_name, 
                COUNT(*) AS occurrence_count
            FROM table_name
            GROUP BY column_name
            HAVING COUNT(*) > 1
            ORDER BY COUNT(*) DESC;
            ```
            
            3. **异常值检查**
            ```sql
            SELECT 
                MIN(numeric_column) AS min_value,
                MAX(numeric_column) AS max_value,
                AVG(numeric_column) AS avg_value,
                STDDEV(numeric_column) AS stddev_value,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY numeric_column) AS median
            FROM table_name;
            ```
            """)
    
    with sub_pages[1]:  # SQL格式化
        st.subheader("SQL格式化")
        
        sql_input = st.text_area("输入SQL语句", height=200)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("格式化SQL"):
                if sql_input:
                    formatted_sql = SQLFormatter.format_sql(sql_input)
                    st.code(formatted_sql, language="sql")
                    st.download_button(
                        label="下载格式化SQL",
                        data=formatted_sql,
                        file_name="formatted_sql.sql",
                        mime="text/plain"
                    )
                else:
                    UIHelper.show_error("请输入SQL语句")
        
        with col2:
            if st.button("美化SQL"):
                if sql_input:
                    beautified_sql = SQLFormatter.beautify_sql(sql_input)
                    st.code(beautified_sql, language="sql")
                    st.download_button(
                        label="下载美化SQL",
                        data=beautified_sql,
                        file_name="beautified_sql.sql",
                        mime="text/plain"
                    )
                else:
                    UIHelper.show_error("请输入SQL语句")
                    
    with sub_pages[2]:  # 语法检查
        st.subheader("SQL语法检查")
        
        sql_input = st.text_area("输入SQL语句", height=200, key="syntax_check_input")
        
        if st.button("检查语法"):
            if sql_input:
                # SQL语法验证
                validation_result = SQLFormatter.validate_sql_syntax(sql_input)
                
                st.subheader("语法检查")
                if validation_result['is_valid']:
                    st.success("✅ SQL语法正确")
                    st.write(f"检测到 {validation_result['statement_count']} 条语句")
                    
                    # 显示语句类型
                    if 'statements' in validation_result and validation_result['statements']:
                        st.subheader("语句分析")
                        
                        # 添加格式化选项
                        with st.expander("SQL格式化选项"):
                            col1, col2 = st.columns(2)
                            with col1:
                                auto_format = st.checkbox("自动格式化SQL", value=True)
                            with col2:
                                show_beauty_sql = st.checkbox("显示美化后的SQL", value=False)
                        
                        # 显示每条语句
                        for i, stmt in enumerate(validation_result['statements']):
                            stmt_text = stmt.get('text', '')
                            
                            # 根据设置决定是否格式化
                            if auto_format:
                                formatted_sql = SQLFormatter.format_sql(stmt_text)
                            else:
                                formatted_sql = stmt_text
                                
                            # 显示语句信息
                            with st.expander(f"语句 {i+1}: {stmt.get('type', 'UNKNOWN')}"):
                                st.code(formatted_sql, language="sql")
                                
                                # 根据语句类型显示不同的描述和图标
                                if stmt.get('type') == 'SELECT':
                                    st.write("📊 查询语句 - 用于从数据库检索数据")
                                elif stmt.get('type') == 'INSERT':
                                    st.write("➕ 插入语句 - 用于向数据库添加新记录")
                                elif stmt.get('type') == 'UPDATE':
                                    st.write("🔄 更新语句 - 用于修改数据库中的现有记录")
                                elif stmt.get('type') == 'DELETE':
                                    st.write("🗑️ 删除语句 - 用于从数据库中删除记录")
                                elif stmt.get('type') == 'CREATE':
                                    st.write("🏗️ 创建语句 - 用于创建数据库对象")
                                elif stmt.get('type') == 'ALTER':
                                    st.write("🔧 修改语句 - 用于更改数据库对象结构")
                                elif stmt.get('type') == 'DROP':
                                    st.write("💥 删除语句 - 用于删除数据库对象")
                                
                                # 显示美化建议
                                formatting_suggestions = SQLFormatter.get_formatting_suggestions(stmt_text)
                                with st.expander("格式化建议"):
                                    for suggestion in formatting_suggestions:
                                        st.write(f"• {suggestion}")
                                
                                # 显示美化后的SQL
                                if show_beauty_sql:
                                    with st.expander("美化后的SQL"):
                                        beautified_sql = SQLFormatter.beautify_sql(stmt_text)
                                        st.code(beautified_sql, language="sql")
                    
                    # 显示最佳实践建议
                    st.subheader("最佳实践检查")
                    
                    # 进行一些简单的最佳实践检查
                    best_practices = []
                    
                    # 检查SQL语句是否格式化良好
                    if sql_input.count("\n") < 2:
                        best_practices.append("⚠️ SQL语句未格式化：建议使用适当的缩进和换行，使SQL更易读")
                    
                    # 检查是否包含关键字大写
                    keywords = ["SELECT", "FROM", "WHERE", "JOIN", "GROUP BY", "ORDER BY", "HAVING", "INSERT", "UPDATE", "DELETE"]
                    lowercase_keywords = [kw.lower() for kw in keywords]
                    has_lowercase = any(kw in sql_input for kw in lowercase_keywords)
                    if has_lowercase:
                        best_practices.append("ℹ️ 建议将SQL关键字大写，以提高可读性")
                    
                    # 检查是否有注释
                    if "--" not in sql_input and "/*" not in sql_input:
                        best_practices.append("ℹ️ 没有发现注释：为复杂SQL添加注释有助于理解")
                    
                    # 检查是否有明确的列名而不是使用通配符
                    if "SELECT *" in sql_input.upper():
                        best_practices.append("⚠️ 使用了SELECT *：建议明确列出需要的列名")
                    
                    # 显示最佳实践结果
                    if best_practices:
                        for practice in best_practices:
                            st.write(practice)
                    else:
                        st.success("✅ 遵循了SQL的最佳实践")
                        
                    # 添加SQL复杂度分析
                    st.subheader("SQL复杂度分析")
                    
                    # 对每条语句进行复杂度分析
                    for i, stmt in enumerate(validation_result['statements']):
                        stmt_text = stmt.get('text', '')
                        complexity_result = SQLFormatter.analyze_sql_complexity(stmt_text)
                        
                        with st.expander(f"语句 {i+1} 复杂度分析"):
                            # 显示复杂度得分
                            score = complexity_result['complexity_score']
                            col1, col2 = st.columns([1, 3])
                            
                            with col1:
                                if score < 30:
                                    st.markdown(f"### 🟢 {score}/100")
                                elif score < 70:
                                    st.markdown(f"### 🟡 {score}/100")
                                else:
                                    st.markdown(f"### 🔴 {score}/100")
                                    
                            with col2:
                                level_text = {
                                    'simple': '简单查询 - 执行效率高',
                                    'moderate': '中等复杂度 - 可能需要优化',
                                    'complex': '复杂查询 - 建议重构或优化'
                                }
                                st.markdown(f"**复杂度级别**: {level_text.get(complexity_result['complexity_level'])}")
                            
                            # 显示详细指标
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("表数量", complexity_result['table_count'])
                            with col2:
                                st.metric("JOIN数量", complexity_result['join_count'])
                            with col3:
                                st.metric("条件数量", complexity_result['condition_count'])
                            with col4:
                                st.metric("子查询数量", complexity_result['subquery_count'])
                            
                            # 显示优化建议
                            if complexity_result.get('suggestions'):
                                st.subheader("优化建议")
                                for suggestion in complexity_result['suggestions']:
                                    st.info(suggestion)
                    
                    # 如果有警告，显示警告
                    if validation_result.get('warnings'):
                        st.subheader("警告")
                        for warning in validation_result['warnings']:
                            st.warning(warning)
                else:
                    st.error("❌ SQL语法错误")
                    
                    # 显示错误信息，并按错误类型分类
                    error_categories = {
                        "括号错误": [],
                        "引号错误": [],
                        "语法结构错误": [],
                        "其他错误": []
                    }
                    
                    for error in validation_result['errors']:
                        if "括号" in error:
                            error_categories["括号错误"].append(error)
                        elif "引号" in error:
                            error_categories["引号错误"].append(error)
                        elif any(keyword in error for keyword in ["FROM", "WHERE", "JOIN", "SELECT"]):
                            error_categories["语法结构错误"].append(error)
                        else:
                            error_categories["其他错误"].append(error)
                    
                    # 显示分类后的错误
                    for category, errors in error_categories.items():
                        if errors:
                            with st.expander(f"{category} ({len(errors)}个)"):
                                for error in errors:
                                    st.error(error)
                    
                    # 提供错误修复建议
                    st.subheader("错误修复指南")
                    
                    # 分析原始SQL，尝试定位问题位置
                    problem_lines = []
                    lines = sql_input.split("\n")
                    for i, line in enumerate(lines):
                        line_issues = []
                        
                        # 检查括号平衡
                        if line.count('(') != line.count(')'):
                            line_issues.append("括号不匹配")
                            
                        # 检查引号
                        single_quotes = line.count("'") - line.count("''")
                        if single_quotes % 2 != 0:
                            line_issues.append("单引号不匹配")
                            
                        # 检查SQL关键字后是否缺少内容
                        keywords_check = {
                            "SELECT": "列名",
                            "FROM": "表名",
                            "WHERE": "条件表达式",
                            "JOIN": "表名和ON条件"
                        }
                        
                        for keyword, expected in keywords_check.items():
                            pattern = rf"\b{keyword}\s*$"
                            if re.search(pattern, line, re.IGNORECASE):
                                line_issues.append(f"{keyword}后缺少{expected}")
                        
                        if line_issues:
                            problem_lines.append((i+1, line, line_issues))
                    
                    # 显示有问题的行
                    if problem_lines:
                        st.write("可能有问题的行：")
                        for line_num, line_text, issues in problem_lines:
                            with st.expander(f"第{line_num}行: {', '.join(issues)}"):
                                st.code(line_text, language="sql")
                                st.write(f"问题: {', '.join(issues)}")
                    
                    # 提供智能修复建议
                    st.write("智能修复建议：")
                    
                    # 尝试自动修复
                    fixed_sql = sql_input
                    
                    # 修复括号不匹配
                    open_brackets = fixed_sql.count('(')
                    close_brackets = fixed_sql.count(')')
                    if open_brackets > close_brackets:
                        # 缺少右括号
                        fixed_sql += ')' * (open_brackets - close_brackets)
                        st.info(f"添加 {open_brackets - close_brackets} 个右括号")
                    elif close_brackets > open_brackets:
                        st.info(f"删除 {close_brackets - open_brackets} 个多余的右括号")
                    
                    # 修复引号不匹配
                    single_quotes = fixed_sql.count("'") - fixed_sql.count("''")
                    if single_quotes % 2 != 0:
                        fixed_sql += "'"
                        st.info("添加缺少的单引号")
                    
                    # 显示可能的修复后SQL
                    if fixed_sql != sql_input:
                        with st.expander("可能的修复后SQL"):
                            st.code(fixed_sql, language="sql")
                            
                            # 提供复制按钮
                            st.download_button(
                                label="📋 复制修复后的SQL",
                                data=fixed_sql,
                                file_name="fixed_sql.sql",
                                mime="text/plain"
                            )
                    
                    # 提供一般性修复建议
                    with st.expander("常见SQL错误解决方案"):
                        common_errors = {
                            "括号不匹配": "确保所有的左括号 '(' 都有对应的右括号 ')'，尤其是在复杂表达式和子查询中",
                            "引号不匹配": "确保所有字符串的引号都成对出现，检查是否有未闭合的引号",
                            "关键字后缺少内容": "确保每个SQL关键字后都跟随适当的内容，如SELECT后需要列名，FROM后需要表名",
                            "JOIN语法错误": "确保JOIN后有表名，并且有ON或USING子句指定连接条件",
                            "缺少分号": "每个SQL语句应该以分号结束，检查是否缺少分号或分号位置不正确"
                        }
                        
                        for error_type, solution in common_errors.items():
                            st.write(f"**{error_type}**: {solution}")
                        
                        st.write("**提示**: 尝试使用SQL格式化工具来帮助识别语法错误，格式化后的SQL更易于阅读和调试")
            else:
                UIHelper.show_error("请输入SQL语句")


def render_advanced_page():
    """渲染高级功能页面"""
    UIHelper.create_section_header("高级SQL功能", "实现更复杂的SQL操作")
    
    # 子页面选择
    sub_pages = st.tabs(ADVANCED_SUB_PAGES)
    
    # 创建高级SQL生成器实例
    adv_sql_gen = AdvancedSQLGenerator()
    
    # 根据子页面渲染不同内容
    with sub_pages[0]:  # 视图管理
        st.subheader("视图管理")
        
        st.markdown("""
        视图是基于SQL查询的虚拟表，可以简化复杂查询并提供数据访问安全控制。
        """)
        
        view_name = st.text_input("视图名称", key="view_name")
        view_query = st.text_area("SELECT查询", height=150, key="view_query")
        
        if st.button("生成CREATE VIEW语句"):
            if view_name and view_query:
                view_sql = f"CREATE OR REPLACE VIEW {view_name} AS\n{view_query};"
                st.code(view_sql, language="sql")
                st.download_button(
                    label="下载SQL文件",
                    data=view_sql,
                    file_name="create_view.sql",
                    mime=MIME_TYPES['sql']
                )
            else:
                UIHelper.show_error("请输入视图名称和查询语句")
    
    with sub_pages[1]:  # 索引优化
        st.subheader("索引管理")
        
        st.markdown("""
        索引可以提高查询性能，但会占用存储空间并可能减慢数据修改操作。
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            table_name = st.text_input("表名", key="index_table")
            index_name = st.text_input("索引名称", key="index_name")
        with col2:
            columns = st.text_input("列名（多列用逗号分隔）", key="index_columns")
            index_type = st.selectbox("索引类型", ["BTREE", "HASH", "UNIQUE"], key="index_type")
        
        if st.button("生成CREATE INDEX语句"):
            if table_name and index_name and columns:
                if index_type == "UNIQUE":
                    index_sql = f"CREATE UNIQUE INDEX {index_name} ON {table_name} ({columns});"
                else:
                    index_sql = f"CREATE INDEX {index_name} ON {table_name} ({columns}) USING {index_type};"
                st.code(index_sql, language="sql")
                st.download_button(
                    label="下载SQL文件",
                    data=index_sql,
                    file_name="create_index.sql",
                    mime=MIME_TYPES['sql']
                )
            else:
                UIHelper.show_error("请输入表名、索引名称和列名")
    
    with sub_pages[2]:  # 存储过程
        st.subheader("存储过程")
        
        st.markdown("""
        存储过程是保存在数据库中的一组SQL语句，可以接受参数并执行复杂的业务逻辑。
        """)
        
        proc_name = st.text_input("存储过程名称", key="proc_name")
        
        col1, col2 = st.columns(2)
        with col1:
            params_in = st.text_area("输入参数 (例如: IN customer_id INT, IN order_date DATE)", height=100, key="params_in")
        with col2:
            params_out = st.text_area("输出参数 (例如: OUT total_amount DECIMAL(10,2))", height=100, key="params_out")
        
        proc_body = st.text_area("存储过程主体", height=200, key="proc_body")
        
        if st.button("生成CREATE PROCEDURE语句"):
            if proc_name and proc_body:
                params = []
                if params_in:
                    params.append(params_in)
                if params_out:
                    params.append(params_out)
                
                params_str = ", ".join(params)
                
                proc_sql = f"""
CREATE PROCEDURE {proc_name}({params_str})
BEGIN
    {proc_body}
END;
"""
                st.code(proc_sql, language="sql")
                st.download_button(
                    label="下载SQL文件",
                    data=proc_sql,
                    file_name="create_procedure.sql",
                    mime=MIME_TYPES['sql']
                )
            else:
                UIHelper.show_error("请输入存储过程名称和主体")
    
    with sub_pages[3]:  # 触发器
        st.subheader("触发器")
        
        st.markdown("""
        触发器是在表上执行INSERT、UPDATE或DELETE操作时自动执行的特殊存储过程。
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            trigger_name = st.text_input("触发器名称", key="trigger_name")
            table_name = st.text_input("表名", key="trigger_table")
        with col2:
            timing = st.selectbox("触发时机", ["BEFORE", "AFTER"], key="trigger_timing")
            event = st.selectbox("触发事件", ["INSERT", "UPDATE", "DELETE"], key="trigger_event")
        
        trigger_body = st.text_area("触发器主体", height=150, key="trigger_body")
        
        if st.button("生成CREATE TRIGGER语句"):
            if trigger_name and table_name and trigger_body:
                trigger_sql = f"""
CREATE TRIGGER {trigger_name}
{timing} {event} ON {table_name}
FOR EACH ROW
BEGIN
    {trigger_body}
END;
"""
                st.code(trigger_sql, language="sql")
                st.download_button(
                    label="下载SQL文件",
                    data=trigger_sql,
                    file_name="create_trigger.sql",
                    mime=MIME_TYPES['sql']
                )
            else:
                UIHelper.show_error("请输入触发器名称、表名和主体")
    
    with sub_pages[4]:  # 函数管理
        st.subheader("自定义函数")
        
        st.markdown("""
        自定义函数可以封装复杂的计算逻辑，并在SQL查询中调用。
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            func_name = st.text_input("函数名称", key="func_name")
            params = st.text_area("参数 (例如: customer_id INT, order_date DATE)", height=100, key="func_params")
        with col2:
            returns = st.text_input("返回类型", key="func_returns")
            deterministic = st.checkbox("确定性函数", key="func_deterministic")
        
        func_body = st.text_area("函数主体", height=150, key="func_body")
        
        if st.button("生成CREATE FUNCTION语句"):
            if func_name and returns and func_body:
                deterministic_str = "DETERMINISTIC" if deterministic else "NOT DETERMINISTIC"
                
                func_sql = f"""
CREATE FUNCTION {func_name}({params})
RETURNS {returns}
{deterministic_str}
BEGIN
    {func_body}
END;
"""
                st.code(func_sql, language="sql")
                st.download_button(
                    label="下载SQL文件",
                    data=func_sql,
                    file_name="create_function.sql",
                    mime=MIME_TYPES['sql']
                )
            else:
                UIHelper.show_error("请输入函数名称、返回类型和主体")
    
    with sub_pages[5]:  # 约束管理
        st.subheader("约束管理")
        
        st.markdown("""
        约束用于确保数据库中的数据符合特定的规则。
        """)
        
        constraint_type = st.selectbox("约束类型", 
                                    ["PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "CHECK", "DEFAULT"],
                                    key="constraint_type")
        
        col1, col2 = st.columns(2)
        with col1:
            table_name = st.text_input("表名", key="constraint_table")
            constraint_name = st.text_input("约束名称", key="constraint_name")
        with col2:
            columns = st.text_input("列名（多列用逗号分隔）", key="constraint_columns")
        
        # 根据约束类型显示不同的输入字段
        if constraint_type == "FOREIGN KEY":
            col1, col2 = st.columns(2)
            with col1:
                ref_table = st.text_input("引用表", key="ref_table")
            with col2:
                ref_columns = st.text_input("引用列（多列用逗号分隔）", key="ref_columns")
        elif constraint_type == "CHECK":
            check_expr = st.text_input("检查条件表达式", key="check_expr")
        elif constraint_type == "DEFAULT":
            default_value = st.text_input("默认值", key="default_value")
        
        if st.button("生成ALTER TABLE语句"):
            if table_name and constraint_name and columns:
                if constraint_type == "PRIMARY KEY":
                    constraint_sql = f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} PRIMARY KEY ({columns});"
                elif constraint_type == "UNIQUE":
                    constraint_sql = f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} UNIQUE ({columns});"
                elif constraint_type == "FOREIGN KEY" and ref_table and ref_columns:
                    constraint_sql = f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({columns}) REFERENCES {ref_table}({ref_columns});"
                elif constraint_type == "CHECK" and check_expr:
                    constraint_sql = f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} CHECK ({check_expr});"
                elif constraint_type == "DEFAULT" and default_value:
                    constraint_sql = f"ALTER TABLE {table_name} ALTER COLUMN {columns} SET DEFAULT {default_value};"
                else:
                    UIHelper.show_error("请填写所有必要字段")
                    constraint_sql = None
                
                if constraint_sql:
                    st.code(constraint_sql, language="sql")
                    st.download_button(
                        label="下载SQL文件",
                        data=constraint_sql,
                        file_name="add_constraint.sql",
                        mime=MIME_TYPES['sql']
                    )
            else:
                UIHelper.show_error("请输入表名、约束名称和列名")


def render_template_page():
    """渲染模板中心页面"""
    UIHelper.create_section_header("SQL模板中心", "常用SQL模板和示例")
    
    # 子页面选择
    sub_pages = st.tabs(TEMPLATE_SUB_PAGES)
    
    # 根据子页面渲染不同内容
    with sub_pages[0]:  # 基础查询
        st.subheader("基础查询模板")
        
        basic_queries = {
            "简单查询": "SELECT column1, column2 FROM table_name;",
            "条件查询": "SELECT * FROM table_name WHERE condition;",
            "排序查询": "SELECT * FROM table_name ORDER BY column_name [ASC|DESC];",
            "分组查询": "SELECT column_name, COUNT(*) FROM table_name GROUP BY column_name;",
            "限制结果": "SELECT * FROM table_name LIMIT 10;"
        }
        
        query_type = st.selectbox("选择查询类型", list(basic_queries.keys()), key="basic_query_type")
        
        st.code(basic_queries[query_type], language="sql")
        st.download_button(
            label="下载SQL",
            data=basic_queries[query_type],
            file_name=f"{query_type}.sql",
            mime=MIME_TYPES['sql']
        )
    
    with sub_pages[1]:  # 数据操作
        st.subheader("数据操作模板")
        
        data_operations = {
            "插入单条记录": "INSERT INTO table_name (column1, column2) VALUES (value1, value2);",
            "插入多条记录": "INSERT INTO table_name (column1, column2) VALUES (value1, value2), (value3, value4);",
            "更新记录": "UPDATE table_name SET column1 = value1, column2 = value2 WHERE condition;",
            "删除记录": "DELETE FROM table_name WHERE condition;",
            "合并记录": """
MERGE INTO target_table t
USING source_table s
ON (t.id = s.id)
WHEN MATCHED THEN
    UPDATE SET t.column1 = s.column1, t.column2 = s.column2
WHEN NOT MATCHED THEN
    INSERT (column1, column2) VALUES (s.column1, s.column2);
"""
        }
        
        operation_type = st.selectbox("选择操作类型", list(data_operations.keys()), key="operation_type")
        
        st.code(data_operations[operation_type], language="sql")
        st.download_button(
            label="下载SQL",
            data=data_operations[operation_type],
            file_name=f"{operation_type}.sql",
            mime=MIME_TYPES['sql']
        )
    
    with sub_pages[2]:  # 表结构
        st.subheader("表结构模板")
        
        structure_operations = {
            "创建表": """
CREATE TABLE table_name (
    id INT PRIMARY KEY,
    column1 VARCHAR(100) NOT NULL,
    column2 DATE,
    column3 DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""",
            "添加列": "ALTER TABLE table_name ADD COLUMN column_name data_type [constraints];",
            "修改列": "ALTER TABLE table_name MODIFY COLUMN column_name new_data_type [constraints];",
            "删除列": "ALTER TABLE table_name DROP COLUMN column_name;",
            "重命名表": "ALTER TABLE old_table_name RENAME TO new_table_name;"
        }
        
        structure_type = st.selectbox("选择结构操作类型", list(structure_operations.keys()), key="structure_type")
        
        st.code(structure_operations[structure_type], language="sql")
        st.download_button(
            label="下载SQL",
            data=structure_operations[structure_type],
            file_name=f"{structure_type}.sql",
            mime=MIME_TYPES['sql']
        )
    
    with sub_pages[3]:  # 性能优化
        st.subheader("性能优化模板")
        
        performance_queries = {
            "创建索引": "CREATE INDEX idx_name ON table_name (column_name);",
            "执行计划分析": "EXPLAIN SELECT * FROM table_name WHERE condition;",
            "统计信息更新": "ANALYZE TABLE table_name;",
            "慢查询优化": """
SELECT 
    t1.column1, 
    t1.column2,
    t2.column3
FROM 
    large_table t1
    JOIN /* 使用索引 */ another_table t2 ON t1.id = t2.id
WHERE 
    t1.status = 'active'
    AND t1.create_date > '2023-01-01'
LIMIT 100;
"""
        }
        
        perf_type = st.selectbox("选择性能优化类型", list(performance_queries.keys()), key="perf_type")
        
        st.code(performance_queries[perf_type], language="sql")
        st.download_button(
            label="下载SQL",
            data=performance_queries[perf_type],
            file_name=f"{perf_type}.sql",
            mime=MIME_TYPES['sql']
        )
    
    with sub_pages[4]:  # 数据分析
        st.subheader("数据分析模板")
        
        analysis_queries = {
            "基础统计": """
SELECT 
    COUNT(*) as total_rows,
    MIN(numeric_column) as min_value,
    MAX(numeric_column) as max_value,
    AVG(numeric_column) as average,
    SUM(numeric_column) as total
FROM table_name;
""",
            "时间序列": """
SELECT 
    DATE_TRUNC('month', date_column) as month,
    COUNT(*) as count,
    SUM(amount) as total_amount
FROM table_name
GROUP BY DATE_TRUNC('month', date_column)
ORDER BY month;
""",
            "同比环比": """
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', date_column) as month,
        SUM(amount) as total_amount
    FROM table_name
    GROUP BY DATE_TRUNC('month', date_column)
)
SELECT 
    current.month,
    current.total_amount as current_amount,
    previous.total_amount as previous_amount,
    (current.total_amount - previous.total_amount) / previous.total_amount * 100 as growth_rate
FROM 
    monthly_sales current
    LEFT JOIN monthly_sales previous ON previous.month = current.month - INTERVAL '1 month'
ORDER BY 
    current.month;
""",
            "分组聚合": """
SELECT 
    category,
    COUNT(*) as count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM table_name
GROUP BY category
ORDER BY total_amount DESC;
"""
        }
        
        analysis_type = st.selectbox("选择数据分析类型", list(analysis_queries.keys()), key="analysis_type")
        
        st.code(analysis_queries[analysis_type], language="sql")
        st.download_button(
            label="下载SQL",
            data=analysis_queries[analysis_type],
            file_name=f"{analysis_type}.sql",
            mime=MIME_TYPES['sql']
        )
    
    with sub_pages[5]:  # 自定义模板
        st.subheader("自定义模板")
        
        st.markdown("""
        在这里，您可以创建和保存自己的SQL模板。
        
        **使用步骤**：
        1. 输入模板名称
        2. 输入SQL语句
        3. 点击"保存模板"按钮
        4. 可以从下拉框中选择已保存的模板
        """)
        
        # 初始化session state来存储自定义模板
        if 'custom_templates' not in st.session_state:
            st.session_state.custom_templates = {}
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            template_name = st.text_input("模板名称", key="custom_template_name")
        
        with col2:
            if st.button("保存模板"):
                if template_name and 'custom_template_sql' in st.session_state:
                    template_sql = st.session_state.custom_template_sql
                    if template_sql:
                        st.session_state.custom_templates[template_name] = template_sql
                        st.success(f"模板 '{template_name}' 保存成功！")
                    else:
                        st.error("请先输入SQL语句")
                else:
                    st.error("请输入模板名称和SQL语句")
        
        template_sql = st.text_area("SQL语句", height=200, key="custom_template_sql")
        
        if st.session_state.custom_templates:
            st.subheader("已保存的模板")
            saved_template = st.selectbox("选择模板", list(st.session_state.custom_templates.keys()), key="saved_template")
            
            if saved_template:
                st.code(st.session_state.custom_templates[saved_template], language="sql")
                st.download_button(
                    label="下载SQL",
                    data=st.session_state.custom_templates[saved_template],
                    file_name=f"{saved_template}.sql",
                    mime=MIME_TYPES['sql']
                )


def render_history_page():
    """渲染历史记录页面"""
    UIHelper.create_section_header("历史记录", "查看和管理生成的SQL历史")
    
    # 子页面选择
    sub_pages = st.tabs(HISTORY_SUB_PAGES)
    
    # 根据子页面渲染不同内容
    with sub_pages[0]:  # 最近记录
        st.subheader("最近生成的SQL")
        
        # 初始化session state来存储历史记录
        if 'sql_history' not in st.session_state:
            st.session_state.sql_history = []
        
        if not st.session_state.sql_history:
            st.info("暂无历史记录")
        else:
            for i, record in enumerate(reversed(st.session_state.sql_history[-10:])):
                with st.expander(f"记录 {len(st.session_state.sql_history) - i}: {record['timestamp']} - {record['type']}"):
                    st.code(record['sql'], language="sql")
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        st.download_button(
                            label="下载",
                            data=record['sql'],
                            file_name=f"{record['type']}_{record['timestamp'].replace(':', '-')}.sql",
                            mime=MIME_TYPES['sql'],
                            key=f"download_history_{i}"
                        )
                    with col2:
                        if st.button("添加到收藏夹", key=f"favorite_{i}"):
                            if 'favorites' not in st.session_state:
                                st.session_state.favorites = []
                            st.session_state.favorites.append(record)
                            st.success("已添加到收藏夹！")
    
    with sub_pages[1]:  # 收藏夹
        st.subheader("收藏的SQL")
        
        # 初始化session state来存储收藏
        if 'favorites' not in st.session_state:
            st.session_state.favorites = []
        
        if not st.session_state.favorites:
            st.info("暂无收藏")
        else:
            for i, record in enumerate(st.session_state.favorites):
                with st.expander(f"收藏 {i+1}: {record['timestamp']} - {record['type']}"):
                    st.code(record['sql'], language="sql")
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        st.download_button(
                            label="下载",
                            data=record['sql'],
                            file_name=f"{record['type']}_{record['timestamp'].replace(':', '-')}.sql",
                            mime=MIME_TYPES['sql'],
                            key=f"download_favorite_{i}"
                        )
                    with col2:
                        if st.button("移出收藏夹", key=f"unfavorite_{i}"):
                            st.session_state.favorites.pop(i)
                            st.experimental_rerun()
    
    with sub_pages[2]:  # 搜索历史
        st.subheader("搜索历史记录")
        
        search_term = st.text_input("输入搜索关键词", key="history_search")
        
        if st.button("搜索"):
            if 'sql_history' not in st.session_state:
                st.session_state.sql_history = []
            
            if not st.session_state.sql_history:
                st.info("暂无历史记录")
            else:
                results = [record for record in st.session_state.sql_history if search_term.lower() in record['sql'].lower()]
                
                if not results:
                    st.info(f"未找到包含关键词 '{search_term}' 的记录")
                else:
                    st.success(f"找到 {len(results)} 条记录")
                    
                    for i, record in enumerate(results):
                        with st.expander(f"结果 {i+1}: {record['timestamp']} - {record['type']}"):
                            st.code(record['sql'], language="sql")
                            st.download_button(
                                label="下载",
                                data=record['sql'],
                                file_name=f"{record['type']}_{record['timestamp'].replace(':', '-')}.sql",
                                mime=MIME_TYPES['sql'],
                                key=f"download_search_{i}"
                            )
    
    with sub_pages[3]:  # 使用统计
        st.subheader("SQL使用统计")
        
        if 'sql_history' not in st.session_state:
            st.session_state.sql_history = []
        
        if not st.session_state.sql_history:
            st.info("暂无历史记录")
        else:
            # 统计各种SQL类型的使用次数
            sql_types = {}
            for record in st.session_state.sql_history:
                sql_type = record['type']
                if sql_type in sql_types:
                    sql_types[sql_type] += 1
                else:
                    sql_types[sql_type] = 1
            
            # 显示统计图表
            st.subheader("SQL类型使用分布")
            st.bar_chart(sql_types)
            
            # 显示统计数据
            st.subheader("使用次数统计")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("总生成次数", len(st.session_state.sql_history))
            with col2:
                st.metric("不同SQL类型", len(sql_types))
            with col3:
                most_used_type = max(sql_types, key=sql_types.get) if sql_types else "无"
                st.metric("最常用类型", most_used_type)
    
    with sub_pages[4]:  # 导出数据
        st.subheader("导出历史记录")
        
        if 'sql_history' not in st.session_state:
            st.session_state.sql_history = []
        
        if not st.session_state.sql_history:
            st.info("暂无历史记录可导出")
        else:
            export_format = st.radio("选择导出格式", ["SQL", "JSON", "CSV"], horizontal=True)
            
            if export_format == "SQL":
                # 生成一个包含所有SQL语句的文件
                all_sql = "\n\n-- " + "-" * 50 + "\n\n".join([f"-- {record['type']} - {record['timestamp']}\n{record['sql']}" for record in st.session_state.sql_history])
                
                st.download_button(
                    label="导出为SQL文件",
                    data=all_sql,
                    file_name="sql_history.sql",
                    mime=MIME_TYPES['sql']
                )
            elif export_format == "JSON":
                # 转换为JSON格式
                import json
                # 将datetime对象转换为字符串
                export_data = []
                for record in st.session_state.sql_history:
                    export_record = record.copy()
                    if isinstance(export_record['timestamp'], object) and not isinstance(export_record['timestamp'], str):
                        export_record['timestamp'] = str(export_record['timestamp'])
                    export_data.append(export_record)
                
                json_data = json.dumps(export_data, ensure_ascii=False, indent=2)
                
                st.download_button(
                    label="导出为JSON文件",
                    data=json_data,
                    file_name="sql_history.json",
                    mime=MIME_TYPES['json']
                )
            elif export_format == "CSV":
                # 转换为CSV格式
                import csv
                import io
                
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(['timestamp', 'type', 'sql'])
                
                for record in st.session_state.sql_history:
                    writer.writerow([record['timestamp'], record['type'], record['sql']])
                
                st.download_button(
                    label="导出为CSV文件",
                    data=output.getvalue(),
                    file_name="sql_history.csv",
                    mime=MIME_TYPES['csv']
                )


def render_example_page():
    """渲染streamlit例子页面"""
    from sql_generator.ui.streamlit_example import example
    example()
