# Web Scraper Assistant

A powerful web scraping CLI tool powered by Crawl4AI.

## Features

- Fast and efficient web crawling using Crawl4AI
- Support for multiple output formats (text, HTML, Markdown)
- Configurable crawl depth and wait times
- Headless browser support
- Built-in diagnostics

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/web-scraper-assistant.git
cd web-scraper-assistant
```

2. Install dependencies using uv:

```bash
uv pip install -e .
```

## Usage

### Basic Crawling

```bash
webscraper crawl https://example.com
```

### Advanced Options

```bash
webscraper crawl https://example.com \
  --depth 5 \
  --wait 2.0 \
  --format markdown \
  --output results.md \
  --no-headless
```

### Options

- `--depth, -d`: Maximum crawl depth (default: 3)
- `--wait, -w`: Wait time between requests in seconds (default: 1.0)
- `--format, -f`: Output format [text|html|markdown] (default: text)
- `--output, -o`: Save results to file
- `--headless/--no-headless`: Run browser in headless mode (default: headless)

### Check Version

```bash
webscraper version
```

### Run Diagnostics

```bash
webscraper doctor
```

## Development

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install development dependencies:

```bash
uv pip install -e ".[dev]"
```

## License

MIT License - see [LICENSE](LICENSE) for details.
