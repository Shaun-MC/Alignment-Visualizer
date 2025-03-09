import streamlit as st
from io import StringIO
from Bio import SeqIO

# Look into Bio.AlingIO

DNA_KEY = "DNA"
RNA_KEY = "RNA"
PROTEIN_KEY = "Protein"

# ASCII values of A, C, G, T
@st.cache_data(persist="disk")
def get_DNA_nucleotides_ascii():
    return {65: None, 67: None, 71: None}

# ASCII values for each of the amino acids: F, L, I, V, etc.,
@st.cache_data(persist="disk")
def get_amino_acid_ascii():
    return {82: None, 76: None, 73: None, 86: None, 77: None, 83: None, 80: None, 84: None, 65: None, 
            89: None, 78: None, 68: None, 81: None, 75: None, 69: None, 67: None, 82: None, 71: None, 87: None}


def validateEncoding(sequence_type: str, sequence: str) -> bool:
    
    """
    Iterates through a sequence to determine if it's valid against the sequence type

    Parameters
    ----------
    sequence_type : str
        type of sequence that's currently supported (DNA, RNA, Protein)
    
    sequence : list
        the sequence that need to be verified against the sequence type

    Returns
    -------
    bool
        True if all characters in the sequence match the sequence type
    """
    
    # https://docs.python.org/3.10/whatsnew/3.10.html#pep-634-structural-pattern-matching
    # Future, In the case statements, I want to use DNA_KEY variables instead of the string literal
    # Might have to wrap the KEY's in a class, look more into the documentation, works for now
    match sequence_type:
        
        case "DNA":
            
            DNA_nucleotides = get_DNA_nucleotides_ascii()
            
            for nucleotide in sequence:
                if ord(nucleotide) not in DNA_nucleotides:
                    return False
        
            return True

        case "RNA":
            
            DNA_nucleotides = get_DNA_nucleotides_ascii()
            
            for nucleotide in sequence:
            
                if ord(nucleotide) not in DNA_nucleotides or nucleotide != 'U':
                    return False
        
            return True

        case "Protein":
            
            amino_acids = get_amino_acid_ascii()
            
            for amino_acid in sequence:
                
                if ord(amino_acid) not in amino_acids:
                    return False
            
        case _:
            # ERROR CASE - ADD TO A LOG
            return True

def validateEncodings(sequence_type: str, sequences: list) -> bool:
    """
    Checks if all the passed in sequences are valid against the passed in sequence type
        Interface for the validateEncoding() function

    Parameters
    ----------
    sequence_type : str
        type of sequence that's currently supported (DNA, RNA, Protein)
    
    sequences : list
        the sequences that need to be verified against the sequence type

    Returns
    -------
    bool
        True if all sequences are valid against the sequence_type

    """
    ret = True

    for sequence in sequences:
        
        ret &= validateEncoding(sequence_type, sequence)
    
    return ret

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
    sequence_type = st.radio("Sequence Type: ", ["DNA", "RNA", "Protein"])
    
with alignment_types:
    alignment_type = st.radio("Alignment Types: ", ["Single", "Multiple"])

with using_scoring_matrix:
    scoring_matrix = st.radio("Using a Scoring Matrix?", ["Yes", "No"])

with format:
    input_format = st.radio("File Format: ", ["FASTA"])

# Modualize the single vs mutliple into it's own files ??? - future
if alignment_type == "Single":
    
    # Narrow down later depending on how long it'll take
    max_char_input = 100
    max_height_pixels = 68
    
    st.header(f"Input (Max {max_char_input} Characters)")
    
    s1_input, s2_input = st.columns(2)
    
    with s1_input:
        S1 = st.text_area(label="S1: ", value="", height=max_height_pixels, max_chars=max_char_input)
    
    with s2_input:
        S2 = st.text_area(label="S2: ", value="", height=max_height_pixels, max_chars=max_char_input)
    
    # WAIT UNTIL THE INPUT IS IN THE TEXT BOX IN BEGIN PARSING IT 
    if not validateEncoding(sequence_type, [S1, S2]):
        
        st.write(f"[red]: Invalid Input Format, Doesn't Meet {sequence_type} Standards")
    
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