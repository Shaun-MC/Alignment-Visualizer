from alignment import Alignment
from header import Header
from footer import Footer

if __name__ == "__main__":

    # Page Header
    Header.display_header() 

    # Execute Algorithm
    program = Alignment()
    program.execute()

    # Page Footer
    Footer.display_footer()