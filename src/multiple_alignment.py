import streamlit as st
from io import StringIO

class MultipleAlignment:
    def __init__(self):
        self.max_char_input = 100
        self.max_height_pixels = 150
        self.input_header = f"Input (Max {self.max_char_input} Characters)"
        self.upload_header = "Upload a Text File"

        self.unparsed_sequences = None

    def _set_unparsed_sequences(self, sequences):
        self.unparsed_sequences = sequences
        
    def get_unparsed_sequences(self) -> list:
        return self.unparsed_sequences

    def handle_input(self) -> None:

        st.header(self.input_header)

        def retrieve_sequences_input() -> str:
            
            uploaded_file = st.file_uploader(self.upload_header, type=["txt"])
            file_input = None

            if uploaded_file is not None:

                file_input = StringIO(uploaded_file.getvalue().decode("utf-8")).read()

                if len(file_input) > self.max_char_input:
                    input_length_error = f":red[File Input Longer Then Permitted. Allowed Length = {self.max_char_input}, File Length = {len(file_input)}]" 
                    st.write(input_length_error)

                    # Leave the text field empty
                    st.text_area(label="Text Input", value="", height=self.max_height_pixels, max_chars=self.max_char_input)
                    return None
                    
            # General text box
            # Display the data in the file if a file was uploaded, else, whatever the user types in the box
            return (
                st.text_area(label="Text Input", value=file_input, height=self.max_height_pixels, max_chars=self.max_char_input,) 
                if uploaded_file is not None else st.text_area(label="Text Input", value="", height=self.max_height_pixels, max_chars=self.max_char_input)
            )
                
        # We don't need to parse or validate the sequence input here as it's handled in a different class
        # This function only has retrieve it from the user - Include in doc in the beginning of the function
        self._set_sequences(retrieve_sequences_input())