def build_identity_matrix_data(labels: "list | tuple", match: int, mismatch: int) -> dict:

    # The gap symbol ('_') always scores 0 so it never adds a penalty on top of
    # whatever the alignment algorithm already charges for a gap.
    return {
        row: {
            col: 0 if row == "_" or col == "_" else (match if row == col else mismatch)
            for col in labels
        }
        for row in labels
    }


def build_editable_template_data(labels: "list | tuple") -> dict:

    # Only the upper triangle (row index <= column index) is populated with a
    # starting value of 0; the rest is left as None awaiting user input, since
    # substitution scores are symmetric and only need to be entered once per pair.
    return {
        row: {
            col: (0 if i <= j else None)
            for j, col in enumerate(labels)
        }
        for i, row in enumerate(labels)
    }
