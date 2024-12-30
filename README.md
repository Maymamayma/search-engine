# Search Engine

This is a simple search engine built from scratch using Python. It crawls web pages, indexes the content, and allows users to search for documents based on their query. It includes features like ranking results using TF-IDF and a basic Flask-based frontend for searching and viewing results.

## Features

- Web crawling using a custom crawler
- Indexing of documents with TF-IDF ranking
- Search functionality via a Flask web interface
- Search results are ranked based on relevance to the query
- API endpoint for programmatic access to search results

## Project Structure

```perl
search_engine/
├── crawler/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── crawler.py        # Main crawling logic
│   ├── robots_handler.py # Code to handle robots.txt
│   └── utils.py          # Utility functions (e.g., URL validation)
│
├── indexer/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── indexer.py        # Main indexing logic
│   ├── tokenizer.py      # Tokenization and text preprocessing
│   ├── ranking.py        # Ranking logic (e.g., TF-IDF or PageRank)
│   └── utils.py          # Utility functions (e.g., stemming, stopword removal)
│
├── frontend/
│   ├── __init__.py
│   ├── app.py            # Backend API (Flask or FastAPI)
│   ├── templates/        # HTML templates for the UI (if using Flask)
│   └── static/           # CSS, JavaScript, and other assets
│
├── tests/
│   ├── test_crawler.py   # Unit tests for the crawler
│   ├── test_indexer.py   # Unit tests for the indexer
│   └── test_frontend.py  # Unit tests for the frontend
│
├── data/
│   ├── raw/              # Raw HTML data from the crawler
│        ├── index.json
│   ├── processed/        # Processed data ready for indexing
│   └── index/            # Index files (e.g., inverted index, metadata)
│
├── docs/                 # Documentation and design files
│   ├── architecture.md
│   └── requirements.md
│
├── config/
│   ├── settings.py       # Configuration for the crawler, indexer, etc.
│   └── logging.conf      # Logging configuration
│
├── requirements.txt      # List of Python dependencies
├── crawled_results.json
├── run.py                # Entry point to run the application
└── README.md             # Project description and setup instructions
```


## Installation

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Install Dependencies

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/search-engine.git
    cd search-engine
    ```

2. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Search Engine

1. **Run the Flask app:**

    The Flask app provides the user interface for searching documents.

    ```bash
    python frontend/app.py
    ```

    By default, the app will run on [http://127.0.0.1:5000](http://127.0.0.1:5000).

2. **Crawling and Indexing:**

    When the Flask app is started, it will automatically run the `run.py` script to start the crawling and indexing process. This will crawl a set of websites, store the HTML data in `data/raw/`, and then build an index for searching.

    To manually run the crawling and indexing process:

    ```bash
    python run.py
    ```

    This will start the crawling and indexing process and generate the index in `data/index/index.json`.

### Search API

You can also interact with the search engine programmatically through the search API.

- **Endpoint: `/search`**

    **Method:** GET  
    **Parameters:**
    - `q` (required): The search query.
    - `page` (optional): The page number (default: 1).
    - `size` (optional): The number of results per page (default: 10).

    **Example Request:**

    ```bash
    curl "http://127.0.0.1:5000/search?q=python&size=5&page=1"
    ```

    **Example Response:**

    ```json
    {
        "query": "python",
        "results": [
            {"document": "document1.html", "score": 3.45},
            {"document": "document2.html", "score": 2.89}
        ],
        "total_results": 50,
        "page": 1,
        "page_size": 5
    }
    ```

### Frontend Search Interface

You can also search directly from the web interface by visiting [http://127.0.0.1:5000/](http://127.0.0.1:5000/). Simply enter a search query, and the results will be displayed below.

## Running Tests

To run the tests for different components of the search engine:

```bash
pytest
```

## Configuration

You can configure various aspects of the crawler, indexer, and application by editing the configuration files located in the `config/` directory:

`settings.py`: Configuration settings for the crawler, indexer, etc.
`logging.conf`: Logging configuration. 

## Contributing

If you'd like to contribute to the project, feel free to fork the repository, make changes, and submit a pull request. All contributions are welcome!

## License

This project is licensed under the MIT [License](https://github.com/Maymamayma/search-engine/blob/master/LICENSE) – see the LICENSE file for details.

## Acknowledgments

- This project uses Flask for the web interface and API.
- The crawler is designed to handle basic web scraping with respect to robots.txt and basic error handling.
- The ranking and indexing components are built to utilize basic TF-IDF, but can be extended for more sophisticated ranking algorithms.

## Known Issues

- The crawler's ability to handle dynamic content (e.g., JavaScript-rendered pages) is limited.
- The search index might need to be rebuilt after significant updates to the crawled pages.

## Future Improvements
- Implement a more advanced ranking algorithm (e.g., PageRank, BM25).
- Improve the crawler to handle dynamic content and websites with JavaScript rendering.
- Implement distributed crawling and indexing for scaling.
- Add authentication or rate-limiting mechanisms for the API.
