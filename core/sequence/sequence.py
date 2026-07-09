class Sequence:

    def __init__(self, valid_characters: set):
        self.valid_characters = valid_characters
        self.validated_sequences = list()

    def get_validated_sequences(self) -> list[str]:
        return self.validated_sequences

    def validate_encoding(self, sequences: list[str]) -> None:

        if sequences is None:
            return

        for i, sequence in enumerate(sequences):

            upper_sequence = sequence.upper()

            sequences[i] = upper_sequence

            for character in upper_sequence:

                if character not in self.valid_characters:
                    self.validated_sequences = list()
                    return

            self.validated_sequences.append(upper_sequence)
