In this tutorial, you’ll learn how to:
  1. Extract links (internal, external) from crawled pages 
  2. Filter or exclude specific domains (e.g., social media or custom domains) 
  3. Access and manage media data (especially images) in the crawl result 
  4. Configure your crawler to exclude or prioritize certain images


> - You have completed or are familiar with the tutorial. - You can run Crawl4AI in your environment (Playwright, Python, etc.).
Below is a revised version of the and sections that includes example data structures showing how links and media items are stored in . Feel free to adjust any field names or descriptions to match your actual output.
When you call or on a URL, Crawl4AI automatically extracts links and stores them in the field of . By default, the crawler tries to distinguish links (same domain) from links (different domains).
```
 crawl4ai  AsyncWebCrawler
  AsyncWebCrawler()  crawler:
  result =  crawler.arun()
   result.success:
    internal_links = result.links.get(, [])
    external_links = result.links.get(, [])
    ()
    ()
    ()
    # Each link is typically a dictionary with fields like:
    # { "href": "...", "text": "...", "title": "...", "base_domain": "..." }
     internal_links:
      (, internal_links[])
  :
    (, result.error_message)

```

```
result.links = {
 : [
  {
   : ,
   : ,
   : ,
   : 
  },
  {
   : ,
   : ,
   : ,
   : 
  },
  
 ],
 : [
  # possibly other links leading to third-party sites
 ]
}

```

  * : The raw hyperlink URL. 
  * : The link text (if any) within the tag. 
  * : The attribute of the link (if present). 
  * : The domain extracted from . Helpful for filtering or grouping by domain.


Some websites contain hundreds of third-party or affiliate links. You can filter out certain domains at by configuring the crawler. The most relevant parameters in are:
  * : If , discard any link pointing outside the root domain. 
  * : Provide a list of social media platforms (e.g., ) to exclude from your crawl. 
  * : If , automatically skip known social platforms. 
  * : Provide a list of custom domains you want to exclude (e.g., ).


### 2.1 Example: Excluding External & Social Media Links
```
 asyncio
 crawl4ai  AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
  ():
  crawler_cfg = CrawlerRunConfig(
    exclude_external_links=,     # No links outside primary domain
    exclude_social_media_links=    # Skip recognized social media domains
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(
      ,
      config=crawler_cfg
    )
     result.success:
      (, result.url)
      (, (result.links.get(, [])))
      (, (result.links.get(, []))) 
      # Likely zero external links in this scenario
    :
      (, result.error_message)
 __name__ == :
  asyncio.run(main())

```

### 2.2 Example: Excluding Specific Domains
If you want to let external links in, but specifically exclude a domain (e.g., ), do this:
```
crawler_cfg = CrawlerRunConfig(
  exclude_domains=[]
)

```

This approach is handy when you still want external links but need to block certain sites you consider spammy.
By default, Crawl4AI collects images, audio, and video URLs it finds on the page. These are stored in , a dictionary keyed by media type (e.g., , , ).
```
 result.success:
  images_info = result.media.get(, [])
  ()
   i, img  (images_info[:]): # Inspect just the first 5
    ()
    (f"      Alt text: ")
    (f"      Score: ")
    (f"      Description: \n")

```

```
result.media = {
 : [
  {
   : ,
   : ,
   : "Trial Class Degrees degrees All Degrees AI Degree Technology ...",
   : ,
   : ,
   : ,
   : ,
   : ,
   : 
  },
  
 ],
 : [
  # Similar structure but with video-specific fields
 ],
 : [
  # Similar structure but with audio-specific fields
 ]
}

```

Depending on your Crawl4AI version or scraping strategy, these dictionaries can include fields like:
  * : The media URL (e.g., image source) 
  * : The alt text for images (if present) 
  * : A snippet of nearby text or a short description (optional) 
  * : A heuristic relevance score if you’re using content-scoring features 
  * , : If the crawler detects dimensions for the image/video 
  * : If you’re grouping related media items, the crawler might assign an ID 


With these details, you can easily filter out or focus on certain images (for instance, ignoring images with very low scores or a different domain), or gather metadata for analytics.
If you’re dealing with heavy pages or want to skip third-party images (advertisements, for example), you can turn on:
This setting attempts to discard images from outside the primary domain, keeping only those from the site you’re crawling.
  * : Set to if you want a full-page screenshot stored as in . 
  * : Set to if you want a PDF version of the page in . 
  * : If , attempts to wait until images are fully loaded before final extraction.


## 4. Putting It All Together: Link & Media Filtering
Here’s a combined example demonstrating how to filter out external links, skip certain domains, and exclude external images:
```
 asyncio
 crawl4ai  AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
  ():
  # Suppose we want to keep only internal links, remove certain domains, 
  # and discard external images from the final crawl data.
  crawler_cfg = CrawlerRunConfig(
    exclude_external_links=,
    exclude_domains=[],
    exclude_social_media_links=,  # skip Twitter, Facebook, etc.
    exclude_external_images=,   # keep only images from main domain
    wait_for_images=,       # ensure images are loaded
    verbose=
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(, config=crawler_cfg)
     result.success:
      (, result.url)
      
      in_links = result.links.get(, [])
      ext_links = result.links.get(, [])
      (, (in_links))
      (, (ext_links)) # should be zero with exclude_external_links=True
      
      images = result.media.get(, [])
      (, (images))
      # Let's see a snippet of these images
       i, img  (images[:]):
        ()
    :
      ("[ERROR] Failed to crawl. Reason:", result.error_message)
 __name__ == :
  asyncio.run(main())

```

## 5. Common Pitfalls & Tips
1. : - but then also specifying is typically fine, but understand that the first setting already discards external links. The second becomes somewhat redundant. - but want to keep some external images? Currently no partial domain-based setting for images, so you might need a custom approach or hook logic.
2. : - If your version of Crawl4AI or your scraping strategy includes an , it’s typically a heuristic based on size, position, or content analysis. Evaluate carefully if you rely on it.
3. : - Excluding certain domains or external images can speed up your crawl, especially for large, media-heavy pages. - If you want a “full” link map, do exclude them. Instead, you can post-filter in your own code.
4. : - typically references an internal list of known social domains like Facebook, Twitter, LinkedIn, etc. If you need to add or remove from that list, look for library settings or a local config file (depending on your version).
**That’s it for Link & Media Analysis!** You’re now equipped to filter out unwanted sites and zero in on the images and videos that matter for your project.
