"""
config info
"""
import pandas as pd


class sql_generate:
    def __init__(self, file_path, table_name):
        self.file_path = file_path
        self.table_name = table_name
        self.df = pd.read_excel(file_path)
        self.df1 = pd.read_excel(file_path, nrows=0)

    def generate_select_statement(self: str) -> str:
        columns = self.df1.columns.tolist()
        select_statement = f"SELECT {', '.join(columns)} FROM {self.table_name};"
        return select_statement

    def generate_bulk_insert_statement(self):
        columns = self.df.columns.tolist()
        values_list = []
        for index, row in self.df.iterrows():
            values = []
            for col in columns:
                value = str(row[col]).replace("'", "''")  # 处理单引号
                values.append(f"'{value}'")  # 添加引号
            values_list.append(f"({', '.join(values)})")
        bulk_insert_statement = (
            f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES\n" +
            ",\n".join(values_list) + ";"
        )
        return bulk_insert_statement
