class FASTAInput:

    def clean_sequences(self, raw_input: str) -> list[str]:

        sequences = []
        current_lines = []

        for line in raw_input.splitlines():
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                if current_lines:
                    sequences.append("".join(current_lines))
                    current_lines = []
            else:
                current_lines.append(line)

        if current_lines:
            sequences.append("".join(current_lines))

        return sequences
