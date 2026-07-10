from .scoring_matrix import ScoringMatrix
from .matrix_data import build_identity_matrix_data

LABELS = ["_", "A", "C", "G", "T"]


class DefaultDNAScoringMatrix(ScoringMatrix):
    def __init__(self):
        super().__init__(LABELS, build_identity_matrix_data(LABELS, match=1, mismatch=-1))
