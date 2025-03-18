from alignment import Alignment
import streamlit as st

if __name__ == "__main__":

    header = """
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Custom Header</title>
        <style>
            header {
                background-color: #660066; /* Dark purple background */
                color: black; /* Text color */
                text-align: center;
            padding: 20px;
            font-family: Arial, sans-serif;
            border-radius: 15px; /* Rounded edges */
        }
        header h1 {
            margin: 0;
            font-weight: bold;
        }
        header p {
            margin: 10px 0 0;
            color: #; 
        }
        </style>
        </head>
        <body>
        <header>
            <h1>AlignView</h1>
            <p>Customizable Alignment Visualizer</p>
        </header>
        </body>
    """

    # Page Header
    st.markdown(header, unsafe_allow_html=True) 
    
    program = Alignment()
    program.execute()

    footer = """
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Custom Footer</title>
        <style>
            footer {
                background-color: #660066; /* Dark purple background */
                text-align: center;
                padding: 10px;
                font-family: Arial;
                font-size: 14px;
                margin-top: 100px;
                border-radius: 15px; /* Rounded edges */
                line-height: 1.5; /* Line height for even spacing between lines */
            }
            footer a {
                color: blue; /* Default link color */
                text-decoration: none;
            }
            footer a:hover {
                text-decoration: underline;
            }
        </style>
        </head>
        <body>

        <footer>
            <p></p>
            <p>University of Washington Bothell CSSE</p>
            <p>This project was created by Shaun Cushman and Aaron Gröpper</p>
        </footer>
        </body>
    """

    # Page Footer
    st.markdown(footer, unsafe_allow_html=True)
    