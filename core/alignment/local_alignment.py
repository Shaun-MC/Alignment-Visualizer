from .scoring_table import (
    fill_table,
    find_local_start_cell,
    find_best_path,
    construct_alignments_from_path,
    construct_lcs,
)


class LocalAlignment:

    def execute_alignment(self, x_axis, y_axis, scoring_matrix) -> dict:

        scores_table, fill_frames = fill_table(x_axis, y_axis, scoring_matrix, clamp_to_zero=True)

        start_row, start_col = find_local_start_cell(scores_table)
        path_coordinates, path_frames, score = find_best_path(scores_table, start_row, start_col)

        aligned_x, aligned_y = construct_alignments_from_path(path_coordinates, x_axis, y_axis)

        return {
            "mode": "local",
            "x_axis": x_axis,
            "y_axis": y_axis,
            "frames": fill_frames + path_frames,
            "result": {
                "alignments": [aligned_x, aligned_y],
                "lcs": construct_lcs((aligned_x, aligned_y)),
                "score": score,
                "path": [[row, col] for row, col in path_coordinates],
            },
        }
