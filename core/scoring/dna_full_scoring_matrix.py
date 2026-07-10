from .scoring_matrix import ScoringMatrix
from .matrix_data import build_identity_matrix_data

LABELS = ["_", "A", "C", "G", "T"]


class DNAFullScoringMatrix(ScoringMatrix):
    def __init__(self):
        # EDNAFULL/DNAfull matrix (EMBOSS needle/water default): match +5, mismatch -4
        super().__init__(LABELS, build_identity_matrix_data(LABELS, match=5, mismatch=-4))
