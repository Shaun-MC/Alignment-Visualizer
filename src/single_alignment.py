import streamlit as st
from alignment_algorithm_factory import AlignmentAlgorithmFactory
        
class SingleAlignment:
    
    def __init__(self, alignment_location):
        self.max_char_input = 10
        self.max_height_pixels = 68
    
        self.S1 = None
        self.S2 = None

        # Global or Local
        self.alignment_location = AlignmentAlgorithmFactory.assign_alignment_algorithm(alignment_location)

    def _set_first_sequence(self, S1):
        self.S1 = S1

    def _set_second_sequence(self, S2):
        self.S2 = S2

    def get_unparsed_sequences(self):
        return [self.S1, self.S2] if self.S1 != "" and self.S2 != "" else []

    def handle_input(self):

        st.header(f"Input (Max {self.max_char_input} Characters)")

        # Declare the options variables for single alignment input
        s1_input, s2_input = st.columns(2)

        # Display the options buttons
        # Once the strings are inputted and validation fails, how will the user be repromted?
        with s1_input:
            self._set_first_sequence(st.text_area(label="S1: ", value="", height=self.max_height_pixels, max_chars=self.max_char_input))
            
        with s2_input:
            self._set_second_sequence(st.text_area(label="S2: ", value="", height=self.max_height_pixels, max_chars=self.max_char_input))

        st.markdown(
                """
                    <style>
                        div[class*="stTextArea"] > label > div[data-testid="stMarkdownContainer"] > p {
                            font-size: 20px;
                        }
                    </style>
                """, 
            unsafe_allow_html=True)

    def execute_alignment(self, input_txt: list, scoring_matrix, animation_speed) -> str:

        y_axis = ["_"] + list(input_txt[0])
        x_axis = ["_"] + list(input_txt[1])

        # Could shorten into just the return statement - not as readable
        # Excutes global or local alignment
        alignments, lcs, final_score = self.alignment_location.execute_alignment(x_axis, y_axis, scoring_matrix, animation_speed)

        return (alignments, lcs, final_score)