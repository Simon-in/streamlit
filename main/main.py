from PIL import Image
import streamlit as st
from SQL import sql
from example import example
import json


if __name__ == "__main__":
    page = st.sidebar.selectbox("选择页面",
                                ["SQL", "example"])

    if page == "SQL":
        sub_page = st.sidebar.selectbox("选择页面",
                                    ["主页", "CREATE", "SELECT", "INSERT", "UPDATE", "MERGE", "DELETE", "TRUNCATE"])
        # , "Dynamodb", "Mapping"
        if sub_page == "主页":
            st.header("欢迎来到主页！")
            st.write('\n')
            st.markdown(
                "在上传文件前请下载样例文件查看如何配置后,\n"
                "你可以从侧面导航栏选择你想进行的操作,\n"
                "复制sql语句或者下载sql文件"
            )
            sql.download_button("样例下载", r"main/static/main_static_样例 - Copy.xlsx", 'xlsx')
            uploaded_file = st.file_uploader("上传文件", type=["csv", "txt", "xlsx"])
            if uploaded_file is not None:
                st.session_state.uploaded_file = uploaded_file
                st.success("文件上传成功！")
        elif sub_page == "CREATE":
            st.header("CREATE页面 ")
            sample_image = Image.open("main/image/create.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.session_state.uploaded_file
            create_sql = sql.bulk_create(uploaded_file)
            sql = sql.sql_formatted(create_sql)
            st.write(f"语句")
            st.code(sql, language='sql')
            st.download_button(
                label="Download sql",
                data=sql,
                file_name="create.sql",
                mime="application/sql"
            )

        elif sub_page == "SELECT":
            st.header("SELECT页面 ")
            page_1 = st.sidebar.selectbox("选择页面", ["单张表", "批量生成多表"])
            if page_1 == "单张表":
                table_name = None
                column_list = None
                if table_name is None and column_list is None:
                    table_name = st.text_input("请输入表名")
                    column_list = st.text_input("请输入字段")
                    if table_name and column_list:
                        select_sql = sql.bulk_select(None, table_name, column_list)
                        st.write(f"语句")
                        st.code(select_sql, language='sql')
            elif page_1 == "批量生成多表":
                sample_image = Image.open("main/image/select.png")
                st.image(sample_image, caption="样例图片", use_column_width=True)
                uploaded_file = st.session_state.uploaded_file
                select_sql = sql.bulk_select(uploaded_file, None, None)
                sql = sql.sql_formatted(select_sql)
                st.write(f"语句")
                st.code(sql, language='sql')
                st.download_button(
                    label="Download sql",
                    data=sql,
                    file_name="select.sql",
                    mime="application/sql"
                )

        elif sub_page == "INSERT":
            st.header("INSERT页面")
            sample_image = Image.open("main/image/insert.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.session_state.uploaded_file
            insert_sql = sql.bulk_insert(uploaded_file)
            sql = sql.sql_formatted(insert_sql)
            st.write(f"语句：")
            st.code(sql, language='sql')
            st.download_button(
                label="Download sql",
                data=sql,
                file_name="insert.sql",
                mime="application/sql"
            )

        elif sub_page == "TRUNCATE":
            st.header("TRUNCATE页面")
            sub_sub_page = st.sidebar.selectbox("选择页面", ["单张表", "批量生成多表", "全删全插"])
            if sub_sub_page == "单张表":
                table = None
                if table is None:
                    table = st.text_input("请输入表名")
                truncate_sql = f"TRUNCATE TABLE {table};"
                st.write(f"语句：")
                st.code(truncate_sql, language='sql')
            elif sub_sub_page == "批量生成多表":
                sample_image = Image.open("main/image/truncate.png")
                st.image(sample_image, caption="样例图片", use_column_width=True)
                uploaded_file = st.session_state.uploaded_file
                truncate_sql = sql.bulk_truncate(uploaded_file, None)
                sql = sql.sql_formatted(truncate_sql)
                st.write(f"语句")
                st.code(sql, language='sql')
                st.download_button(
                    label="Download sql",
                    data=sql,
                    file_name="truncate.sql",
                    mime="application/sql"
                )
            elif sub_sub_page == "全删全插":
                sample_image = Image.open("main/image/truncate_1.png")
                st.image(sample_image, caption="样例图片", use_column_width=True)
                uploaded_file = st.session_state.uploaded_file
                a = 1
                truncate_sql = sql.bulk_truncate(uploaded_file, a)
                sql = sql.sql_formatted(truncate_sql)
                st.write(f"语句")
                st.code(sql, language='sql')
                st.download_button(
                    label="Download sql",
                    data=sql,
                    file_name="truncate.sql",
                    mime="application/sql"
                )

        elif sub_page == "UPDATE":  # 暂时没有想到批量化
            st.header("UPDATE页面")
            st.write(f"暂时没有想法")

        elif sub_page == "DELETE":
            st.header("DELETE页面")
            sub_sub_page = st.sidebar.selectbox("选择页面", ["单张表", "批量生成多表"])
            if sub_sub_page == "单张表":
                target_table = None
                column = None
                uniqueid = None
                source_table = None
                if target_table is None and column is None and uniqueid is None and source_table is None:
                    target_table = st.text_input("请输入表名")
                    column = st.text_input("请输入字段")
                    uniqueid = st.text_input('请输入增量字段如 ID 等')
                    source_table = st.text_input('请输入staging层表')
                    delete_sql = sql.bulk_delete(None, target_table, column, uniqueid, source_table)
                    st.write(f"语句：")
                    st.code(delete_sql, language='sql')

            elif sub_sub_page == "批量生成多表":
                sample_image = Image.open("main/image/delete.png")
                st.image(sample_image, caption="样例图片", use_column_width=True)
                uploaded_file = st.session_state.uploaded_file
                delete_sql = sql.bulk_delete(uploaded_file, None, None, None, None)
                sql = sql.sql_formatted(delete_sql)
                st.write(f"语句")
                st.code(sql, language='sql')
                st.download_button(
                    label="Download sql",
                    data=sql,
                    file_name="delete.sql",
                    mime="application/sql"
                )

        elif sub_page == "MERGE":
            st.header("MERGE页面")
            sample_image = Image.open("main/image/merge.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.session_state.uploaded_file
            merge_sql = sql.bulk_merge(uploaded_file)
            sql = sql.sql_formatted(merge_sql)
            st.write(f"语句")
            st.code(sql, language='sql')
            st.download_button(
                label="Download sql",
                data=sql,
                file_name="merge.sql",
                mime="application/sql"
            )

    elif page == 'example':
        page = st.sidebar.selectbox("选择示例页面",
                                    ["主页", "button", "write", "slider", "line_chart", "selectbox"])
        if page == 'button':
            example.button()
        elif page == 'write':
            example.write()
        elif page == 'slider':
            example.slider()
        elif page == 'line_chart':
            example.line_chart()
        elif page == 'selectbox':
            example.select_box()
