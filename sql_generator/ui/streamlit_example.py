# -*- coding: utf-8 -*-
"""
Streamlit示例模块 - 提供Streamlit基础功能演示
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


def example():
    """
    Streamlit功能演示示例
    """
    # 获取当前子页面
    current_sub_page = st.session_state.get('current_sub_page', "主页")
    
    # 设置页面标题
    st.title("Streamlit功能演示")
    
    # 创建选择框
    sub_page = st.selectbox(
        "选择示例功能",
        ["主页", "button", "write", "slider", "line_chart", "selectbox"]
    )
    
    # 更新session state
    st.session_state.current_sub_page = sub_page
    
    # 显示选定的示例
    st.markdown("---")
    
    if sub_page == "主页":
        render_home_example()
    elif sub_page == "button":
        render_button_example()
    elif sub_page == "write":
        render_write_example()
    elif sub_page == "slider":
        render_slider_example()
    elif sub_page == "line_chart":
        render_line_chart_example()
    elif sub_page == "selectbox":
        render_selectbox_example()


def render_home_example():
    """渲染主页示例"""
    st.header("Streamlit示例主页")
    
    st.markdown("""
    这是一个Streamlit基础功能演示页面，包含以下示例：
    
    - **button**: 按钮组件示例
    - **write**: 文本显示示例
    - **slider**: 滑块控件示例
    - **line_chart**: 折线图示例
    - **selectbox**: 选择框示例
    
    请从上方选择框中选择要查看的示例。
    """)
    
    # 添加图片示例
    st.subheader("图片显示示例")
    st.markdown("使用`st.image()`可以显示图片")
    
    # 创建示例数据
    data = pd.DataFrame({
        'x': range(10),
        'y': np.random.randn(10)
    })
    
    # 显示图表
    st.subheader("图表显示示例")
    st.markdown("使用`st.line_chart()`可以显示折线图")
    st.line_chart(data.set_index('x'))


def render_button_example():
    """渲染按钮示例"""
    st.header("按钮组件示例")
    
    st.markdown("""
    Streamlit提供了多种按钮组件，用于与用户交互：
    
    1. 标准按钮
    2. 复选框
    3. 单选按钮
    """)
    
    # 标准按钮示例
    st.subheader("标准按钮")
    if st.button("点击我"):
        st.write("按钮被点击了！")
    
    # 复选框示例
    st.subheader("复选框")
    if st.checkbox("选中我"):
        st.write("复选框被选中了！")
    
    # 单选按钮示例
    st.subheader("单选按钮")
    option = st.radio(
        "选择一个选项",
        ["选项1", "选项2", "选项3"]
    )
    st.write(f"您选择了：{option}")


def render_write_example():
    """渲染文本显示示例"""
    st.header("文本显示示例")
    
    st.markdown("""
    Streamlit提供多种文本显示方式：
    
    1. st.write() - 通用显示函数
    2. st.markdown() - Markdown格式
    3. st.text() - 纯文本
    4. st.code() - 代码块
    5. st.latex() - LaTeX公式
    """)
    
    # st.write示例
    st.subheader("st.write示例")
    st.write("这是使用st.write显示的文本")
    st.write(pd.DataFrame({
        '第一列': [1, 2, 3, 4],
        '第二列': [10, 20, 30, 40]
    }))
    
    # st.markdown示例
    st.subheader("st.markdown示例")
    st.markdown("""
    # 标题1
    ## 标题2
    ### 标题3
    
    - 列表项1
    - 列表项2
    
    **加粗文本** 和 *斜体文本*
    """)
    
    # st.text示例
    st.subheader("st.text示例")
    st.text("这是使用st.text显示的纯文本\n不会解析Markdown语法")
    
    # st.code示例
    st.subheader("st.code示例")
    code = """def hello_world():
    print("Hello, world!")
    
hello_world()"""
    st.code(code, language="python")
    
    # st.latex示例
    st.subheader("st.latex示例")
    st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} = \sum_{k=0}^{n-1} ar^k = a \frac{1-r^{n}}{1-r}
    ''')


def render_slider_example():
    """渲染滑块控件示例"""
    st.header("滑块控件示例")
    
    st.markdown("""
    Streamlit提供了多种滑块控件，用于选择数值：
    
    1. 普通滑块
    2. 范围滑块
    3. 日期滑块
    """)
    
    # 普通滑块示例
    st.subheader("普通滑块")
    age = st.slider("选择年龄", 0, 100, 25)
    st.write(f"选择的年龄：{age}")
    
    # 浮点数滑块
    st.subheader("浮点数滑块")
    weight = st.slider("选择重量(kg)", 0.0, 100.0, 50.0, 0.1)
    st.write(f"选择的重量：{weight} kg")
    
    # 范围滑块示例
    st.subheader("范围滑块")
    price_range = st.slider(
        "选择价格范围",
        0, 1000, (200, 500)
    )
    st.write(f"选择的价格范围：{price_range[0]} - {price_range[1]}")
    
    # 日期滑块示例
    import datetime
    st.subheader("日期滑块")
    start_date = st.date_input(
        "选择开始日期",
        datetime.date(2023, 1, 1)
    )
    st.write(f"选择的开始日期：{start_date}")


def render_line_chart_example():
    """渲染折线图示例"""
    st.header("图表示例")
    
    st.markdown("""
    Streamlit提供多种图表类型：
    
    1. st.line_chart() - 折线图
    2. st.bar_chart() - 柱状图
    3. st.area_chart() - 面积图
    4. Altair图表 - 更高级的图表库
    """)
    
    # 创建示例数据
    chart_data = pd.DataFrame({
        '日期': pd.date_range('2023-01-01', periods=30),
        '销量': np.random.randn(30).cumsum() + 100,
        '价格': np.random.randn(30).cumsum() + 50,
        '库存': np.random.randn(30).cumsum() + 80
    }).set_index('日期')
    
    # 折线图示例
    st.subheader("折线图")
    st.line_chart(chart_data)
    
    # 柱状图示例
    st.subheader("柱状图")
    st.bar_chart(chart_data.head(10))
    
    # 面积图示例
    st.subheader("面积图")
    st.area_chart(chart_data)
    
    # Altair图表示例
    st.subheader("Altair图表示例")
    
    # 创建一个简单的折线图示例
    # 使用Streamlit内置的图表来避免Altair版本问题
    st.subheader("使用Streamlit的line_chart替代Altair")
    st.line_chart(chart_data)
    
    # 如果想使用Altair且安装了兼容版本，可以取消注释下面的代码
    try:
        # 重置索引
        alt_data = chart_data.reset_index()
        alt_data = alt_data.melt('日期', var_name='指标', value_name='值')
        
        # 创建Altair图表
        chart = alt.Chart(alt_data).mark_line().encode(
            x='日期:T',
            y='值:Q',
            color='指标:N',
            tooltip=['日期', '指标', '值']
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.warning(f"无法显示Altair图表，请检查Altair版本是否与Streamlit兼容: {str(e)}")
        st.info("尝试运行 `pip install altair==4.2.0` 来安装兼容版本的Altair")


def render_selectbox_example():
    """渲染选择框示例"""
    st.header("选择框示例")
    
    st.markdown("""
    Streamlit提供多种选择输入组件：
    
    1. selectbox - 下拉选择框
    2. multiselect - 多选框
    3. select_slider - 选择滑块
    """)
    
    # 单选框示例
    st.subheader("单选框")
    option = st.selectbox(
        '选择您喜欢的编程语言',
        ['Python', 'Java', 'JavaScript', 'C++', 'Go', 'Ruby']
    )
    st.write(f'您选择了: {option}')
    
    # 多选框示例
    st.subheader("多选框")
    options = st.multiselect(
        '选择您熟悉的框架',
        ['Streamlit', 'Flask', 'Django', 'FastAPI', 'Spring', 'React', 'Vue'],
        ['Streamlit']
    )
    st.write(f'您选择了: {", ".join(options)}')
    
    # 选择滑块示例
    st.subheader("选择滑块")
    level = st.select_slider(
        '选择经验级别',
        options=['初级', '中级', '高级', '专家']
    )
    st.write(f'您的经验级别是: {level}')
