# Hooks & Auth in AsyncWebCrawler
Crawl4AI’s let you customize the crawler at specific points in the pipeline:
1. – After browser creation. 2. – After a new context & page are created. 3. – Just before navigating to a page. 4. – Right after navigation completes. 5. – Whenever the user agent changes. 6. – Once custom JavaScript execution begins. 7. – Just before the crawler retrieves final HTML. 8. – Right before returning the HTML content.
: Avoid heavy tasks in since you don’t yet have a page context. If you need to , do so in .
> note "Important Hook Usage Warning" : Do not manipulate page objects in the wrong hook or at the wrong time, as it can crash the pipeline or produce incorrect results. A common mistake is attempting to handle authentication prematurely—such as creating or closing pages in . 
> **Use the Right Hook for Auth** : If you need to log in or set tokens, use . This ensures you have a valid page/context to work with, without disrupting the main crawling flow.
> : For robust auth, consider identity-based crawling (or passing a session ID) to preserve state. Run your initial login steps in a separate, well-defined process, then feed that session to your main crawl—rather than shoehorning complex authentication into early hooks. Check out for more details.
> : Overwriting or removing elements in the wrong hook can compromise the final crawl. Keep hooks focused on smaller tasks (like route filters, custom headers), and let your main logic (crawling, data extraction) proceed normally.
Below is an example demonstration.
## Example: Using Hooks in AsyncWebCrawler
```
 asyncio
 json
 crawl4ai  AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
 playwright.async_api  Page, BrowserContext
  ():
  ("🔗 Hooks Example: Demonstrating recommended usage")
  # 1) Configure the browser
  browser_config = BrowserConfig(
    headless=,
    verbose=
  )
  # 2) Configure the crawler run
  crawler_run_config = CrawlerRunConfig(
    js_code=,
    wait_for=,
    cache_mode=CacheMode.BYPASS
  )
  # 3) Create the crawler instance
  crawler = AsyncWebCrawler(config=browser_config)
  
  
  
    ():
    # Called once the browser instance is created (but no pages or contexts yet)
    ("[HOOK] on_browser_created - Browser created successfully!")
    # Typically, do minimal setup here if needed
     browser
    (page: Page, context: BrowserContext, **kwargs):
    # Called right after a new page + context are created (ideal for auth or route config).
    ("[HOOK] on_page_context_created - Setting up page & context.")
    # Example 1: Route filtering (e.g., block images)
      ():
       route.request.resource_type == :
        ()
         route.abort()
      :
         route.continue_()
     context.route(, route_filter)
    # Example 2: (Optional) Simulate a login scenario
    # (We do NOT create or close pages here, just do quick steps if needed)
    
    # e.g., await page.fill("input[name='username']", "testuser")
    # e.g., await page.fill("input[name='password']", "password123")
    
    
    
    
    # Example 3: Adjust the viewport
     page.set_viewport_size({: , : })
     page
    (
    page: Page, context: BrowserContext, url: , **kwargs
  ):
    # Called before navigating to each URL.
    (f"[HOOK] before_goto - About to navigate: ")
    # e.g., inject custom headers
     page.set_extra_http_headers({
      : 
    })
     page
    (
    page: Page, context: BrowserContext, 
    url: , response, **kwargs
  ):
    # Called after navigation completes.
    (f"[HOOK] after_goto - Successfully loaded: ")
    # e.g., wait for a certain element if we want to verify
    :
       page.wait_for_selector(, timeout=)
      ()
    :
      ("[HOOK] .content not found, continuing anyway.")
     page
    (
    page: Page, context: BrowserContext, 
    user_agent: , **kwargs
  ):
    # Called whenever the user agent updates.
    (f"[HOOK] on_user_agent_updated - New user agent: ")
     page
    (page: Page, context: BrowserContext, **kwargs):
    # Called after custom JavaScript execution begins.
    ("[HOOK] on_execution_started - JS code is running!")
     page
    (page: Page, context: BrowserContext, **kwargs):
    # Called before final HTML retrieval.
    ("[HOOK] before_retrieve_html - We can do final actions")
    
     page.evaluate()
     page
    (
    page: Page, context: BrowserContext, html: , **kwargs
  ):
    # Called just before returning the HTML in the result.
    (f"[HOOK] before_return_html - HTML length: ")
     page
  
  
  
  crawler.crawler_strategy.set_hook(, on_browser_created)
  crawler.crawler_strategy.set_hook(
    , on_page_context_created
  )
  crawler.crawler_strategy.set_hook(, before_goto)
  crawler.crawler_strategy.set_hook(, after_goto)
  crawler.crawler_strategy.set_hook(
    , on_user_agent_updated
  )
  crawler.crawler_strategy.set_hook(
    , on_execution_started
  )
  crawler.crawler_strategy.set_hook(
    , before_retrieve_html
  )
  crawler.crawler_strategy.set_hook(
    , before_return_html
  )
   crawler.start()
  # 4) Run the crawler on an example page
  url = 
  result =  crawler.arun(url, config=crawler_run_config)
   result.success:
    (, result.url)
    (, (result.html))
  :
    (, result.error_message)
   crawler.close()
 __name__ == :
  asyncio.run(main())

```

1. : - Browser is up, but pages or contexts yet. - Light setup only—don’t try to open or close pages here (that belongs in ).
2. : - Perfect for advanced or route blocking. - You have a + ready but haven’t navigated to the target URL yet.
3. : - Right before navigation. Typically used for setting or logging the target URL.
4. : - After page navigation is done. Good place for verifying content or waiting on essential elements. 
5. : - Whenever the user agent changes (for stealth or different UA modes).
6. : - If you set or run custom scripts, this runs once your JS is about to start.
7. : - Just before the final HTML snapshot is taken. Often you do a final scroll or lazy-load triggers here.
8. : - The last hook before returning HTML to the . Good for logging HTML length or minor modifications.
: Use if you need to:
  * Navigate to a login page or fill forms
  * Set cookies or localStorage tokens
  * Block resource routes to avoid ads


This ensures the newly created context is under your control navigates to the main URL.
  * : If you want multiple calls to reuse a single session, pass in your . Hooks remain the same. 
  * : Hooks can slow down crawling if they do heavy tasks. Keep them concise. 
  * : If a hook fails, the overall crawl might fail. Catch exceptions or handle them gracefully. 
  * : If you run , each URL triggers these hooks in parallel. Ensure your hooks are thread/async-safe.



Follow the recommended usage: - or advanced tasks in - or logs in / - or final checks in / 
