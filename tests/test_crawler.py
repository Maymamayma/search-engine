import unittest
from crawler.crawler import WebCrawler

class TestCrawler(unittest.TestCase):
    def test_crawl_basic(self):
        crawler = WebCrawler(start_url="https://example.com", max_pages=5)
        crawler.crawl()
        self.assertGreater(len(crawler.results), 0)

if __name__ == "__main__":
    unittest.main()
