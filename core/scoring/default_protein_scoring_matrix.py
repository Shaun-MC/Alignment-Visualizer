from .scoring_matrix import ScoringMatrix
from .matrix_data import build_identity_matrix_data

LABELS = ("_", "A", "C", "D", "E", "F", "G", "H", "I", "K",
          "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y")


class DefaultProteinScoringMatrix(ScoringMatrix):
    def __init__(self):
        super().__init__(LABELS, build_identity_matrix_data(LABELS, match=1, mismatch=0))
