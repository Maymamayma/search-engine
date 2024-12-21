from flask import Flask
import os
from crawler.crawler import WebCrawler
from indexer.indexer import Indexer

def ensure_directories():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/index", exist_ok=True)

def create_app():
    app = Flask(__name__)
    ensure_directories()

    # You can optionally trigger crawling and indexing through dedicated routes
    return app
