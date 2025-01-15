from flask import Flask
from crawler.crawler import WebCrawler
from indexer.indexer import Indexer
from searchengine import SearchEngine
import os

def ensure_directories():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/index", exist_ok=True)

def run_crawling_and_indexing():
    # Step 1: Crawl web pages
    print("Starting the web crawler...")
    start_url = "https://fr.wikipedia.org/"
    crawler = WebCrawler(start_url, max_pages=5)
    crawler.crawl()
    print("Crawl finished.")

    # Step 2: Build the index
    print("Indexing the crawled data...")
    indexer = Indexer("crawled_results.json", "data/index")
    indexer.build_index()
    print("Indexing completed.")

def interactive_search():
    # Step 3: Search the index interactively
    search_engine = SearchEngine("data/index")
    query = input("Enter your search query: ")
    results = search_engine.search(query)

    # Display search results
    if results:
        print(f"Found {len(results)} results:")
        for url, score in results:
            print(f"URL: {url} | Score: {score}")
    else:
        print("No results found.")

if __name__ == "__main__":
    ensure_directories()
    run_crawling_and_indexing()
    interactive_search()