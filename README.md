# Firecrawl CLI

A command-line interface for the Firecrawl API that helps you crawl and scrape websites with ease.

## Features

- Start web crawls with customizable parameters
- Check crawl status
- Support for both markdown and HTML output formats
- Rich terminal UI with colored output
- Environment variable configuration

## Prerequisites

- Python 3.7 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- A Firecrawl API key from [firecrawl.dev](https://firecrawl.dev)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/firecrawl-cli.git
cd firecrawl-cli
```

2. Create and activate a virtual environment using uv:

```bash
uv venv
# On Windows:
.venv/Scripts/activate
# On Unix/MacOS:
source .venv/bin/activate
```

3. Install dependencies:

```bash
uv pip install -r requirements/requirements.txt
```

4. Install the CLI in development mode:

```bash
uv pip install -e .
```

## Configuration

Create a `.env` file in the root directory with your Firecrawl API key:

```env
FIRECRAWL_API_KEY=your-api-key-here
```

## Usage

### Check Version

```bash
firecrawl version
```

### Start a Crawl

```bash
firecrawl crawl https://example.com --depth 3 --wait 1 --format both
```

Options:

- `--depth, -d`: Maximum number of pages to crawl (default: 3)
- `--wait, -w`: Wait time between requests in seconds (default: 0)
- `--format, -f`: Output format [markdown|html|both] (default: both)

### Check Crawl Status

```bash
firecrawl status <crawl-id>
```

## Development

The project structure:

```
firecrawl-cli/
├── src/
│   ├── __init__.py
│   └── cli.py
├── requirements/
│   └── requirements.txt
├── .env
├── README.md
└── setup.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Firecrawl](https://firecrawl.dev) for providing the API
- [Click](https://click.palletsprojects.com/) for the CLI framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal formatting
