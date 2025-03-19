from single_alignment import SingleAlignment
from multiple_alignment import MultipleAlignment

class AlignmentTypeFactory:
    @staticmethod
    def create_alignment_type(alignment_type_option, input_type, alignment_location):

        match alignment_type_option:
            case "Single":
                return SingleAlignment(alignment_location)
            case "Multiple":
                return MultipleAlignment(input_type, alignment_location)
            case _:
                raise ValueError("Invalid alignment type option")