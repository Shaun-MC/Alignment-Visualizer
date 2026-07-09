from .sequence import Sequence


class DNA(Sequence):
    def __init__(self):
        super().__init__({'A', 'C', 'G', 'T'})
