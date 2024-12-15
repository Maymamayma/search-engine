import os
import json
from .tokenizer import tokenize
from bs4 import BeautifulSoup
import logging
import logging.config
import sys  # Required for consoleHandler's arguments

# Load logging configuration
logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger(__name__)

class Indexer:
    def __init__(self, data_dir, index_dir):
        self.data_dir = data_dir
        self.index_dir = index_dir
        self.index = {}
        logger.info("Indexer initialized.")

    def build_index(self):
        logger.info(f"Building index from directory: {self.data_dir}")
        # Indexing logic here
        logger.info("Indexing completed.")
        for file_name in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, file_name)
            logger.info(f"Processing file: {file_name}")  # Log the file being processed
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                title = soup.title.string if soup.title else "No Title"
                tokens = tokenize(soup.get_text())
                
                for token in tokens:
                    if token not in self.index:
                        self.index[token] = {"count": 0, "documents": {}}
                    self.index[token]["count"] += 1
                    if file_name not in self.index[token]["documents"]:
                        self.index[token]["documents"][file_name] = 0
                    self.index[token]["documents"][file_name] += 1

                    logger.debug(f"Indexed token: {token} in {file_name}")  # Log each token processed

        self.save_index()

    def save_index(self):
        os.makedirs(self.index_dir, exist_ok=True)
        index_path = os.path.join(self.index_dir, "index.json")
        logger.info(f"Saving index to {index_path}")  # Log where the index is being saved
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f)
        logger.info("Index saved successfully.")

# Example usage:
if __name__ == "__main__":
    indexer = Indexer("data/raw", "data/index")
    indexer.build_index()
