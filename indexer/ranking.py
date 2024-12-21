from math import log
import os
import requests  # To fetch content from URLs

def calculate_tf(term, document_content):
    """
    Calculate term frequency (TF) for a term in the document content.

    Args:
    - term (str): The term to calculate TF for.
    - document_content (str): The content of the document.

    Returns:
    - float: Term frequency of the term in the document.
    """
    if isinstance(document_content, str):
        tokens = document_content.split()  # Tokenize the document content
    else:
        tokens = document_content

    return tokens.count(term) / len(tokens) if tokens else 0


def calculate_idf(term, corpus):
    num_documents_with_term = sum(1 for doc in corpus if term in doc)
    return log(len(corpus) / (1 + num_documents_with_term))

def fetch_content(doc):
    """
    Fetch content from a document.
    If it's a URL, download its content.
    If it's a file path, read the content from the file.

    Args:
    - doc (str): Document path or URL.

    Returns:
    - str: Content of the document.
    """
    if doc.startswith("http://") or doc.startswith("https://"):
        response = requests.get(doc)
        response.raise_for_status()  # Raise error for bad responses
        return response.text
    elif os.path.exists(doc):  # Check if it's a local file
        with open(doc, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"Invalid document path or URL: {doc}")

def rank_documents(query, results, index):
    """
    Rank documents based on TF-IDF or other ranking metrics, incorporating the index.

    Args:
    - query (str): The search query.
    - results (dict): Documents and their corresponding term occurrence counts.
    - index (dict): The inverted index used for searching.

    Returns:
    - list: Ranked list of documents with scores.
    """
    ranked_results = []
    query_terms = query.split()

    for doc, score in results.items():
        try:
            document_content = fetch_content(doc)
        except Exception as e:
            print(f"Error fetching content for {doc}: {e}")
            continue

        doc_score = 0
        for term in query_terms:
            tf = calculate_tf(term, document_content)

            # Optionally use the index for inverse document frequency (IDF)
            if term in index:
                idf = calculate_idf(term, index)  # You can implement this method
            else:
                idf = 1  # If term is not in the index, default IDF to 1

            # Calculate TF-IDF score for the term
            doc_score += tf * idf  # TF-IDF score

        ranked_results.append((doc, doc_score))
    # Debug: Print the ranked results before sorting
    print(f"Ranked results (before sorting): {ranked_results}")
    # Sort the documents by their scores in descending order
    return sorted(ranked_results, key=lambda x: x[1], reverse=True)
