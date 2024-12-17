from crawler.crawler import WebCrawler
from indexer.indexer import Indexer
from searchengine import SearchEngine
import os

def ensure_directories():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/index", exist_ok=True)

def main():
    ensure_directories()

    # Step 1: Crawl web pages
    print("Starting the web crawler...")
    start_url = "https://example.com"
    crawler = WebCrawler(start_url, max_pages=50)
    crawler.crawl()

    # Save crawled pages
    #print("Saving crawled data...")
    #for idx, (url, content) in enumerate(crawler.results):
    #    file_path = f"data/raw/page_{idx}.html"
    #    with open(file_path, "w", encoding="utf-8") as f:
    #        f.write(content)

    # Step 2: Build the index
    print("Indexing the crawled data...")
    indexer = Indexer("data/crawled_results.json", "data/index")
    indexer.build_index()

    # Step 3: Search the index
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
    main()
