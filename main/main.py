# -*- coding: utf-8 -*-
"""
Streamlit SQL生成工具主应用
"""

from PIL import Image
import streamlit as st
from SQL import SQLGenerator
from streamlit_example import example
from utils import SessionStateManager, FileHandler, UIHelper, InputValidator
from config import *
import json

# 配置页面
st.set_page_config(
    page_title=APP_CONFIG['page_title'],
    page_icon=APP_CONFIG['page_icon'],
    layout=APP_CONFIG['layout'],
    initial_sidebar_state=APP_CONFIG['initial_sidebar_state']
)

if __name__ == "__main__":
    # 初始化session state
    SessionStateManager.init_session_state()
    
    # 侧边栏导航
    st.sidebar.title("🔧 SQL生成工具")
    page = st.sidebar.selectbox("选择页面", MAIN_PAGES)

    if page == "SQL生成":
        sub_page = st.sidebar.selectbox("选择SQL功能", SQL_SUB_PAGES)
        
        if sub_page == "主页":
            UIHelper.create_section_header("🏠 欢迎使用SQL生成工具", 
                                         "这是一个强大的SQL语句生成工具，支持多种SQL操作")
            
            st.markdown("""
            ### 📋 使用说明
            1. **下载样例文件**：首次使用请先下载样例文件了解配置格式
            2. **上传配置文件**：根据样例格式准备您的Excel配置文件
            3. **选择功能**：从侧边栏选择您需要的SQL操作类型
            4. **生成并下载**：查看生成的SQL语句并下载文件
            
            ### 🔧 支持的功能
            - **CREATE**：创建表结构
            - **SELECT**：查询数据
            - **INSERT**：插入数据  
            - **UPDATE**：更新数据
            - **MERGE**：合并数据
            - **DELETE**：删除数据
            - **TRUNCATE**：清空表数据
            """)
            
            # 文件上传区域
            st.subheader("📁 文件上传")
            uploaded_file = st.file_uploader(
                "选择配置文件", 
                type=SUPPORTED_FILE_TYPES,
                help="支持CSV、TXT、XLSX格式的文件"
            )
            
            if uploaded_file is not None:
                if FileHandler.validate_file_type(uploaded_file):
                    SessionStateManager.set_uploaded_file(uploaded_file)
                    UIHelper.show_success(f"文件 '{uploaded_file.name}' 上传成功！")
                else:
                    UIHelper.show_error(f"不支持的文件类型，请上传 {', '.join(SUPPORTED_FILE_TYPES)} 格式的文件")
            
            # 样例文件下载
            st.subheader("📥 样例文件下载")
            col1, col2 = st.columns([1, 2])
            with col1:
                FileHandler.create_download_button("📋 下载样例文件", SAMPLE_FILE_PATH, 'xlsx')
            with col2:
                st.info("请下载样例文件查看各功能的配置格式")
        elif sub_page == "CREATE":
            UIHelper.create_section_header("🏗️ CREATE TABLE 语句生成", 
                                         "根据配置文件生成创建表的SQL语句")
            
            # 显示样例图片
            try:
                sample_image = Image.open(IMAGE_PATHS["create"])
                st.image(sample_image, caption="配置格式示例", use_column_width=True)
            except FileNotFoundError:
                UIHelper.show_warning("示例图片未找到")
            
            uploaded_file = SessionStateManager.get_uploaded_file()
            if uploaded_file is not None:
                sql_generator = SQLGenerator()
                create_sql_list = sql_generator.bulk_create(uploaded_file)
                
                if create_sql_list:
                    formatted_sql = sql_generator.sql_formatted(create_sql_list)
                    UIHelper.display_sql_with_download(formatted_sql, "create.sql", "🏗️ CREATE TABLE 语句")
                else:
                    UIHelper.show_warning("未能生成CREATE语句，请检查文件格式")
            else:
                UIHelper.show_info("请先在主页上传配置文件")

        elif sub_page == "SELECT":
            UIHelper.create_section_header("🔍 SELECT 语句生成", 
                                         "生成查询数据的SQL语句")
            
            select_mode = st.sidebar.selectbox("选择模式", SELECT_SUB_PAGES)
            
            if select_mode == "单张表":
                st.subheader("📝 单表查询")
                
                col1, col2 = st.columns(2)
                with col1:
                    table_name = st.text_input("表名", placeholder="例如：users 或 schema.users")
                with col2:
                    column_list = st.text_input("字段列表", placeholder="例如：id, name, email")
                
                if st.button("生成SELECT语句", type="primary"):
                    if table_name and column_list:
                        # 验证输入
                        if not InputValidator.validate_table_name(table_name):
                            UIHelper.show_error("表名格式不正确")
                        elif not InputValidator.validate_column_list(column_list):
                            UIHelper.show_error("字段列表格式不正确")
                        else:
                            sql_generator = SQLGenerator()
                            select_sql = sql_generator.bulk_select(None, table_name.strip(), column_list.strip())
                            if select_sql:
                                UIHelper.display_sql_with_download(select_sql, "select_single.sql", "🔍 SELECT 语句")
                    else:
                        UIHelper.show_warning("请输入表名和字段列表")
                        
            elif select_mode == "批量生成多表":
                st.subheader("📊 批量多表查询")
                
                # 显示样例图片
                try:
                    sample_image = Image.open(IMAGE_PATHS["select"])
                    st.image(sample_image, caption="配置格式示例", use_column_width=True)
                except FileNotFoundError:
                    UIHelper.show_warning("示例图片未找到")
                
                uploaded_file = SessionStateManager.get_uploaded_file()
                if uploaded_file is not None:
                    sql_generator = SQLGenerator()
                    select_sql_list = sql_generator.bulk_select(uploaded_file, None, None)
                    
                    if select_sql_list:
                        formatted_sql = sql_generator.sql_formatted(select_sql_list)
                        UIHelper.display_sql_with_download(formatted_sql, "select_batch.sql", "🔍 批量SELECT 语句")
                    else:
                        UIHelper.show_warning("未能生成SELECT语句，请检查文件格式")
                else:
                    UIHelper.show_info("请先在主页上传配置文件")

        elif sub_page == "INSERT":
            UIHelper.create_section_header("➕ INSERT 语句生成", 
                                         "根据配置文件生成插入数据的SQL语句")
            
            # 显示样例图片（如果存在）
            insert_image_path = IMAGE_PATHS.get("insert", "main/image/insert.png")
            try:
                sample_image = Image.open(insert_image_path)
                st.image(sample_image, caption="配置格式示例", use_column_width=True)
            except FileNotFoundError:
                UIHelper.show_warning("示例图片未找到")
            
            uploaded_file = SessionStateManager.get_uploaded_file()
            if uploaded_file is not None:
                sql_generator = SQLGenerator()
                insert_sql_list = sql_generator.bulk_insert(uploaded_file)
                
                if insert_sql_list:
                    formatted_sql = sql_generator.sql_formatted(insert_sql_list)
                    UIHelper.display_sql_with_download(formatted_sql, "insert.sql", "➕ INSERT 语句")
                else:
                    UIHelper.show_warning("未能生成INSERT语句，请检查文件格式")
            else:
                UIHelper.show_info("请先在主页上传配置文件")

        elif sub_page == "TRUNCATE":
            UIHelper.create_section_header("🗑️ TRUNCATE 语句生成", 
                                         "生成清空表数据的SQL语句")
            
            truncate_mode = st.sidebar.selectbox("选择模式", ["单张表", "批量生成多表", "全删全插"])
            
            if truncate_mode == "单张表":
                st.subheader("📝 单表TRUNCATE")
                
                table_name = st.text_input("表名", placeholder="例如：users 或 schema.users")
                
                if st.button("生成TRUNCATE语句", type="primary"):
                    if table_name:
                        if InputValidator.validate_table_name(table_name):
                            sql_generator = SQLGenerator()
                            truncate_sql_list = sql_generator.bulk_truncate(table_name=table_name.strip())
                            if truncate_sql_list:
                                formatted_sql = sql_generator.sql_formatted(truncate_sql_list)
                                UIHelper.display_sql_with_download(formatted_sql, "truncate_single.sql", "🗑️ TRUNCATE 语句")
                        else:
                            UIHelper.show_error("表名格式不正确")
                    else:
                        UIHelper.show_warning("请输入表名")
                        
            elif truncate_mode == "批量生成多表":
                st.subheader("📊 批量TRUNCATE")
                
                # 显示样例图片
                try:
                    sample_image = Image.open("main/image/truncate.png")
                    st.image(sample_image, caption="配置格式示例", use_column_width=True)
                except FileNotFoundError:
                    UIHelper.show_warning("示例图片未找到")
                
                uploaded_file = SessionStateManager.get_uploaded_file()
                if uploaded_file is not None:
                    sql_generator = SQLGenerator()
                    truncate_sql_list = sql_generator.bulk_truncate(uploaded_file, mode='simple')
                    
                    if truncate_sql_list:
                        formatted_sql = sql_generator.sql_formatted(truncate_sql_list)
                        UIHelper.display_sql_with_download(formatted_sql, "truncate_batch.sql", "🗑️ 批量TRUNCATE 语句")
                    else:
                        UIHelper.show_warning("未能生成TRUNCATE语句，请检查文件格式")
                else:
                    UIHelper.show_info("请先在主页上传配置文件")
                    
            elif truncate_mode == "全删全插":
                st.subheader("🔄 TRUNCATE + INSERT")
                
                # 显示样例图片
                try:
                    sample_image = Image.open("main/image/truncate_1.png")
                    st.image(sample_image, caption="配置格式示例", use_column_width=True)
                except FileNotFoundError:
                    UIHelper.show_warning("示例图片未找到")
                
                uploaded_file = SessionStateManager.get_uploaded_file()
                if uploaded_file is not None:
                    sql_generator = SQLGenerator()
                    truncate_sql_list = sql_generator.bulk_truncate(uploaded_file, mode='with_insert')
                    
                    if truncate_sql_list:
                        formatted_sql = sql_generator.sql_formatted(truncate_sql_list)
                        UIHelper.display_sql_with_download(formatted_sql, "truncate_insert.sql", "🔄 TRUNCATE + INSERT 语句")
                    else:
                        UIHelper.show_warning("未能生成TRUNCATE语句，请检查文件格式")
                else:
                    UIHelper.show_info("请先在主页上传配置文件")

        elif sub_page == "UPDATE":
            UIHelper.create_section_header("✏️ UPDATE 语句生成", 
                                         "UPDATE功能正在开发中")
            
            st.info("🚧 UPDATE功能正在开发中，敬请期待！")
            
            # 可以添加一个简单的UPDATE生成器
            with st.expander("💡 简单UPDATE生成器"):
                col1, col2 = st.columns(2)
                with col1:
                    table_name = st.text_input("表名", key="update_table")
                    set_clause = st.text_input("SET子句", placeholder="例如：name = 'John', age = 30")
                with col2:
                    where_clause = st.text_input("WHERE条件", placeholder="例如：id = 1")
                
                if st.button("生成UPDATE语句"):
                    if all([table_name, set_clause, where_clause]):
                        update_sql = f"UPDATE {table_name} \nSET {set_clause} \nWHERE {where_clause};"
                        UIHelper.display_sql_with_download(update_sql, "update.sql", "✏️ UPDATE 语句")
                    else:
                        UIHelper.show_warning("请填写所有必需字段")

        elif sub_page == "DELETE":
            UIHelper.create_section_header("🗑️ DELETE 语句生成", 
                                         "生成删除并重新插入数据的SQL语句")
            
            delete_mode = st.sidebar.selectbox("选择模式", ["单张表", "批量生成多表"])
            
            if delete_mode == "单张表":
                st.subheader("📝 单表DELETE + INSERT")
                
                col1, col2 = st.columns(2)
                with col1:
                    target_table = st.text_input("目标表名", placeholder="例如：target_table")
                    column = st.text_input("字段列表", placeholder="例如：id, name, email")
                with col2:
                    uniqueid = st.text_input("增量字段", placeholder="例如：id")
                    source_table = st.text_input("源表名", placeholder="例如：staging_table")
                
                if st.button("生成DELETE语句", type="primary"):
                    if all([target_table, column, uniqueid, source_table]):
                        # 验证输入
                        if not InputValidator.validate_table_name(target_table):
                            UIHelper.show_error("目标表名格式不正确")
                        elif not InputValidator.validate_table_name(source_table):
                            UIHelper.show_error("源表名格式不正确")
                        else:
                            sql_generator = SQLGenerator()
                            delete_sql = sql_generator.bulk_delete(
                                None, target_table.strip(), column.strip(), 
                                uniqueid.strip(), source_table.strip()
                            )
                            if delete_sql:
                                UIHelper.display_sql_with_download(delete_sql, "delete_single.sql", "🗑️ DELETE + INSERT 语句")
                    else:
                        UIHelper.show_warning("请填写所有必需字段")
                        
            elif delete_mode == "批量生成多表":
                st.subheader("📊 批量DELETE + INSERT")
                
                # 显示样例图片
                try:
                    sample_image = Image.open("main/image/delete.png")
                    st.image(sample_image, caption="配置格式示例", use_column_width=True)
                except FileNotFoundError:
                    UIHelper.show_warning("示例图片未找到")
                
                uploaded_file = SessionStateManager.get_uploaded_file()
                if uploaded_file is not None:
                    sql_generator = SQLGenerator()
                    delete_sql_list = sql_generator.bulk_delete(uploaded_file)
                    
                    if delete_sql_list:
                        formatted_sql = sql_generator.sql_formatted(delete_sql_list)
                        UIHelper.display_sql_with_download(formatted_sql, "delete_batch.sql", "🗑️ 批量DELETE + INSERT 语句")
                    else:
                        UIHelper.show_warning("未能生成DELETE语句，请检查文件格式")
                else:
                    UIHelper.show_info("请先在主页上传配置文件")

        elif sub_page == "MERGE":
            UIHelper.create_section_header("🔄 MERGE 语句生成", 
                                         "根据配置文件生成合并数据的SQL语句")
            
            # 显示样例图片
            try:
                sample_image = Image.open(IMAGE_PATHS["merge"])
                st.image(sample_image, caption="配置格式示例", use_column_width=True)
            except FileNotFoundError:
                UIHelper.show_warning("示例图片未找到")
            
            uploaded_file = SessionStateManager.get_uploaded_file()
            if uploaded_file is not None:
                sql_generator = SQLGenerator()
                merge_sql_list = sql_generator.bulk_merge(uploaded_file)
                
                if merge_sql_list:
                    formatted_sql = sql_generator.sql_formatted(merge_sql_list)
                    UIHelper.display_sql_with_download(formatted_sql, "merge.sql", "🔄 MERGE 语句")
                else:
                    UIHelper.show_warning("未能生成MERGE语句，请检查文件格式")
            else:
                    UIHelper.show_info("请先在主页上传配置文件")

    elif page == "高级功能":
        from advanced_sql import AdvancedSQLGenerator
        
        sub_page = st.sidebar.selectbox("选择高级功能", ADVANCED_SUB_PAGES)
        advanced_sql = AdvancedSQLGenerator()
        
        if sub_page == "视图管理":
            UIHelper.create_section_header("👁️ 视图管理", "创建和管理数据库视图")
            
            col1, col2 = st.columns(2)
            with col1:
                view_name = st.text_input("视图名称", placeholder="例如：user_summary")
                schema = st.text_input("模式名称（可选）", placeholder="例如：public")
            with col2:
                select_query = st.text_area("SELECT查询语句", 
                                          placeholder="SELECT id, name, email FROM users WHERE status = 'active'",
                                          height=100)
            
            if st.button("生成CREATE VIEW语句", type="primary"):
                if view_name and select_query:
                    view_sql = advanced_sql.generate_view(view_name, select_query, schema)
                    if view_sql:
                        UIHelper.display_sql_with_download(view_sql, f"create_view_{view_name}.sql", "👁️ CREATE VIEW 语句")
                else:
                    UIHelper.show_warning("请填写视图名称和查询语句")
        
        elif sub_page == "索引优化":
            UIHelper.create_section_header("🚀 索引优化", "创建和管理数据库索引")
            
            col1, col2 = st.columns(2)
            with col1:
                table_name = st.text_input("表名", placeholder="例如：users")
                index_name = st.text_input("索引名称（可选）", placeholder="自动生成")
                columns_input = st.text_input("索引列", placeholder="例如：email, status")
            with col2:
                unique = st.checkbox("唯一索引")
                index_type = st.selectbox("索引类型", ["BTREE", "HASH", "FULLTEXT"])
            
            if st.button("生成CREATE INDEX语句", type="primary"):
                if table_name and columns_input:
                    columns = [col.strip() for col in columns_input.split(',')]
                    index_sql = advanced_sql.generate_index(table_name, columns, index_name, unique, index_type)
                    if index_sql:
                        UIHelper.display_sql_with_download(index_sql, f"create_index_{table_name}.sql", "🚀 CREATE INDEX 语句")
                else:
                    UIHelper.show_warning("请填写表名和索引列")
        
        elif sub_page == "存储过程":
            UIHelper.create_section_header("⚙️ 存储过程", "创建存储过程")
            
            proc_name = st.text_input("存储过程名称", placeholder="例如：UpdateUserStatus")
            schema = st.text_input("模式名称（可选）", placeholder="例如：public")
            
            st.subheader("参数设置")
            if 'proc_params' not in st.session_state:
                st.session_state.proc_params = []
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                param_name = st.text_input("参数名", key="param_name")
            with col2:
                param_type = st.text_input("参数类型", key="param_type", placeholder="INT, VARCHAR(100)")
            with col3:
                param_direction = st.selectbox("方向", ["IN", "OUT", "INOUT"], key="param_direction")
            with col4:
                if st.button("添加参数"):
                    if param_name and param_type:
                        st.session_state.proc_params.append({
                            'name': param_name,
                            'type': param_type,
                            'direction': param_direction
                        })
                        st.rerun()
            
            if st.session_state.proc_params:
                st.write("当前参数：")
                for i, param in enumerate(st.session_state.proc_params):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"{param['direction']} {param['name']} {param['type']}")
                    with col2:
                        if st.button("删除", key=f"del_param_{i}"):
                            st.session_state.proc_params.pop(i)
                            st.rerun()
            
            proc_body = st.text_area("存储过程体", 
                                   placeholder="DECLARE result INT DEFAULT 0;\nSELECT COUNT(*) INTO result FROM users;\nSELECT result;",
                                   height=150)
            
            if st.button("生成CREATE PROCEDURE语句", type="primary"):
                if proc_name and proc_body:
                    proc_sql = advanced_sql.generate_stored_procedure(proc_name, st.session_state.proc_params, proc_body, schema)
                    if proc_sql:
                        UIHelper.display_sql_with_download(proc_sql, f"create_procedure_{proc_name}.sql", "⚙️ CREATE PROCEDURE 语句")
                else:
                    UIHelper.show_warning("请填写存储过程名称和过程体")

    elif page == "模板中心":
        from sql_templates import SQLTemplateManager, CommonSQLPatterns
        
        sub_page = st.sidebar.selectbox("选择模板类型", TEMPLATE_SUB_PAGES)
        template_manager = SQLTemplateManager()
        
        if sub_page == "基础查询":
            UIHelper.create_section_header("🔍 基础查询模板", "常用的基础查询语句模板")
            
            templates = template_manager.get_templates_by_category("basic_queries")
            
            template_choice = st.selectbox("选择模板", list(templates.keys()), 
                                         format_func=lambda x: templates[x].get('name', x))
            
            if template_choice:
                template_info = templates[template_choice]
                
                st.subheader(f"📋 {template_info['name']}")
                st.write(template_info['description'])
                
                # 显示示例
                with st.expander("查看示例"):
                    st.code(template_info['example'], language='sql')
                
                # 参数输入
                st.subheader("参数设置")
                parameters = {}
                for param in template_info['parameters']:
                    parameters[param] = st.text_input(f"{param}:", key=f"param_{param}")
                
                if st.button("生成SQL", type="primary"):
                    if all(parameters.values()):
                        rendered_sql = template_manager.render_template(template_info['template'], parameters)
                        UIHelper.display_sql_with_download(rendered_sql, f"{template_choice}.sql", f"🔍 {template_info['name']}")
                    else:
                        UIHelper.show_warning("请填写所有参数")

    elif page == "历史记录":
        from history_manager import HistoryManager
        
        sub_page = st.sidebar.selectbox("选择功能", HISTORY_SUB_PAGES)
        history_manager = HistoryManager()
        
        if sub_page == "最近记录":
            UIHelper.create_section_header("📚 最近记录", "查看最近生成的SQL语句")
            
            # 过滤选项
            col1, col2, col3 = st.columns(3)
            with col1:
                operation_filter = st.selectbox("操作类型", ["全部"] + SQL_SUB_PAGES[1:])
            with col2:
                limit = st.number_input("显示条数", min_value=10, max_value=100, value=20)
            with col3:
                show_favorites_only = st.checkbox("仅显示收藏")
            
            # 获取记录
            operation_type = None if operation_filter == "全部" else operation_filter
            records = history_manager.get_history_records(limit=limit, operation_type=operation_type)
            
            if show_favorites_only:
                records = [r for r in records if r.get('favorite')]
            
            if records:
                for record in records:
                    with st.expander(f"{record['operation_type']} - {record['created_at'][:19]}"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.code(record['sql_content'], language='sql')
                        with col2:
                            favorite_icon = "⭐" if record.get('favorite') else "☆"
                            if st.button(f"{favorite_icon} 收藏", key=f"fav_{record['id']}"):
                                history_manager.toggle_favorite(record['id'])
                                st.rerun()
                            
                            if st.button("🗑️ 删除", key=f"del_{record['id']}"):
                                history_manager.delete_record(record['id'])
                                st.rerun()
                        
                        if record.get('user_notes'):
                            st.write(f"备注: {record['user_notes']}")
            else:
                st.info("暂无历史记录")

    elif page == "数据分析":
        from advanced_sql import DataAnalyzer, SQLFormatter
        
        sub_page = st.sidebar.selectbox("选择分析功能", ANALYSIS_SUB_PAGES)
        
        if sub_page == "文件分析":
            UIHelper.create_section_header("📊 文件结构分析", "分析Excel文件的结构和内容")
            
            uploaded_file = st.file_uploader("选择要分析的文件", type=['xlsx', 'xls', 'csv'])
            
            if uploaded_file:
                if uploaded_file.name.endswith(('.xlsx', '.xls')):
                    analysis_result = DataAnalyzer.analyze_excel_structure(uploaded_file)
                    
                    if analysis_result:
                        st.subheader("📋 文件概况")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("工作表数量", analysis_result['total_sheets'])
                        with col2:
                            st.metric("文件大小", f"{analysis_result['file_size']/1024:.1f} KB")
                        with col3:
                            st.metric("工作表", len(analysis_result['sheet_names']))
                        
                        st.subheader("📑 工作表详情")
                        for sheet_name, info in analysis_result['sheet_info'].items():
                            with st.expander(f"工作表: {sheet_name}"):
                                if 'error' in info:
                                    st.error(f"读取错误: {info['error']}")
                                else:
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"行数: {info['rows']}")
                                        st.write(f"列数: {info['columns']}")
                                    with col2:
                                        st.write("列名:")
                                        st.write(info['column_names'])
                                    
                                    if info['sample_data']:
                                        st.write("数据预览:")
                                        st.dataframe(info['sample_data'])
        
        elif sub_page == "SQL格式化":
            UIHelper.create_section_header("✨ SQL格式化", "美化和格式化SQL语句")
            
            sql_input = st.text_area("输入SQL语句", height=200, 
                                   placeholder="SELECT * FROM users WHERE status = 'active'")
            
            col1, col2 = st.columns(2)
            with col1:
                format_style = st.selectbox("格式化风格", ["standard", "compact", "pretty"])
            with col2:
                if st.button("格式化SQL", type="primary"):
                    if sql_input:
                        formatted_sql = SQLFormatter.format_sql(sql_input, format_style)
                        st.subheader("格式化结果")
                        st.code(formatted_sql, language='sql')
                        
                        # 提供下载
                        st.download_button(
                            label="📥 下载格式化后的SQL",
                            data=formatted_sql,
                            file_name="formatted.sql",
                            mime="application/sql"
                        )
            
            if sql_input:
                # SQL语法验证
                validation_result = SQLFormatter.validate_sql_syntax(sql_input)
                
                st.subheader("语法检查")
                if validation_result['is_valid']:
                    st.success("✅ SQL语法正确")
                    st.write(f"检测到 {validation_result['statement_count']} 条语句")
                else:
                    st.error("❌ SQL语法错误")
                    for error in validation_result['errors']:
                        st.error(error)

    elif page == 'streamlit_example':
        UIHelper.create_section_header("📚 Streamlit 示例", 
                                     "学习和体验Streamlit各种组件的使用方法")
        
        sub_page = st.sidebar.selectbox("选择示例", EXAMPLE_SUB_PAGES)
        
        if sub_page == '主页':
            st.markdown("""
            ### 🎯 Streamlit组件示例
            
            本页面展示了常用的Streamlit组件使用方法，包括：
            
            - **Button** 🔘 - 按钮组件的使用
            - **Write** ✍️ - 文本和数据显示
            - **Slider** 🎚️ - 滑块组件
            - **Line Chart** 📊 - 折线图展示
            - **Selectbox** 📋 - 选择框组件
            
            请从侧边栏选择您想要查看的示例。
            """)
            
        elif sub_page == 'button':
            example.button()
        elif sub_page == 'write':
            example.write()
        elif sub_page == 'slider':
            example.slider()
        elif sub_page == 'line_chart':
            example.line_chart()
        elif sub_page == 'selectbox':
            example.select_box()
