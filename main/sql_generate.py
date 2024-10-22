

import pandas as pd


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


def bulk_update(self):
    pass


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
