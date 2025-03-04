import streamlit as st
from io import StringIO

# Header
st.markdown(
    '<header style="text-align: center"> Sequence Alignment Visualizer </header>', 
    unsafe_allow_html=True
)

# Buttons for DNA or Protein Alignment
st.header("Input Settings")

sequence_types, alignment_types = st.columns(2)
is_using_scoring_matrix, placeholder = st.columns(2)

seq_type = al_type = None

input_txt = []

with sequence_types:
    sequence_type = st.radio("Sequence Type: ", ["DNA", "Protein"])
    
with alignment_types:
    alignment_type = st.radio("Alignment Types: ", ["Single", "Multiple"])

with is_using_scoring_matrix:
    scoring_matrix = st.radio("Using a Scoring Matrix?", ["Yes", "No"])

if alignment_type == "Single":
    
    max_char_input = 20
    st.header(f"Input (Max {max_char_input} Characters)")
    
    max_height_pixels = 68
    
    s1_input, s2_input = st.columns(2)
    
    with s1_input:
        S1 = st.text_area(label="S1: ", value="", height=max_height_pixels, max_chars=max_char_input)
    
    with s2_input:
        S2 = st.text_area(label="S2: ", value="", height=max_height_pixels, max_chars=max_char_input)
    
    def validateEncoding(sequence_type, S1, S2):
        
        if sequence_type == "DNA":
            return True
            
        elif sequence_type == "Protein":
            return True
            
    if not validateEncoding(sequence_type, S1, S2):
        
        # Display some kind of error message
        st.write("Placeholder")
        
    # Test if the string is on multiple lines - if that matters
    # If the strings is DNA or Protein encoding
    
else: 

    # Input Text Box - FASTA Only & Choose File
    # Display the contents of this file
    st.header("Input (FATSA)")
    uploaded_file = st.file_uploader("Upload a Text File") # When the file is updated - keep the file name & display the contents 

    def readFromFile():

        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        return stringio.read()
        
    input_txt = st.text_area("Text Input", readFromFile()) if uploaded_file is not None else st.text_area("Text Input", "")

# Parse the Input for correct syntax, >Rosalind...`

# Footer
st.markdown(
    '<footer style="text-align: center"> University of Washington Bothell CSSE, (Shaun Cushman, Aaron Gröpper) </footer>', 
    unsafe_allow_html=True
)