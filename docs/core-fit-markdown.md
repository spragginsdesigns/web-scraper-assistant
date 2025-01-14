# Fit Markdown with Pruning & BM25
is a specialized version of your page’s markdown, focusing on the most relevant content. By default, Crawl4AI converts the entire HTML into a broad . With fit markdown, we apply a algorithm (e.g., or ) to remove or rank low-value sections—such as repetitive sidebars, shallow text blocks, or irrelevancies—leaving a concise textual “core.”
## 1. How “Fit Markdown” Works
In , you can specify a to shape how content is pruned or ranked before final markdown generation. A filter’s logic is applied or the HTML→Markdown process, producing:
  * (the corresponding HTML snippet that produced )


> : We’re currently storing the result in , but eventually we’ll unify it as .
1. – Scores each node by text density, link density, and tag importance, discarding those below a threshold. 2. – Focuses on textual relevance using BM25 ranking, especially useful if you have a specific user query (e.g., “machine learning” or “food nutrition”).
discards less relevant nodes based on **text density, link density, and tag importance**. It’s a heuristic-based approach—if certain sections appear too “thin” or too “spammy,” they’re pruned.
```
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
 crawl4ai.content_filter_strategy  PruningContentFilter
 crawl4ai.markdown_generation_strategy  DefaultMarkdownGenerator
  ():
  # Step 1: Create a pruning filter
  prune_filter = PruningContentFilter(
    # Lower → more content retained, higher → more content pruned
    threshold=,      
    
    threshold_type=, 
    # Ignore nodes with <5 words
    min_word_threshold=   
  )
  # Step 2: Insert it into a Markdown Generator
  md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)
  # Step 3: Pass it to CrawlerRunConfig
  config = CrawlerRunConfig(
    markdown_generator=md_generator
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(
      url=, 
      config=config
    )
     result.success:
      # 'fit_markdown' is your pruned content, focusing on "denser" text
      (, (result.markdown_v2.raw_markdown))
      (, (result.markdown_v2.fit_markdown))
    :
      (, result.error_message)
 __name__ == :
  asyncio.run(main())

```

  * (int): If a block has fewer words than this, it’s pruned. 
  * → each node must exceed (0–1). 
  * → node scoring adjusts according to tag type, text/link density, etc. 
  * (float, default ~0.48): The base or “anchor” cutoff. 


  * – Encourages blocks that have a higher ratio of text to overall content. 
  * – Penalizes sections that are mostly links. 
  * – e.g., an or might be more important than a . 
  * – If a node is deeply nested or in a suspected sidebar, it might be deprioritized.


is a classical text ranking algorithm often used in search engines. If you have a or rely on page metadata to derive a query, BM25 can identify which text chunks best match that query.
```
 asyncio
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig
 crawl4ai.content_filter_strategy  BM25ContentFilter
 crawl4ai.markdown_generation_strategy  DefaultMarkdownGenerator
  ():
  # 1) A BM25 filter with a user query
  bm25_filter = BM25ContentFilter(
    user_query=,
    # Adjust for stricter or looser results
    bm25_threshold= 
  )
  # 2) Insert into a Markdown Generator
  md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)
  # 3) Pass to crawler config
  config = CrawlerRunConfig(
    markdown_generator=md_generator
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(
      url=, 
      config=config
    )
     result.success:
      ()
      (result.markdown_v2.fit_markdown)
    :
      (, result.error_message)
 __name__ == :
  asyncio.run(main())

```

  * (str, optional): E.g. . If blank, the filter tries to glean a query from page metadata. 
  * Higher → fewer chunks but more relevant. 


> In more advanced scenarios, you might see parameters like , , or to refine how text is tokenized or weighted.
## 4. Accessing the “Fit” Output
After the crawl, your “fit” content is found in . In future versions, it will be . Meanwhile:
If the content filter is , you might see additional logic or references in that highlight relevant segments. If it’s , the text is typically well-cleaned but not necessarily matched to a query.
```
prune_filter = PruningContentFilter(
  threshold=0.5,
  threshold_type=,
  min_word_threshold=10
)
md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)
config = CrawlerRunConfig(markdown_generator=md_generator)


```

```
bm25_filter = BM25ContentFilter(
  user_query=,
  bm25_threshold=1.2
)
md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)
config = CrawlerRunConfig(markdown_generator=md_generator)


```

## 6. Combining with “word_count_threshold” & Exclusions
Remember you can also specify:
```
config  CrawlerRunConfig
  word_count_threshold,
  excluded_tags, , ,
  exclude_external_links,
  markdown_generatorDefaultMarkdownGenerator
    content_filterPruningContentFilterthreshold
  


```

  1. The crawler’s are removed from the HTML first. 
  2. The content filter (Pruning, BM25, or custom) prunes or ranks the remaining text blocks. 
  3. The final “fit” content is generated in .


If you need a different approach (like a specialized ML model or site-specific heuristics), you can create a new class inheriting from and implement . Then inject it into your :
```
 crawl4ai.content_filter_strategy  RelevantContentFilter
 ():
   ():
    # parse HTML, implement custom logic
     [block  block  ...  ... some condition...]

```

is a crucial feature for:
  * : Quickly get the important text from a cluttered page. 
  * : Combine with to produce content relevant to a query. 
  * : Filter out boilerplate so LLM-based extraction or summarization runs on denser text.


: - : Great if you just want the “meatiest” text without a user query. - : Perfect for query-based extraction or searching. - Combine with to refine your final “fit” text. - Fit markdown ends up in ; eventually in future versions.
With these tools, you can on the text that truly matters, ignoring spammy or boilerplate content, and produce a concise, relevant “fit markdown” for your AI or data pipelines. Happy pruning and searching!
