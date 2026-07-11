from .global_alignment import GlobalAlignment
from .local_alignment import LocalAlignment
from .multiple_alignment import MultipleAlignment


class AlignmentFactory:
    @staticmethod
    def create(mode: str):
        match mode:
            case "global":
                return GlobalAlignment()
            case "local":
                return LocalAlignment()
            case "multiple":
                return MultipleAlignment()
            case _:
                raise ValueError(f"Invalid alignment mode: {mode!r}")
