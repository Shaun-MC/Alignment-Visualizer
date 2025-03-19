import streamlit as st
from typing import List
import sys
import time
import numpy as np
import pandas as pd

class Cell:
    def __init__(self, score: int, direction: str):
        self.score = score
        self.direction = direction

    def __str__(self) -> str:
        return f"Cell(score={self.score}, direction='{self.direction}')"

    def __repr__(self) -> str:
        return self.__str__()
            
class SingleAlignment:
    
    def __init__(self):
        self.max_char_input = 20
        self.max_height_pixels = 68

        self.S1 = None
        self.S2 = None

    def _set_first_sequence(self, S1):
        self.S1 = S1

    def _set_second_sequence(self, S2):
        self.S2 = S2

    def get_unparsed_sequences(self):
        return [self.S1, self.S2] if self.S1 != "" and self.S2 != "" else []

    def handle_input(self):

        st.header(f"Input (Max {self.max_char_input} Characters)")

        # Declare the options variables for single alignment input
        s1_input, s2_input = st.columns(2)

        # Display the options buttons
        # Once the strings are inputted and validation fails, how will the user be repromted?
        with s1_input:
            self._set_first_sequence(st.text_area(label="S1: ", value="", height=self.max_height_pixels, max_chars=self.max_char_input))
            
        with s2_input:
            self._set_second_sequence(st.text_area(label="S2: ", value="", height=self.max_height_pixels, max_chars=self.max_char_input))

        st.markdown(
                """
                    <style>
                        div[class*="stTextArea"] > label > div[data-testid="stMarkdownContainer"] > p {
                            font-size: 20px;
                        }
                    </style>
                """, 
            unsafe_allow_html=True)

    def _fill_table_w_scores(self, y_axis: list, x_axis: list, scoring_matrix) -> list[list[Cell]]:

        def init_scores_table(y_axis, x_axis):

            min_int = -sys.maxsize - 1
            scores = []
            for _ in range(len(y_axis)):
                row = []
                for _ in range(len(x_axis)):
                    cell = Cell(min_int, "")
                    row.append(cell)
                scores.append(row)
            scores[0][0].score = 0

            return scores
    
        scores_table = init_scores_table(y_axis, x_axis)

        def populate_scoring_table(scores_table, y_axis, x_axis, scoring_matrix):

            min_int = -sys.maxsize - 1
            
            for row in range(len(y_axis)):
                for col in range(len(x_axis)):

                    # Skip the origin (0,0) as it's already set
                    if row == 0 and col == 0:
                        continue
                        
                    top_nucleotide = x_axis[col]
                    left_nucleotide = y_axis[row]

                    def compute_optimal_score():
                        
                        insertion_score = min_int if col - 1 < 0 else int(scores_table[row][col - 1].score)
                        deletion_score = min_int if row - 1 < 0 else int(scores_table[row - 1][col].score)
                        subsitution_score = min_int if row - 1 < 0 or col - 1 < 0 else int(scores_table[row - 1][col - 1].score)

                        # Get penalties from scoring matrix
                        # Handle asymmetrical matrix filled with some 'none'
                        insertion_penalty = (int(scoring_matrix.at['_', left_nucleotide]) 
                            if pd.isna(scoring_matrix.at[left_nucleotide, '_']) else int(scoring_matrix.at[left_nucleotide, '_'])
                        )

                        deletion_penalty = (int(scoring_matrix.at[top_nucleotide, '_'])
                            if pd.isna(scoring_matrix.at['_', top_nucleotide]) else int(scoring_matrix.at['_', top_nucleotide])
                        )

                        subsitution_penalty = (int(scoring_matrix.at[top_nucleotide, left_nucleotide])
                            if pd.isna(scoring_matrix.at[left_nucleotide, top_nucleotide]) else int(scoring_matrix.at[left_nucleotide, top_nucleotide])
                        )

                        # Calculate possible scores
                        insertion_indel_score = insertion_penalty + deletion_score
                        deletion_indel_score = deletion_penalty + insertion_score
                        subsitution_indel_score = subsitution_penalty + subsitution_score

                        best_score = max(insertion_indel_score, deletion_indel_score, subsitution_indel_score)

                        # Direction protocol: diagonal > top > left
                        if best_score == subsitution_indel_score:
                            best_direction = "↘"
                        
                        elif best_score == insertion_indel_score:
                            best_direction = "↓"

                        else: 
                            best_direction = "→"
                        
                        return best_score, best_direction
                    
                    best_score, best_direction = compute_optimal_score()
                    
                    # Update scores table
                    scores_table[row][col].score = best_score
                    scores_table[row][col].direction = best_direction
            
        populate_scoring_table(scores_table, y_axis, x_axis, scoring_matrix)

        return scores_table

    def _show_best_path_table(self, path_coordinates: List[tuple], scores, x_axis, y_axis):

        st.markdown(f"<pre>Best Path Table </pre>", unsafe_allow_html=True)

        st.markdown(
            """
                <style>
                    div[class*="stMarkdown"] > div > div[data-testid="stMarkdownPre"] {
                        font-size: 20x;
                    }
                </style>
            """, 
            unsafe_allow_html=True
        )
        
        table_html = "<table><thead><tr><th></th>"

        # write the labels at the top of the table
        for col in x_axis:
            table_html += f"<th> {col} </th>"
        table_html += "</tr></thead><tbody>"

        # Write the labels on the left side and the scores in the cells
        for row_idx, row_label in enumerate(y_axis):
            table_html += f"<tr><td> {row_label} </td>"
            for col_idx in range(len(x_axis)):
                score = scores[row_idx][col_idx].score
                inPath = False
                for coordinates in path_coordinates:
                    temp = [row_idx, col_idx]
                    if temp == coordinates:
                        inPath = True
                if (inPath):
                    table_html += f"<td>({score})</td>"
                else:
                    table_html += f"<td>{score}</td>"
            table_html += "</tr>"
        table_html += "</tbody></table>"
        
        # Display the table in Streamlit
        st.markdown(table_html, unsafe_allow_html=True)

    def _find_best_path(self, scores, x_axis, y_axis):
        
        isStart = False
        row = len(scores) - 1
        col = len(scores[0]) - 1
        min_int = -sys.maxsize - 1
        path = ""
        path_coordinates = [[0,0]]
        totalScore = scores[row][col].score
        
        while(isStart == False):

            moveOptions = scores[row][col].direction
            leftScore = min_int
            diagScore = min_int
            topScore = min_int

            if "→" in moveOptions:
                if col - 1 < 0:
                    leftScore = min_int
                leftScore = scores[row][col - 1].score
            if "↘" in moveOptions:
                if row - 1 < 0 and col - 1 < 0:
                    diagScore = min_int
                diagScore = scores[row - 1][col - 1].score
            if "↓" in moveOptions:
                if col - 1 < 0:
                    topScore = min_int
                topScore = scores[row - 1][col].score

            bestScore = max(leftScore, diagScore, topScore)

            if (row == 0 and col > 0):
                path_coordinates.append([row, col])
                path += "→"
                col = col - 1
                
            elif (col == 0 and row > 0):
                path_coordinates.append([row, col])
                path += "↓"
                row = row - 1
                
            else:
                if bestScore == diagScore:
                    path_coordinates.append([row, col])
                    row = row-1
                    if (row < 0):
                        row = 0
                    col = col-1
                    if (col < 0):
                        col = 0
                   
                    path += "↘"
                     
                elif bestScore == topScore:
                    path_coordinates.append([row, col])
                    row = row - 1
                    if (row < 0):
                        row = 0
                    
                    path += "↓"
                    
                elif bestScore == leftScore:
                    path_coordinates.append([row, col])
                    col = col - 1
                    if (col < 0):
                        col = 0
                    
                    path += "→"
            
            if row == 0 and col == 0:
                isStart = True
                break

        path = path[::-1]

        return path, path_coordinates, totalScore

    def _generate_table_html(self, scores, x_axis, y_axis, curRow, curCol, show_scores=False):
        """Generates HTML for the table at a specific point in the animation."""
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

    def _construct_alignments(self, path: str, x_axis: list, y_axis: list) -> str:
    
        final_S1 = []
        final_S2 = []

        # x_axis is S1, y_axis is S2
        # Remove the '_' character from the axis's 
        x_axis, y_axis = x_axis[1:], y_axis[1:]

        for direction in path:

            S1_char = ""
            S2_char = ""

            match direction:
                case "↘":
                    S1_char = x_axis.pop(0)
                    S2_char = y_axis.pop(0)
                
                case "↓":
                    S1_char = "_"
                    S2_char = y_axis.pop(0)

                case "→":
                    S1_char = x_axis.pop(0)
                    S2_char = "_"
                
            final_S1.append(S1_char)
            final_S2.append(S2_char)

        return "".join(final_S1), "".join(final_S2)

    def _construct_lcs(self, alignments: List[str]) -> str:
        return "AA"
    
    def execute_alignment(self, input_txt: list, scoring_matrix, animation_speed) -> str:
        """
        Purpose
        -----
        Run the alignment on the provided list of strings.

        Parameters
        -----
        input_txt : list
            List of strings to be aligned.

        Returns
        ----
        str
            Result of the alignment.
        """
        
        y_axis = ["_"] + list(input_txt[0])
        x_axis = ["_"] + list(input_txt[1])
       
        scores = self._fill_table_w_scores(y_axis, x_axis, scoring_matrix)

        self._animate_scoring_process(scores, x_axis, y_axis, animation_speed)

        path, path_coordinates, final_score = self._find_best_path(scores, x_axis, y_axis)

        self._show_best_path_table(path_coordinates, scores, x_axis, y_axis)

        alignments = self._construct_alignments(path, x_axis, y_axis)

        lcs = self._construct_lcs(alignments)

        return (alignments, lcs, final_score)