Session management in Crawl4AI is a powerful feature that allows you to maintain state across multiple requests, making it particularly suitable for handling complex multi-step crawling tasks. It enables you to reuse the same browser tab (or page object) across sequential actions and crawls, which is beneficial for:
  * **Performing JavaScript actions before and after crawling.**
  * **Executing multiple sequential crawls faster** without needing to reopen tabs or allocate memory repeatedly.


This feature is designed for sequential workflows and is not suitable for parallel operations.
Use and to maintain state with a :
```
 crawl4ai.async_configs import BrowserConfig,  = 
  
  config1 = CrawlerRunConfig(
    url=, session_id=session_id
  )
  config2 = CrawlerRunConfig(
    url=, session_id=session_id
  )
  
  result1 =  crawler.arun(config=config1)
  # Subsequent request using the same session
  result2 =  crawler.arun(config=config2)
  # Clean up when done
   crawler.crawler_strategy.kill_session(session_id)

```

Here's an example of crawling GitHub commits across multiple pages while preserving session state:
```
 crawl4ai.async_configs  CrawlerRunConfig
 crawl4ai.extraction_strategy  JsonCssExtractionStrategy
 crawl4ai.cache_context  CacheMode
  ():
    AsyncWebCrawler()  crawler:
    session_id = 
    url = 
    all_commits = []
    
    schema = {
      : ,
      : ,
      : [{
        : , : , : 
      }],
    }
    extraction_strategy = JsonCssExtractionStrategy(schema)
    # JavaScript and wait configurations
    js_next_page = 
    wait_for = """() => document.querySelectorAll('li.Box-sc-g0xbh4-0').length > 0"""
    
     page  ():
      config = CrawlerRunConfig(
        url=url,
        session_id=session_id,
        extraction_strategy=extraction_strategy,
        js_code=js_next_page  page >   ,
        wait_for=wait_for  page >   ,
        js_only=page > ,
        cache_mode=CacheMode.BYPASS
      )
      result =  crawler.arun(config=config)
       result.success:
        commits = json.loads(result.extracted_content)
        all_commits.extend(commits)
        ()
    
     crawler.crawler_strategy.kill_session(session_id)
     all_commits

```

## Example 1: Basic Session-Based Crawling
A simple example using session-based crawling:
```
 asyncio
 crawl4ai.async_configs  BrowserConfig, CrawlerRunConfig
 crawl4ai.cache_context  CacheMode
  ():
    AsyncWebCrawler()  crawler:
    session_id = 
    url = 
     page  ():
      config = CrawlerRunConfig(
        url=url,
        session_id=session_id,
        js_code=  page >   ,
        css_selector=,
        cache_mode=CacheMode.BYPASS
      )
      result =  crawler.arun(config=config)
      ()
     crawler.crawler_strategy.kill_session(session_id)
asyncio.run(basic_session_crawl())

```

This example shows: 1. Reusing the same across multiple requests. 2. Executing JavaScript to load more content dynamically. 3. Properly closing the session to free resources.
## Advanced Technique 1: Custom Execution Hooks
> Warning: You might feel confused by the end of the next few examples 😅, so make sure you are comfortable with the order of the parts before you start this.
Use custom hooks to handle complex scenarios, such as waiting for content to load dynamically:
```
  ():
  first_commit = 
    ():
     first_commit
    :
       :
         page.wait_for_selector()
        commit =  page.query_selector()
        commit =  commit.evaluate().strip()
         commit  commit != first_commit:
          first_commit = commit
          
         asyncio.sleep()
     Exception  e:
      (f"Warning: New content didn't appear: ")
    AsyncWebCrawler()  crawler:
    session_id = 
    url = 
    crawler.crawler_strategy.set_hook(, on_execution_started)
    js_next_page = 
     page  ():
      config = CrawlerRunConfig(
        url=url,
        session_id=session_id,
        js_code=js_next_page  page >   ,
        css_selector=,
        js_only=page > ,
        cache_mode=CacheMode.BYPASS
      )
      result =  crawler.arun(config=config)
      ()
     crawler.crawler_strategy.kill_session(session_id)
asyncio.run(advanced_session_crawl_with_hooks())

```

This technique ensures new content loads before the next action.
## Advanced Technique 2: Integrated JavaScript Execution and Waiting
Combine JavaScript execution and waiting logic for concise handling of dynamic content:
```
  ():
    AsyncWebCrawler()  crawler:
    session_id = 
    url = 
    js_next_page_and_wait = """
    (async () => {
      const getCurrentCommit = () => document.querySelector('li.commit-item h4').textContent.trim();
      const initialCommit = getCurrentCommit();
      document.querySelector('a.pagination-next').click();
      while (getCurrentCommit() === initialCommit) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    })();
    """
     page  ():
      config = CrawlerRunConfig(
        url=url,
        session_id=session_id,
        js_code=js_next_page_and_wait  page >   ,
        css_selector=,
        js_only=page > ,
        cache_mode=CacheMode.BYPASS
      )
      result =  crawler.arun(config=config)
      ()
     crawler.crawler_strategy.kill_session(session_id)
asyncio.run(integrated_js_and_wait_crawl())

```

#### Common Use Cases for Sessions
1. : Login and interact with secured pages.
2. : Navigate through multiple pages.
3. : Fill forms, submit, and process results.
4. : Complete workflows that span multiple actions.
5. : Handle JavaScript-rendered or event-triggered content.
