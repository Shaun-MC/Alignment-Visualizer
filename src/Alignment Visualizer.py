from alignment.core import Alignment
from ui.header import Header
from ui.footer import Footer

if __name__ == "__main__":

    # Page Header
    Header.display_header() 

    # Execute Algorithm
    program = Alignment()
    program.execute()

    # Page Footer
    Footer.display_footer()