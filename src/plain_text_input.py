class PlainTextInput:

    @staticmethod
    def validateFileFormat(sequences) -> bool:

        sequences = sequences.splitlines()
                    
        for line in sequences:

            for char in line:

                if type(char) != str:
                    return False
                            
                char_ascii = ord(char)
                            
                if char_ascii < 65 or char_ascii > 90:
                    return False
                                       
        return True