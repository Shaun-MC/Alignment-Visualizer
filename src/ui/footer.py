import streamlit as st
from htbuilder import div, p, styles, footer as htfooter
from htbuilder.units import px

class Footer:
    @staticmethod
    def display_footer():

        def create_footer():

            footer_style = styles(
                background_color="#660066",
                text_align="center",
                padding=px(10),
                font_family="Arial",
                font_size=px(14),
                margin_top=px(100),
                border_radius=px(15),
                line_height=1.5,
                color="white"
            )
        
            # Creating the footer content with htbuilder
            footer = div()(
                htfooter(style=footer_style)(
                    p(""),
                    p("University of Washington Bothell CSSE"),
                    p("This project was created by Shaun Cushman and Aaron Gröpper")
                )
            )
        
            # CSS to hide default elements
            hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .stApp {bottom: 105px;}
                </style>
            """

            return footer, hide_st_style

        footer, hide_styles = create_footer()

        # Display the actual elements 
        st.markdown(str(footer), unsafe_allow_html=True) 