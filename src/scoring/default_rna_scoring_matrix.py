import pandas as pd

class DefaultRNAScoringMatrix:
    def __init__(self):
        
        # Initialize the matrix
        labels = ["_", "A", "G", "C", "U"]

        data = {
            "_": [0, 0, 0, 0, 0],
            "A": [0, 1, 0, 0, 0],
            "G": [0, 0, 1, 0, 0],
            "C": [0, 0, 0, 1, 0],
            "U": [0, 0, 0, 0, 1]
        }

        # Display the matrix
        self.scoring_matrix = pd.DataFrame(data, index=labels)

    # Preset matrices don't need to be validated because it's not displayed to the user
    def validate_scoring_matrix(self) -> None:
        return