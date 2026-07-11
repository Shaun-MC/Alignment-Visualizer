class InvalidSequenceEncodingError(ValueError):
    def __init__(self, offending_index: int, offending_char: str, valid_characters: set):
        self.offending_index = offending_index
        self.offending_char = offending_char
        self.valid_characters = valid_characters
        super().__init__(
            f"Sequence {offending_index + 1} contains {offending_char!r}, "
            f"which is not a valid character ({', '.join(sorted(valid_characters))})."
        )


class Sequence:

    def __init__(self, valid_characters: set):
        self.valid_characters = valid_characters

    def validate_encoding(self, sequences: list[str]) -> list[str]:
        validated = []

        for index, sequence in enumerate(sequences):
            upper_sequence = sequence.upper()

            for character in upper_sequence:
                if character not in self.valid_characters:
                    raise InvalidSequenceEncodingError(index, character, self.valid_characters)

            validated.append(upper_sequence)

        return validated
