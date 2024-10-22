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


def bulk_insert(path, table):
    df = pd.read_excel(path, nrows=0)
    columns = df.columns.tolist()
    values_list = []
    for index, row in df.iterrows():
        values = []
        for col in columns:
            value = str(row[col]).replace("'", "''")
            values.append(f"'{value}'")
        values_list.append(f"({', '.join(values)})")
    insert_statement = (
            f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n" +
            ",\n".join(values_list) + ";"
    )
    return insert_statement


def bulk_update(self):
    pass


def bulk_delete(self):
    pass


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
            uploaded_file = st.file_uploader("上传文件", type=["xlsx", "csv"])
            if uploaded_file is not None:
                select_sql = bulk_select(uploaded_file, None, None)
                st.write(f"语句")
                st.code(select_sql, language='sql')

    elif page == "INSERT":
        st.header("INSERT页面")
        sample_image = Image.open("image/insert.png")
        st.image(sample_image, caption="样例图片", use_column_width=True)
        table = st.text_input("请输入表名")
        uploaded_file = st.file_uploader("上传文件", type=["xlsx", "csv"])
        if uploaded_file is not None:
            insert_sql = bulk_insert(uploaded_file, table)
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

delete from table
where column = ---
insert into table
column_list
select
column_list
from table

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
