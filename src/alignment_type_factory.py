from single_alignment import SingleAlignment
from multiple_alignment import MultipleAlignment

class AlignmentTypeFactory:
    @staticmethod
    def create_alignment_type(alignment_type_option):

        match alignment_type_option:
            case "Single":
                return SingleAlignment()
            case "Multiple":
                return MultipleAlignment()
            case _:
                raise ValueError("Invalid alignment type option")