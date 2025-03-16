import streamlit as st

class ProteinScoringMatrix:
    def __init__(self):

        st.header("Available Protein Scoring Matrices")
        st.radio("Scoring Matrix: ", ["BLOSUM62"])

        @st.cache_data(persist="disk")
        def retrieve_blosum62():
            # TODO
            return
            
        self.blosum62 = retrieve_blosum62()
        