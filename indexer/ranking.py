from math import log

def calculate_tf(term, document):
    return document.count(term) / len(document)

def calculate_idf(term, corpus):
    num_documents_with_term = sum(1 for doc in corpus if term in doc)
    return log(len(corpus) / (1 + num_documents_with_term))

def rank_documents(query, documents):
    scores = {}
    query_terms = query.split()
    for doc_id, content in documents.items():
        score = 0
        for term in query_terms:
            tf = calculate_tf(term, content)
            idf = calculate_idf(term, documents.values())
            score += tf * idf
        scores[doc_id] = score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
