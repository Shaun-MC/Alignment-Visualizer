from alignment import Alignment
import streamlit as st

if __name__ == "__main__":

    # Page Header
    st.markdown(
        '<header style="text-align: center"> Sequence Alignment Visualizer </header>', 
        unsafe_allow_html=True
    )
    
    program = Alignment()
    program.execute()

    # Page Footer
    st.markdown(
        '<footer style="text-align: center"> University of Washington Bothell CSSE, (Shaun Cushman, Aaron Gröpper) </footer>', 
        unsafe_allow_html=True
    )
    