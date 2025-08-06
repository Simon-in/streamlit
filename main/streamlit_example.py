# -*- coding: utf-8 -*-
"""
Streamlit组件示例 - 展示各种Streamlit组件的使用方法
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import time, datetime
from utils import UIHelper


class example:
    """Streamlit组件示例类"""
    
    def __init__(self):
        pass

    def button(self):
        """按钮组件示例"""
        UIHelper.create_section_header("🔘 Button 组件", "展示按钮的基本用法")
        
        st.markdown("### 基础按钮示例")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("演示效果")
            if st.button('Say hello', key="demo_button"):
                st.success('Why hello there! 👋')
            else:
                st.info('点击按钮试试看')
                
        with col2:
            st.subheader("代码示例")
            code = '''import streamlit as st

if st.button('Say hello'):
    st.success('Why hello there! 👋')
else:
    st.info('点击按钮试试看')'''
            st.code(code, language='python')
            
        # 更多按钮示例
        st.markdown("### 更多按钮样式")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Primary", type="primary"):
                st.balloons()
        with col2:
            if st.button("Secondary", type="secondary"):
                st.snow()
        with col3:
            if st.button("Disabled", disabled=True):
                pass

    def write(self):
        st.header('st.write')
        st.write('样例1：Hello, *World!* :sunglasses:')

        code1 = """
        import streamlit as st \n
        st.write('Hello, *World!* :sunglasses:')
        """
        st.code(code1, language='python')

        code2 = """
        import streamlit as st \n
        st.write(1234)
        """
        st.write('样例2：', 1234)
        st.code(code2, language='python')

        code3 = """
        import streamlit as st
        import pandas as pd
        import numpy as np
        import altair as alt \n
        df = pd.DataFrame({
            'first column': [1, 2, 3, 4],
            'second column': [10, 20, 30, 40]
        })
        st.write('Below is a DataFrame:', df, 'Above is a dataframe')
        df2 = pd.DataFrame(
            np.random.randn(200, 3),
            columns=['a', 'b', 'c']
        )
        c = alt.Chart(df2).mark_circle().encode(
            x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c']
        )
        """
        df = pd.DataFrame({
            'first column': [1, 2, 3, 4],
            'second column': [10, 20, 30, 40]
        })
        st.write('样例3：Below is a DataFrame:', df, 'Above is a dataframe')
        st.code(code3, language='python')

        code4 = """
        import streamlit as st
        import pandas as pd
        import numpy as np
        from datetime import time, datetime \n
        df2 = pd.DataFrame(
            np.random.randn(200, 3),
            columns=['a', 'b', 'c']
        )
        c = alt.Chart(df2).mark_circle().encode(
            x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c']
        )
        """
        df2 = pd.DataFrame(
            np.random.randn(200, 3),
            columns=['a', 'b', 'c']
        )
        c = alt.Chart(df2).mark_circle().encode(
            x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c']
        )
        st.write('样例4：', c)
        st.code(code4, language='python')

    def slider(self):
        code = """
        import streamlit as st \n
        st.subheader('Slider')
        age = st.slider('How old are you?', 0, 130, 25)
        st.write("I'm ", age, 'years old')
        """
        st.header('st.slider')
        st.subheader('样例1：Slider')
        age = st.slider('How old are you?', 0, 130, 25)
        st.write("I'm ", age, 'years old')
        st.code(code, language='python')

        code2 = """
        import streamlit as st \n
        values = st.slider(
            'Select a range of values',
            0.0, 100.0, (25.0, 75.0)
        )
        st.write('Values: ', values)
        """
        st.subheader('样例2：Range slider')
        values = st.slider(
            'Select a range of values',
            0.0, 100.0, (25.0, 75.0)
        )
        st.write('Values: ', values)
        st.code(code2, language='python')

        code3 = """
        import streamlit as st
        from datetime import time \n
        appointment = st.slider(
            "Schedule your appointment:",
            value=(time(11, 30), time(12, 45))
        )
        st.write("You're scheduled for: ", appointment)
        """
        st.subheader('样例3：Range time slider')
        appointment = st.slider(
            "Schedule your appointment:",
            value=(time(11, 30), time(12, 45))
        )
        st.write("You're scheduled for: ", appointment)
        st.code(code3, language='python')

        code4 = """
        import streamlit as st
        from datetime import time, datetime \n
        start_time = st.slider(
            "When do you start?",
            value=datetime(2020, 1, 1, 9, 30),
            format="MM/DD/YYYY - hh:mm"
        )
        st.write("Start time:", start_time)
        """
        st.subheader('样例4：Datatime slider')
        start_time = st.slider(
            "When do you start?",
            value=datetime(2020, 1, 1, 9, 30),
            format="MM/DD/YYYY - hh:mm"
        )
        st.write("Start time:", start_time)
        st.code(code4, language='python')

    def line_chart(self):
        code = """
        import streamlit as st
        import pandas as pd
        import numpy as np \n
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c']
        )
        st.line_chart(chart_data)
        """
        st.header('Line Chart')
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c']
        )
        st.line_chart(chart_data)
        st.code(code, language='python')

    def select_box(self):
        st.header('st.selectbox')
        code = """
        import streamlit as st \n
        option = st.selectbox(
            'What is your favorite color?',
            ('Blue',' Red', 'Green')
        )
        st.write('Your favorite color is ', option)
        """
        option = st.selectbox(
            'What is your favorite color?',
            ('Blue', ' Red', 'Green')
        )
        st.write('Your favorite color is ', option)
        st.code(code, language='python')


# if __name__ == '__main__':
#     page = st.sidebar.selectbox("选择示例页面",
#                                 ["主页", "button", "write", "slider", "line_chart", "selectbox"])
#     if page == 'button':
#         example.button()
#     elif page == 'write':
#         example.write()
#     elif page == 'slider':
#         example.slider()
#     elif page == 'line_chart':
#         example.line_chart()
#     elif page == 'selectbox':
#         example.select_box()
