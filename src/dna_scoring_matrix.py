import streamlit as st
import pandas as pd

class DNAScoringMatrix:
    # todo either mirror input on diagonal axis or make a symetrical 
    def __init__(self):
        self.scoring_matrix = None
        self.total_characters = 5
        self.scoring_matrix = None

        # Initialize the matrix
        st.header("Custom Scoring Matrix")
        labels = ["_", "A", "G", "C", "T"]
        data = {label: [0] * self.total_characters for label in labels}

        # Display the matrix
        self.scoring_matrix = st.data_editor(pd.DataFrame(data, index=labels), use_container_width=True)