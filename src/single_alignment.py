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

    def fill_table_w_scores(self, input_txt: list, scoring_matrix, animation_speed) -> List[List[Cell]]:
        
        # Create a DataFrame with input_txt[0] on the y-axis and input_txt[1] on the x-axis
        y_axis = ["_"] + list(input_txt[0])
        x_axis = ["_"] + list(input_txt[1])
            
        # Create a custom HTML table with non-unique column and row names
        table_html = "<table><thead><tr><th></th>"
        for col in x_axis:
            table_html += f"<th> {col} </th>"
        table_html += "</tr></thead><tbody>"
        for row in y_axis:
            table_html += f"<tr><td> {row} </td>"
            for col in x_axis:
                table_html += "<td></td>"
            table_html += "</tr>"
        table_html += "</tbody></table>"

        # Create a placeholder for the table
        table_placeholder = st.empty()

        # Initialize session state for visibility if it doesn't exist
        if 'visible' not in st.session_state:
            st.session_state.visible = True

        curRow = 0
        curColumn = 0
        
        #fill a score table with lowest possible scores
        min_int = -sys.maxsize - 1
        scores = []
        for i in range(len(y_axis)):
            row = []
            for j in range(len(x_axis)):
                cell = Cell(min_int, "x")
                row.append(cell)
            scores.append(row)
        scores[0][0].score = 0

        #iterate through the table scoring
        for num in range(len(y_axis) * len(x_axis) + 1):
            # Toggle visibility
            if st.session_state.visible:
                table_placeholder.markdown(table_html, unsafe_allow_html=True)
            else:
                table_placeholder.empty()
            
            # st.session_state.visible = not st.session_state.visible
            time.sleep(animation_speed)

            # Calculate current row and column positions
            curRow = num // len(x_axis)
            curCol = num % len(x_axis)

            # edit table
            table_html = "<table><thead><tr><th></th>"
            for col in range(len(x_axis)):
                if (col == curCol):
                    table_html += f"<th>({x_axis[col]})</th>"
                else:
                    table_html += f"<th> {x_axis[col]} </th>"
            table_html += "</tr></thead><tbody>"
        
            for row in range(len(y_axis)):
                if (row == curRow):
                    table_html += f"<tr><td>({y_axis[row]})</td>"
                else:
                    table_html += f"<tr><td> {y_axis[row]} </td>"
                for col in range(len(x_axis)):
                    # If this cell should be filled (we've reached it in our iteration)
                    if (row < curRow):
                        table_html += f"<td>{scores[row][col].score}</td>"
                    elif (row <= curRow and col < curCol):
                        table_html += f"<td>{scores[row][col].score}</td>"
                    elif (row == curRow and col == curCol):
                        topLetter = x_axis[col]
                        leftLetter = y_axis[row]

                        #pull surronding scores
                        leftscore = min_int
                        topscore = min_int
                        diagonalscore = min_int
                        if ((col - 1) < 0):
                            leftscore = 0
                        else:
                            leftscore = int(scores[row][col - 1].score)

                        if ((row - 1) < 0 ):
                            topscore = 0
                        else:
                            topscore = int(scores[row - 1][col].score)

                        if (row - 1 < 0 or col - 1 < 0):
                            diagonalscore = 0
                        else:
                            diagonalscore = int(scores[row - 1][col - 1].score)

                        indelLpen = min_int
                        indelTpen = min_int
                        matchLTpen = min_int
                        #access scoring matrix /////////////////////////////////
                        # handle assymetrical matrix filled with some 'none'
                        if pd.isna(scoring_matrix.at[leftLetter, '_']):
                            indelLpen =  int(scoring_matrix.at['_', leftLetter])
                        else:
                            indelLpen =  int(scoring_matrix.at[leftLetter, '_'])

                        if pd.isna(scoring_matrix.at['_', topLetter]):
                            indelTpen =  int(scoring_matrix.at[topLetter, '_'])
                        else:
                            indelTpen =  int(scoring_matrix.at['_', topLetter])

                        if pd.isna(scoring_matrix.at[leftLetter, topLetter]):
                            matchLTpen =  int(scoring_matrix.at[topLetter, leftLetter])
                        else: 
                            matchLTpen =  int(scoring_matrix.at[leftLetter, topLetter])
                        
                        indelLscore = int(indelLpen + topscore)
                        indelTscore = int(indelTpen + leftscore)
                        diagMatchScore = int(matchLTpen + diagonalscore)

                        bestScore = max(indelLscore, indelTscore, diagMatchScore)
                        bestDirection = ""
                        if (bestScore == indelLscore):
                            bestDirection += "|" #down
                        if (bestScore == indelTscore):
                            bestDirection += "--" #left
                        if (bestScore == diagMatchScore):
                            bestDirection += "\\" #diagonal
                        
                        scores[row][col].score = bestScore
                        scores[row][col].direction = bestDirection
                        table_html += f"<td>{leftLetter+topLetter}</td>"
                    else:
                        table_html += "<td></td>"
                table_html += "</tr>"
            table_html += "</tbody></table>"
                
            
            table_placeholder.markdown(table_html, unsafe_allow_html=True)
            print(animation_speed)
            time.sleep(animation_speed)
            # show the scores

            # TODO fix whitespace in table so it doesn't expand and contract
            # edit table
            table_html = "<table><thead><tr><th></th>"
            for col in range(len(x_axis)):
                if (col == curCol):
                    table_html += f"<th>({x_axis[col]})</th>"
                else:
                    table_html += f"<th> {x_axis[col]} </th>"
            table_html += "</tr></thead><tbody>"
        
            for row in range(len(y_axis)):
                if (row == curRow):
                    table_html += f"<tr><td>({y_axis[row]})</td>"
                else:
                    table_html += f"<tr><td> {y_axis[row]} </td>"
                for col in range(len(x_axis)):
                    # If this cell should be filled (we've reached it in our iteration)
                    if row < curRow or (row == curRow and col <= curCol):
                        # todo: display fancy direction
                        table_html += f"<td>{scores[row][col].score}{scores[row][col].direction}</td>"
                    else:
                        table_html += "<td></td>"
                table_html += "</tr>"
            table_html += "</tbody></table>"

            table_placeholder.markdown(table_html, unsafe_allow_html=True)
        
        self.findBestPath(scores, x_axis, y_axis)

        return scores

    def showBestPath(self, pathCoordinates: List[tuple], scores, x_axis, y_axis):
       
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
                for coordinates in pathCoordinates:
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
        

    def findBestPath(self, scores, x_axis, y_axis) -> str:
        
        isStart = False
        row = len(scores) - 1
        col = len(scores[0]) - 1
        min_int = -sys.maxsize - 1
        path = ""
        isBottom = True
        pathCoordinates = [[0,0]]
        while(isStart == False):
            moveOptions = scores[row][col].direction
            leftScore = min_int
            diagScore = min_int
            topScore = min_int
            if "--" in moveOptions:
                if col - 1 < 0:
                    leftScore = min_int
                leftScore = scores[row][col - 1].score
            if "\\" in moveOptions:
                if row - 1 < 0 and col - 1 < 0:
                    diagScore = min_int
                diagScore = scores[row - 1][col - 1].score
            if "|" in moveOptions:
                if col - 1 < 0:
                    topScore = min_int
                topScore = scores[row - 1][col].score

            bestScore = max(leftScore, diagScore, topScore)

            if bestScore == diagScore:
                pathCoordinates.append([row, col])
                row = row-1
                if (row < 0):
                    row = 0
                col = col-1
                if (col < 0):
                    col = 0
                if (isBottom):
                    path += str(bestScore) + " " 
                    isBottom = False
                else:
                    path += "\\" + str(bestScore) + " " 
            elif bestScore == topScore:
                pathCoordinates.append([row, col])
                row = row - 1
                if (row < 0):
                    row = 0
                if (isBottom):
                    path += str(bestScore) + " "
                    isBottom = False
                else: 
                    path += "|" + str(bestScore) + " "
            elif bestScore == leftScore:
                pathCoordinates.append([row, col])
                col = col - 1
                if (col < 0):
                    col = 0
                if (isBottom):
                    path += str(bestScore) + " "
                    isBottom = False
                else:
                    path += "--" + str(bestScore) + " "
            
            
            if row == 0 and col == 0:
                isStart = True
                break

        path = path[::-1]
        self.showBestPath(pathCoordinates, scores, x_axis, y_axis)
        return path

    def execute_alignment(self, input_txt: list, scoring_matrix, animation_speed) -> str:
        """
        Purpose
        ----------
        Run the alignment on the provided list of strings.

        Parameters
        ----------
        input_txt : list
            List of strings to be aligned.

        Returns
        -------
        str
            Result of the alignment.
        """
       
        scores = self.fill_table_w_scores(input_txt, scoring_matrix, animation_speed)
    
        #todo: display alignment
        #todo: display score - only return the score, display is handled elsewhere
        return "\n"