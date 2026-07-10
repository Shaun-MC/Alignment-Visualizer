from .scoring_matrix import ScoringMatrix
from .matrix_data import build_identity_matrix_data

LABELS = ["_", "A", "C", "G", "T"]


class NCBIBlastDivergentDNAScoringMatrix(ScoringMatrix):
    def __init__(self):
        # NCBI blastn guidance for more divergent sequences: reward +1, penalty -3
        super().__init__(LABELS, build_identity_matrix_data(LABELS, match=1, mismatch=-3))
