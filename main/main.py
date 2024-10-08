import os
import streamlit as st
import logging as log
from conf import sql_generate

if __name__ == "__main__":
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    file_path = parent_directory + "/data/test.xlsx"
    print(file_path)
    table_name = 'model_sci.sci_simulation_config_xinyu_test'  # 替换为你的数据库表名
    sql_generate = sql_generate(file_path, table_name)
    it = sql_generate.generate_bulk_insert_statement()
    st = sql_generate.generate_select_statement()
    print("这是INSERT语句：", it)
    print("这是SELECT语句：", st)
