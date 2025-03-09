# AppTest documentation: https://docs.streamlit.io/develop/api-reference/app-testing

from streamlit.testing.v1 import AppTest

"""Single Alignment Tests"""

def test_single_zero_input() -> bool:
    
    # Arrange
    at = AppTest.from_file("streamlit_app.py")
    
    # Act
    
    # Assert
    assert True

# Over the character limit input - currently a hardcoded value
def test_single_character_limit() -> bool:
    
    # Arrange
    
    # Act
    
    # Assert
    assert True
    
# DNA button is selected - not 'A', 'C', 'G', 'T' input
def test_single_DNA_input_fail_validation() -> bool:
    # Arrange
    
    # Act
    
    # Assert
    assert True

# DNA button is selected - is 'A', 'C', 'G', 'T' input
def test_single_DNA_input_pass_validation() -> bool:
    # Arrange
    
    # Act
    
    # Assert
    assert True

# RNA button is selected - is 'A', 'C', 'G', 'U' input
def test_single_RNA_input_fail_validation() -> bool:
    # Arrange
    
    # Act
    
    # Assert
    assert True

# RNA button is selected - not 'A', 'C', 'G', 'U' input
def test_single_RNA_input_pass_validation() -> bool:
    # Arrange
    
    # Act
    
    # Assert 
    assert True

# Protein button is selected - not 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y' input
def test_single_protein_input_fail_validation() -> bool:
    # Arrange
    
    # Act
    
    # Assert
    assert True

# Protein button is selected - is 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y' input
def test_single_protein_input_fail_validation() -> bool:
    # Arrange
    
    # Act
    
    # Assert
    assert True


# ...