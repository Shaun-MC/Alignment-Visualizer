import streamlit as st
from input_format_factory import InputFormatFactory
from io import StringIO

class MultipleAlignment:
    def __init__(self, input_type):
        self.max_char_input = 50
        self.max_height_pixels = 150
        self.unparsed_sequences = list()
        self.input_type = InputFormatFactory.create_input_format(input_type)

    def _set_unparsed_sequences(self, sequences):
        self.unparsed_sequences = sequences
        
    def get_unparsed_sequences(self):
        return self.unparsed_sequences if self.unparsed_sequences is not None else None

    def handle_input(self):

        st.header(f"Input (Max {self.max_char_input} Characters)")

        def retrieve_sequences_input() -> str:
            
            uploaded_file = st.file_uploader("Upload a Text File", type=["txt"])
            unclean_sequences = file_input = None

            if uploaded_file is not None:

                file_input = StringIO(uploaded_file.getvalue().decode("utf-8")).read()

                if len(file_input) > self.max_char_input:
                    input_length_error = f":red[File Input Longer Then Permitted. Allowed Length = {self.max_char_input}, File Length = {len(file_input)}]" 
                    st.write(input_length_error)

                    # Leave the text field empty
                    text = st.text_area(label="Text Input", value="", height=self.max_height_pixels, max_chars=self.max_char_input)

                    if text == "":
                        return None
                     
            # General text box
            # Display the data in the file if a file was uploaded, else, whatever the user types in the box
            unclean_sequences = (
                st.text_area(label="Text Input", value=file_input, height=self.max_height_pixels, max_chars=self.max_char_input) 
                if uploaded_file is not None else st.text_area(label="Text Input", value="", height=self.max_height_pixels, max_chars=self.max_char_input)
            )

            return None if unclean_sequences == "" else self.input_type.cleanSequences(unclean_sequences)

        # We don't need to parse input here as it's handled in a different class
        # This function only has retrieve it from the user - Include in documentation in the beginning of the function
        self._set_unparsed_sequences(retrieve_sequences_input())

    def execute_alignment(self, sequences, scoring_matrix):
        pass