from .scoring_matrix import ScoringMatrix

LABELS = ["_", "A", "C", "G", "U"]

# Real RIBOSUM matrices (e.g. RIBOSUM85-60) score RNA base-*pairs* for structure-aware
# alignment, not single nucleotides - there's no standard single-base reduction. This is
# an approximate, unverified placeholder: transitions (A<->G, C<->U) score better than
# transversions to loosely reflect RIBOSUM's transition bias, but the exact numbers below
# aren't derived from the published matrix.
_DATA = {
    "_": {"_": 0, "A": 0, "C": 0, "G": 0, "U": 0},
    "A": {"_": 0, "A": 2, "C": -2, "G": 0, "U": -2},
    "C": {"_": 0, "A": -2, "C": 2, "G": -2, "U": 0},
    "G": {"_": 0, "A": 0, "C": -2, "G": 2, "U": -2},
    "U": {"_": 0, "A": -2, "C": 0, "G": -2, "U": 2},
}


class RibosumRNAScoringMatrix(ScoringMatrix):
    def __init__(self):
        super().__init__(LABELS, _DATA)
