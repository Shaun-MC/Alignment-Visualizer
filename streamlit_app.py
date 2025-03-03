import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Streamlit Playground")

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")
