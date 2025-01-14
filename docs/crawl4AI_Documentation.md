## Setup & Installation

### UV pip Installation

```bash
uv pip install crawl4ai
```

## Quick Start

### Your First Crawl

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler()
    result = await crawler.arun("https://example.com")
    print(result.text)

import asyncio
asyncio.run(main())
```

### Generating Markdown

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler()
    result = await crawler.arun("https://example.com")
    markdown = result.to_markdown()
    print(markdown)

import asyncio
asyncio.run(main())
```

### Simple Extraction

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler()
    result = await crawler.arun("https://example.com")
    extracted = result.extract({"title": "h1", "paragraphs": "p"})
    print(extracted)

import asyncio
asyncio.run(main())
```

## Core Features

### Single-Page Crawling

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler()
    result = await crawler.arun("https://example.com/specific-page")
    print(result.text)

import asyncio
asyncio.run(main())
```

### Advanced Browser/Crawler Parameters

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler(
        headless=False,
        user_agent="Custom User Agent",
        viewport={"width": 1920, "height": 1080}
    )
    result = await crawler.arun("https://example.com")
    print(result.text)

import asyncio
asyncio.run(main())
```

### Content Filtering

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler()
    result = await crawler.arun("https://example.com", filter_by={"tag": "article"})
    print(result.text)

import asyncio
asyncio.run(main())
```

### Caching

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler(cache_dir="./cache")
    result = await crawler.arun("https://example.com")
    print(result.text)

import asyncio
asyncio.run(main())
```

## Advanced Features

### Link & Media Handling

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler(follow_links=True, download_media=True)
    result = await crawler.arun("https://example.com")
    print(result.links)
    print(result.media)

import asyncio
asyncio.run(main())
```

### Lazy Loading

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler(scroll_to_bottom=True)
    result = await crawler.arun("https://example.com")
    print(result.text)

import asyncio
asyncio.run(main())
```

### Hooking & Authentication

```python
from crawl4ai import AsyncWebCrawler

async def login(page):
    await page.goto("https://example.com/login")
    await page.fill("#username", "your_username")
    await page.fill("#password", "your_password")
    await page.click("#login-button")

async def main():
    crawler = AsyncWebCrawler(hooks={"before_crawl": login})
    result = await crawler.arun("https://example.com/protected-page")
    print(result.text)

import asyncio
asyncio.run(main())
```

### Proxies

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler(proxy="http://proxy.example.com:8080")
    result = await crawler.arun("https://example.com")
    print(result.text)

import asyncio
asyncio.run(main())
```

### Session Management

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler(persistent_context=True)
    result1 = await crawler.arun("https://example.com/page1")
    result2 = await crawler.arun("https://example.com/page2")
    print(result1.text, result2.text)

import asyncio
asyncio.run(main())
```

## Extraction

### No-LLM Extraction (CSS, XPath)

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler()
    result = await crawler.arun("https://example.com")
    extracted = result.extract({
        "title": "h1",
        "paragraphs": "p",
        "links": "//a/@href"
    })
    print(extracted)

import asyncio
asyncio.run(main())
```

### LLM-Based Extraction

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler()
    result = await crawler.arun("https://example.com")
    extracted = result.extract_llm("Extract the main topic and key points from this page.")
    print(extracted)

import asyncio
asyncio.run(main())
```

### Chunking

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler()
    result = await crawler.arun("https://example.com")
    chunks = result.chunk(max_tokens=1000)
    for chunk in chunks:
        print(chunk)

import asyncio
asyncio.run(main())
```

### Clustering

```python
from crawl4ai import AsyncWebCrawler

async def main():
    crawler = AsyncWebCrawler()
    result = await crawler.arun("https://example.com")
    clusters = result.cluster(n_clusters=3)
    for cluster in clusters:
        print(cluster)

import asyncio
asyncio.run(main())
```

## API Reference

### AsyncWebCrawler

```python
class AsyncWebCrawler:
    def __init__(self, **kwargs):
        """
        Initialize the AsyncWebCrawler with various options.

        :param headless: Boolean to run browser in headless mode
        :param user_agent: Custom user agent string
        :param viewport: Dictionary with 'width' and 'height' for viewport size
        :param cache_dir: Directory to store cache
        :param follow_links: Boolean to follow links during crawl
        :param download_media: Boolean to download media during crawl
        :param scroll_to_bottom: Boolean to scroll to bottom of page
        :param hooks: Dictionary of hook functions
        :param proxy: Proxy server URL
        :param persistent_context: Boolean to maintain browser context between runs
        """
        pass

    async def arun(self, url, **kwargs):
        """
        Asynchronously crawl a URL and return a CrawlResult.

        :param url: URL to crawl
        :param filter_by: Dictionary of filters to apply to content
        :return: CrawlResult object
        """
        pass
```

### CrawlResult

```python
class CrawlResult:
    def __init__(self, **kwargs):
        """
        Initialize the CrawlResult with crawl data.
        """
        pass

    def to_markdown(self):
        """
        Convert the crawl result to Markdown format.

        :return: String of Markdown content
        """
        pass

    def extract(self, selectors):
        """
        Extract content using CSS or XPath selectors.

        :param selectors: Dictionary of name:selector pairs
        :return: Dictionary of extracted content
        """
        pass

    def extract_llm(self, prompt):
        """
        Extract content using LLM-based extraction.

        :param prompt: Extraction prompt for the LLM
        :return: Extracted content based on the prompt
        """
        pass

    def chunk(self, max_tokens):
        """
        Split the content into chunks.

        :param max_tokens: Maximum number of tokens per chunk
        :return: List of content chunks
        """
        pass

    def cluster(self, n_clusters):
        """
        Cluster the content into groups.

        :param n_clusters: Number of clusters to create
        :return: List of content clusters
        """
        pass
```

This documentation guide provides a comprehensive overview of Crawl4AI's features and usage. It includes code samples for each major functionality, making it easy for developers to get started and implement advanced features in their projects.

Citations:
[1] https://docs.crawl4ai.com/

## Optimized Multi-URL Crawling

Crawl4AI’s can handle multiple URLs in a single run, which can greatly reduce overhead and speed up crawling. This guide shows how to:

1. crawl a list of URLs using the session, avoiding repeated browser creation. 2. -crawl subsets of URLs in batches, again reusing the same browser.
   When the entire process finishes, you close the browser once— memory and resource usage.

## 1. Why Avoid Simple Loops per URL?

```
 url  urls:
    ()  crawler:
    result =  crawler.arun(url)

```

1. Spinning up a browser for each URL
2. Closing it immediately after the single crawl
3. Potentially using a lot of CPU/memory for short-living browsers
4. Missing out on session reusability if you have login or ongoing states

approaches ensure you the browser once, then crawl multiple URLs with minimal overhead.

## 2. Sequential Crawling with Session Reuse

1. instance for URLs. 2. session (via ) so we can preserve local storage or cookies across URLs if needed. 3. The crawler is only closed at the .
   is the simplest pattern if your workload is moderate (dozens to a few hundred URLs).

```
 asyncio
 typing
 crawl4ai  AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
 crawl4ai.markdown_generation_strategy  DefaultMarkdownGenerator
  ():
  ("\n=== Sequential Crawling with Session Reuse ===")
  browser_config = BrowserConfig(
    headless=,
    # For better performance in Docker or low-memory environments:
    extra_args=[, , ],
  )
  crawl_config = CrawlerRunConfig(
    markdown_generator=DefaultMarkdownGenerator()
  )
  # Create the crawler (opens the browser)
  crawler = AsyncWebCrawler(config=browser_config)
   crawler.start()
  :
    session_id =  # Reuse the same session across all URLs
     url  urls:
      result =  crawler.arun(
        url=url,
        config=crawl_config,
        session_id=session_id
      )
       result.success:
        ()
        # E.g. check markdown length
        ()
      :
        ()
  :
    # After all URLs are done, close the crawler (and the browser)
     crawler.close()
  ():
  urls = [
    ,
    ,

  ]
   crawl_sequential(urls)
 __name__ == :
  asyncio.run(main())

```

- If the site requires login, you can log in once in context and preserve auth across all URLs.

## 3. Parallel Crawling with Browser Reuse

To speed up crawling further, you can crawl multiple URLs in (batches or a concurrency limit). The crawler still uses browser, but spawns different sessions (or the same, depending on your logic) for each task.
For this example make sure to install the package.
Then you can run the following code:

```
 os
 sys
 psutil
 asyncio
__location__ = os.path.dirname(os.path.abspath(__file__))
__output__ = os.path.join(__location__, )
# Append parent directory to system path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
 typing
 crawl4ai  AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
  ():
  ("\n=== Parallel Crawling with Browser Reuse + Memory Check ===")
  # We'll keep track of peak memory usage across all tasks
  peak_memory =
  process = psutil.Process(os.getpid())
   ():
     peak_memory
    current_mem = process.memory_info().rss
     current_mem > peak_memory:
      peak_memory = current_mem
    (f" Current Memory:  MB, Peak:  MB")

  browser_config = BrowserConfig(
    headless=,
    verbose=,
    extra_args=[, , ],
  )
  crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
  # Create the crawler instance
  crawler = AsyncWebCrawler(config=browser_config)
   crawler.start()
  :
    # We'll chunk the URLs in batches of 'max_concurrent'
    success_count =
    fail_count =
     i  (, (urls), max_concurrent):
      batch = urls[i : i + max_concurrent]
      tasks = []
       j, url  (batch):
        # Unique session_id per concurrent sub-task
        session_id =
        task = crawler.arun(url=url, config=crawl_config, session_id=session_id)
        tasks.append(task)
      # Check memory usage prior to launching tasks
      log_memory(prefix=)

      results =  asyncio.gather(*tasks, return_exceptions=)
      # Check memory usage after tasks complete
      log_memory(prefix=)

       url, result  (batch, results):
         (result, Exception):
          ()
          fail_count +=
         result.success:
          success_count +=
        :
          fail_count +=
    ()
    ()
    ()
  :
    ()
     crawler.close()

    log_memory(prefix=)
    (f"\nPeak memory usage (MB): ")
  ():
  urls = [
    ,
    ,
    ,

  ]
   crawl_parallel(urls, max_concurrent=)
 __name__ == :
  asyncio.run(main())

```

- We the same instance for all parallel tasks, launching browser.
- Each parallel sub-task might get its own so they don’t share cookies/localStorage (unless that’s desired).
- We limit concurrency to or 3 to avoid saturating CPU/memory.

1. - , can help in Docker or restricted environments. - avoids using which can be small on some systems.
2. - If your site requires a login or you want to maintain local data across URLs, share the . - If you want isolation (each URL fresh), create unique sessions.
3. - If you have URLs (like thousands), you can do parallel crawling in chunks (like ). - Use for a built-in approach if you prefer, but the example above is often more flexible.
4. - If your pages share many resources or you’re re-crawling the same domain repeatedly, consider setting in . - If you need fresh data each time, keep .
5. - You can set up global hooks for each crawler (like to block images) or per-run if you want. - Keep them consistent if you’re reusing sessions.

- - multiple calls to is far more efficient than launching a new crawler per URL.
- approach with a shared session is simple and memory-friendly for moderate sets of URLs.
- approach can speed up large crawls by concurrency, but keep concurrency balanced to avoid overhead.
- Close the crawler once at the end, ensuring the browser is only opened/closed once.

For even more advanced memory optimizations or dynamic concurrency patterns, see future sections on hooking or distributed crawling. The patterns above suffice for the majority of multi-URL scenarios—**giving you speed, simplicity, and minimal resource usage**. Enjoy your optimized crawling!
