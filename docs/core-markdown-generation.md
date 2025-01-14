One of Crawl4AI’s core features is generating from web pages. Originally built to solve the problem of extracting only the “actual” content and discarding boilerplate or noise, Crawl4AI’s markdown system remains one of its biggest draws for AI workflows.
In this tutorial, you’ll learn:
  1. How to configure the 
  2. How (BM25 or Pruning) help you refine markdown and discard junk 
  3. The difference between raw markdown () and filtered markdown () 


> - You’ve completed or read to understand how to run a simple crawl. - You know how to configure .
Here’s a minimal code snippet that uses the with no additional filtering:
```
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
 crawl4ai.markdown_generation_strategy  DefaultMarkdownGenerator
  ():
  config = CrawlerRunConfig(
    markdown_generator=DefaultMarkdownGenerator()
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(, config=config)
     result.success:
      ()
      (result.markdown) # The unfiltered markdown from the page
    :
      (, result.error_message)
 __name__ == :
  asyncio.run(main())

```

- `CrawlerRunConfig( markdown_generator = DefaultMarkdownGenerator() )` instructs Crawl4AI to convert the final HTML into markdown at the end of each crawl. - The resulting markdown is accessible via .
## 2. How Markdown Generation Works
### 2.1 HTML-to-Text Conversion (Forked & Modified)
Under the hood, uses a specialized HTML-to-text approach that:
  * Preserves headings, code blocks, bullet points, etc. 
  * Removes extraneous tags (scripts, styles) that don’t add meaningful content. 
  * Can optionally generate references for links or skip them altogether.


A set of (passed as a dict) allows you to customize precisely how HTML converts to markdown. These map to standard html2text-like configuration plus your own enhancements (e.g., ignoring internal links, preserving certain tags verbatim, or adjusting line widths).
### 2.2 Link Citations & References
By default, the generator can convert elements into citations, then place the actual links at the bottom of the document. This is handy for research workflows that demand references in a structured manner.
Before or after the HTML-to-Markdown step, you can apply a (like BM25 or Pruning) to reduce noise and produce a “fit_markdown”—a heavily pruned version focusing on the page’s main text. We’ll cover these filters shortly.
## 3. Configuring the Default Markdown Generator
You can tweak the output by passing an dict to . For example:
```
 crawl4ai.markdown_generation_strategy  DefaultMarkdownGenerator
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
  ():
  # Example: ignore all links, don't escape HTML, and wrap text at 80 characters
  md_generator = DefaultMarkdownGenerator(
    options={
      : ,
      : ,
      : 
    }
  )
  config = CrawlerRunConfig(
    markdown_generator=md_generator
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(, config=config)
     result.success:
      (, result.markdown[:]) 
    :
      (, result.error_message)
 __name__ == :
   asyncio
  asyncio.run(main())

```

  * (bool): Whether to remove all hyperlinks in the final markdown. 
  * (bool): Turn HTML entities into text (default is often ). 
  * (int): Wrap text at N characters. or means no wrapping. 
  * (bool): If , omit or internal links referencing the same page. 
  * (bool): Attempt to handle / in a more readable way.


selectively remove or rank sections of text before turning them into Markdown. This is especially helpful if your page has ads, nav bars, or other clutter you don’t want.
If you have a , BM25 is a good choice:
```
 crawl4ai.markdown_generation_strategy  DefaultMarkdownGenerator
 crawl4ai.content_filter_strategy  BM25ContentFilter
 crawl4ai  CrawlerRunConfig
bm25_filter = BM25ContentFilter(
  user_query=,
  bm25_threshold=,
  use_stemming=
)
md_generator = DefaultMarkdownGenerator(
  content_filter=bm25_filter,
  options={: }
)
config = CrawlerRunConfig(markdown_generator=md_generator)

```

  * : The term you want to focus on. BM25 tries to keep only content blocks relevant to that query. 
  * : Raise it to keep fewer blocks; lower it to keep more. 
  * : If , variations of words match (e.g., “learn,” “learning,” “learnt”).


BM25 tries to glean a context from page metadata, or you can simply treat it as a scorched-earth approach that discards text with low generic score. Realistically, you want to supply a query for best results.
If you have a specific query, or if you just want a robust “junk remover,” use . It analyzes text density, link density, HTML structure, and known patterns (like “nav,” “footer”) to systematically prune extraneous or repetitive sections.
```
from crawl4ai.content_filter_strategy  PruningContentFilter
prune_filter = (
  threshold=,
  threshold_type=, 
  min_word_threshold=
)

```

  * : Score boundary. Blocks below this score get removed. 
  * : 
    * : Straight comparison ( keeps the block). 
    * : The filter adjusts threshold in a data-driven manner. 
  * : Discard blocks under N words as likely too short or unhelpful.


- You want a broad cleanup without a user query. - The page has lots of repeated sidebars, footers, or disclaimers that hamper text extraction.
When a content filter is active, the library produces two forms of markdown inside or (if using the simplified field) :
1. : The full unfiltered markdown. 2. : A “fit” version where the filter has removed or trimmed noisy segments.
> In earlier examples, you may see references to . Depending on your library version, you might access , , or an object named . The idea is the same: you’ll have a raw version and a filtered (“fit”) version if a filter is used.
```
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
 crawl4ai.markdown_generation_strategy  DefaultMarkdownGenerator
 crawl4ai.content_filter_strategy  PruningContentFilter
  ():
  config = CrawlerRunConfig(
    markdown_generator=DefaultMarkdownGenerator(
      content_filter=PruningContentFilter(threshold=),
      options={: }
    )
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(, config=config)
     result.success:
      (, result.markdown)
      # If a filter is used, we also have .fit_markdown:
      md_object = result.markdown_v2 
      (, md_object.fit_markdown)
    :
      (, result.error_message)
 __name__ == :
  asyncio.run(main())

```

If your library stores detailed markdown output in an object like , you’ll see fields such as:
  * : The direct HTML-to-markdown transformation (no filtering). 
  * : A version that moves links to reference-style footnotes. 
  * : A separate string or section containing the gathered references. 
  * : The filtered markdown if you used a content filter. 
  * : The corresponding HTML snippet used to generate (helpful for debugging or advanced usage).


```
md_obj  result.markdown_v2 # your library’s naming may vary
(, md_obj.raw_markdown)
(, md_obj.markdown_with_citations)
(, md_obj.references_markdown)
(, md_obj.fit_markdown)

```

- You can supply to an LLM if you want the entire text. - Or feed into a vector database to reduce token usage. - can help you keep track of link provenance.
Below is a under “Combining Filters (BM25 + Pruning)” that demonstrates how you can run passes of content filtering without re-crawling, by taking the HTML (or text) from a first pass and feeding it into the second filter. It uses real code patterns from the snippet you provided for , which directly accepts strings (and can also handle plain text with minimal adaptation).
## 7. Combining Filters (BM25 + Pruning) in Two Passes
You might want to noisy boilerplate first (with ), and then against a user query (with ). You don’t have to crawl the page twice. Instead:
1. : Apply directly to the raw HTML from (the crawler’s downloaded HTML). 2. : Take the pruned HTML (or text) from step 1, and feed it into , focusing on a user query.
```
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
 crawl4ai.content_filter_strategy  PruningContentFilter, BM25ContentFilter
 bs4  BeautifulSoup
  ():
  # 1. Crawl with minimal or no markdown generator, just get raw HTML
  config = CrawlerRunConfig(
    # If you only want raw HTML, you can skip passing a markdown_generator
    # or provide one but focus on .html in this example
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(, config=config)
      result.success   result.html:
      ("Crawl failed or no HTML content.")
      
    raw_html = result.html
    # 2. First pass: PruningContentFilter on raw HTML
    pruning_filter = PruningContentFilter(threshold=, min_word_threshold=)
    # filter_content returns a list of "text chunks" or cleaned HTML sections
    pruned_chunks = pruning_filter.filter_content(raw_html)
    # This list is basically pruned content blocks, presumably in HTML or text form
    # For demonstration, let's combine these chunks back into a single HTML-like string
    # or you could do further processing. It's up to your pipeline design.
    pruned_html = .join(pruned_chunks)
    # 3. Second pass: BM25ContentFilter with a user query
    bm25_filter = BM25ContentFilter(
      user_query=,
      bm25_threshold=,
      language=
    )
    # returns a list of text chunks
    bm25_chunks = bm25_filter.filter_content(pruned_html) 
      bm25_chunks:
      ("Nothing matched the BM25 query after pruning.")
      
    # 4. Combine or display final results
    final_text = .join(bm25_chunks)
    ("==== PRUNED OUTPUT (first pass) ====")
    (pruned_html[:], ) 
    ("\n==== BM25 OUTPUT (second pass) ====")
    (final_text[:], )
 __name__ == :
  asyncio.run(main())

```

1. : We crawl once and store the raw HTML in . 2. : Takes HTML + optional parameters. It extracts blocks of text or partial HTML, removing headings/sections deemed “noise.” It returns a . 3. : We join these pruned chunks back into a single HTML-like string. (Alternatively, you could store them in a list for further logic—whatever suits your pipeline.) 4. : We feed the pruned string into with a user query. This second pass further narrows the content to chunks relevant to “machine learning.”
: We used from the first pass, so there’s no need to run again—.
  * : If your pruned output is mostly text, BM25 can still handle it; just keep in mind it expects a valid string input. If you supply partial HTML (like ), it will parse it as HTML. 
  * **Chaining in a Single Pipeline** : If your code supports it, you can chain multiple filters automatically. Otherwise, manual two-pass filtering (as shown) is straightforward. 
  * : If you see too much or too little text in step one, tweak or . Similarly, can be raised/lowered for more or fewer chunks in step two.


If your codebase or pipeline design allows applying multiple filters in one pass, you could do so. But often it’s simpler—and more transparent—to run them sequentially, analyzing each step’s result.
: By your filtering logic in two passes, you get powerful incremental control over the final content. First, remove “global” clutter with Pruning, then refine further with BM25-based query relevance—without incurring a second network crawl.
## 8. Common Pitfalls & Tips
1. - Make sure the crawler actually retrieved HTML. If the site is heavily JS-based, you may need to enable dynamic rendering or wait for elements. - Check if your content filter is too aggressive. Lower thresholds or disable the filter to see if content reappears.
2. - Very large pages with multiple filters can be slower. Consider to avoid re-downloading. - If your final use case is LLM ingestion, consider summarizing further or chunking big texts.
3. - Great for RAG pipelines, semantic search, or any scenario where extraneous boilerplate is unwanted. - Still verify the textual quality—some sites have crucial data in footers or sidebars.
4. - If you see lots of raw HTML slipping into the text, turn on . - If code blocks look messy, experiment with or .
## 9. Summary & Next Steps
In this tutorial, you learned to:
  * Use for query-specific extraction or for general noise removal. 
  * Distinguish between raw and filtered markdown (). 
  * Leverage the object to handle different forms of output (citations, references, etc.).


Now you can produce high-quality Markdown from any website, focusing on exactly the content you need—an essential step for powering AI models, summarization pipelines, or knowledge-base queries.
