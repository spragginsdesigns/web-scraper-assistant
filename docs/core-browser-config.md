# Browser & Crawler Configuration (Quick Overview)
Crawl4AI’s flexibility stems from two key classes:
1. – Dictates the browser is launched and behaves (e.g., headless or visible, proxy, user agent). 2. – Dictates each operates (e.g., caching, extraction, timeouts, JavaScript code to run, etc.).
In most examples, you create for the entire crawler session, then pass a or re-used whenever you call . This tutorial shows the most commonly used parameters. If you need advanced or rarely used fields, see the .
```
 :
   (
    browser_type=,
    headless=,
    proxy_config=,
    viewport_width=,
    viewport_height=,
    verbose=,
    use_persistent_context=,
    user_data_dir=,
    cookies=,
    headers=,
    user_agent=,
    text_mode=,
    light_mode=,
    extra_args=,
    # ... other advanced parameters omitted here
  ):
    ...

```

1. - Options: , , or . - Defaults to . - If you need a different engine, specify it here.
2. - : Runs the browser in headless mode (invisible browser). - : Runs the browser in visible mode, which helps with debugging.
3. - A dictionary with fields like: 
- Leave as if a proxy is not required. 
4. : - The initial window size. - Some sites behave differently with smaller or bigger viewports.
5. : - If , prints extra logs. - Handy for debugging.
6. : - If , uses a browser profile, storing cookies/local storage across runs. - Typically also set to point to a folder.
7. & : - If you want to start with specific cookies or add universal HTTP headers, set them here. - E.g. `cookies=[{"name": "session", "value": "abc123", "domain": "example.com"}]`.
8. : - Custom User-Agent string. If , a default is used. - You can also set for randomization (if you want to fight bot detection).
9. & : - disables images, possibly speeding up text-only crawls. - turns off certain background features for performance. 
10. : - Additional flags for the underlying browser. - E.g. .
```
 crawl4ai  AsyncWebCrawler, BrowserConfig
browser_conf = BrowserConfig(
  browser_type=,
  headless=,
  text_mode=
)
  AsyncWebCrawler(config=browser_conf)  crawler:
  result =  crawler.arun()
  (result.markdown[:])

```

```
 :
   (
    word_count_threshold=,
    extraction_strategy=,
    markdown_generator=,
    cache_mode=,
    js_code=,
    wait_for=,
    screenshot=,
    pdf=,
    verbose=,
    # ... other advanced parameters omitted
  ):
    ...

```

1. : - The minimum word count before a block is considered. - If your site has lots of short paragraphs or items, you can lower it.
2. : - Where you plug in JSON-based extraction (CSS, LLM, etc.). - If , no structured extraction is done (only raw/cleaned HTML + markdown).
3. : - E.g., , controlling how HTML→Markdown conversion is done. - If , a default approach is used.
4. : - Controls caching behavior (, , , etc.). - If , defaults to some level of caching or you can specify .
5. : - A string or list of JS strings to execute. - Great for “Load More” buttons or user interactions. 
6. : - A CSS or JS expression to wait for before extracting content. - Common usage: or `wait_for="js:() => window.loaded === true"`.
7. & : - If , captures a screenshot or PDF after the page is fully loaded. - The results go to (base64) or (bytes).
8. : - Logs additional runtime details. - Overlaps with the browser’s verbosity if also set to in .
```
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
crawl_conf = CrawlerRunConfig(
  js_code=,
  wait_for=,
  screenshot=
)
  AsyncWebCrawler()  crawler:
  result =  crawler.arun(url=, config=crawl_conf)
  (result.screenshot[:]) 

```

## 3. Putting It All Together
In a typical scenario, you define for your crawler session, then create depending on each call’s needs:
```
 asyncio
 crawl4ai  AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
 crawl4ai.extraction_strategy  JsonCssExtractionStrategy
  ():
  # 1) Browser config: headless, bigger viewport, no proxy
  browser_conf = BrowserConfig(
    headless=,
    viewport_width=,
    viewport_height=
  )
  # 2) Example extraction strategy
  schema = {
    : ,
    : ,
    : [
      {: , : , : },
      {: , : , : , : }
    ]
  }
  extraction = JsonCssExtractionStrategy(schema)
  # 3) Crawler run config: skip cache, use extraction
  run_conf = CrawlerRunConfig(
    extraction_strategy=extraction,
    cache_mode=CacheMode.BYPASS
  )
    AsyncWebCrawler(config=browser_conf)  crawler:
    # 4) Execute the crawl
    result =  crawler.arun(url=, config=run_conf)
     result.success:
      (, result.extracted_content)
    :
      (, result.error_message)
 __name__ == :
  asyncio.run(main())

```

For a of available parameters (including advanced ones), see:
You can explore topics like:
  * (Inject JavaScript or handle login forms). 
  * (Re-use pages, preserve state across multiple calls). 
  * or (Fight bot detection by simulating user behavior). 
  * (Fine-tune read/write cache modes). 


and give you straightforward ways to define:
  * browser to launch, how it should run, and any proxy or user agent needs. 
  * each crawl should behave—caching, timeouts, JavaScript code, extraction strategies, etc.


Use them together for code, and when you need more specialized behavior, check out the advanced parameters in the . Happy crawling!
