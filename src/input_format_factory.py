from fasta_input import FASTAInput
from plain_text_input import PlainTextInput

class InputFormatFactory:
    @staticmethod
    def create_input_format(input_format_option):

        match input_format_option:
            case "FASTA":
                return FASTAInput()
            case "Plain Text":
                return PlainTextInput()
            case _:
                raise ValueError("Invalid input format option")