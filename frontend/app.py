from flask import Flask, request, jsonify, render_template
from flask_restx import Api, Resource
import os
import json
import sys
import subprocess

# Add the root directory to the Python path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from indexer.ranking import rank_documents

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app)

# Ensure crawling and indexing happens by calling run.py
def run_crawling_and_indexing():
    index_path = "data/index/index.json"
    if not os.path.exists(index_path):
        print("Index file not found. Starting crawling and indexing via run.py...")
        try:
            subprocess.run(
                [sys.executable, "run.py"],  # Runs run.py using the same Python interpreter
                check=True,
            )
            print("Crawling and indexing completed.")
        except subprocess.CalledProcessError as e:
            print(f"Error while running crawling and indexing: {e}")
    else:
        print("Index file already exists. Skipping crawling and indexing.")

# Call the crawling process when the app starts
run_crawling_and_indexing()

# Define routes and API
@api.route('/search')
class SearchAPI(Resource):
    def get(self):
        """
        API Endpoint to handle search queries via HTTP GET requests.
        """
        query = request.args.get('q', '').strip().lower()
        if not query:
            return {"error": "Query parameter 'q' is required."}, 400

        # Load the index
        try:
            with open('data/index/index.json', 'r', encoding='utf-8') as f:
                index = json.load(f)
        except FileNotFoundError:
            return {"error": "Index file not found. Please rebuild the index."}, 500

        # Process the query
        results = {}
        for term in query.split():
            if term in index:
                for doc, count in index[term]["documents"].items():
                    results[doc] = results.get(doc, 0) + count

        # Rank results
        ranked_results = rank_documents(query, results, index)

        # Paginate results
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        paginated_results = ranked_results[start:end]

        response = [{"document": doc, "score": score} for doc, score in paginated_results]
        return {
            "query": query,
            "results": response,
            "total_results": len(ranked_results),
            "page": page,
            "page_size": page_size
        }

@app.route('/')
def home():
    """
    Render the home page with the search UI.
    """
    return render_template('home.html')  # Ensure `home.html` exists in `frontend/templates`

@app.route('/search_ui', methods=['GET'])
def search_ui():
    """
    Render the search results page for user queries.
    """
    query = request.args.get('q', '').strip()
    if query:
        # Load the index
        try:
            with open('data/index/index.json', 'r', encoding='utf-8') as f:
                index = json.load(f)
        except FileNotFoundError:
            return render_template('search.html', query=query, results=[], error="Index file not found. Please rebuild the index.")

        # Process and rank results
        results = {}
        for term in query.lower().split():
            if term in index:
                for doc, count in index[term]["documents"].items():
                    results[doc] = results.get(doc, 0) + count

        ranked_results = rank_documents(query, results, index)
        print(f"Ranked Results: {ranked_results}")  # Debug: Check ranked results
        
        # Pass the ranked results and scores to the template
        response = [{"document": doc, "score": score} for doc, score in ranked_results]
        return render_template('search.html', query=query, results=response)

    # Render an empty search UI if no query
    return render_template('search.html', query=query, results=[])

if __name__ == "__main__":
    app.run(debug=True)
