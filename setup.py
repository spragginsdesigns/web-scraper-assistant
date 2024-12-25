from setuptools import setup, find_packages

setup(
    name="firecrawl-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.7",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "pydantic>=2.5.3",
    ],
    entry_points={
        "console_scripts": [
            "firecrawl=src.cli:cli",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool for interacting with the Firecrawl API",
    keywords="web crawler, cli, api",
    python_requires=">=3.7",
)