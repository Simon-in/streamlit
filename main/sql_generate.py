# 停止更新，方法都放到main.py文件中

# import pandas as pd
#
#
# def bulk_select(file_path, table_name, column):
#     if not file_path:
#         select_statement = f"SELECT {''.join(column)} FROM {table_name};"
#         return select_statement
#     elif file_path:
#         df = pd.read_excel(file_path)
#         table_field_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
#         select_statement = []
#         for table, field in table_field_dict.items():
#             sql = f"SELECT {field} FROM {table};"
#             select_statement.append(sql)
#         cleaned_statements = [stmt.strip() for stmt in select_statement if stmt.strip()]
#         output = "\n".join(cleaned_statements)
#         return output
#
#
# def bulk_insert(file_path, table_name):
#     df = pd.read_excel(file_path, nrows=0)
#     columns = df.columns.tolist()
#     values_list = []
#     for index, row in df.iterrows():
#         values = []
#         for col in columns:
#             value = str(row[col]).replace("'", "''")
#             values.append(f"'{value}'")
#         values_list.append(f"({', '.join(values)})")
#     bulk_insert_statement = (
#             f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n" +
#             ",\n".join(values_list) + ";"
#     )
#     return bulk_insert_statement
#
#
# def bulk_update(self):
#     pass
#
#
# def bulk_delete(self):
#     pass
#
#
# def bulk_merge(self):
#     pass
#
#
# def bulk_truncate(self):
#     pass
