import streamlit as st

class DefaultProteinScoringMatrix:
    def __init__(self):

        @st.cache_data(persist="disk")
        def retrieve_blosum62():
            # TODO
            return
            
        self.blosum62 = retrieve_blosum62()
        