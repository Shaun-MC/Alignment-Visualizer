import streamlit as st

class Options:
    # Constructor
    def __init__(self):
        self.alignment_type = None
        self.using_scoring_matrix = None
        self.input_format = None
        self.sequence_type = None
        self.alignment_location = None

        self._execute()

    # Getters - Setters
    def set_alignment_type(self, alignment_type):
        self.alignment_type = alignment_type

    def set_using_scoring_matrix(self, scoring_matrix):
        self.using_scoring_matrix = scoring_matrix

    def set_input_format(self, file_format):
        self.input_format = file_format

    def set_sequence_type(self, sequence_type):
        self.sequence_type = sequence_type

    def set_alignment_location(self, alignment_location):
        self.alignment_location = alignment_location

    def get_alignment_type(self):
        return self.alignment_type

    def get_using_scoring_matrix(self):
        return self.using_scoring_matrix

    def get_input_format(self):
        return self.input_format

    def get_sequence_type(self):
        return self.sequence_type

    def get_alignment_location(self):
        return self.alignment_location

    # Actions
    def _execute(self):

        st.header("Input Settings")
        
        # Declare all the options variables
        sequence_types, alignment_types = st.columns(2)
        using_scoring_matrix, file_formats = st.columns(2)
        alignment_location, blank = st.columns(2)

        # Display the option buttons
        # First options in the list is the default
        with sequence_types:
            self.set_sequence_type(st.radio("Sequence Type: ", ["DNA", "RNA", "Protein"]))
   
        with alignment_types:
            self.set_alignment_type(st.radio("Alignment Types: ", ["Single", "Multiple"]))

        with using_scoring_matrix:
            self.set_using_scoring_matrix(st.radio("Using a Scoring Matrix?", ["No", "Yes"]))

        with file_formats:
            self.set_input_format(st.radio("Input Format: ", ["Plain Text", "FASTA"]))

        with alignment_location:
            self.set_alignment_location(st.radio("Alignment Location: ", ["Local", "Global"]))

        st.markdown(
            """
                <style>
                    div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
                        font-size: 20px;
                    }
                </style>
            """, 
        unsafe_allow_html=True)