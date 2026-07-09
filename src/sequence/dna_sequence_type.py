import streamlit as st

class DNA:
    def __init__(self):

        @st.cache_data(persist="disk")
        def retrieve_valid_nucleotides():
            return {'A': None, 'C': None, 'G': None, 'T': None}
        
        self.valid_nucleotides = retrieve_valid_nucleotides()
        self.validated_sequences = list()

    def get_validated_sequences(self):
        return self.validated_sequences
    
    def validate_encoding(self, sequences: list[str]) -> None:

        if sequences is None:
            return

        for i, sequence in enumerate(sequences):
            
            upper_sequence = sequence.upper()
    
            sequences[i] = upper_sequence
    
            for nucleotide in upper_sequence:

                if nucleotide not in self.valid_nucleotides:
                    st.write(f":red[Invalid Input Format, Doesn't Match DNA Encoding Scheme (A, C, G, T): ]")
                    self.validated_sequences = list()
                    return 

            self.validated_sequences.append(upper_sequence)