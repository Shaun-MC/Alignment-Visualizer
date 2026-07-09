from .sequence import Sequence


class RNA(Sequence):
    def __init__(self):
        super().__init__({'A', 'C', 'G', 'U'})
