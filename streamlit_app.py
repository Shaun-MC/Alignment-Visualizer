import streamlit as st
import pandas as pd
import numpy as np

st.title("Streamlit Playground")

dataframe = np.random.randn(10, 20)

st.dataframe(dataframe)