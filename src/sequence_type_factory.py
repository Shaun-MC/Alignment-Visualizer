from dna_sequence_type import DNA
from rna_sequence_type import RNA
from protein_sequence_type import Protein

class SequenceTypeFactory:
    @staticmethod
    def create_sequence_type(sequence_type_option):

        match sequence_type_option:
            case "DNA":
                return DNA()
            case "RNA":
                return RNA()
            case "Protein":
                return Protein()
            case _:
                raise ValueError("Invalid sequence type option")