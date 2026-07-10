from .scoring_matrix import ScoringMatrix
from .matrix_data import build_editable_template_data

LABELS = ["_", "A", "C", "G", "U"]


class CustomRNAScoringMatrix(ScoringMatrix):
    def __init__(self):
        super().__init__(LABELS, build_editable_template_data(LABELS))
