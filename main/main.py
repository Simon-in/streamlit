import json
import pandas as pd
import streamlit as st
from PIL import Image


def bulk_select(path, table, column):
    if not path:
        select_statement = f"SELECT {', '.join(column)} FROM {table};"
        return select_statement
    else:
        df = pd.read_excel(path, sheet_name='select')
        se_list = []
        for index, row in df.iterrows():
            target_table = row[0]
            fields = row[1]
            select_statements = (
                f"SELECT {fields} FROM {target_table};"
            )
            se_list.append(select_statements)
        return se_list


def bulk_insert(path):
    df = pd.read_excel(path, sheet_name='insert')
    isrt_list = [
        f"INSERT INTO {row[0]} ({row[1]}) VALUES ({row[2]});"
        for row in df.itertuples(index=False)
    ]
    return isrt_list


def bulk_delete(path, target_table, column, uniqueid, source_table):
    if path is None:
        del_list = f"delete from {target_table} \n" \
                           f" where {uniqueid} in (" \
                           f"select {uniqueid} from {source_table})  \n" \
                           f"insert into {target_table} \n" \
                           f" ({column})  \n" \
                           f"select {column} \n" \
                           f" from {source_table};"
        return del_list
    else:
        del_list = []
        df = pd.read_excel(path, sheet_name='delete')
        for index, row in df.iterrows():
            target_domain = row[0]
            target_table = row[1]
            fields = row[2].split(',')
            increment_field = row[3]
            source_table = row[4]
            delete_statement = (
                f"--------- {target_table} --------- \n"
                f"DELETE FROM {target_domain}.{target_table}  \n"
                f"WHERE {increment_field} IN (SELECT {increment_field} FROM {source_table});"
            )
            formatted_fields = ',\n    '.join(fields)
            insert_statement = (
                f"INSERT INTO {target_domain}.{target_table} \n (\n    {formatted_fields}\n)\n"
                f"SELECT \n    {formatted_fields}\n"
                f"FROM {target_domain}.{source_table}; \n"
            )
            del_list.append(delete_statement)
            del_list.append(insert_statement)
        return del_list


def bulk_truncate(path, a):
    if path is not None and a is None:
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
    if path is not None and a is not None:
        df = pd.read_excel(path, sheet_name='truncate')
        trun_list = []
        for index, row in df.iterrows():
            target_table = row[0]
            target_column = row[1].split(',')
            source_table = row[2]
        # 生成 TRUNCATE 和 INSERT 语句
            truncate_statement = (
                f"--------- {target_table} --------- \n"
                f"TRUNCATE TABLE {target_table};  \n"
            )

            # 生成 INSERT 语句，字段换行
            formatted_fields = ',\n    '.join(target_column)  # 将字段换行格式化
            insert_statement = (
                f"INSERT INTO {target_table}\n"
                    f"(\n"
                    f"    {formatted_fields}\n"
                    f")\n"
                    f"SELECT\n"
                    f"    {formatted_fields}\n"
                    f"FROM {source_table}; \n"
            )
            trun_list.append(truncate_statement)
            trun_list.append(insert_statement)
        return trun_list


def bulk_merge(path):
    if path is not None:
        df = pd.read_excel(path, sheet_name='merge')
        merge_list = []
        for index, row in df.iterrows():
            target_table = row[0]
            target_column = row[1].split(',')
            uniqueid = row[2]
            source_table = row[3]
            source_column = row[4].split(',')
            formatted_fields_target = ',\n    '.join(target_column)  # 将字段换行格式化
            formatted_fields_source = ',\n    '.join(source_column)  # 将字段换行格式化
            update_set = ',\n    '.join(
                [f"{target_column[i]} = SOURCE.{source_column[i]}" for i in range(len(target_column))])
            merge_statement = (
                f"--------- {target_table} --------- \n"
                f"MERGE INTO {target_table} \n"
                f"USING {source_table} AS SOURCE \n"
                f"ON {target_table.split('.')[1]}.{uniqueid} = SOURCE.{uniqueid} \n"
                f"WHEN MATCHED THEN \n"
                f"    UPDATE SET \n"
                f"    {update_set} \n"
                f"WHEN NOT MATCHED THEN \n"
                f"    INSERT (\n"
                f"    {formatted_fields_target} \n"
                f"    ) \n"
                f"VALUES (\n"
                f"    {formatted_fields_source} \n"
                f"    ); \n"
            )
            merge_list.append(merge_statement)
        return merge_list


def download_button(button_name: str, file_path: str, file_type: str) -> None:
    mime_types = {
        'xlsx': "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        'zip': "application/zip",
        'json': "application/json"
    }
    try:
        with open(file_path, "rb") as file:
            file_bytes = file.read()

        mime_type = mime_types.get(file_type, "text/plain")

        if mime_type == "text/plain":
            st.error(f"file_type: {file_type}. Unsupported file type.")
        else:
            st.download_button(
                label=button_name,
                data=file_bytes,
                file_name=file_path,
                mime=mime_type
            )
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")


def bulk_create(path):
    df = pd.read_excel(path, sheet_name='create')
    create_statements = {}
    for _, row in df.iterrows():
        domain = row[0]
        table = row[1]
        column = row[2]
        data_type = row[3]
        if table not in create_statements:
            create_statements[table] = []
        create_statements[table].append(f"{column} {data_type}")
    sql_statements = []
    for table, columns in create_statements.items():
        sql_statements.append(f"--------- {table} --------- \n")
        sql_statements.append(f"CREATE TABLE {domain}.{table} (\n    " + ",\n    ".join(columns) + "\n);")
    return sql_statements


def bulk_update(self):
    pass


def sql_formatted(sql_list):
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
            sample_image = Image.open("main/image/truncate_1.png")
            st.image(sample_image, caption="样例图片", use_column_width=True)
            uploaded_file = st.session_state.uploaded_file
            a = 1
            truncate_sql = bulk_truncate(uploaded_file, a)
            sql = sql_formatted(truncate_sql)
            st.write(f"语句")
            st.code(sql, language='sql')
            st.download_button(
                label="Download sql",
                data=sql,
                file_name="truncate.sql",
                mime="application/sql"
            )

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
        uploaded_file = st.session_state.uploaded_file
        domain = st.text_input("请输入domain")
        env = st.text_input("请输入env")
        state_machine_name = st.text_input("请输入step function名称")
        df = pd.read_excel(uploaded_file, sheet_name='dynamodb')
        dy_statements = {}
        dy_list = []
        for index, row in df.iterrows():
            table = row[0]
            column = row[1]
            if table not in dy_statements:
                dy_statements[table] = []
            dy_statements[table].append(f"{column}")
        for k, v in dy_statements.items():
            dy_dict = {
                "domain": domain,
                "entity": f"staging_{k}",
                "delimiter": ",",
                "file_inzip_pattern": "",
                "file_inzip_suffix": "",
                "is_archive": "N",
                "is_exchange_merge": "false",
                "is_header": "true",
                "is_signal_file": "false",
                "is_soft_fail": "true",
                "landing_file_format": "csv",
                "merge_order_cols": "",
                "merge_order_sc": "desc",
                "primary_keys": "",
                "redshift_enriched_post_job": f"truncate table enriched_em.staging_{k}",
                "salesforce_identifier": env,
                "salesforce_name": k,
                "skip_row": "0",
                "source_sensor_poke_interval": "60",
                "source_sensor_retry_time": "1",
                "source_system": "salesforce",
                "sql_query": f"select id,name,isdeleted,currencyisocode,createddate,createdbyid,lastmodifieddate,lastmodifiedbyid,systemmodstamp,{','.join(v)} from {k} where systemmodstamp >= LAST_N_DAYS:10",
                "standard_columns": f"id,name,isdeleted,currencyisocode,createddate,createdbyid,lastmodifieddate,lastmodifiedbyid,systemmodstamp,{','.join(v)}",
                "state_machine_name": state_machine_name,
                "time_delta": "0*60",
                "use_cols": ""
            }
            dy_list.append(dy_dict)
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
        uploaded_file = st.session_state.uploaded_file
        df = pd.read_excel(uploaded_file, sheet_name='mapping')
        df['derive_desc'].fillna('None', inplace=True)
        start_id = st.number_input("Input Start Number:  :rainbow[[id]]", value=1,
                                   placeholder="Type a number...", step=1)
        json_data = df.to_dict(orient='records')
        for index, item in enumerate(json_data, start=start_id):
            item["id"] = str(index)
        st.download_button(
            label="Download JSON",
            data=json.dumps(json_data, indent=4),
            file_name="output.json",
            mime="application/json"
        )
        st.json(json_data)

