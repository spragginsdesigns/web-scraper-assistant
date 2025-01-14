When you call on a page, Crawl4AI returns a object containing everything you might need—raw HTML, a cleaned version, optional screenshots or PDFs, structured extraction results, and more. This document explains those fields and how they map to different output types. 
Below is the core schema. Each field captures a different aspect of the crawl’s result:
```
 ():
  raw_markdown: 
  markdown_with_citations: 
  references_markdown: 
  fit_markdown: [] = 
  fit_html: [] = 
 ():
  url: 
  html: 
  success: 
  cleaned_html: [] = 
  media: [, []] = {}
  links: [, []] = {}
  downloaded_files: [[]] = 
  screenshot: [] = 
  pdf : [] = 
  markdown: [[, MarkdownGenerationResult]] = 
  markdown_v2: [MarkdownGenerationResult] = 
  extracted_content: [] = 
  metadata: [] = 
  error_message: [] = 
  session_id: [] = 
  response_headers: [] = 
  status_code: [] = 
  ssl_certificate: [SSLCertificate] = 
   :
    arbitrary_types_allowed = 

```

The final or actual URL crawled (in case of redirects).  
---  
Original, unmodified page HTML. Good for debugging or custom processing.  
if the crawl completed without major errors, else .  
Sanitized HTML with scripts/styles removed; can exclude tags if configured via etc.  
Extracted media info (images, audio, etc.), each with attributes like , , , etc.  
Extracted link data, split by and . Each link usually has , , etc.  
If in , this lists the filepaths of saved downloads.  
Screenshot of the page (base64-encoded) if .  
PDF of the page if .  
For now, holds a . Over time, this will be consolidated into . The generator can provide raw markdown, citations, references, and optionally .  
Legacy field for detailed markdown output. This will be replaced by soon.  
The output of a structured extraction (CSS/LLM-based) stored as JSON string or other text.  
Additional info about the crawl or extracted data.  
If , contains a short description of what went wrong.  
The ID of the session used for multi-page or persistent crawling.  
HTTP response headers, if captured.  
HTTP status code (e.g., 200 for OK).  
Crawl4AI preserves the exact HTML as . Useful for:
  * Debugging page issues or checking the original content.
  * Performing your own specialized parse if needed.


If you specify any cleanup or exclusion parameters in (like , , etc.), you’ll see the result here:
```
 = CrawlerRunConfig(
  excluded_tags=[, , ],
  keep_data_attributes=False
)
result = await crawler.arun(, =)
(result.cleaned_html) # Freed of forms, header, footer, data-* attributes

```

  * : The current location for detailed markdown output, returning a object. 
  * : Eventually, we’re merging these fields. For now, you might see used widely in code examples.

Markdown including inline citations that reference links at the end.  
---  
The filtered/“fit” markdown if a content filter was used.  
The filtered HTML that generated .  
### 3.2 Basic Example with a Markdown Generator
```
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
 crawl4ai.markdown_generation_strategy  DefaultMarkdownGenerator
config = CrawlerRunConfig(
  markdown_generator=DefaultMarkdownGenerator(
    options={: , : } # e.g. pass html2text style options
  )
)
result =  crawler.arun(url=, config=config)
md_res = result.markdown_v2 
(md_res.raw_markdown[:])
(md_res.markdown_with_citations)
(md_res.references_markdown)

```

: If you use a filter like , you’ll get and as well.
If you run a JSON-based extraction strategy (CSS, XPath, LLM, etc.), the structured data is stored in —it’s placed in as a JSON string (or sometimes plain text).
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
      {: , : , : , : }
    ]
  }
  raw_html = "<div class='item'><h2>Item 1</h2><a href='https://example.com/item1'>Link 1</a></div>"
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(
      url= + raw_html,
      config=CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(schema)
      )
    )
    data = json.loads(result.extracted_content)
    (data)
 __name__ == :
  asyncio.run(main())

```

Here: - passes the HTML content directly, no network requests. - The extraction strategy populates with the JSON array .
## 5. More Fields: Links, Media, and More
A dictionary, typically with and lists. Each entry might have , , , etc. This is automatically captured if you haven’t disabled link extraction.
```
(result.links[][:3]) # Show first 3 internal links

```

Similarly, a dictionary with , , , etc. Each item could include , , , and more, if your crawler is set to gather them.
```
images = result.media.(, [])
 img  images:
  print(, img[], , img.())

```

  * contains a base64-encoded PNG string. 
  * contains raw PDF bytes (you can write them to a file).


If , holds details about the site’s SSL cert, such as issuer, validity dates, etc.
```
if result:
  (result.status_code, result.response_headers)
  (, (result.links.(, [])))
  if result.markdown_v2:
    (, result.markdown_v2.raw_markdown[:])
  if result.extracted_content:
    (, result.extracted_content)
else:
  (, result.error_message)

```

: Use for now. It will eventually become .
  * : Dive deeper into how to configure and various filters. 
  * : Learn how to use and .
  * : If you want to manipulate the page or preserve state across multiple calls, see the hooking or session docs. 
  * : For complex or unstructured content requiring AI-driven parsing, check the LLM-based strategies doc.


exploring all that offers—whether you need raw HTML, sanitized output, markdown, or fully structured data, Crawl4AI has you covered!
