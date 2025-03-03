import streamlit as st
import pandas as pd
import numpy as np

st.title("Streamlit Playground")

dataframe = np.random.randn(10, 20)

st.dataframe(dataframe)


# Button Stuff
""" 
if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button

st.button('Click me', on_click=click_button)

if st.session_state.button:
    # The message and nested widget will remain on the page
    st.write('Button is on!')
    
else:
    st.write('Button is off!')
"""