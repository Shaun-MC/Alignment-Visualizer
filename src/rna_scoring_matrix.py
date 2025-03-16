import streamlit as st
import pandas as pd

class RNAScoringMatrix:

    def __init__(self):
        self.scoring_matrix = None
        self.total_characters = 5

        # Initialize the matrix
        st.header("Custom Scoring Matrix")
        labels = ["_", "A", "G", "C", "U"]
        data = {label: [0] * self.total_characters for label in labels}

        # Display the matrix
        st.data_editor(pd.DataFrame(data, index=labels), use_container_width=True)