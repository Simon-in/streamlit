import pandas as pd
import streamlit as st


class sql:
    def __init__(self, path):
        self.path = path

    def bulk_select(self, table, column):
        if not self.path:
            select_statement = f"SELECT {', '.join(column)} FROM {table};"
            return select_statement
        else:
            df = pd.read_excel(self.path, sheet_name='select')
            se_list = []
            for index, row in df.iterrows():
                target_table = row[0]
                fields = row[1]
                select_statements = (
                    f"SELECT {fields} FROM {target_table};"
                )
                se_list.append(select_statements)
            return se_list

    def bulk_insert(self):
        df = pd.read_excel(self.path, sheet_name='insert')
        isrt_list = [
            f"INSERT INTO {row[0]} ({row[1]}) VALUES ({row[2]});"
            for row in df.itertuples(index=False)
        ]
        return isrt_list

    def bulk_delete(self, target_table, column, uniqueid, source_table):
        if self.path is None:
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
            df = pd.read_excel(self.path, sheet_name='delete')
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

    def bulk_truncate(self, a):
        if self.path is not None and a is None:
            df = pd.read_excel(self.path, sheet_name='truncate')
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
        if self.path is not None and a is not None:
            df = pd.read_excel(self.path, sheet_name='truncate')
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

    def bulk_merge(self):
        if self.path is not None:
            df = pd.read_excel(self.path, sheet_name='merge')
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

    def download_button(self, button_name: str, file_path: str, file_type: str) -> None:
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

    def bulk_create(self):
        df = pd.read_excel(self.path, sheet_name='create')
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

    def sql_formatted(self, sql_list):
        cleaned_statements = [stmt.strip() for stmt in sql_list if stmt.strip()]
        statement = "\n".join(cleaned_statements)
        return statement




        # elif sub_page == "Dynamodb":
        #     st.header("Dynamodb页面")
        #     sub_sub_page = st.sidebar.selectbox("选择页面", ["opera2", "fusion", "待定"])
        #     if sub_sub_page == "opera2":
        #         uploaded_file = st.session_state.uploaded_file
        #         domain = st.text_input("请输入domain")
        #         env = st.text_input("请输入env")
        #         state_machine_name = st.text_input("请输入step function名称")
        #         df = pd.read_excel(uploaded_file, sheet_name='dynamodb')
        #         dy_statements = {}
        #         dy_list = []
        #         for index, row in df.iterrows():
        #             table = row[0]
        #             column = row[1]
        #             if table not in dy_statements:
        #                 dy_statements[table] = []
        #             dy_statements[table].append(f"{column}")
        #         for k, v in dy_statements.items():
        #             dy_dict = {
        #                 "domain": domain,
        #                 "entity": f"staging_{k}",
        #                 "delimiter": ",",
        #                 "file_inzip_pattern": "",
        #                 "file_inzip_suffix": "",
        #                 "is_archive": "N",
        #                 "is_exchange_merge": "false",
        #                 "is_header": "true",
        #                 "is_signal_file": "false",
        #                 "is_soft_fail": "true",
        #                 "landing_file_format": "csv",
        #                 "merge_order_cols": "",
        #                 "merge_order_sc": "desc",
        #                 "primary_keys": "",
        #                 "redshift_enriched_post_job": f"truncate table enriched_em.staging_{k}",
        #                 "salesforce_identifier": env,
        #                 "salesforce_name": k,
        #                 "skip_row": "0",
        #                 "source_sensor_poke_interval": "60",
        #                 "source_sensor_retry_time": "1",
        #                 "source_system": "salesforce",
        #                 "sql_query": f"select id,name,isdeleted,currencyisocode,createddate,createdbyid,lastmodifieddate,lastmodifiedbyid,systemmodstamp,{','.join(v)} from {k} where systemmodstamp >= LAST_N_DAYS:10",
        #                 "standard_columns": f"id,name,isdeleted,currencyisocode,createddate,createdbyid,lastmodifieddate,lastmodifiedbyid,systemmodstamp,{','.join(v)}",
        #                 "state_machine_name": state_machine_name,
        #                 "time_delta": "0*60",
        #                 "use_cols": ""
        #             }
        #             dy_list.append(dy_dict)
        #         json_str = json.dumps(dy_list, indent=4)
        #         st.json(json_str)
        #         st.download_button(
        #             label="Download JSON",
        #             data=json_str,
        #             file_name="dynamodb.json",
        #             mime="application/json"
        #         )
        #     elif sub_sub_page == "fusion":
        #         uploaded_file = st.session_state.uploaded_file
        #         domain = st.text_input("请输入domain")
        #         state_machine_name = st.text_input("请输入step function名称")
        #         conn_id = st.text_input("请输入conn_id")
        #         src_database = st.text_input("请输入src_database")
        #         source_system = st.text_input("请输入source_system")
        #         df = pd.read_excel(uploaded_file, sheet_name='dynamodb')
        #         dy_statements = {}
        #         dy_list = []
        #         for index, row in df.iterrows():
        #             table = row[0]
        #             column = row[1]
        #             if table not in dy_statements:
        #                 dy_statements[table] = []
        #             dy_statements[table].append(f"{column}")
        #         for k, v in dy_statements.items():
        #             dy_dict = {
        #                 "domain": domain,
        #                 "entity": k,
        #                 "conn_id": conn_id,
        #                 "customized_load_sql": f"select {','.join(v)} from dbo.{k}",
        #                 "is_soft_fail": "true",
        #                 "landing_file_format": "parquet",
        #                 "load_mode": "customized",
        #                 "src_database": src_database,
        #                 "redshift_enriched_post_job": f"truncate table enriched_prestage_content.{k};",
        #                 "source_sensor_poke_interval": "60",
        #                 "source_sensor_retry_time": "5",
        #                 "source_system": source_system,
        #                 "standard_columns": f"{','.join(v)}",
        #                 "state_machine_name": state_machine_name,
        #                 "time_delta": "10*60"
        #             }
        #             dy_list.append(dy_dict)
        #         json_str = json.dumps(dy_list, indent=4)
        #         st.json(json_str)
        #         st.download_button(
        #             label="Download JSON",
        #             data=json_str,
        #             file_name="dynamodb.json",
        #             mime="application/json"
        #         )
        # elif sub_page == "Mapping":
        #     st.header("Mapping页面")
        #     uploaded_file = st.session_state.uploaded_file
        #     df = pd.read_excel(uploaded_file, sheet_name='mapping')
        #     df['derive_desc'].fillna('None', inplace=True)
        #     start_id = st.number_input("Input Start Number:  :rainbow[[id]]", value=1,
        #                                placeholder="Type a number...", step=1)
        #     json_data = df.to_dict(orient='records')
        #     for index, item in enumerate(json_data, start=start_id):
        #         item["id"] = str(index)
        #     st.download_button(
        #         label="Download JSON",
        #         data=json.dumps(json_data, indent=4),
        #         file_name="mapping.json",
        #         mime="application/json"
        #     )
        #     st.json(json_data)
