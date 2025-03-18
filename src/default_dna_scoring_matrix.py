import streamlit as st
import pandas as pd

class DefaultDNAScoringMatrix:
    # todo either mirror input on diagonal axis or make a symetrical 
    def __init__(self):
        self.scoring_matrix = None
        self.total_characters = 5
        self.scoring_matrix = None

        # Initialize the matrix
        labels = ["_", "A", "G", "C", "T"]
        # Hard-coded data for the scoring matrix
        data = {
            "_": [0, 0, 0, 0, 0],
            "A": [0, 1, 0, 0, 0],
            "G": [0, 0, 1, 0, 0],
            "C": [0, 0, 0, 1, 0],
            "T": [0, 0, 0, 0, 1]
        }

        # Display the matrix
        self.scoring_matrix = pd.DataFrame(data, index=labels)