# Overview of Some Important Advanced Features
(Proxy, PDF, Screenshot, SSL, Headers, & Storage State)
Crawl4AI offers multiple power-user features that go beyond simple crawling. This tutorial covers:
1. 2. 3. 4. 5. **Session Persistence & Local Storage**
> - You have a basic grasp of - You know how to run or configure your Python environment with Playwright installed
If you need to route your crawl traffic through a proxy—whether for IP rotation, geo-testing, or privacy—Crawl4AI supports it via .
```
 asyncio
 crawl4ai  AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
  ():
  browser_cfg = BrowserConfig(
    proxy_config={
      : ,
      : ,
      : ,
    },
    headless=
  )
  crawler_cfg = CrawlerRunConfig(
    verbose=
  )
    AsyncWebCrawler(config=browser_cfg)  crawler:
    result =  crawler.arun(
      url=,
      config=crawler_cfg
    )
     result.success:
      ("[OK] Page fetched via proxy.")
      (, result.html[:])
    :
      (, result.error_message)
 __name__ == :
  asyncio.run(main())

```

- expects a dict with and optional auth credentials. - Many commercial proxies provide an HTTP/HTTPS “gateway” server that you specify in . - If your proxy doesn’t need auth, omit /.
## 2. Capturing PDFs & Screenshots
Sometimes you need a visual record of a page or a PDF “printout.” Crawl4AI can do both in one pass:
```
 os, asyncio
 base64  b64decode
 crawl4ai  AsyncWebCrawler, CacheMode
  ():
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(
      url=,
      cache_mode=CacheMode.BYPASS,
      pdf=,
      screenshot=
    )
     result.success:
      
       result.screenshot:
         (, )  f:
          f.write(b64decode(result.screenshot))
      
       result.pdf:
         (, )  f:
          f.write(result.pdf)
      ("[OK] PDF & screenshot captured.")
    :
      (, result.error_message)
 __name__ == :
  asyncio.run(main())

```

- Large or complex pages can be slow or error-prone with “traditional” full-page screenshots. - Exporting a PDF is more reliable for very long pages. Crawl4AI automatically converts the first PDF page into an image if you request both. 
- : Exports the current page as a PDF (base64-encoded in ). - : Creates a screenshot (base64-encoded in ). - or advanced hooking can further refine how the crawler captures content.
If you need to verify or export a site’s SSL certificate—for compliance, debugging, or data analysis—Crawl4AI can fetch it during the crawl:
```
 asyncio, os
 crawl4ai  AsyncWebCrawler, CrawlerRunConfig, CacheMode
  ():
  tmp_dir = os.path.join(os.getcwd(), )
  os.makedirs(tmp_dir, exist_ok=)
  config = CrawlerRunConfig(
    fetch_ssl_certificate=,
    cache_mode=CacheMode.BYPASS
  )
    AsyncWebCrawler()  crawler:
    result =  crawler.arun(url=, config=config)
     result.success  result.ssl_certificate:
      cert = result.ssl_certificate
      ()
      ()
      ()
      ()
      # Export in multiple formats:
      cert.to_json(os.path.join(tmp_dir, ))
      cert.to_pem(os.path.join(tmp_dir, ))
      cert.to_der(os.path.join(tmp_dir, ))
      ("\nCertificate exported to JSON/PEM/DER in 'tmp' folder.")
    :
      ("[ERROR] No certificate or crawl failed.")
 __name__ == :
  asyncio.run(main())

```

- triggers certificate retrieval. - includes methods (, , ) for saving in various formats (handy for server config, Java keystores, etc.).
Sometimes you need to set custom headers (e.g., language preferences, authentication tokens, or specialized user-agent strings). You can do this in multiple ways:
```
 asyncio
 crawl4ai  AsyncWebCrawler
  ():
  # Option 1: Set headers at the crawler strategy level
  crawler1 = AsyncWebCrawler(
    # The underlying strategy can accept headers in its constructor
    crawler_strategy= # We'll override below for clarity
  )
  crawler1.crawler_strategy.update_user_agent()
  crawler1.crawler_strategy.set_custom_headers({
    : 
  })
  result1 =  crawler1.arun()
  (, result1.success)
  # Option 2: Pass headers directly to `arun()`
  crawler2 = AsyncWebCrawler()
  result2 =  crawler2.arun(
    url=,
    headers={: }
  )
  (, result2.success)
 __name__ == :
  asyncio.run(main())

```

- Some sites may react differently to certain headers (e.g., ). - If you need advanced user-agent randomization or client hints, see or use .
## 5. Session Persistence & Local Storage
Crawl4AI can preserve cookies and localStorage so you can continue where you left off—ideal for logging into sites or skipping repeated auth flows.
```
 asyncio
 crawl4ai  AsyncWebCrawler
  ():
  storage_dict = {
    : [
      {
        : ,
        : ,
        : ,
        : ,
        : ,
        : ,
        : ,
        : 
      }
    ],
    : [
      {
        : ,
        : [
          {: , : }
        ]
      }
    ]
  }
  # Provide the storage state as a dictionary to start "already logged in"
    AsyncWebCrawler(
    headless=,
    storage_state=storage_dict
  )  crawler:
    result =  crawler.arun()
     result.success:
      (, (result.html))
    :
      ("Failed to crawl protected page")
 __name__ == :
  asyncio.run(main())

```

### 5.2 Exporting & Reusing State
You can sign in once, export the browser context, and reuse it later—without re-entering credentials.
  * : Exports cookies, localStorage, etc. to a file. 
  * Provide on subsequent runs to skip the login step.


: or [Explanations → Browser Context & Managed Browser](https://docs.crawl4ai.com/advanced/advanced-features/<../identity-based-crawling/>) for more advanced scenarios (like multi-step logins, or capturing after interactive pages).
Here’s a snippet that combines multiple “advanced” features (proxy, PDF, screenshot, SSL, custom headers, and session reuse) into one run. Normally, you’d tailor each setting to your project’s needs.
```
 os, asyncio
 base64  b64decode
 crawl4ai  AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
  ():
  # 1. Browser config with proxy + headless
  browser_cfg = BrowserConfig(
    proxy_config={
      : ,
      : ,
      : ,
    },
    headless=,
  )
  # 2. Crawler config with PDF, screenshot, SSL, custom headers, and ignoring caches
  crawler_cfg = CrawlerRunConfig(
    pdf=,
    screenshot=,
    fetch_ssl_certificate=,
    cache_mode=CacheMode.BYPASS,
    headers={: },
    storage_state=, # Reuse session from a previous sign-in
    verbose=,
  )
  
    AsyncWebCrawler(config=browser_cfg)  crawler:
    result =  crawler.arun(
      url = , 
      config=crawler_cfg
    )
     result.success:
      ("[OK] Crawled the secure page. Links found:", (result.links.get(, [])))
      # Save PDF & screenshot
       result.pdf:
         (, )  f:
          f.write(b64decode(result.pdf))
       result.screenshot:
         (, )  f:
          f.write(b64decode(result.screenshot))
      
       result.ssl_certificate:
        (, result.ssl_certificate.issuer.get(, ))
    :
      (, result.error_message)
 __name__ == :
  asyncio.run(main())

```

  * capturing for large or critical pages 
  * for language or specialized requests 


With these power tools, you can build robust scraping workflows that mimic real user behavior, handle secure sites, capture detailed snapshots, and manage sessions across multiple runs—streamlining your entire data collection pipeline.
