import streamlit as st
import pandas as pd
import numpy as np

class DNAScoringMatrix:
    # todo either mirror input on diagonal axis or make a symetrical 
    def __init__(self):
        self.scoring_matrix = None
        self.total_characters = 5
        self.scoring_matrix = None

        # Initialize the matrix
        st.header("Custom Scoring Matrix")
        labels = ["_", "A", "G", "C", "T"]
        # Define the data with varying column heights
        data = {
            "_": [0, np.nan, np.nan, np.nan, np.nan],
            "A": [0, 0, np.nan, np.nan, np.nan],
            "G": [0, 0, 0, np.nan, np.nan],
            "C": [0, 0, 0, 0, np.nan],
            "T": [0, 0, 0, 0, 0]
        }

        # Display the matrix
        self.scoring_matrix = st.data_editor(pd.DataFrame(data, index=labels), use_container_width=True)