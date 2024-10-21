import streamlit as st
import logging as log
from PIL import Image
from sql_generate import bulk_insert, bulk_select

if __name__ == "__main__":
    logger = log.getLogger('console')
    logger.setLevel(log.DEBUG)  # 设置成 DEBUG 默认会把 INFO WARNING ERROR CRITICAL 都输出
    ch = log.StreamHandler()
    ch.setLevel(log.DEBUG)
    formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    st.title("Streamlit 应用")
    page = st.sidebar.selectbox("选择页面",
                                ["主页", "SELECT", "INSERT", "UPDATE", "MERGE", "DELETE", "TRUNCATE", "Dynamodb", "Mapping"])
    if page == "主页":
        st.header("欢迎来到主页！")
        st.write('\n')
        st.write("你可以从侧面导航栏选择你想进行的操作")
    elif page == "SELECT":
        st.header("SELECT页面 ")
        page_1 = st.sidebar.selectbox("选择页面",["单张表", "批量生成多表"])
        if page_1 == "单张表":
            st.header("生成单张表Select语句")
            table_name = None
            column_list = None
            if table_name is None and column_list is None:
                table_name = st.text_input("请输入表名")
                column_list = st.text_input("请输入字段")
                if table_name and column_list:
                    select_sql = bulk_select(None, table_name, column_list)
                    st.write(f"语句")
                    st.code(select_sql, language='sql')
        elif page_1 == "批量生成多表":
            st.header("生成多张表Select语句")
            sample_image = Image.open("image/select.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.file_uploader("上传文件", type=["xlsx", "csv"])
            if uploaded_file is not None:
                select_sql = bulk_select(uploaded_file, None, None)
                st.write(f"语句")
                st.code(select_sql, language='sql')

    elif page == "INSERT":
        st.header("INSERT页面")
        sample_image = Image.open("image/insert.png")
        st.image(sample_image, caption="样例图片", use_column_width=True)
        table_name = st.text_input("请输入表名")
        uploaded_file = st.file_uploader("上传文件", type=["xlsx", "csv"])
        if uploaded_file is not None:
            insert_sql = bulk_insert(uploaded_file, table_name)
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
