import streamlit as st

# Header
st.markdown(
    '<header style="text-align: center"> Sequence Alignment Visualizer </header>', 
    unsafe_allow_html=True
)

# Buttons for DNA or Protein Alignment
st.header("Input Settings")

DNA_key = "DNA"
Protein_key = "Protein"
SingleAlignment_key = "SingleAlignment"
MultipleAlignment_key = "MultipleAlignment"

def click_button(button_key):
    st.session_state[button_key] = not st.session_state[button_key]

# Bug - when the button is pressed, it resets all states of the button because the session state is refreshed

# Error checking - making sure at least one of these are selected before executing sequence alignment
# Testing - only one can be selected at a time, exepected behavior
if 'DNA' not in st.session_state:
    st.session_state.DNA = False
    
if 'Protein' not in st.session_state:
    st.session_state.Protein = False
     
# Error checking - making sure at least one of these are selected before executing sequence alignment
# Testing - only one can be selected at a time, exepected behavior
if 'SingleAlignment' not in st.session_state:
    st.session_state.SingleAlignment = False

if 'MultipleAlignment' not in st.session_state:
    st.session_state.MultipleAlignment = False

st.header("Sequence Type:")

DNA_col, protein_col = st.columns(2)

with DNA_col:
    st.button('DNA', on_click=click_button(DNA_key))

with protein_col:
    st.button('Protein', on_click=click_button(Protein_key))

st.header("Alignment Type:")

signle_col, multi_col = st.columns(2)

with signle_col:
    st.button('Single Alignment', on_click=click_button(SingleAlignment_key))
    
with multi_col:
    st.button('Multiple Alignment', on_click=click_button(MultipleAlignment_key))

# Footer
st.markdown(
    '<footer style="text-align: center"> University of Washington Bothell CSSE, (Shaun Cushman, Aaron Gröpper) </footer>', 
    unsafe_allow_html=True
)