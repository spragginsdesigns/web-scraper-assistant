This guide covers the basics of web crawling with Crawl4AI. You'll learn how to set up a crawler, make your first request, and understand the response.
Set up a simple crawl using and :
```
 asyncio
 crawl4ai  AsyncWebCrawler
 crawl4ai.async_configs  BrowserConfig, CrawlerRunConfig
  ():
  browser_config = BrowserConfig() 
  run_config = CrawlerRunConfig()  # Default crawl run configuration
    AsyncWebCrawler(config=browser_config)  crawler:
    result =  crawler.arun(
      url=,
      config=run_config
    )
    (result.markdown) # Print clean markdown content
 __name__ == :
  asyncio.run(main())

```

The method returns a object with several useful properties. Here's a quick overview (see for complete details):
```
result =  crawler.arun(
  url=,
  config=CrawlerRunConfig(fit_markdown=)
)

(result.html)     
(result.cleaned_html) 
(result.markdown)   
(result.fit_markdown) # Most relevant content in markdown

(result.success)   # True if crawl succeeded
(result.status_code) # HTTP status code (e.g., 200, 404)
# Access extracted media and links
(result.media)    # Dictionary of found media (images, videos, audio)
(result.links)    # Dictionary of internal and external links

```

```
run_config = CrawlerRunConfig(
  word_count_threshold=,    # Minimum words per content block
  exclude_external_links=,  
  remove_overlay_elements=,  
  process_iframes=      
)
result =  crawler.arun(
  url=,
  config=run_config
)

```

Always check if the crawl was successful:
```
run_config = CrawlerRunConfig()
result =  crawler.arun(url=, config=run_config)
  result.success:
  ()
  ()

```

```
browser_config = BrowserConfig(verbose=True)
 = CrawlerRunConfig()
  result =  crawler.arun(url=, config=run_config)

```

Here's a more comprehensive example demonstrating common usage patterns:
```
 asyncio
 crawl4ai  AsyncWebCrawler
 crawl4ai.async_configs  BrowserConfig, CrawlerRunConfig, CacheMode
  ():
  browser_config = BrowserConfig(verbose=)
  run_config = CrawlerRunConfig(
    
    word_count_threshold=,
    excluded_tags=[, ],
    exclude_external_links=,
    
    process_iframes=,
    remove_overlay_elements=,
    
    cache_mode=CacheMode.ENABLED # Use cache if available
  )
    AsyncWebCrawler(config=browser_config)  crawler:
    result =  crawler.arun(
      url=,
      config=run_config
    )
     result.success:
      
      (, result.markdown[:]) 
      
       image  result.media[]:
        ()
      
       link  result.links[]:
        ()
    :
      ()
 __name__ == :
  asyncio.run(main())

```

