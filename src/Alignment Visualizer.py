from ui.footer import Footer
from ui.header import Header
from alignment.core import Alignment
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


if __name__ == "__main__":

    # Page Header
    Header.display_header()

    # Execute Algorithm
    program = Alignment()
    program.execute()

    # Page Footer
    Footer.display_footer()
