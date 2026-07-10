from .scoring_matrix import ScoringMatrix
from .matrix_data import build_identity_matrix_data

LABELS = ["_", "A", "C", "G", "T"]


class NCBIBlastCloseDNAScoringMatrix(ScoringMatrix):
    def __init__(self):
        # NCBI blastn default for highly similar sequences: reward +1, penalty -2
        super().__init__(LABELS, build_identity_matrix_data(LABELS, match=1, mismatch=-2))
