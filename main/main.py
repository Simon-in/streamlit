import os
import streamlit as st
import logging as log
import datetime as dt
import pandas as pd

if __name__ == "__main__":
    st.title("Hello, Streamlit!")
    st.write("Welcome to your first Streamlit app.")
    # 添加一个输入框
    user_input = st.text_input("Type something:")
    st.write(f"You typed: {user_input}")
    # 添加一个按钮
    if st.button("Click me!"):
        st.write("Button clicked!")