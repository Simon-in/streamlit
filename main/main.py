import os
import streamlit as st
import logging as log
from sql_generate import sql_generate

if __name__ == "__main__":
    st.title("Streamlit 应用")
    page = st.sidebar.selectbox("选择页面", ["主页", "SELECT", "INSERT", "UPDATE", "MERGE", "DELETE", "TRUNCATE", "Dynamodb", "Mapping"])
    if page == "主页":
        st.header("欢迎来到主页！")
        st.write('\n')
        st.write("你可以从侧面导航栏选择你想进行的操作")
    elif page == "SELECT":
        st.header("SELECT页面 ")
        table_name = st.text_input("请输入表名")
        uploaded_file = st.file_uploader("上传文件", type=["xlsx", "csv"])
        if uploaded_file is not None:
            sql_generate = sql_generate(uploaded_file, table_name)
            select_sql = sql_generate.bulk_select()
            st.write(f"语句")
            st.code(select_sql, language='sql')
    elif page == "INSERT":
        st.header("INSERT页面")
        table_name = st.text_input("请输入表名")
        uploaded_file = st.file_uploader("上传文件", type=["xlsx", "csv"])
        if uploaded_file is not None:
            sql_generate = sql_generate(uploaded_file, table_name)
            insert_sql = sql_generate.bulk_insert()
            st.write(f"语句：")
            st.code(insert_sql, language='sql')
    elif page == "UPDATE":
        st.header("UPDATE页面")

    elif page == "DELETE":
        st.header("DELETE页面")

    elif page == "MERGE":
        st.header("MERGE页面")

    elif page == "TRUNCATE":
        st.header("TRUNCATE页面")

    elif page == "Dynamodb":
        st.header("Dynamodb页面")

    elif page == "Mapping":
        st.header("Mapping页面")

    #本地测试
    #     current_directory = os.getcwd()
    #     parent_directory = os.path.dirname(current_directory)
    #     file_path = parent_directory + "/data/test.xlsx"
    #     table_name = 'model_sci.sci_simulation_config_xinyu_test'
    #     sql_generate = sql_generate(file_path, table_name)
    #     it = sql_generate.generate_bulk_insert_statement()
    #     st = sql_generate.generate_select_statement()
    #     print("这是INSERT语句：", it)
    #     print("这是SELECT语句：", st)