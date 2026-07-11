from .fasta_input import FASTAInput
from .plain_text_input import PlainTextInput


class InputFormatFactory:
    @staticmethod
    def create_input_format(input_format_option: str):
        match input_format_option:
            case "FASTA":
                return FASTAInput()
            case "plain":
                return PlainTextInput()
            case _:
                raise ValueError(f"Invalid input format option: {input_format_option!r}")
