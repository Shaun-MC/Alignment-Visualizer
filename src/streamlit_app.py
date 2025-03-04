import streamlit as st
from io import StringIO
from Bio import SeqIO

# Look into Bio.AlingIO

# Two lines
def isFASTATwoStrings(S1: str, S2: str) -> bool:
    """
    Purpose
    ----------
    

    Parameters
    ----------

    Returns
    -------
    
    """
    return True
    
def isFASTABatchInput(input: list) -> bool:
    """
    Purpose
    ----------
    

    Parameters
    ----------

    Returns
    -------
    
    """
    return True
# Bulk

def isValidEncodingTwoStrings(sequence_type: str, S1: str, S2: str) -> bool:
    """
    Purpose
    ----------
    

    Parameters
    ----------

    Returns
    -------
    
    """
    if sequence_type == "DNA":
        return True
            
    elif sequence_type == "Protein":
        return True

def isValidEncodingBatchInput(sequence_type: str, input: list) -> bool:
    """
    Purpose
    ----------
    

    Parameters
    ----------

    Returns
    -------
    
    """
    return True

# Header
st.markdown(
    '<header style="text-align: center"> Sequence Alignment Visualizer </header>', 
    unsafe_allow_html=True
)

# Buttons for DNA or Protein Alignment
st.header("Input Settings")

sequence_types, alignment_types = st.columns(2)
using_scoring_matrix, format = st.columns(2)

seq_type = al_type = None

input_txt = []

with sequence_types:
    sequence_type = st.radio("Sequence Type: ", ["DNA", "Protein"])
    
with alignment_types:
    alignment_type = st.radio("Alignment Types: ", ["Single", "Multiple"])

with using_scoring_matrix:
    scoring_matrix = st.radio("Using a Scoring Matrix?", ["Yes", "No"])

with format:
    input_format = st.radio("File Format: ", ["FASTA"])

# Modualize into it's own file ???
if alignment_type == "Single":
    
    # Narrow down later depending on how long it'll take
    max_char_input = 100
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
    
    # Validation Passed
    input_txt.append(S1)
    input_txt.append(S2)
        
    # Test if the string is on multiple lines - if that matters
    # If the strings is DNA or Protein encoding
    
# Modularize into multiple strings input - 2 strings would go into the 'single' alignment module
else: 

    # Input Text Box - FASTA Only & Choose File
    # Display the contents of this file
    st.header("Input (FATSA)")
    uploaded_file = st.file_uploader("Upload a Text File") # When the file is updated - keep the file name & display the contents 

    # Can probably use pandas to read in the data if its long
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