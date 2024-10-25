import json

import pandas as pd
import streamlit as st
from PIL import Image


def bulk_select(path, table, column):
    if not path:
        select_statement = f"SELECT {''.join(column)} FROM {table};"
        return select_statement
    elif path:
        df = pd.read_excel(path)
        table_field_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        select_statement = []
        for table, field in table_field_dict.items():
            sql = f"SELECT {field}  \n" \
                  f"FROM {table}; "
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
            f"INSERT INTO {info.get('table')}  \n"
            f" ({info.get('column')})  \n"
            f"VALUES ("
            f"{info.get('values')}"
            f");"
        )
        isrt_list.append(insert_statement)
    cleaned_statements = [stmt.strip() for stmt in isrt_list if stmt.strip()]
    insert_statement = "\n".join(cleaned_statements)
    return insert_statement


def bulk_delete(path, target_table, column, uniqueid, source_table):
    if path is None:
        delete_statement = f"delete from {target_table} \n" \
                           f" where {uniqueid} in (" \
                           f"select {uniqueid} from {source_table})  \n" \
                           f"insert into {target_table} \n" \
                           f" ({column})  \n" \
                           f"select {column} \n" \
                           f" from {source_table};"
        return delete_statement
    else:
        df = pd.read_excel(path)
        df_list = []
        del_list = []
        for i in range(df.__len__()):
            df_dict = {}
            df_dict['target_table'] = df.iloc[i, 0]
            df_dict['column'] = df.iloc[i, 1]
            df_dict['uniqueid'] = df.iloc[i, 2]
            df_dict['source_table'] = df.iloc[i, 3]
            df_list.append(df_dict)
        for info in df_list:
            delete_statement = (
                f"DELETE FROM {info.get('target_table')}  \n"
                f"WHERE {info.get('uniqueid')} IN ("
                f"SELECT {info.get('uniqueid')} FROM {info.get('source_table')});  \n"
                f"INSERT INTO {info.get('table')}  \n"
                f"({info.get('column')})  \n"
                f"SELECT {info.get('column')}  \n"
                f"FROM {info.get('source_table')};"
            )
            del_list.append(delete_statement)
        cleaned_statements = [stmt.strip() for stmt in del_list if stmt.strip()]
        delete_statement = "\n".join(cleaned_statements)
        return delete_statement


def bulk_truncate(path, table):
    if path is not None:
        df = pd.read_excel(path)
        df_list = []
        trun_list = []
        for i in range(df.__len__()):
            df_dict = {}
            df_dict['table'] = df.iloc[i, 0]
            df_list.append(df_dict)
        for info in df_list:
            truncate_statement = (
                f"truncate table {info.get('table')};"
            )
            trun_list.append(truncate_statement)
        cleaned_statements = [stmt.strip() for stmt in trun_list if stmt.strip()]
        truncate_statement = "\n".join(cleaned_statements)
        return truncate_statement
    else:
        trun_list = []
        for i in range(table.__len__()):
            truncate_statement = (
                f"truncate table {table[i]};"
            )
            trun_list.append(truncate_statement)
        cleaned_statements = [stmt.strip() for stmt in trun_list if stmt.strip()]
        truncate_statement = "\n".join(cleaned_statements)
        return truncate_statement


def bulk_merge(path):
    if path is not None:
        df = pd.read_excel(path)
        df_list = []
        merge_list = []
        up_list = []
        for i in range(df.__len__()):
            df_dict = {}
            df_dict['target_table'] = df.iloc[i, 0]
            df_dict['target_column'] = df.iloc[i, 1]
            df_dict['uniqueid'] = df.iloc[i, 2]
            df_dict['source_table'] = df.iloc[i, 3]
            df_dict['source_column'] = df.iloc[i, 4]
            df_list.append(df_dict)
            i = 0
        for info in df_list:
            target_columns = info.get('target_column').split(",")
            up_list = []
            for column in target_columns:
                up_statement = f"{column} = source.{column}"
                up_list.append(up_statement)
            update_set_clause = ", ".join(up_list)
            mrege_statement = (
                    f"merge into {info.get('target_table')} \n"
                    f" using {info.get('source_table')} as source \n"
                    f" on {info.get('target_table').split('.')[1]}.{info.get('uniqueid')} = source.{info.get('uniqueid')} \n"
                    f" when matched then update set \n"
                    f" {update_set_clause}  \n"
                    f" when not matched then \n"
                    f" insert("
                    f" {info.get('target_column')}"
                    f") \n"
                    f" values("
                    f" {info.get('source_column')}"
                    f");"
                )
            merge_list.append(mrege_statement)
        cleaned_statements = [stmt.strip() for stmt in merge_list if stmt.strip()]
        merge_statement = "\n".join(cleaned_statements)
        return merge_statement


def download_button(button_name: str, file_path, file_type: str) -> None:
    try:
        with open(file_path, "rb") as file:
            file_bytes = file.read()
        if file_type in ['xlsx', 'zip', 'json']:
            if file_type == 'xlsx':
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif file_type == 'zip':
                mime_type = "application/zip"
            elif file_type == 'json':
                mime_type = "application/json"
            else:
                st.error(f"file_type: {file_type}. Unsupported file type.")
                mime_type = "text/plain"
            st.download_button(
                label=button_name,
                data=file_bytes,
                file_name=file_path,
                mime=mime_type
            )
        else:
            st.error(f"file_type: {file_type}. Unsupported file type.")
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")


def bulk_create(path):
    df = pd.read_excel(path)
    create_statements = {}
    create_statement = []
    for index, row in df.iterrows():
        table__ = row[0]
        column__ = row[1]
        type__ = row[2]
        if table__ not in create_statements:
            create_statements[table__] = []
        create_statements[table__].append(f"{column__} {type__}")
    for table_, column_ in create_statements.items():
        columns_definition = ",\n    ".join(column_)
        create_ = f"CREATE TABLE {table_} (\n    {columns_definition}\n);"
        create_statement.append(create_)
    return create_statement

def bulk_update(self):
    pass


if __name__ == "__main__":
    st.title("Streamlit 应用")
    page = st.sidebar.selectbox("选择页面",
                                ["主页", "CREATE", "SELECT", "INSERT", "UPDATE", "MERGE", "DELETE", "TRUNCATE", "Dynamodb", "Mapping"])
    if page == "主页":
        st.header("欢迎来到主页！")
        st.write('\n')
        st.write("你可以从侧面导航栏选择你想进行的操作")

    elif page == "CREATE":
        st.header("CREATE页面 ")
        sample_image = Image.open("main/image/create.png")
        st.image(sample_image, caption="样例图片", use_column_width=True)
        uploaded_file = st.file_uploader("上传文件", type=["xlsx"])
        if uploaded_file is not None:
            create_sql = bulk_create(uploaded_file)
            st.write(f"语句")
            st.code(create_sql, language='sql')

    elif page == "SELECT":
        st.header("SELECT页面 ")
        page_1 = st.sidebar.selectbox("选择页面", ["单张表", "批量生成多表"])
        if page_1 == "单张表":
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
            sample_image = Image.open("main/image/select.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.file_uploader("上传文件", type=["xlsx"])
            if uploaded_file is not None:
                select_sql = bulk_select(uploaded_file, None, None)
                st.write(f"语句")
                st.code(select_sql, language='sql')

    elif page == "INSERT":
        st.header("INSERT页面")
        sample_image = Image.open("main/image/insert.png")
        st.image(sample_image, caption="样例图片", use_column_width=True)
        uploaded_file = st.file_uploader("上传文件", type=["xlsx"])
        if uploaded_file is not None:
            insert_sql = bulk_insert(uploaded_file)
            st.write(f"语句：")
            st.code(insert_sql, language='sql')

    elif page == "TRUNCATE":
        st.header("TRUNCATE页面")
        page_1 = st.sidebar.selectbox("选择页面", ["单张表", "批量生成多表", "全删全插"])
        if page_1 == "单张表":
            table = None
            if table is None:
                table = st.text_input("请输入表名")
            table = table.replace("'", "")
            table = table.split(",")
            truncate_sql = bulk_truncate(None, table)
            st.write(f"语句：")
            st.code(truncate_sql, language='sql')
        elif page_1 == "批量生成多表":
            sample_image = Image.open("main/image/truncate.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.file_uploader("上传文件", type=["xlsx"])
            if uploaded_file is not None:
                truncate_sql = bulk_truncate(uploaded_file, None)
                st.write(f"语句")
                st.code(truncate_sql, language='sql')
        elif page_1 == "全删全插":
            pass

    elif page == "UPDATE":  # 暂时没有想到批量化
        st.header("UPDATE页面")
        st.write(f"暂时没有想法")

    elif page == "DELETE":
        st.header("DELETE页面")
        page_1 = st.sidebar.selectbox("选择页面", ["单张表", "批量生成多表"])
        if page_1 == "单张表":
            target_table = None
            column = None
            uniqueid = None
            source_table = None
            if target_table is None and column is None and uniqueid is None and source_table is None:
                target_table = st.text_input("请输入表名")
                column = st.text_input("请输入字段")
                uniqueid = st.text_input('请输入增量字段如 ID 等')
                source_table = st.text_input('请输入staging层表')
                delete_sql = bulk_delete(None, target_table, column, uniqueid, source_table)
                st.write(f"语句：")
                st.code(delete_sql, language='sql')

        elif page_1 == "批量生成多表":
            st.write(f"请上传文件")
            sample_image = Image.open("main/image/delete.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.file_uploader("上传文件", type=["xlsx"])
            if uploaded_file is not None:
                delete_sql = bulk_delete(uploaded_file, None, None, None, None)
                st.write(f"语句")
                st.code(delete_sql, language='sql')

    elif page == "MERGE":
        st.header("MERGE页面")
        st.write(f"请上传文件")
        sample_image = Image.open("main/image/merge.png")
        st.image(sample_image, caption="样例图片", use_column_width=True)
        uploaded_file = st.file_uploader("上传文件", type=["xlsx"])
        if uploaded_file is not None:
            merge_sql = bulk_merge(uploaded_file)
            st.write(f"语句")
            st.code(merge_sql, language='sql')

    elif page == "Dynamodb":
        st.header("Dynamodb页面")

    elif page == "Mapping":
        st.header("Mapping页面")
        COLS_NUM = 4
        MAX_TEMP_FILES = 10
        st.title("id类型的接数mapping_用于非SCI")
        st.markdown(
            """
            1)上传的xlsx里得自己配上系统字段,id不用配
            2)配多张就在一个sheet页里往下写就好
            """
        )
        download_button("单张模板下载", r"main/static/接单张模板.xlsx", 'xlsx')
        download_button("多张模板下载", r"main/static/接多张模板.xlsx", 'xlsx')
        uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
            df['derive_desc'] = df['derive_desc'].fillna('None')
            json_data = df.to_dict(orient='records')
            start_id = st.number_input("Input Start Number:  :rainbow[[id]]", value=1,
                                       placeholder="Type a number...", step=1)
            for index, item in enumerate(json_data, start=start_id):
                item["id"] = str(index)
            json_str = json.dumps(json_data, indent=4)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="output.json",
                mime="application/json"
            )
            st.json(json_data)


