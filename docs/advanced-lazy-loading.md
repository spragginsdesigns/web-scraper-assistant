Many websites now load images as you scroll. If you need to ensure they appear in your final crawl (and in ), consider:
1. – Wait for images to fully load. 2. – Force the crawler to scroll the entire page, triggering lazy loads. 3. – Add small delays between scroll steps. 
: If the site requires multiple “Load More” triggers or complex interactions, see the .
### Example: Ensuring Lazy Images Appear
```
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
 crawl4ai.async_configs  CacheMode
  ():
  config = CrawlerRunConfig(
    # Force the crawler to wait until images are fully loaded
    wait_for_images=,
    # Option 1: If you want to automatically scroll the page to load images
    scan_full_page=, # Tells the crawler to try scrolling the entire page
    scroll_delay=,   # Delay (seconds) between scroll steps
    # Option 2: If the site uses a 'Load More' or JS triggers for images,
    # you can also specify js_code or wait_for logic here.
    cache_mode=CacheMode.BYPASS,
    verbose=
  )
    AsyncWebCrawler(config=BrowserConfig(headless=))  crawler:
    result =  crawler.arun(, config=config)
     result.success:
      images = result.media.get(, [])
      (, (images))
       i, img  (images[:]):
        ()
    :
      (, result.error_message)
 __name__ == :
  asyncio.run(main())

```

  * The crawler tries to ensure images have finished loading before finalizing the HTML. 
  * Tells the crawler to attempt scrolling from top to bottom. Each scroll step helps trigger lazy loading. 
  * Pause half a second between each scroll step. Helps the site load images before continuing.


  * : If images appear only when the user scrolls into view, + helps the crawler see them. 
  * : If a page is extremely long, be mindful that scanning the entire page can be slow. Adjust or the max scroll steps as needed.


## Combining with Other Link & Media Filters
You can still combine logic with the usual , , or link filtration:
```
config  CrawlerRunConfig
  wait_for_images,
  scan_full_page,
  scroll_delay,
  # Filter out external images if you only want local ones
  exclude_external_images,
  # Exclude certain domains for links
  exclude_domains,


```

This approach ensures you see images from the main domain while ignoring external ones, and the crawler physically scrolls the entire page so that lazy-loading triggers.
1. - Setting on extremely long or infinite-scroll pages can be resource-intensive. - Consider using or specialized logic to load specific sections or “Load More” triggers repeatedly.
2. - Some sites load images in batches as you scroll. If you’re missing images, increase your or call multiple partial scrolls in a loop with JS code or hooks.
3. - If the site has a placeholder that only changes to a real image after a certain event, you might do or a custom JS .
4. - If is enabled, repeated crawls might skip some network fetches. If you suspect caching is missing new images, set for fresh fetches.
With support, , and settings, you can capture the entire gallery or feed of images you expect—even if the site only loads them as the user scrolls. Combine these with the standard media filtering and domain exclusion for a complete link & media handling strategy.
