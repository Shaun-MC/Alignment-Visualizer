import sys
import time
import streamlit as st
import pandas as pd
from enum import Enum

class Cell:
    def __init__(self, score: int, direction: str):
        self.score = score
        self.direction = direction

class EditSymbols(Enum):
    SUBSTITUTION = "↘"
    INSERTION = "↓"
    DELETION = "→"

class GlobalAlignment:
    def __init__(self):
        self.min_int = -sys.maxsize - 1
        self.symbols = EditSymbols

    def _init_scores_table(self, x_axis, y_axis):

        scores = []
        for _ in range(len(y_axis)):
            row = []
            for _ in range(len(x_axis)):
                cell = Cell(self.min_int, "")
                row.append(cell)
            scores.append(row)
        scores[0][0].score = 0

        return scores

    def _compute_cell_score_and_direction(self, row, col, top_nucleotide, left_nucleotide, scores_table, scoring_matrix):
                
        insertion_score = self.min_int if col - 1 < 0 else int(scores_table[row][col - 1].score)
        deletion_score = self.min_int if row - 1 < 0 else int(scores_table[row - 1][col].score)
        subsitution_score = self.min_int if row - 1 < 0 or col - 1 < 0 else int(scores_table[row - 1][col - 1].score)

        # Get penalties from scoring matrix
        # Handle asymmetrical matrix filled with some 'none'
        insertion_penalty = (int(scoring_matrix.at[left_nucleotide, '_']) 
            if pd.isna(scoring_matrix.at['_', left_nucleotide]) else int(scoring_matrix.at['_', left_nucleotide])
        )

        deletion_penalty = (int(scoring_matrix.at['_', top_nucleotide])
            if pd.isna(scoring_matrix.at[top_nucleotide, '_',]) else int(scoring_matrix.at[top_nucleotide, '_'])
        )

        subsitution_penalty = (int(scoring_matrix.at[left_nucleotide, top_nucleotide])
            if pd.isna(scoring_matrix.at[top_nucleotide, left_nucleotide]) else int(scoring_matrix.at[top_nucleotide, left_nucleotide])
        )

        # Calculate possible scores
        insertion_indel_score = insertion_penalty + deletion_score
        deletion_indel_score = deletion_penalty + insertion_score
        subsitution_indel_score = subsitution_penalty + subsitution_score

        best_score = max(insertion_indel_score, deletion_indel_score, subsitution_indel_score)

        # Direction protocol priority: diagonal > top > left
        if best_score == subsitution_indel_score:
            best_direction = self.symbols.SUBSTITUTION.value
        
        elif best_score == insertion_indel_score:
            best_direction = self.symbols.INSERTION.value

        else: 
            best_direction = self.symbols.DELETION.value
        
        return best_score, best_direction

    def _populate_scoring_table(self, scores_table, x_axis, y_axis, scoring_matrix):

        for row in range(len(y_axis)):
            for col in range(len(x_axis)):

                # Skip the origin (0,0) as it's already set
                if row == 0 and col == 0:
                    continue
                    
                top_nucleotide = x_axis[col]
                left_nucleotide = y_axis[row]

                best_score, best_direction = self._compute_cell_score_and_direction(row, col, top_nucleotide, left_nucleotide, scores_table, scoring_matrix)
            
                # Update scores table
                scores_table[row][col].score = best_score
                scores_table[row][col].direction = best_direction

        return scores_table

    def _compute_scores(self, x_axis, y_axis, scoring_matrix):

        scores_table = self._init_scores_table(x_axis, y_axis)
    
        return self._populate_scoring_table(scores_table, x_axis, y_axis, scoring_matrix)

    def _generate_table_html(self, scores, x_axis, y_axis, curRow, curCol, show_scores=False):
        
        # Create table header
        table_html = "<table><thead><tr><th></th>"
        for col in range(len(x_axis)):
            if col == curCol:
                table_html += f"<th>({x_axis[col]})</th>"
            else:
                table_html += f"<th> {x_axis[col]} </th>"
        table_html += "</tr></thead><tbody>"
        
        # Create table rows
        for row in range(len(y_axis)):
            if row == curRow:
                table_html += f"<tr><td>({y_axis[row]})</td>"
            else:
                table_html += f"<tr><td> {y_axis[row]} </td>"
                
            for col in range(len(x_axis)):
                if row < curRow or (row == curRow and col < curCol):
                    # Already processed cells
                    table_html += f"<td>{scores[row][col].score}{scores[row][col].direction}</td>"
                elif row == curRow and col == curCol:
                    # Current cell being processed
                    if show_scores:
                        table_html += f"<td>{scores[row][col].score}{scores[row][col].direction}</td>"
                    else:
                        # Show what we're comparing
                        table_html += f"<td>{y_axis[row]}{x_axis[col]}</td>"
                else:
                    # Not yet processed
                    table_html += "<td></td>"
            table_html += "</tr>"
        table_html += "</tbody></table>"
        
        return table_html

    def _animate_scoring_process(self, scores, x_axis, y_axis, animation_speed):

        st.markdown(f"<pre>Scoring Table </pre>", unsafe_allow_html=True)

        st.markdown(
            """
                <style>
                    div[class*="stMarkdown"] > div > div[data-testid="stMarkdownPre"] {
                        font-size: 20px;
                    }
                </style>
            """, 
            unsafe_allow_html=True
        )
        
        # Create a placeholder for the table
        table_placeholder = st.empty()
    
        # Initialize session state for visibility if it doesn't exist
        if 'visible' not in st.session_state:
            st.session_state.visible = True
        
        total_cells = len(y_axis) * len(x_axis)
        
        for num in range(total_cells + 1):
            # Calculate current row and column positions
            curRow = num // len(x_axis)
            curCol = num % len(x_axis)
            
            # Generate and display table showing current progress
            table_html = self._generate_table_html(scores, x_axis, y_axis, curRow, curCol)
            table_placeholder.markdown(table_html, unsafe_allow_html=True)
            
            time.sleep(animation_speed)
            
            # For the last cell, also show its score after calculation
            if num < total_cells:
                table_html = self._generate_table_html(scores, x_axis, y_axis, curRow, curCol, show_scores=True)
                table_placeholder.markdown(table_html, unsafe_allow_html=True)
                time.sleep(animation_speed)

    def _find_best_path(self, scores_table):
        
        row, col = len(scores_table) - 1, len(scores_table[0]) - 1
        path = []
        path_coordinates = [(row, col)]
        total_score = scores_table[row][col].score

        direction_map = {
            self.symbols.DELETION.value: (-1, 0),
            self.symbols.SUBSTITUTION.value: (-1, -1),
            self.symbols.INSERTION.value: (0, -1)
        }

        # Iterating backwards to find the best path from the bottom right corner
        while row > 0 or col > 0:

            move_options = scores_table[row][col].direction
            best_move = None
            best_score = self.min_int

            # Check all possible moves
            for move, (dr, dc) in direction_map.items():

                new_row, new_col = row + dr, col + dc
                
                if 0 <= new_row < len(scores_table) and 0 <= new_col < len(scores_table[0]):

                    score = scores_table[new_row][new_col].score

                    # Ensures that the current move was the one actually performed
                    if move in move_options and score > best_score:
                        best_score, best_move = score, move

            # A move is always expected unless the end is reached        
            if best_move:

                row, col = row + direction_map[best_move][0], col + direction_map[best_move][1]

                path.append(best_move)

                path_coordinates.append((row, col))

        return "".join(reversed(path)), path_coordinates, total_score

    def _generate_best_path_table_html(self, scores, x_axis, y_axis, path_set):
    
        table_html = "<table><thead><tr><th></th>"

        # Add column headers (x_axis)
        table_html += "".join(f"<th> {col} </th>" for col in x_axis)
        table_html += "</tr></thead><tbody>"

        # Add row headers (y_axis) and scores
        for row, row_label in enumerate(y_axis):
            table_html += f"<tr><td> {row_label} </td>"

            for col in range(len(x_axis)):
                score = scores[row][col].score

                if (row, col) in path_set:
                    table_html += f"<td>({score})</td>"  # Highlight path cells
                else:
                    table_html += f"<td>{score}</td>"
            table_html += "</tr>"

        table_html += "</tbody></table>"

        return table_html
    
    def _show_best_path_table(self, path_coordinates: list[tuple], scores, x_axis, y_axis):
        st.markdown("<pre>Best Path Table</pre>", unsafe_allow_html=True)

        st.markdown(
            """
                <style>
                    div[class*="stMarkdown"] > div > div[data-testid="stMarkdownPre"] {
                        font-size: 20px;
                    }
                </style>
            """, 
            unsafe_allow_html=True
        )

        # Allows for a quicker look up
        path_set = set(map(tuple, path_coordinates))

        table_html = self._generate_best_path_table_html(scores, x_axis, y_axis, path_set)

        st.markdown(table_html, unsafe_allow_html=True)

    def _construct_alignments(self, path: str, x_axis: list, y_axis: list) -> str:
    
        final_S1, final_S2 = [], []

        # Converting the lists to iterators allows for efficiently fetched elements
        x_iter, y_iter = iter(x_axis[1:]), iter(y_axis[1:])  

        for direction in path:
            if direction == self.symbols.SUBSTITUTION.value:  # Substitution (keep both characters)
                final_S1.append(next(x_iter))
                final_S2.append(next(y_iter))
            elif direction == self.symbols.INSERTION.value:  # Insertion (gap in S1)
                final_S1.append("_")
                final_S2.append(next(y_iter))
            elif direction == self.symbols.DELETION.value:  # Deletion (gap in S2)
                final_S1.append(next(x_iter))
                final_S2.append("_")

        return "".join(final_S1), "".join(final_S2)

    def _construct_lcs(self, alignments: tuple[str, str]) -> str:

        # Super pythonic way of doing it but it works
        S1, S2 = alignments
        return "".join(c1 for c1, c2 in zip(S1, S2) if c1 == c2)

    def execute_alignment(self, x_axis, y_axis, scoring_matrix, animation_speed):

        # Alot of concerns in this function 
        # Should be broken down into smaller functions for clarity
        # Ah well
        scores_table = self._compute_scores(x_axis, y_axis, scoring_matrix)

        self._animate_scoring_process(scores_table, x_axis, y_axis, animation_speed)

        path, path_coordinates, total_score = self._find_best_path(scores_table)

        self._show_best_path_table(path_coordinates, scores_table, x_axis, y_axis)

        alignments = self._construct_alignments(path, x_axis, y_axis)

        return alignments, self._construct_lcs(alignments), total_score