from flask import Flask, request, jsonify
import json
from indexer.ranking import rank_documents

app = Flask(__name__)

@app.route('/')
def home():
    return (
        "Welcome to the Search Engine! "
        "Use the `/search?q=your_query` endpoint to perform a search."
    )

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required."}), 400

    try:
        with open('data/index/index.json', 'r', encoding='utf-8') as f:
            index = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "Index file not found. Please rebuild the index."}), 500

    # Process query
    results = {}
    for term in query.split():
        if term in index:
            for doc, count in index[term]["documents"].items():
                results[doc] = results.get(doc, 0) + count

    if not results:
        return jsonify({"query": query, "results": [], "message": "No results found. Try different keywords."})

    # Rank results
    ranked_results = rank_documents(query, results, index)

    # Paginate results
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('size', 10))
    start = (page - 1) * page_size
    end = start + page_size
    paginated_results = ranked_results[start:end]

    response = [{"document": doc, "score": score} for doc, score in paginated_results]
    return jsonify({
        "query": query,
        "results": response,
        "total_results": len(ranked_results),
        "page": page,
        "page_size": page_size
    })

if __name__ == "__main__":
    app.run(debug=True)
