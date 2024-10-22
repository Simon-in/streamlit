import streamlit as st
import logging as log
from PIL import Image
import pandas as pd


logger = log.getLogger('console')
logger.setLevel(log.DEBUG)  # 设置成 DEBUG 默认会把 INFO WARNING ERROR CRITICAL 都输出
ch = log.StreamHandler()
ch.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)


def bulk_select(path, table, column):
    if not path:
        select_statement = f"SELECT {''.join(column)} FROM {table};"
        return select_statement
    elif path:
        df = pd.read_excel(path)
        table_field_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        select_statement = []
        for table, field in table_field_dict.items():
            sql = f"SELECT {field} FROM {table};"
            select_statement.append(sql)
        cleaned_statements = [stmt.strip() for stmt in select_statement if stmt.strip()]
        select_statement = "\n".join(cleaned_statements)
        return select_statement


def bulk_insert(path):
    df = pd.read_excel(path)
    df_list = []
    isrt_list = []
    for i in range(df.__len__()):
        df_dict = {}
        df_dict['table'] = df.iloc[i, 0]
        df_dict['column'] = df.iloc[i, 1]
        df_dict['values'] = df.iloc[i, 2]
        df_list.append(df_dict)
    for info in df_list:
        insert_statement = (
            f"INSERT INTO {info.get('table')} "
            f" ({info.get('column')}) "
            f"VALUES ("
            f"{info.get('values')}"
            f");"
        )
        isrt_list.append(insert_statement)
    cleaned_statements = [stmt.strip() for stmt in isrt_list if stmt.strip()]
    insert_statement = "\n".join(cleaned_statements)
    return insert_statement


def bulk_update(self):
    pass


def bulk_delete(path, table, column, del_column, tmp_table):
    if path is None:
        delete_statement = f"delete from {table}" \
                           f" where {del_column} in (" \
                           f"select {del_column} from {tmp_table}) " \
                           f"insert into {table}" \
                           f" ({column}) " \
                           f"select {column}" \
                           f" from {tmp_table};"
        return delete_statement
    else:
        df = pd.read_excel(path)
        df_list = []
        del_list = []
        for i in range(df.__len__()):
            df_dict = {}
            df_dict['table'] = df.iloc[i, 0]
            df_dict['column'] = df.iloc[i, 1]
            df_dict['del_column'] = df.iloc[i, 2]
            df_dict['tmp_table'] = df.iloc[i, 3]
            df_list.append(df_dict)
        for info in df_list:
            delete_statement = (
                f"DELETE FROM {info.get('table')} "
                f"WHERE {info.get('del_column')} IN ("
                f"SELECT {info.get('del_column')} FROM {info.get('tmp_table')}); "
                f"INSERT INTO {info.get('table')} "
                f"({info.get('column')}) "
                f"SELECT {info.get('column')} "
                f"FROM {info.get('tmp_table')};"
            )
            del_list.append(delete_statement)
        cleaned_statements = [stmt.strip() for stmt in del_list if stmt.strip()]
        delete_statement = "\n".join(cleaned_statements)
        return delete_statement


def bulk_merge(self):
    pass


def bulk_truncate(table):
    trun_list = []
    for i in range(table.__len__()):
        sql = f"truncate table {table[i]};"
        trun_list.append(sql)
    cleaned_statements = [stmt.strip() for stmt in trun_list if stmt.strip()]
    truncate_statement = "\n".join(cleaned_statements)
    return truncate_statement


if __name__ == "__main__":
    st.title("Streamlit 应用")
    page = st.sidebar.selectbox("选择页面",
                                ["主页", "SELECT", "INSERT", "UPDATE", "MERGE", "DELETE", "TRUNCATE", "Dynamodb", "Mapping"])
    if page == "主页":
        st.header("欢迎来到主页！")
        st.write('\n')
        st.write("你可以从侧面导航栏选择你想进行的操作")
    elif page == "SELECT":
        st.header("SELECT页面 ")
        page_1 = st.sidebar.selectbox("选择页面", ["单张表", "批量生成多表"])
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
            uploaded_file = st.file_uploader("上传文件", type=["xlsx"])
            if uploaded_file is not None:
                select_sql = bulk_select(uploaded_file, None, None)
                st.write(f"语句")
                st.code(select_sql, language='sql')

    elif page == "INSERT":
        st.header("INSERT页面")
        sample_image = Image.open("image/insert.png")
        st.image(sample_image, caption="样例图片", use_column_width=True)
        uploaded_file = st.file_uploader("上传文件", type=["xlsx"])
        if uploaded_file is not None:
            insert_sql = bulk_insert(uploaded_file)
            st.write(f"语句：")
            st.code(insert_sql, language='sql')

    elif page == "TRUNCATE":
        st.header("TRUNCATE页面")
        table = None
        if table is None:
            table = st.text_input("请输入表名")
        table = table.replace("'", "")
        table = table.split(",")
        truncate_sql = bulk_truncate(table)
        st.write(f"语句：")
        st.code(truncate_sql, language='sql')

    elif page == "UPDATE":  # 暂时没有想到批量化
        st.header("UPDATE页面")
        st.write(f"暂时没有想到想法")

    elif page == "DELETE":
        st.header("DELETE页面")
        page_1 = st.sidebar.selectbox("选择页面", ["单张表", "批量生成多表"])
        if page_1 == "单张表":
            table = None
            column = None
            del_column = None
            tmp_table = None
            if table is None and column is None and del_column is None and tmp_table is None:
                table = st.text_input("请输入表名")
                column = st.text_input("请输入字段")
                del_column = st.text_input('请输入增量字段如 ID 等')
                tmp_table = st.text_input('请输入staging层表')
                delete_sql = bulk_delete(None, table, column, del_column, tmp_table)
                st.write(f"语句：")
                st.code(delete_sql, language='sql')
        elif page_1 == "批量生成多表":
            st.write(f"请上传文件")
            sample_image = Image.open("image/delete.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.file_uploader("上传文件", type=["xlsx"])
            if uploaded_file is not None:
                delete_sql = bulk_delete(uploaded_file, None, None, None, None)
                st.write(f"语句")
                st.code(delete_sql, language='sql')

    elif page == "MERGE":
        st.header("MERGE页面")

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
