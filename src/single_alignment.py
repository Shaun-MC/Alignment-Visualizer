import streamlit as st

class SingleAlignment:
    def __init__(self):
        self.max_char_input = 20
        self.max_height_pixels = 68
        self.input_header = f"Input (Max {self.max_char_input} Characters)"

        self.S1 = None
        self.S2 = None

    def _set_first_sequence(self, S1):
        self.S1 = S1

    def _set_second_sequence(self, S2):
        self.S2 = S2

    def get_unparsed_sequences(self) -> list:
        return [self.S1, self.S2]

    def handle_input(self):

        st.header(self.input_header)

        # Declare the options variables for single alignment input
        s1_input, s2_input = st.columns(2)

        # Display the options buttons
        # Once the strings are inputted and validation fails, how will the user be repromted?
        with s1_input:
            self._set_first_sequence(st.text_area(label="S1: ", value="", height=self.max_height_pixels, max_chars=self.max_char_input))
            
        with s2_input:
            self._set_second_sequence(st.text_area(label="S2: ", value="", height=self.max_height_pixels, max_chars=self.max_char_input))

    def execute_alignment(self, sequences, scoring_matrix):
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

        #calculate matrix letter matrix
        matrix = []
        for i in range(len(y_axis)):
            row = []
            for j in range(len(x_axis)):
                row.append(y_axis[i] + x_axis[j])
            matrix.append(row)

        #todo: calculate scores
        scores = []
        row0 = [0,-1,-3,-4,-5,-6,-7,-8]
        scores.append(row0)
        row1 = [-1,1,-1,-2,1,0,-1,-2]
        scores.append(row1)
        row2 = [-2,5,3,2,1,7,6,5]
        scores.append(row2)
        row3 = [-3,4,8,10,9,8,7,13]
        scores.append(row3)
        row4 = [-4,3,7,9,11,15,14,13]
        scores.append(row4)
        row5 = [-6,1,10,10,9,13,13,17]
        scores.append(row5)
        row6 = [-7,0,9,9,15,14,18,17]
        scores.append(row6)
        row7 = [-8,-1,8,9,14,21,20,19]
        scores.append(row7)
        row8 = [-9,-2,7,15,14,20,20,27]
        scores.append(row8)

        #iterate through the table scoring
        for num in range(len(y_axis) * len(x_axis) + 1):
            # Toggle visibility
            if st.session_state.visible:
                table_placeholder.markdown(table_html, unsafe_allow_html=True)
            else:
                table_placeholder.empty()
            
            # st.session_state.visible = not st.session_state.visible
            time.sleep(1)

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
                        table_html += f"<td>{scores[row][col]}</td>"
                    elif (row <= curRow and col < curCol):
                        table_html += f"<td>{scores[row][col]}</td>"
                    elif (row == curRow and col == curCol):
                        table_html += f"<td>{matrix[row][col]}</td>"
                    else:
                        table_html += "<td></td>"
                table_html += "</tr>"
            table_html += "</tbody></table>"
                
            table_placeholder.markdown(table_html, unsafe_allow_html=True)
            time.sleep(1)
            # todo: this is hard coded
            # show the scores

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
                        table_html += f"<td>{scores[row][col]}</td>"
                    else:
                        table_html += "<td></td>"
                table_html += "</tr>"
            table_html += "</tbody></table>"

            table_placeholder.markdown(table_html, unsafe_allow_html=True)

    
        #todo: display alignment
        st.write("Alignment:")
        st.write("A T C T G A T _ C")
        st.write("_ T G _ C A T A C")
        st.write("Score: 27")
        return "\n"