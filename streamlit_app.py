import streamlit as st
import pandas as pd

st.title("2D Alignment Visualizer")
st.write("Hello World")



df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df


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