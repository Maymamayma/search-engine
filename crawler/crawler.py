import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque
import logging
from crawler.robots_handler import is_allowed
import hashlib
import logging
import logging.config
import sys  # Required for consoleHandler's arguments

# Load logging configuration
logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self, start_url, max_pages=50):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited = set()
        self.queue = deque([start_url])
        self.results = []
        self.hashes = set()
        logger.info("WebCrawler initialized.")
    
    def is_duplicate(self, content):
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        if content_hash in self.hashes:
            return True
        self.hashes.add(content_hash)
        return False

    def crawl(self):
        logger.info(f"Starting crawl from {self.start_url}...")
        # Crawl logic here
        logger.info(f"Crawl completed. {len(self.visited)} pages visited.")
        while self.queue and len(self.visited) < self.max_pages:
            current_url = self.queue.popleft()
            if current_url in self.visited:
                continue

            html = self.fetch_page(current_url)
            if not html or self.is_duplicate(html):
                continue

            self.visited.add(current_url)
            self.results.append((current_url, html))
            links = self.extract_links(html, current_url)
            self.queue.extend(links - self.visited)

    def fetch_page(self, url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text
            logging.warning(f"Failed to fetch {url} - Status: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
        return None

    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for anchor in soup.find_all('a', href=True):
            full_url = urljoin(base_url, anchor['href'])
            if is_allowed(full_url) and full_url not in self.visited:
                links.add(full_url)
        return links

    def crawl(self):
        while self.queue and len(self.visited) < self.max_pages:
            current_url = self.queue.popleft()
            if current_url in self.visited:
                continue

            logging.info(f"Crawling: {current_url}")
            html = self.fetch_page(current_url)
            if not html:
                continue

            self.visited.add(current_url)
            self.results.append((current_url, html))
            links = self.extract_links(html, current_url)
            self.queue.extend(links - self.visited)

        logging.info(f"Crawled {len(self.visited)} pages.")

# Example usage:
if __name__ == "__main__":
    crawler = WebCrawler("https://example.com", max_pages=20)
    crawler.crawl()
