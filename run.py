from crawler.crawler import WebCrawler
from indexer.indexer import Indexer
from frontend.app import app
import os

def ensure_directories():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/index", exist_ok=True)

def main():
    ensure_directories()

    # Step 1: Crawl web pages
    print("Starting the web crawler...")
    crawler = WebCrawler(start_url="https://example.com", max_pages=10)
    crawler.crawl()

    # Save crawled pages
    print("Saving crawled data...")
    for idx, (url, content) in enumerate(crawler.results):
        file_path = f"data/raw/page_{idx}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Step 2: Build the index
    print("Indexing the crawled data...")
    indexer = Indexer(data_dir="data/raw", index_dir="data/index")
    indexer.build_index()

    # Step 3: Start the search frontend
    print("Starting the search frontend...")
    app.run(debug=True)

if __name__ == "__main__":
    main()
