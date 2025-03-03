import streamlit as st
import pandas as pd
import numpy as np

st.title("Streamlit Playground")

st.write("Example Widgets")

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)