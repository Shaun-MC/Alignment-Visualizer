class FASTAInput():
    # This class doesn't need to store data
    def __init__(self):
        pass

    def cleanSequences(self, sequences: str) -> list:

        if sequences == "":
            return []
        
        ret = []
        sequences = sequences.splitlines()
                    
        for line in sequences:

            if line[0] != ">":
                ret.append(line)
                    
        return ret
        
    def validateFileFormat(sequences) -> bool:

        sequences = sequences.splitlines()
        keys = set()
        line_counter = 0
                    
        # Every other line starts w/ an '>' and each key is unique
        for line in sequences:
            # The line with the keys are only on even lines
            if line_counter % 2 == 0:
                            
                if line[0] != '>' or line in keys:
                    return False

                else:
                    keys.add(line)
                            
        return True
