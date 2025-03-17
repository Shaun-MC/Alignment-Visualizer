import streamlit as st
import pandas as pd
import numpy as np

class RNAScoringMatrix:

    def __init__(self):
        self.scoring_matrix = None
        self.total_characters = 5

        # Initialize the matrix
        st.header("Custom Scoring Matrix")
        labels = ["_", "A", "G", "C", "U"]

        data = {
            "_": [0, np.nan, np.nan, np.nan, np.nan],
            "A": [0, 0, np.nan, np.nan, np.nan],
            "G": [0, 0, 0, np.nan, np.nan],
            "C": [0, 0, 0, 0, np.nan],
            "U": [0, 0, 0, 0, 0]
        }

        # Display the matrix
        self.scoring_matrix = st.data_editor(pd.DataFrame(data, index=labels), use_container_width=True)