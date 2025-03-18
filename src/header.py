import streamlit as st
from htbuilder import div, p, styles, header as htheader, h1
from htbuilder.units import px

class Header:

    @staticmethod
    def display_header():

        def create_header():

            header_style = styles(
                background_color="#660066",
                color="black",
                text_align="center",
                padding=px(20),
                font_family="Arial, sans-serif",
                border_radius=px(15)
            )

            h1_style = styles(
                margin=0,
                font_weight="bold"
            )

            # Header paragraph style
            p_style = styles(
                margin=f"{px(10)} 0 0",
                color="white"  
            )

            # Creating the header content with htbuilder
            header = div()(
                htheader(style=header_style)(
                    h1(style=h1_style)("AlignView"),
                    p(style=p_style)("Customizable Alignment Visualizer")
                )
            )

            return header
            
        st.markdown(create_header(), unsafe_allow_html=True) 