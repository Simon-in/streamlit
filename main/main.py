import json
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image
from sql_generate import bulk_insert, bulk_select, bulk_merge, bulk_delete, bulk_truncate, bulk_update



def download_button(button_name: str, file_path: Path, file_type: str) -> None:
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
        page_1 = st.sidebar.selectbox("选择页面", ["单张表", "批量生成多表"])
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
        # 文件上传
        uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
        if uploaded_file is not None:
            # 转换为 JSON
            df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
            df['derive_desc'] = df['derive_desc'].fillna('None')
            json_data = df.to_dict(orient='records')
            start_id = st.number_input("Input Start Number:  :rainbow[[id]]", value=1,
                                       placeholder="Type a number...", step=1)
            for index, item in enumerate(json_data, start=start_id):
                item["id"] = str(index)
            # 下载 JSON 文件
            json_str = json.dumps(json_data, indent=4)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="output.json",
                mime="application/json"
            )
            # 显示 JSON 数据
            st.json(json_data)
