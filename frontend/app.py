from flask import Flask, request, jsonify
import json
from indexer.ranking import rank_documents

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    with open('data/index/index.json', 'r', encoding='utf-8') as f:
        index = json.load(f)

    # Retrieve matching documents
    results = {}
    for term in query.split():
        if term in index:
            for doc, count in index[term]["documents"].items():
                if doc not in results:
                    results[doc] = 0
                results[doc] += count

    # Rank the results
    ranked_results = rank_documents(query, results)

    # Format results
    response = [{"document": doc, "score": score} for doc, score in ranked_results]
    return jsonify({"query": query, "results": response})

if __name__ == "__main__":
    app.run(debug=True)
