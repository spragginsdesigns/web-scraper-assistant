One of Crawl4AI’s features is extracting from websites relying on large language models. By defining a with CSS or XPath selectors, you can extract data instantly—even from complex or nested HTML structures—without the cost, latency, or environmental impact of an LLM.
**Why avoid LLM for basic extractions?**
1. : No API calls or GPU overhead. 2. : LLM inference can be energy-intensive. A well-defined schema is practically carbon-free. 3. : CSS/XPath selectors do exactly what you specify. LLM outputs can vary or hallucinate. 4. : For thousands of pages, schema-based extraction runs quickly and in parallel.
Below, we’ll explore how to craft these schemas and use them with (or if you prefer XPath). We’ll also highlight advanced features like and .
## 1. Intro to Schema-Based Extraction
  1. A that identifies each “container” element on the page (e.g., a product row, a blog post card). 2. describing which CSS/XPath selectors to use for each piece of data you want to capture (text, attribute, HTML block, etc.). 3. or types for repeated or hierarchical structures. 


For example, if you have a list of products, each one might have a name, price, reviews, and “related products.” This approach is faster and more reliable than an LLM for consistent, structured pages.
## 2. Simple Example: Crypto Prices
Let’s begin with a schema-based extraction using the . Below is a snippet that extracts cryptocurrency prices from a site (similar to the legacy Coinbase example). Notice we call any LLM:
```
 json
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig, CacheMode
 crawl4ai.extraction_strategy  JsonCssExtractionStrategy
  ():
  # 1. Define a simple extraction schema
  schema = {
    : ,
    : ,  
    : [
      {
        : ,
        : ,
        : 
      },
      {
        : ,
        : ,
        : 
      }
    ]
  }
  # 2. Create the extraction strategy
  extraction_strategy = JsonCssExtractionStrategy(schema, verbose=)
  # 3. Set up your crawler config (if needed)
  config = CrawlerRunConfig(
    # e.g., pass js_code or wait_for if the page is dynamic
    
    cache_mode = CacheMode.BYPASS,
    extraction_strategy=extraction_strategy,
  )
    AsyncWebCrawler(verbose=)  crawler:
    # 4. Run the crawl and extraction
    result =  crawler.arun(
      url=,
      config=config
    )
      result.success:
      (, result.error_message)
      
    # 5. Parse the extracted JSON
    data = json.loads(result.extracted_content)
    ()
    (json.dumps(data[], indent=)  data  )
asyncio.run(extract_crypto_prices())

```

  * : Tells us where each “item” (crypto row) is. 
  * : Two fields (, ) using simple CSS selectors. 
  * Each field defines a (e.g., , , , , etc.).


No LLM is needed, and the performance is for hundreds or thousands of items.
Below is a short example demonstrating extraction plus the scheme. We’ll pass a directly (no network request) and define the extraction strategy in .
```
 json
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
 crawl4ai.extraction_strategy  JsonXPathExtractionStrategy
  ():
  # 1. Minimal dummy HTML with some repeating rows
  dummy_html = """
  <html>
   <body>
    <div class='crypto-row'>
     <h2 class='coin-name'>Bitcoin</h2>
     <span class='coin-price'>$28,000</span>
    </div>
    <div class='crypto-row'>
     <h2 class='coin-name'>Ethereum</h2>
     <span class='coin-price'>$1,800</span>
    </div>
   </body>
  </html>
  """
  # 2. Define the JSON schema (XPath version)
  schema = {
    : ,
    : ,
    : [
      {
        : ,
        : ,
        : 
      },
      {
        : ,
        : ,
        : 
      }
    ]
  }
  # 3. Place the strategy in the CrawlerRunConfig
  config = CrawlerRunConfig(
    extraction_strategy=JsonXPathExtractionStrategy(schema, verbose=)
  )
  # 4. Use raw:// scheme to pass dummy_html directly
  raw_url = 
    AsyncWebCrawler(verbose=)  crawler:
    result =  crawler.arun(
      url=raw_url,
      config=config
    )
      result.success:
      (, result.error_message)
      
    data = json.loads(result.extracted_content)
    ()
     data:
      (, data[])
asyncio.run(extract_crypto_prices_xpath())

```

1. is used instead of . 2. and each field’s use instead of CSS. 3. lets us pass with no real network request—handy for local testing. 4. Everything (including the extraction strategy) is in . 
That’s how you keep the config self-contained, illustrate usage, and demonstrate the scheme for direct HTML input—all while avoiding the old approach of passing directly to .
## 3. Advanced Schema & Nested Structures
Real sites often have or repeated data—like categories containing products, which themselves have a list of reviews or features. For that, we can define or (and even ) fields.
We have a HTML file on GitHub (example): 
This snippet includes categories, products, features, reviews, and related items. Let’s see how to define a schema that fully captures that structure . 
```
  
   ,
   ,
  # (1) We can define optional baseFields if we want to extract attributes 
  # from the category container
   
     ,  ,  , 
  ,
   
    
       ,
       ,
       
    ,
    
       ,
       ,
       ,  
       
        
           ,
           ,
           
        ,
        
           ,
           ,
           
        ,
        
           ,
           ,
           , 
           
            
               ,
               ,
               
            ,
            
               ,
               ,
               
            
          
        ,
        
           ,
           ,
           ,
           
             ,   
          
        ,
        
           ,
           ,
           ,
           
            
               , 
               , 
               
            ,
            
               , 
               , 
               
            ,
            
               , 
               , 
               
            
          
        ,
        
           ,
           ,
           ,
           
            
               , 
               , 
               
            ,
            
               , 
               , 
               
            
          
        
      
    
  


```

  * means multiple items that are dictionaries or single text fields. 
  * : We can extract from the container element via . For instance, might be . 
  * : We can also define a if we want to lower/upper case, strip whitespace, or even run a custom function.


```
 json
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
 crawl4ai.extraction_strategy  JsonCssExtractionStrategy
ecommerce_schema = {
  # ... the advanced schema from above ...
}
  ():
  strategy = JsonCssExtractionStrategy(ecommerce_schema, verbose=)
  config = CrawlerRunConfig()
    AsyncWebCrawler(verbose=)  crawler:
    result =  crawler.arun(
      url=,
      extraction_strategy=strategy,
      config=config
    )
      result.success:
      (, result.error_message)
      
    # Parse the JSON output
    data = json.loads(result.extracted_content)
    (json.dumps(data, indent=)  data  )
asyncio.run(extract_ecommerce_data())

```

If all goes well, you get a JSON array with each “category,” containing an array of . Each product includes , , , etc. All of that an LLM.
## 4. Why “No LLM” Is Often Better
1. : Schema-based extraction doesn’t guess text. It either finds it or not. 2. : The same schema yields consistent JSON across many pages, so your downstream pipeline can rely on stable keys. 3. : LLM-based extraction can be 10–1000x slower for large-scale crawling. 4. : Adding or updating a field is a matter of adjusting the schema, not re-tuning a model.
**When might you consider an LLM?** Possibly if the site is extremely unstructured or you want AI summarization. But always try a schema approach first for repeated or consistent data patterns.
## 5. Base Element Attributes & Additional Fields
It’s easy to (like , , or ) from your base or nested elements using:
You can define them in (extracted from the main container element) or in each field’s sub-lists. This is especially helpful if you need an item’s link or ID stored in the parent .
## 6. Putting It All Together: Larger Example
Consider a blog site. We have a schema that extracts the from each post card (via with an ), plus the title, date, summary, and author:
Then run with to get an array of blog post objects, each with , , , , .
## 7. Tips & Best Practices
1. in Chrome DevTools or Firefox’s Inspector to find stable selectors. 2. : Verify you can extract a single field. Then add complexity like nested objects or lists. 3. your schema on partial HTML or a test page before a big crawl. 4. if the site loads content dynamically. You can pass or in . 5. when : if your selectors are off or your schema is malformed, it’ll often show warnings. 6. if you need attributes from the container element (e.g., , ), especially for the “parent” item. 7. : For large pages, make sure your selectors are as narrow as possible.
With (or ), you can build powerful, pipelines that:
  * Scrape any consistent site for structured data. 
  * Support nested objects, repeating lists, or advanced transformations. 
  * Scale to thousands of pages quickly and reliably.


  * Combine your extracted JSON with advanced filtering or summarization in a second pass if needed. 
  * For dynamic pages, combine strategies with or infinite scroll hooking to ensure all content is loaded.


: For repeated, structured data, you don’t need to pay for or wait on an LLM. A well-crafted schema plus CSS or XPath gets you the data faster, cleaner, and cheaper— of Crawl4AI.
That’s it for ! You’ve seen how schema-based approaches (either CSS or XPath) can handle everything from simple lists to deeply nested product catalogs—instantly, with minimal overhead. Enjoy building robust scrapers that produce consistent, structured JSON for your data pipelines!
