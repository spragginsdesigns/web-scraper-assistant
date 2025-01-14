> : We’re developing a new that uses a sophisticated algorithm to dynamically manage multi-URL crawling, optimizing for speed and memory usage. The approaches in this document remain fully valid, but keep an eye on ’s upcoming releases for this powerful feature! Follow on X and check the changelogs to stay updated.
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

  * If the site requires login, you can log in once in context and preserve auth across all URLs.


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

  * We the same instance for all parallel tasks, launching browser. 
  * Each parallel sub-task might get its own so they don’t share cookies/localStorage (unless that’s desired). 
  * We limit concurrency to or 3 to avoid saturating CPU/memory.


1. - , can help in Docker or restricted environments. - avoids using which can be small on some systems.
2. - If your site requires a login or you want to maintain local data across URLs, share the . - If you want isolation (each URL fresh), create unique sessions.
3. - If you have URLs (like thousands), you can do parallel crawling in chunks (like ). - Use for a built-in approach if you prefer, but the example above is often more flexible.
4. - If your pages share many resources or you’re re-crawling the same domain repeatedly, consider setting in . - If you need fresh data each time, keep .
5. - You can set up global hooks for each crawler (like to block images) or per-run if you want. - Keep them consistent if you’re reusing sessions.
  * + multiple calls to is far more efficient than launching a new crawler per URL. 
  * approach with a shared session is simple and memory-friendly for moderate sets of URLs. 
  * approach can speed up large crawls by concurrency, but keep concurrency balanced to avoid overhead. 
  * Close the crawler once at the end, ensuring the browser is only opened/closed once.


For even more advanced memory optimizations or dynamic concurrency patterns, see future sections on hooking or distributed crawling. The patterns above suffice for the majority of multi-URL scenarios—**giving you speed, simplicity, and minimal resource usage**. Enjoy your optimized crawling!
