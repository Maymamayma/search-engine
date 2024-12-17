import os
import json
from .tokenizer import tokenize
import logging
import logging.config

# Load logging configuration
logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger(__name__)

class SearchEngine:
    def __init__(self, index_dir):
        self.index_dir = index_dir
        self.index = self.load_index()
        logger.info("SearchEngine initialized.")
    
    def load_index(self):
        index_path = os.path.join(self.index_dir, "index.json")
        logger.info(f"Loading index from {index_path}")
        
        if not os.path.exists(index_path):
            logger.error(f"Index file not found at {index_path}")
            return {}
        
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        logger.info(f"Index loaded with {len(index)} tokens.")
        return index

    def search(self, query):
        tokens = tokenize(query)  # Tokenize the query
        
        # Initialize a dictionary to store the document scores
        scores = {}
        
        # Search for each token in the index
        for token in tokens:
            if token in self.index:
                for url, frequency in self.index[token]["documents"].items():
                    if url not in scores:
                        scores[url] = 0
                    # Add the frequency of the token to the score
                    scores[url] += frequency

        # Sort results by score (in descending order)
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return the sorted URLs with their scores
        return sorted_results


# Example usage:
if __name__ == "__main__":
    search_engine = SearchEngine("data/index")
    query = input("Enter your search query: ")
    results = search_engine.search(query)

    if results:
        print(f"Found {len(results)} results:")
        for url, score in results:
            print(f"URL: {url} | Score: {score}")
    else:
        print("No results found.")
