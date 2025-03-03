import streamlit as st
import pandas as pd
import numpy as np

st.title("Streamlit Playground")

st.write("Example Dataframe")

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))