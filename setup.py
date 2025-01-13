from setuptools import setup, find_packages

setup(
    name="web-scraper-assistant",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.7",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "pydantic>=2.5.3",
        "crawl4ai>=0.4.247",
        "asyncio>=3.4.3",
    ],
    entry_points={
        "console_scripts": [
            "webscraper=src.cli:cli",
        ],
    },
    author="Web Scraper Assistant Contributors",
    author_email="your.email@example.com",
    description="A CLI tool for web scraping using Crawl4AI",
    keywords="web crawler, cli, api, crawl4ai",
    python_requires=">=3.8",
)