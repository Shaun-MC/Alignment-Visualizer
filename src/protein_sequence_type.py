import streamlit as st

class Protein:
    def __init__(self):

        @st.cache_data(persist="disk")
        def retrieve_valid_nucleotides():
            return {
                'A': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None, 'H': None, 'I': None, 'K': None, 
                'L': None, 'M': None, 'P': None, 'Q': None, 'R': None, 'S': None, 'T': None, 'V': None, 'Y': None
            }
        
        self.valid_nucleotides = retrieve_valid_nucleotides()
        self.validated_sequences = list()

    def get_validated_sequences(self):
        return self.validated_sequences
    
    def validate_sequences(self, sequences):

        if sequences is None:
            return

        for sequence in sequences:

            for nucleotide in sequence:

                if nucleotide not in self.valid_nucleotides:
                    st.write(f":red[Invalid Input Format, Doesn't Meet DNA Standards: ]")
                    return

            self.validated_sequences.append(sequence)