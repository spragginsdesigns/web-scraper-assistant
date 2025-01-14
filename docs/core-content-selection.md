Crawl4AI provides multiple ways to , , and the content from your crawls. Whether you need to target a specific CSS region, exclude entire tags, filter out external links, or remove certain domains and images, offers a wide range of parameters.
Below, we show how to configure these parameters and combine them for precise control.
A straightforward way to your crawl results to a certain region of the page is in :
```
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
  ():
  config = CrawlerRunConfig(
    # e.g., first 30 items from Hacker News
    css_selector= 
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(
      url=, 
      config=config
    )
    (, (result.cleaned_html))
 __name__ == :
  asyncio.run(main())

```

: Only elements matching that selector remain in .
## 2. Content Filtering & Exclusions
```
config = CrawlerRunConfig(
  
  word_count_threshold=,    # Minimum words per block
  
  excluded_tags=[, , , ],
  
  exclude_external_links=,  
  exclude_social_media_links=,
  
  exclude_domains=[, ],  
  exclude_social_media_domains=[, ],
  
  exclude_external_images=
)

```

  * : Ignores text blocks under X words. Helps skip trivial blocks like short nav or disclaimers. 
  * : Removes entire tags (, , , etc.). 
  * : Strips out external links and may remove them from . 
  * : Removes links pointing to known social media domains. 
  * : A custom list of domains to block if discovered in links. 
  * : A curated list (override or add to it) for social media sites. 
  * : Discards images not hosted on the same domain as the main page (or its subdomains).


By default in case you set , the following social media domains are excluded: 
```
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig, CacheMode
  ():
  config = CrawlerRunConfig(
    css_selector=, 
    word_count_threshold=,
    excluded_tags=[, ],
    exclude_external_links=,
    exclude_social_media_links=,
    exclude_domains=[, ],
    exclude_external_images=,
    cache_mode=CacheMode.BYPASS
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(url=, config=config)
    (, (result.cleaned_html))
 __name__ == :
  asyncio.run(main())

```

: If these parameters remove too much, reduce or disable them accordingly.
Some sites embed content in tags. If you want that inline: 
```
config  CrawlerRunConfig(
  #  iframe content  the  output
  process_iframes,  
  remove_overlay_elements
)

```

```
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
  ():
  config = CrawlerRunConfig(
    process_iframes=,
    remove_overlay_elements=
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(
      url=, 
      config=config
    )
    (, (result.cleaned_html))
 __name__ == :
  asyncio.run(main())

```

You can combine content selection with a more advanced extraction strategy. For instance, a or extraction strategy can run on the filtered HTML.
```
 asyncio
 json
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig, CacheMode
 crawl4ai.extraction_strategy  JsonCssExtractionStrategy
  ():
  # Minimal schema for repeated items
  schema = {
    : ,
    : ,
    : [
      {: , : , : },
      {
        : , 
        : , 
        : , 
        : 
      }
    ]
  }
  config = CrawlerRunConfig(
    
    excluded_tags=[, ],
    exclude_domains=[],
    # CSS selection or entire page
    css_selector=,
    # No caching for demonstration
    cache_mode=CacheMode.BYPASS,
    
    extraction_strategy=JsonCssExtractionStrategy(schema)
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(
      url=, 
      config=config
    )
    data = json.loads(result.extracted_content)
    (, data[:]) 
 __name__ == :
  asyncio.run(main())

```

```
 asyncio
 json
 pydantic  BaseModel, Field
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
 crawl4ai.extraction_strategy  LLMExtractionStrategy
 ():
  headline: 
  summary: 
  ():
  llm_strategy = LLMExtractionStrategy(
    provider=,
    api_token=,
    schema=ArticleData.schema(),
    extraction_type=,
    instruction="Extract 'headline' and a short 'summary' from the content."
  )
  config = CrawlerRunConfig(
    exclude_external_links=,
    word_count_threshold=,
    extraction_strategy=llm_strategy
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(url=, config=config)
    article = json.loads(result.extracted_content)
    (article)
 __name__ == :
  asyncio.run(main())

```

  * Filters out external links (). 
  * Ignores very short text blocks (). 
  * Passes the final HTML to your LLM strategy for an AI-driven parse.


Below is a short function that unifies , logic, and a pattern-based extraction, demonstrating how you can fine-tune your final data:
```
 asyncio
 json
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig, CacheMode
 crawl4ai.extraction_strategy  JsonCssExtractionStrategy
  ():
  schema = {
    : ,
    : ,
    : [
      {: , : , : },
      {: , : , : },
      {
        : ,
        : ,
        : [
          {: , : , : },
          {: , : , : }
        ]
      }
    ]
  }
  config = CrawlerRunConfig(
    
    css_selector=,
    
    word_count_threshold=,
    excluded_tags=[, ], 
    exclude_external_links=,
    exclude_domains=[],
    exclude_external_images=,
    
    extraction_strategy=JsonCssExtractionStrategy(schema),
    cache_mode=CacheMode.BYPASS
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(url=url, config=config)
      result.success:
      ()
       
     json.loads(result.extracted_content)
  ():
  articles =  extract_main_articles()
   articles:
    (, articles[:]) 
 __name__ == :
  asyncio.run(main())

```

: - scoping with . - Multiple parameters to remove domains, external images, etc. - A to parse repeated article blocks.
By mixing scoping, parameters, and advanced , you can precisely which data to keep. Key parameters in for content selection include:
1. – Basic scoping to an element or region. 2. – Skip short blocks. 3. – Remove entire HTML tags. 4. , , – Filter out unwanted links or domains. 5. – Remove images from external sources. 6. – Merge iframe content if needed. 
Combine these with structured extraction (CSS, LLM-based, or others) to build powerful crawls that yield exactly the content you want, from raw or cleaned HTML up to sophisticated JSON structures. For more detail, see . Enjoy curating your data to the max!
