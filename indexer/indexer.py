import os
import json
from .tokenizer import tokenize
from bs4 import BeautifulSoup
import logging
import logging.config
import sys  # Required for consoleHandler's arguments
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from indexer.tokenizer import tokenize

#from tokenizer import tokenize
# Load logging configuration
logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger(__name__)

class Indexer:
    def __init__(self, crawled_file, index_dir):
        self.crawled_file = crawled_file  # Path to the crawled results JSON file
        self.index_dir = index_dir
        self.index = {}
        logger.info("Indexer initialized.")

    def clean_html(html_content):
        """
        Extract text content from HTML while removing tags.
        
        Args:
        - html_content (str): Raw HTML content.
        
        Returns:
        - str: Cleaned text content.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)

    def build_index(self):
        logger.info(f"Building index from file: {self.crawled_file}")
        
        # Load the crawled results from the JSON file
        with open(self.crawled_file, 'r', encoding='utf-8') as f:
            crawled_data = json.load(f)

        # Indexing logic
        for page in crawled_data:
            url = page['url']
            html_content = page['html_content']

            logger.info(f"Processing page: {url}")  # Log the URL being processed

            # Tokenize the page content
            tokens = tokenize(html_content)
                
            for token in tokens:
                if token not in self.index:
                    self.index[token] = {"count": 0, "documents": {}}
                self.index[token]["count"] += 1
                if url not in self.index[token]["documents"]:
                    self.index[token]["documents"][url] = 0
                self.index[token]["documents"][url] += 1

                logger.debug(f"Indexed token: {token} in {url}")  # Log each token processed

        self.save_index()

    def save_index(self):
        os.makedirs(self.index_dir, exist_ok=True)
        index_path = os.path.join(self.index_dir, "index.json")
        logger.info(f"Saving index to {index_path}")  # Log where the index is being saved
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=4)
        logger.info("Index saved successfully.")

# Example usage:
if __name__ == "__main__":
    # Specify the path to the crawled results and the directory to save the index
    indexer = Indexer("crawled_results.json", "data/index")
    indexer.build_index()
    print("Indexing completed and saved.")