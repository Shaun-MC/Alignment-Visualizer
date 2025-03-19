from options import Options
from scoring_matrix_factory import ScoringMatrixFactory
from alignment_type_factory import AlignmentTypeFactory
from sequence_type_factory import SequenceTypeFactory
import streamlit as st

class Alignment:
    def __init__(self):
        
        self.alignment_type = None

        # Should the sequence_type object store it's own scoring matrix?
        # The construction of the scoring matrix is based on the sequence type - unless it's Protein which is predefined w/ Blosum62
        self.sequence_type = None
        
        self.scoring_matrix = None
        self.input_format = None

        self.sequence_input = list()

    def execute(self):

        def instantiate_objects():

            def retrieve_options():
                # Visual options still exist after the Options class goes out of scope
                options = Options()
                return (
                    options.get_alignment_type(),  
                    options.get_sequence_type(), 
                    options.get_using_scoring_matrix(), 
                    options.get_input_format(),
                    options.get_alignment_location()
                )    

            # Get all the options from the user
            alignment_type_option, sequence_type_option, using_scoring_matrix_option, input_format_option, alignment_location = retrieve_options()

            try:
                # Create the objects based on the options
                # Input Format doesn't get it's own object as it only matters for multiple alignment
                self.scoring_matrix = ScoringMatrixFactory.create_scoring_matrix(using_scoring_matrix_option, sequence_type_option)
                self.sequence_type = SequenceTypeFactory.create_sequence_type(sequence_type_option)
                self.alignment_type = AlignmentTypeFactory.create_alignment_type(alignment_type_option, input_format_option, alignment_location)

            except ValueError as e:

                # Not sure how else to handle like this 
                # This exception should never happen as it's based on 'button' data that is never user writeable 
                # Only type of exception ever actually thrown
                st.error(e)
                return

            except Exception as e:
                # If anything else happens
                # Check for other exceptions
                st.error(e)
                return

        instantiate_objects()

        def retrieve_sequence_input():
            # Depending on the alignment, the respective handleInput() will be called
            # Deciding if there should be a base class for alignment_type of if SingleAlignment and MultipleAlignment are fine as is
            # Test to make sure the correct function is called
            self.alignment_type.handle_input()
            
            unparsed_sequence_input = self.alignment_type.get_unparsed_sequences()

            self.sequence_type.validate_encoding(unparsed_sequence_input)

            return self.sequence_type.get_validated_sequences()
        
        sequence_input = retrieve_sequence_input()
        
        if not sequence_input:
            return

        def execute_alignment(sequence_input):
            
            animation_speed = st.selectbox("Animation Speed (Seconds)", options=[2, 1, 0.5, 0])

            st.markdown(
                """
                    <style>
                        div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {
                            font-size: 20px;
                        }
                    </style>
                """, 
            unsafe_allow_html=True)

            if 'alignment_running' not in st.session_state:
                st.session_state.alignment_running = False

            running_alignment, pause_algorithm, blank = st.columns(3)

            with running_alignment:
                if st.button("Run Alignment"):
                    st.session_state.alignment_running = True

                    # TODO When this modules is updated, the alignment algorithm resets - figure how to keep the state of the alignment algorithm
                    # Should probably in the execute_alignment function to make that happen 
                    with pause_algorithm:
                        if st.button("Pause"):
                            st.session_state.alignment_running = False

                    return self.alignment_type.execute_alignment(sequence_input, self.scoring_matrix.scoring_matrix, animation_speed)

                else:
                    return (None, None, None)
            
        formatted_alignments, lcs, score = execute_alignment(sequence_input)

        def display_alignments(formatted_alignments, lcs, score):

            if formatted_alignments is None or lcs is None or score is None:
                return
            
            else:
                
                st.header("Alignment Output")

                st.markdown(f"<pre>S1: {formatted_alignments[0]}</pre>", unsafe_allow_html=True)
                st.markdown(f"<pre>S2: {formatted_alignments[1]}</pre>", unsafe_allow_html=True)

                st.markdown(f"<pre>Score: {str(score)}</pre>", unsafe_allow_html=True)

                st.header("Longest Common Subsequence")
                st.markdown(f"<pre>LCS: {lcs}</pre>", unsafe_allow_html=True)

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

        display_alignments(formatted_alignments, lcs, score)