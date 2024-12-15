import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque
import logging
from .robots_handler import is_allowed
import hashlib
import logging.config
import json

# Load logging configuration
logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self, start_url, max_pages=50, crawled_file='crawled_results.json'):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited = set()
        self.queue = deque([start_url])
        self.results = []
        self.hashes = set()
        self.crawled_file = crawled_file
        logger.info("WebCrawler initialized.")
    
    # Ensure no duplicate content is processed
    def is_duplicate(self, content):
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        if content_hash in self.hashes:
            return True
        self.hashes.add(content_hash)
        return False

    # Crawl web pages starting from the start_url
    def crawl(self):
        logger.info(f"Starting crawl from {self.start_url}...")
        while self.queue and len(self.visited) < self.max_pages:
            current_url = self.queue.popleft()

            # Skip if already visited
            if current_url in self.visited:
                continue

            logger.info(f"Crawling: {current_url}")
            html = self.fetch_page(current_url)

            # Skip if the page could not be fetched or is duplicate
            if not html or self.is_duplicate(html):
                continue

            self.visited.add(current_url)
            self.results.append((current_url, html))

            # Save the crawled page for indexing
            self.save_results_to_json()

            links = self.extract_links(html, current_url)
            self.queue.extend(link for link in links if link not in self.visited and link not in self.queue)

        logger.info(f"Crawl completed. {len(self.visited)} pages visited.")

    # Fetch a web page
    def fetch_page(self, url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text
            logger.warning(f"Failed to fetch {url} - Status: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
        return None

    # Extract all valid links from the HTML
    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for anchor in soup.find_all('a', href=True):
            full_url = urljoin(base_url, anchor['href'])
            if is_allowed(full_url) and full_url not in self.visited:
                links.add(full_url)
        return links

    # Save results to a JSON file
    def save_results_to_json(self):
        """
        Save the crawled results in a structured JSON format.
        Each result includes the URL and the HTML content.
        """
        data = [{"url": url, "html_content": html} for url, html in self.results]
        try:
            with open(self.crawled_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Results saved to {self.crawled_file}")
        except IOError as e:
            logger.error(f"Error saving results to {self.crawled_file}: {e}")

# Example usage:
if __name__ == "__main__":
    crawler = WebCrawler("https://example.com", max_pages=5, crawled_file="crawled_results.json")
    crawler.crawl()

    print("Crawling completed. Results saved to 'crawled_results.json'.")
