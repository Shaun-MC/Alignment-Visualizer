import streamlit as st
import pandas as pd
from io import StringIO
from Bio import SeqIO
import time

# Look into Bio.AlingIO

DNA_KEY = "DNA"
RNA_KEY = "RNA"
PROTEIN_KEY = "Protein"

# Keys for each nucleotide letter representation
@st.cache_data(persist="disk")
def get_DNA_nucleotides_ascii():
    return {'A': None, 'C': None, 'G': None, 'T': None}

# Could have a single table or remove nucleotides from amino acid table 
# Not a big difference, doesn't really matter

# Keys for each amino acid letter representation
@st.cache_data(persist="disk")
def get_amino_acid_ascii():
    return {'A': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None, 'H': None, 'I': None, 'K': None, 
            'L': None, 'M': None, 'P': None, 'Q': None, 'R': None, 'S': None, 'T': None, 'V': None, 'Y': None}

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
    match sequence_type:
        case "DNA":
            DNA_nucleotides = get_DNA_nucleotides_ascii()
            for nucleotide in sequence:
                if nucleotide not in DNA_nucleotides:
                    return False
            return True
        case "RNA":
            DNA_nucleotides = get_DNA_nucleotides_ascii()
            for nucleotide in sequence:
            
                if nucleotide not in DNA_nucleotides or nucleotide != 'U':
                    return False
            return True
        case "Protein":
            amino_acids = get_amino_acid_ascii()
            for amino_acid in sequence:
                
                if amino_acid not in amino_acids:
                    return False
            return True
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

def runSingleAlignment(input_txt: list) -> str:
    """
    Purpose
    ----------
    Run the alignment on the provided list of strings.

    Parameters
    ----------
    input_txt : list
        List of strings to be aligned.

    Returns
    -------
    str
        Result of the alignment.
    """
    # Create a DataFrame with input_txt[0] on the y-axis and input_txt[1] on the x-axis
    y_axis = list(input_txt[0])
    x_axis = list(input_txt[1])
    
    # Create a custom HTML table with non-unique column and row names
    table_html = "<table><thead><tr><th></th>"
    for col in x_axis:
        table_html += f"<th> {col} </th>"
    table_html += "</tr></thead><tbody>"
    for row in y_axis:
        table_html += f"<tr><td> {row} </td>"
        for col in x_axis:
            table_html += "<td></td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"

    # Create a placeholder for the table
    table_placeholder = st.empty()

    # Initialize session state for visibility if it doesn't exist
    if 'visible' not in st.session_state:
        st.session_state.visible = True

    desiredRow = 0
    desiredColumn = 0
    curRow = 0
    curColumn = 0

    for num in range(len(y_axis) * len(x_axis) + 1):
        # Toggle visibility
        if st.session_state.visible:
            table_placeholder.markdown(table_html, unsafe_allow_html=True)
        else:
            table_placeholder.empty()
        
        # st.session_state.visible = not st.session_state.visible
        time.sleep(1)

        # Calculate current row and column positions
        curRow = num // len(x_axis)
        curCol = num % len(x_axis)
        
        # edit table
        table_html = "<table><thead><tr><th></th>"
        for col in range(len(x_axis)):
            if (col == curCol):
                table_html += f"<th>({x_axis[col]})</th>"
            else:
                table_html += f"<th> {x_axis[col]} </th>"
        table_html += "</tr></thead><tbody>"
        
        # Fill the table cells
        for row in range(len(y_axis)):
            if (row == curRow):
                table_html += f"<tr><td>({y_axis[row]})</td>"
            else:
                table_html += f"<tr><td> {y_axis[row]} </td>"
            for col in range(len(x_axis)):
                # If this cell should be filled (we've reached it in our iteration)
                if row < curRow or (row == curRow and col <= curCol):
                    random_value = 2  # 
                    table_html += f"<td>{random_value}</td>"
                else:
                    table_html += "<td></td>"
            table_html += "</tr>"
        table_html += "</tbody></table>"


    # Placeholder for the actual alignment logic
    # For now, just join the input strings with a newline
    #todo: display alignment
    return "\n".join(input_txt)

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
    scoring_matrix = st.radio("Using a Scoring Matrix?", ["No", "Yes"])

with format:
    input_format = st.radio("File Format: ", ["FASTA"])

# Display a 5x5 table for scoring matrix input if "Yes" is selected
if scoring_matrix == "Yes":
    st.header("Custom Scoring Matrix")
    labels = ["_", "A", "G", "C", "T"]
    data = {label: [0] * 5 for label in labels}
    df = pd.DataFrame(data, index=labels)
    edited_df = st.data_editor(df, use_container_width=True)
    #st.write("Scoring Matrix:", edited_df)

# Modualize the single vs multiple into its own files ??? - future
if alignment_type == "Single":
    
    # Narrow down later depending on how long it'll take
    max_char_input = 20
    max_height_pixels = 68
    
    st.header(f"Input (Max {max_char_input} Characters)")
    
    s1_input, s2_input = st.columns(2)
    
    with s1_input:
        S1 = st.text_area(label="S1: ", value="", height=max_height_pixels, max_chars=max_char_input)
    
    with s2_input:
        S2 = st.text_area(label="S2: ", value="", height=max_height_pixels, max_chars=max_char_input)
    
    # WAIT UNTIL THE INPUT IS IN THE TEXT BOX IN BEGIN PARSING IT 
    if not validateEncodings(sequence_type, [S1, S2]):
        
        st.write(f":red[Invalid Input Format, Doesn't Meet {sequence_type} Standards: ]")
    
    # Validation Passed
    input_txt.append(S1)
    input_txt.append(S2)
        
    # Test if the string is on multiple lines - if that matters
    # If the strings is DNA or Protein encoding
    
    # Add the "Run Alignment" button
    if st.button("Run Alignment"):
        # Placeholder for the alignment function
        st.write("Running alignment...")
        returnValue = runSingleAlignment(input_txt)
        st.write(returnValue)

# Modularize into multiple strings input - 2 strings would go into the 'single' alignment module
else: 

    max_char_input = 100
    max_height_pixels = 150
    # Input Text Box - FASTA Only & Choose File
    # Display the contents of this file
    
    st.header("Input")
    uploaded_file = st.file_uploader("Upload a Text File") # When the file is updated - keep the file name & display the contents 
    input = ""
    file_input = ""

    # Can probably use pandas to read in the data if its long
    def readFromFile():
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        return stringio.read()
    
    if uploaded_file:
        file_input = readFromFile()
    
    if len(file_input) > max_char_input:
        st.write(f":red[File Input Longer Then Permitted. Allowed Length = {max_char_input}, File Length = {len(file_input)}]")
        st.text_area(label="Text Input", value="", height=max_height_pixels, max_chars=max_char_input)
    else:
        input = st.text_area(label="Text Input", value=file_input, height=max_height_pixels, max_chars=max_char_input,) if uploaded_file is not None else st.text_area(label="Text Input", value="", height =max_height_pixels, max_chars=max_char_input)


# Footer
st.markdown(
    '<footer style="text-align: center"> University of Washington Bothell CSSE, (Shaun Cushman, Aaron Gröpper) </footer>', 
    unsafe_allow_html=True
)