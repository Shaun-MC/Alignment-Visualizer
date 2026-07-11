MIN_INT = -(2 ** 62)

# Backward deltas: given a cell whose recorded direction is the key, this is the
# offset to its predecessor. No "reset" entry - that absence is what makes a
# non-terminating traceback structurally impossible rather than just avoided at runtime.
MOVES = {
    "diag": (-1, -1),
    "up": (-1, 0),
    "left": (0, -1),
}


class Cell:
    def __init__(self, score: int, direction: str):
        self.score = score
        self.direction = direction


def init_scores_table(x_axis, y_axis):
    scores_table = [
        [Cell(MIN_INT, "") for _ in range(len(x_axis))]
        for _ in range(len(y_axis))
    ]
    scores_table[0][0].score = 0
    return scores_table


def compute_cell_score_and_direction(row, col, top, left, scores_table, scoring_matrix, clamp_to_zero):

    top_score = MIN_INT if row - 1 < 0 else scores_table[row - 1][col].score
    left_score = MIN_INT if col - 1 < 0 else scores_table[row][col - 1].score
    diag_score = MIN_INT if row - 1 < 0 or col - 1 < 0 else scores_table[row - 1][col - 1].score

    # Handle asymmetrical matrix filled with some 'none' - mirror fallback
    top_penalty = (scoring_matrix['_'][top]
                   if scoring_matrix[top]['_'] is None else scoring_matrix[top]['_']
                   )
    left_penalty = (scoring_matrix[left]['_']
                    if scoring_matrix['_'][left] is None else scoring_matrix['_'][left]
                    )
    diag_penalty = (scoring_matrix[left][top]
                    if scoring_matrix[top][left] is None else scoring_matrix[top][left]
                    )

    top_total = top_penalty + top_score
    left_total = left_penalty + left_score
    diag_total = diag_penalty + diag_score

    best_score = max(top_total, left_total, diag_total)

    if clamp_to_zero and best_score <= 0:
        return 0, "reset"

    # Direction protocol priority: diagonal > top > left
    if best_score == diag_total:
        return best_score, "diag"
    elif best_score == top_total:
        return best_score, "up"
    else:
        return best_score, "left"


def fill_table(x_axis, y_axis, scoring_matrix, clamp_to_zero):
    scores_table = init_scores_table(x_axis, y_axis)
    frames = []

    for row in range(len(y_axis)):
        for col in range(len(x_axis)):

            if row == 0 and col == 0:
                continue

            top, left = x_axis[col], y_axis[row]

            frames.append({"type": "compare", "row": row, "col": col, "top": top, "left": left})

            score, direction = compute_cell_score_and_direction(
                row, col, top, left, scores_table, scoring_matrix, clamp_to_zero)
            scores_table[row][col] = Cell(score, direction)

            frames.append({"type": "score", "row": row, "col": col, "score": score, "direction": direction})

    return scores_table, frames


def find_local_start_cell(scores_table):
    best_row, best_col, best_score = 0, 0, scores_table[0][0].score
    for row in range(len(scores_table)):
        for col in range(len(scores_table[0])):
            if scores_table[row][col].score > best_score:
                best_score, best_row, best_col = scores_table[row][col].score, row, col
    return best_row, best_col


def find_best_path(scores_table, start_row, start_col):
    row, col = start_row, start_col
    score = scores_table[row][col].score
    coords_backward = [(row, col)]

    while (row > 0 or col > 0) and scores_table[row][col].direction != "reset":
        dr, dc = MOVES[scores_table[row][col].direction]
        row, col = row + dr, col + dc
        coords_backward.append((row, col))

    path_coordinates = list(reversed(coords_backward))
    path_frames = [{"type": "path", "row": r, "col": c} for r, c in path_coordinates]
    return path_coordinates, path_frames, score


def construct_alignments_from_path(path_coordinates, x_axis, y_axis):
    aligned_x, aligned_y = [], []

    for (prev_row, prev_col), (row, col) in zip(path_coordinates, path_coordinates[1:]):
        delta = (row - prev_row, col - prev_col)

        if delta == (1, 1):
            aligned_x.append(x_axis[col])
            aligned_y.append(y_axis[row])
        elif delta == (1, 0):
            aligned_x.append("-")
            aligned_y.append(y_axis[row])
        elif delta == (0, 1):
            aligned_x.append(x_axis[col])
            aligned_y.append("-")
        else:
            raise AssertionError(f"non-adjacent path step {(prev_row, prev_col)} -> {(row, col)}")

    return "".join(aligned_x), "".join(aligned_y)


def construct_lcs(alignments):
    x, y = alignments
    return "".join(c1 for c1, c2 in zip(x, y) if c1 == c2)
