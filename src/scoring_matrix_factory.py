from custom_dna_scoring_matrix import CustomDNAScoringMatrix
from custom_rna_scoring_matrix import CustomRNAScoringMatrix
from protein_scoring_matrix import ProteinScoringMatrix
from default_dna_scoring_matrix import DefaultDNAScoringMatrix
from default_rna_scoring_matrix import DefaultRNAScoringMatrix
from default_protein_scoring_matrix import DefaultProteinScoringMatrix

class ScoringMatrixFactory:
    @staticmethod
    def create_scoring_matrix(using_scoring_matrix_option, sequence_type_option):

        if using_scoring_matrix_option == "No":
            match sequence_type_option:
                case "DNA":
                    return DefaultDNAScoringMatrix()
                case "RNA":
                    return DefaultRNAScoringMatrix()
                case "Protein":
                    return DefaultProteinScoringMatrix()
                case _:
                    raise ValueError("Invalid sequence type option")
        
        match sequence_type_option:
            case "DNA":
                return CustomDNAScoringMatrix()
            case "RNA":
                return CustomRNAScoringMatrix()
            case "Protein":
                return ProteinScoringMatrix()
            case _:
                raise ValueError("Invalid sequence type option")