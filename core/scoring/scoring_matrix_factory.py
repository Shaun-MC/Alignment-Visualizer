from .custom_dna_scoring_matrix import CustomDNAScoringMatrix
from .custom_rna_scoring_matrix import CustomRNAScoringMatrix
from .custom_protein_scoring_matrix import ProteinScoringMatrix
from .default_dna_scoring_matrix import DefaultDNAScoringMatrix
from .default_rna_scoring_matrix import DefaultRNAScoringMatrix
from .default_protein_scoring_matrix import DefaultProteinScoringMatrix
from .ncbi_blast_dna_scoring_matrix_close import NCBIBlastCloseDNAScoringMatrix
from .ncbi_blast_dna_scoring_matrix_divergent import NCBIBlastDivergentDNAScoringMatrix
from .dna_full_scoring_matrix import DNAFullScoringMatrix
from .ribosum_rna_scoring_matrix import RibosumRNAScoringMatrix


class ScoringMatrixFactory:
    @staticmethod
    def create_scoring_matrix(using_scoring_matrix_option, sequence_type_option, preset_option=None):

        if using_scoring_matrix_option == "No":
            match sequence_type_option:
                case "DNA":
                    match preset_option:
                        case "NCBI BLAST (Close)":
                            return NCBIBlastCloseDNAScoringMatrix()
                        case "NCBI BLAST (Divergent)":
                            return NCBIBlastDivergentDNAScoringMatrix()
                        case "DNAfull":
                            return DNAFullScoringMatrix()
                        case _:
                            return DefaultDNAScoringMatrix()
                case "RNA":
                    match preset_option:
                        case "RIBOSUM":
                            return RibosumRNAScoringMatrix()
                        case _:
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
