import pandas as pd

class DefaultDNAScoringMatrix:
    def __init__(self):
        # Initialize the matrix
        labels = ["_", "A", "G", "C", "T"]

        # Hard-coded data for the scoring matrix
        data = {
            "_": [0, 0, 0, 0, 0],
            "A": [0, 1, 0, 0, 0],
            "G": [0, 0, 1, 0, 0],
            "C": [0, 0, 0, 1, 0],
            "T": [0, 0, 0, 0, 1]
        }
        
        self.scoring_matrix = pd.DataFrame(data, index=labels)

    # Preset matrices don't need to be validated because it's not displayed to the user
    def validate_scoring_matrix(self) -> None:
        return