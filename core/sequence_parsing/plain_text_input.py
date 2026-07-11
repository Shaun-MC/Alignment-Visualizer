class PlainTextInput:

    def clean_sequences(self, raw_input: str) -> list[str]:
        return [line.strip() for line in raw_input.splitlines() if line.strip()]
