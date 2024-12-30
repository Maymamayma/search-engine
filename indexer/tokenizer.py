import re

def tokenize(text):
    """
    Tokenize a string into terms.
    
    Args:
    - text (str): Input text.
    
    Returns:
    - list: List of terms (words).
    """
    # Remove non-alphanumeric characters and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    return words
