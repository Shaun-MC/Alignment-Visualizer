from .sequence import Sequence


class Protein(Sequence):
    def __init__(self):
        super().__init__({
            'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
            'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'W', 'V', 'Y'
        })
