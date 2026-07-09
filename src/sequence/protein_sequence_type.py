import streamlit as st

class Protein:
    def __init__(self):

        @st.cache_data(persist="disk")
        def retrieve_valid_nucleotides() -> dict:
            return {
                'A': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None, 'H': None, 'I': None, 'K': None, 
                'L': None, 'M': None, 'P': None, 'Q': None, 'R': None, 'S': None, 'T': None, 'V': None, 'Y': None
            }
        
        self.valid_nucleotides = retrieve_valid_nucleotides()
        self.validated_sequences = list()

    def get_validated_sequences(self) -> list[str]:
        return self.validated_sequences
    
    def validate_encoding(self, sequences: list[str]) -> None:

        if sequences is None:
            return

        for i, sequence in enumerate(sequences):
            
            upper_sequence = sequence.upper()
    
            sequences[i] = upper_sequence
    
            for nucleotide in upper_sequence:
                if nucleotide not in self.valid_nucleotides:
                    st.write(f":red[Invalid Input Format, Doesn't Meet Amino Acid Encoding Scheme (A, C, D, E, F, etc.,): ]")
                    return 

            self.validated_sequences.append(upper_sequence)