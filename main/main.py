import json
import pandas as pd
import streamlit as st
from PIL import Image


def bulk_select(path, table, column):
    # if not path:
    #     select_statement = f"SELECT {''.join(column)} FROM {table};"
    #     return select_statement
    # elif path:
    #     df = pd.read_excel(path, sheet_name='select')
    #     table_field_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
    #     select_statement = []
    #     for table, field in table_field_dict.items():
    #         sql = f"SELECT {field}  \n" \
    #               f"FROM {table}; "
    #         select_statement.append(sql)
    #     return select_statement
    if not path:
        # 当没有提供 path 时，直接构建 SELECT 语句
        select_statement = f"SELECT {', '.join(column)} FROM {table};"
        return select_statement
    else:
        # 当提供 path 时，从 Excel 读取表和字段信息
        df = pd.read_excel(path, sheet_name='select')
        table_field_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

        # 使用列表推导式生成 SQL 语句
        select_statements = [
            f"SELECT {field} FROM {table};"
            for table, field in table_field_dict.items()
        ]
        return select_statements


def bulk_insert(path):
    df = pd.read_excel(path, sheet_name='insert')
    df_list = []
    isrt_list = []
    for i in range(df.__len__()):
        df_dict = {}
        df_dict['table'] = df.iloc[i, 0]
        df_dict['column'] = df.iloc[i, 1]
        df_dict['values'] = df.iloc[i, 2]
        df_list.append(df_dict)
    for info in df_list:
        info['values'] = [value.replace(",", "") for value in info.get('values', [])]
        info['column'] = [column.replace(",", "") for column in info.get('column', [])]
        insert_statement = f"INSERT INTO {info.get('table')} (\n" + \
                           ",\n".join(f"    {column}" for column in info.get('column')) + \
                           f"\n) VALUES (\n" + \
                           ",\n".join(f"    {value}" for value in info.get('values')) + \
                           f"\n);"
        isrt_list.append(insert_statement)
    return isrt_list


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
        df = pd.read_excel(path, sheet_name='delete')
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
        return del_list


def bulk_truncate(path, table):
    if path is not None:
        df = pd.read_excel(path, sheet_name='truncate')
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
        return trun_list
    else:
        df = pd.read_excel(path, sheet_name='truncate')
        trun_statements = {}
        trun_list = []
        for index, row in df.iterrows():
            target_table = row[0]
            target_column = row[1]
            source_table = row[2]
            source_column = row[3]
            if target_table not in trun_statements:
                trun_statements[target_table] = []
                trun_statements[source_table] = []
            trun_statements[target_table].append(f"{target_column}")
            trun_statements[source_table].append(f"{source_column}")
        for table_, column_ in trun_statements.items():
            columns_definition = ",".join(column_)
            trun_ = f"""
                    TRUNCATE TABLE {table_};
                    INSERT INTO {table_}
                    (
                        {columns_definition}
                    )
                    SELECT 
                        {columns_definition}
                    FROM {table_};
    """
            trun_list.append(trun_)
        return trun_list


def bulk_merge(path):
    if path is not None:
        df = pd.read_excel(path, sheet_name='merge')
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
        return merge_list


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
    df = pd.read_excel(path, sheet_name='create')
    create_statements = {}
    for _, row in df.iterrows():
        table = row[0]
        column = row[1]
        data_type = row[2]
        if table not in create_statements:
            create_statements[table] = []
        create_statements[table].append(f"{column} {data_type}")
    sql_statements = []
    for table, columns in create_statements.items():
        sql_statements.append(f"CREATE TABLE {table} (\n    " + ",\n    ".join(columns) + "\n);")
    return sql_statements


def bulk_update(self):
    pass


def sql_formatted(sql_list):
    # list = []
    # for sql in sql_list:
    #     formatted_sql = sqlparse.format(sql,reindent=True,keyword_case='upper')
    #     list.append(formatted_sql)
    cleaned_statements = [stmt.strip() for stmt in sql_list if stmt.strip()]
    statement = "\n".join(cleaned_statements)
    return statement


if __name__ == "__main__":
    page = st.sidebar.selectbox("选择页面",
                                ["主页", "CREATE", "SELECT", "INSERT", "UPDATE", "MERGE", "DELETE", "TRUNCATE", "Dynamodb", "Mapping"])
    if page == "主页":
        st.header("欢迎来到主页！")
        st.write('\n')
        st.markdown(
            "在上传文件前请下载样例文件查看如何配置后,\n"
            "你可以从侧面导航栏选择你想进行的操作,\n"
            "复制sql语句或者下载sql文件"
        )
        download_button("样例下载", r"main/static/样例.xlsx", 'xlsx')
        uploaded_file = st.file_uploader("上传文件", type=["csv", "txt", "xlsx"])
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            st.success("文件上传成功！")
    elif page == "CREATE":
        st.header("CREATE页面 ")
        sample_image = Image.open("main/image/create.png")
        st.image(sample_image, caption="样例图片", use_column_width=True)
        uploaded_file = st.session_state.uploaded_file
        create_sql = bulk_create(uploaded_file)
        sql = sql_formatted(create_sql)
        st.write(f"语句")
        st.code(sql, language='sql')
        st.download_button(
            label="Download sql",
            data=sql,
            file_name="create.sql",
            mime="application/sql"
        )

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
            uploaded_file = st.session_state.uploaded_file
            select_sql = bulk_select(uploaded_file, None, None)
            sql = sql_formatted(select_sql)
            st.write(f"语句")
            st.code(sql, language='sql')
            st.download_button(
                label="Download sql",
                data=sql,
                file_name="select.sql",
                mime="application/sql"
            )

    elif page == "INSERT":
        st.header("INSERT页面")
        sample_image = Image.open("main/image/insert.png")
        st.image(sample_image, caption="样例图片", use_column_width=True)
        uploaded_file = st.session_state.uploaded_file
        insert_sql = bulk_insert(uploaded_file)
        sql = sql_formatted(insert_sql)
        st.write(f"语句：")
        st.code(sql, language='sql')
        st.download_button(
            label="Download sql",
            data=sql,
            file_name="insert.sql",
            mime="application/sql"
        )

    elif page == "TRUNCATE":
        st.header("TRUNCATE页面")
        page_1 = st.sidebar.selectbox("选择页面", ["单张表", "批量生成多表", "全删全插"])
        if page_1 == "单张表":
            table = None
            if table is None:
                table = st.text_input("请输入表名")
            truncate_sql = f"TRUNCATE TABLE {table};"
            st.write(f"语句：")
            st.code(truncate_sql, language='sql')
        elif page_1 == "批量生成多表":
            sample_image = Image.open("main/image/truncate.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.session_state.uploaded_file
            truncate_sql = bulk_truncate(uploaded_file, None)
            sql = sql_formatted(truncate_sql)
            st.write(f"语句")
            st.code(sql, language='sql')
            st.download_button(
                label="Download sql",
                data=sql,
                file_name="truncate.sql",
                mime="application/sql"
            )
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
            sample_image = Image.open("main/image/delete.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.session_state.uploaded_file
            delete_sql = bulk_delete(uploaded_file, None, None, None, None)
            sql = sql_formatted(delete_sql)
            st.write(f"语句")
            st.code(sql, language='sql')
            st.download_button(
                label="Download sql",
                data=sql,
                file_name="delete.sql",
                mime="application/sql"
            )

    elif page == "MERGE":
        st.header("MERGE页面")
        sample_image = Image.open("main/image/merge.png")
        st.image(sample_image, caption="样例图片", use_column_width=True)
        uploaded_file = st.session_state.uploaded_file
        merge_sql = bulk_merge(uploaded_file)
        sql = sql_formatted(merge_sql)
        st.write(f"语句")
        st.code(sql, language='sql')
        st.download_button(
            label="Download sql",
            data=sql,
            file_name="merge.sql",
            mime="application/sql"
        )

    elif page == "Dynamodb":
        st.header("Dynamodb页面")
        uploaded_file = st.file_uploader("上传文件", type=["csv", "txt", "xlsx"])
        domain = st.text_input("请输入domain")
        env = st.text_input("请输入env")
        state_machine_name = st.text_input("请输入step function名称")
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            dy_statements = {}
            dy_list = []
            for index, row in df.iterrows():
                table = row[0]
                column = row[1]
                if table not in dy_statements:
                    dy_statements[table] = []
                dy_statements[table].append(f"{column}")
            for k, v in dy_statements.items():
                dy_json = '{ \n' \
                          f'"domain":"{domain}", \n' \
                          f'"entity":"{k}",\n' \
                          f'"delimiter": ",",\n' \
                          f'"file_inzip_pattern": "",\n' \
                          f'"file_inzip_suffix": "",\n' \
                          f'"is_archive": "N",\n' \
                          f'"is_exchange_merge": "false",\n' \
                          f'"is_header": "true",\n' \
                          f'"is_signal_file": "false",\n' \
                          f'"is_soft_fail": "true",\n' \
                          f'"landing_file_format": "csv",\n' \
                          f'"merge_order_cols": "",\n' \
                          f'"merge_order_sc": "desc",\n' \
                          f'"primary_keys": "",\n' \
                          f'"redshift_enriched_post_job": "truncate table enriched_em.staging_{k}",\n' \
                          f'"salesforce_identifier": "{env}",\n' \
                          f'"salesforce_name": "{k}",\n' \
                          f'"skip_row": "0",\n' \
                          f'"source_sensor_poke_interval": "60",\n' \
                          f'"source_sensor_retry_time": "1",\n' \
                          f'"source_system": "salesforce",\n' \
                          f'"sql_query": "select id,name,isdeleted,currencyisocode,createddate,createdbyid,lastmodifieddate,lastmodifiedbyid,systemmodstamp,{",".join(v)} from {k} where systemmodstamp >= LAST_N_DAYS:10",\n' \
                          f'"standard_columns": "id,name,isdeleted,currencyisocode,createddate,createdbyid,lastmodifieddate,lastmodifiedbyid,systemmodstamp,{",".join(v)}",\n' \
                          f'"state_machine_name": "{state_machine_name}",\n' \
                          f'"time_delta": "0*60",\n' \
                          f'"use_cols": ""\n' \
                          '},\n'
                dy_list.append(dy_json)
            json_str = json.dumps(dy_list, indent=4)
            st.json(json_str)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="output.json",
                mime="application/json"
            )


    elif page == "Mapping":
        st.header("Mapping页面")
        COLS_NUM = 4
        MAX_TEMP_FILES = 10
        uploaded_file = st.session_state.uploaded_file
        df = pd.read_excel(uploaded_file, sheet_name='mapping')
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
