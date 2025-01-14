# Prefix-Based Input Handling in Crawl4AI
This guide will walk you through using the Crawl4AI library to crawl web pages, local HTML files, and raw HTML strings. We'll demonstrate these capabilities using a Wikipedia page as an example.
To crawl a live web page, provide the URL starting with or , using a object:
```
 asyncio
 crawl4ai  AsyncWebCrawler
 crawl4ai.async_configs  CrawlerRunConfig
  ():
  config = CrawlerRunConfig(bypass_cache=)
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(
      url=, 
      config=config
    )
     result.success:
      ()
      (result.markdown)
    :
      ()
asyncio.run(crawl_web())

```

## Crawling a Local HTML File
To crawl a local HTML file, prefix the file path with .
```
 asyncio
 crawl4ai  AsyncWebCrawler
 crawl4ai.async_configs  CrawlerRunConfig
  ():
  local_file_path =  # Replace with your file path
  file_url = 
  config = CrawlerRunConfig(bypass_cache=)
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(url=file_url, config=config)
     result.success:
      ("Markdown Content from Local File:")
      (result.markdown)
    :
      (f"Failed to crawl local file: ")
asyncio.run(crawl_local_file())

```

To crawl raw HTML content, prefix the HTML string with .
```
 asyncio
 crawl4ai  AsyncWebCrawler
 crawl4ai.async_configs  CrawlerRunConfig
  ():
  raw_html = 
  raw_html_url = 
  config = CrawlerRunConfig(bypass_cache=)
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(url=raw_html_url, config=config)
     result.success:
      ("Markdown Content from Raw HTML:")
      (result.markdown)
    :
      (f"Failed to crawl raw HTML: ")
asyncio.run(crawl_raw_html())

```

Below is a comprehensive script that:
  1. Crawls the Wikipedia page for "Apple."
  2. Saves the HTML content to a local file ().
  3. Crawls the local HTML file and verifies the markdown length matches the original crawl.
  4. Crawls the raw HTML content from the saved file and verifies consistency.


```
 os
 sys
 asyncio
 pathlib  Path
 crawl4ai  AsyncWebCrawler
 crawl4ai.async_configs  CrawlerRunConfig
  ():
  wikipedia_url = 
  script_dir = Path(__file__).parent
  html_file_path = script_dir / 
    AsyncWebCrawler()  crawler:
    # Step 1: Crawl the Web URL
    ("\n=== Step 1: Crawling the Wikipedia URL ===")
    web_config = CrawlerRunConfig(bypass_cache=)
    result =  crawler.arun(url=wikipedia_url, config=web_config)
      result.success:
      ()
      
     (html_file_path, , encoding=)  f:
      f.write(result.html)
    web_crawl_length = (result.markdown)
    (f"Length of markdown from web crawl: \n")
    # Step 2: Crawl from the Local HTML File
    ("=== Step 2: Crawling from the Local HTML File ===")
    file_url = 
    file_config = CrawlerRunConfig(bypass_cache=)
    local_result =  crawler.arun(url=file_url, config=file_config)
      local_result.success:
      (f"Failed to crawl local file : ")
      
    local_crawl_length = (local_result.markdown)
     web_crawl_length == local_crawl_length, 
    ("✅ Markdown length matches between web and local file crawl.\n")
    # Step 3: Crawl Using Raw HTML Content
    ("=== Step 3: Crawling Using Raw HTML Content ===")
     (html_file_path, , encoding=)  f:
      raw_html_content = f.read()
    raw_html_url = 
    raw_config = CrawlerRunConfig(bypass_cache=)
    raw_result =  crawler.arun(url=raw_html_url, config=raw_config)
      raw_result.success:
      (f"Failed to crawl raw HTML content: ")
      
    raw_crawl_length = (raw_result.markdown)
     web_crawl_length == raw_crawl_length, 
    ("✅ Markdown length matches between web and raw HTML crawl.\n")
    ()
   html_file_path.exists():
    os.remove(html_file_path)
 __name__ == :
  asyncio.run(main())

```

With the unified parameter and prefix-based handling in , you can seamlessly handle web URLs, local HTML files, and raw HTML content. Use for flexible and consistent configuration in all scenarios.
