import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

# Hide streamlit default menu and footer from the template
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden}
    footer {visibility: hidden}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title('Project realestate')