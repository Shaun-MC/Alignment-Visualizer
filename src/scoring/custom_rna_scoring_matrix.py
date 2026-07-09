import streamlit as st
import pandas as pd
import numpy as np
from streamlit import session_state as ss
import uuid

class CustomRNAScoringMatrix:

    def __init__(self):
        self.scoring_matrix = None
        self.total_characters = 5

        # Initialize the matrix
        st.header("Custom Scoring Matrix")
        labels = ["_", "A", "C", "G", "U"]

        data = {
            "_": [0, np.nan, np.nan, np.nan, np.nan],
            "A": [0, 0, np.nan, np.nan, np.nan],
            "C": [0, 0, 0, np.nan, np.nan],
            "G": [0, 0, 0, 0, np.nan],
            "U": [0, 0, 0, 0, 0]
        }

        self.original_scoring_matrix = pd.DataFrame(data, index=labels)

        # Idk about keeping this here - apart of my final attempt to reset the table
        if "table_uuid" not in ss:
            ss.table_uuid = str(uuid.uuid4())

        # Idk about keeping this here - apart of my final attempt to reset the table
        if "dna_scoring_matrix" not in ss:
            ss.dna_scoring_matrix = self.original_scoring_matrix.copy(deep=True)
            
        self.scoring_matrix = st.data_editor(
            ss.dna_scoring_matrix, 
            on_change=self.validate_scoring_matrix, 
            use_container_width=True,
            key=ss.table_uuid,
            args=[self.original_scoring_matrix]
        )

    # I beilieve the solution to resetting the table is in this discussion posts
    # Resetting st.data_editor keys: https://discuss.streamlit.io/t/how-to-refresh-datasets-in-st-data-editor/66710
    # Swapping source dataframes: https://discuss.streamlit.io/t/update-data-in-data-editor-automatically/49839/5
    # I've spent way to long trying to make this work, it doesn't work, I'm going to move on
    # Should also change the name of this function to reflect what it's supposed to do - reset the table if an 'None' value is updated
    def validate_scoring_matrix(self, original_matrix) -> None:
    
        current_matrix = st.session_state["dna_scoring_matrix"]
        
        for row, updates in st.session_state[ss.table_uuid]["edited_rows"].items():

            for _, column in updates.items():

                if pd.isna(original_matrix.iloc[row, column]) and not pd.isna(current_matrix.iloc[row, column]):
                    ss.table_uuid = str(uuid.uuid4())