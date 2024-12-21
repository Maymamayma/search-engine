from flask import Flask, request, jsonify, render_template
from flask_restx import Api, Resource
import os
import json
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from indexer.ranking import rank_documents

app = Flask(__name__)
api = Api(app)

def ensure_directories():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/index", exist_ok=True)

# Route for API-based search
@api.route('/search')
class SearchAPI(Resource):
    def get(self):
        query = request.args.get('q', '').strip().lower()
        if not query:
            return {"error": "Query parameter 'q' is required."}, 400

        try:
            with open('data/index/index.json', 'r', encoding='utf-8') as f:
                index = json.load(f)
        except FileNotFoundError:
            return {"error": "Index file not found. Please rebuild the index."}, 500

        results = {}
        for term in query.split():
            if term in index:
                for doc, count in index[term]["documents"].items():
                    results[doc] = results.get(doc, 0) + count

        if not results:
            return {"query": query, "results": [], "message": "No results found. Try different keywords."}

        ranked_results = rank_documents(query, results, index)
        response = [{"document": doc, "score": score} for doc, score in ranked_results]
        return {
            "query": query,
            "results": response,
            "total_results": len(ranked_results),
        }

# Route for web-based UI
@app.route('/search_ui', methods=['GET'])
def search_ui():
    query = request.args.get('q', '').strip()
    if query:
        try:
            with open('data/index/index.json', 'r', encoding='utf-8') as f:
                index = json.load(f)
        except FileNotFoundError:
            return render_template('error.html', message="Index file not found. Please rebuild the index.")

        results = {}
        for term in query.lower().split():
            if term in index:
                for doc, count in index[term]["documents"].items():
                    results[doc] = results.get(doc, 0) + count

        ranked_results = rank_documents(query, results, index)
        return render_template('search.html', query=query, results=ranked_results)

    return render_template('search.html', query='', results=[])

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    ensure_directories()
    app.run(debug=True)
