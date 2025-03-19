from global_alignment import GlobalAlignment
from local_alignment import LocalAlignment

class AlignmentAlgorithmFactory:
    @staticmethod
    def assign_alignment_algorithm(alignment_location):
        match alignment_location:
            case "Global":
                return GlobalAlignment()
            case "Local":
                return LocalAlignment()
            case _:
                raise ValueError("Invalid alignment algorithm option")