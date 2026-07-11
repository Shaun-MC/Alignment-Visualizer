from .alignment_factory import AlignmentFactory


def align(sequences: list[str], scoring_matrix: dict, mode: str) -> dict:

    algorithm = AlignmentFactory.create(mode)

    if mode in ("global", "local"):
        if len(sequences) != 2:
            raise ValueError(f"{mode} alignment requires exactly 2 sequences, got {len(sequences)}")

        x, y = sequences
        x_axis, y_axis = ["_"] + list(x), ["_"] + list(y)
        return algorithm.execute_alignment(x_axis, y_axis, scoring_matrix)

    return algorithm.execute_alignment(sequences, scoring_matrix)
