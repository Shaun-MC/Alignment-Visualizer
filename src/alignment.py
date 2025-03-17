from options import Options
from scoring_matrix_factory import ScoringMatrixFactory
from alignment_type_factory import AlignmentTypeFactory
from sequence_type_factory import SequenceTypeFactory
from input_format_factory import InputFormatFactory
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
                return (options.get_alignment_type(),  options.get_sequence_type(), options.get_using_scoring_matrix(), options.get_input_format())    

            # Get all the options from the user
            alignment_type_option, sequence_type_option, using_scoring_matrix_option, input_format_option = retrieve_options()

            try:
                # Create the objects based on the options
                # Input Format doesn't get it's own object as it only matters for multiple alignment
                self.scoring_matrix = ScoringMatrixFactory.create_scoring_matrix(using_scoring_matrix_option, sequence_type_option)
                self.sequence_type = SequenceTypeFactory.create_sequence_type(sequence_type_option)
                self.alignment_type = AlignmentTypeFactory.create_alignment_type(alignment_type_option, input_format_option)

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

            st.write("Hello")

        sequence_input = retrieve_sequence_input()

        # Create the objects that take in the rest of the data

        