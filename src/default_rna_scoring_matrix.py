import streamlit as st
import pandas as pd
import numpy as np

class DefaultRNAScoringMatrix:

    def __init__(self):
        self.scoring_matrix = None
        self.total_characters = 5

        # Initialize the matrix
        labels = ["_", "A", "G", "C", "U"]

        data = {
            "_": [0, 0, 0, 0, 0],
            "A": [0, 1, 0, 0, 0],
            "G": [0, 0, 1, 0, 0],
            "C": [0, 0, 0, 1, 0],
            "U": [0, 0, 0, 0, 1]
        }

        # Display the matrix
        self.scoring_matrix = pd.DataFrame(data, index=labels)