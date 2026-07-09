class PlainTextInput:
    # This class doesn't need to store data
    def __init__(self):
        pass

    def cleanSequences(self, sequences: str) -> list:
        return [] if sequences == "" else sequences.splitlines()
    
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