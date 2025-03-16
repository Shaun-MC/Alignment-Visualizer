import streamlit as st

class SingleAlignment:
    def __init__(self):
        self.max_char_input = 20
        self.max_height_pixels = 68
        self.input_header = f"Input (Max {self.max_char_input} Characters)"

        self.S1 = None
        self.S2 = None

        self._handleInput()

    def set_first_sequence(self, S1):
        self.S1 = S1

    def set_second_sequence(self, S2):
        self.S2 = S2

    def retrieve_input(self) -> list:
        return [self.S1, self.S2]

    def _handleInput(self):

        st.header(self.input_header)

        # Declare the options variables for single alignment input
        s1_input, s2_input = st.columns(2)

        # Display the options buttons
        # Once the strings are inputted and validation fails, how will the user be repromted?
        with s1_input:
            self.set_first_sequence(st.text_area(label="S1: ", value="", height=self.max_height_pixels, max_chars=self.max_char_input))
            
        with s2_input:
            self.set_second_sequence(st.text_area(label="S2: ", value="", height=self.max_height_pixels, max_chars=self.max_char_input))

    