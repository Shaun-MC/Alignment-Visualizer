class ScoringMatrixFactory:
    @staticmethod
    def create_scoring_matrix_type(using_scoring_matrix_option, sequence_type_option):

        if using_scoring_matrix_option is None:
            return None
        
        match sequence_type_option:
            case "DNA":
                return DNAScoringMatrix()
            case "RNA":
                return RNAScoringMatrix()
            case "Protein":
                return ProteinScoringMatrix()
            case _:
                raise ValueError("Invalid sequence type option")