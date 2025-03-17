from single_alignment import SingleAlignment
from multiple_alignment import MultipleAlignment

class AlignmentTypeFactory:
    @staticmethod
    def create_alignment_type(alignment_type_option, input_type):

        match alignment_type_option:
            case "Single":
                return SingleAlignment()
            case "Multiple":
                return MultipleAlignment(input_type)
            case _:
                raise ValueError("Invalid alignment type option")