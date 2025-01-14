# Crawl4AI Cache System and Migration Guide
Starting from version 0.5.0, Crawl4AI introduces a new caching system that replaces the old boolean flags with a more intuitive enum. This change simplifies cache control and makes the behavior more predictable.
The old system used multiple boolean flags: - : Skip cache entirely - : Disable all caching - : Don't read from cache - : Don't write to cache
The new system uses a single enum: - : Normal caching (read/write) - : No caching at all - : Only read from cache - : Only write to cache - : Skip cache for this operation
```
 asyncio
 crawl4ai  AsyncWebCrawler
  ():
    AsyncWebCrawler(verbose=)  crawler:
    result =  crawler.arun(
      url=,
      bypass_cache= 
    )
    ((result.markdown))
  ():
   use_proxy()
 __name__ == :
  asyncio.run(main())

```

```
 asyncio
 crawl4ai  AsyncWebCrawler, CacheMode
 crawl4ai.async_configs  CrawlerRunConfig
  ():
  # Use CacheMode in CrawlerRunConfig
  config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS) 
    AsyncWebCrawler(verbose=)  crawler:
    result =  crawler.arun(
      url=,
      config=config # Pass the configuration object
    )
    ((result.markdown))
  ():
   use_proxy()
 __name__ == :
  asyncio.run(main())

```

