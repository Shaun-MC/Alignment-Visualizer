from dna_scoring_matrix import DNAScoringMatrix
from rna_scoring_matrix import RNAScoringMatrix
from protein_scoring_matrix import ProteinScoringMatrix
from default_dna_scoring_matrix import DefaultDNAScoringMatrix
from default_rna_scoring_matrix import DefaultRNAScoringMatrix

class ScoringMatrixFactory:
    @staticmethod
    def create_scoring_matrix(using_scoring_matrix_option, sequence_type_option):

        if using_scoring_matrix_option == "No":
            # todo: return default scoring matrix for DNA, RNA and Protein
            match sequence_type_option:
                case "DNA":
                    return DefaultDNAScoringMatrix()
                case "RNA":
                    # todo: make defautl rna matrix
                    return DefaultRNAScoringMatrix()
                case "Protein":
                    # todo: make defautl protein matrix
                    return ProteinScoringMatrix()
                case _:
                    raise ValueError("Invalid sequence type option")
        
        match sequence_type_option:
            case "DNA":
                return DNAScoringMatrix()
            case "RNA":
                return RNAScoringMatrix()
            case "Protein":
                return ProteinScoringMatrix()
            case _:
                raise ValueError("Invalid sequence type option")