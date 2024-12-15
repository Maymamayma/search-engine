import re

def tokenize(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and non-alphanumeric characters
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Split into words
    tokens = text.split()
    return tokens
