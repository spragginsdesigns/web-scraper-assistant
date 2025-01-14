```
 crawl4ai.async_configs import BrowserConfig

browser_config = BrowserConfig(proxy=)
 =  crawler.arun(url=)

browser_config = BrowserConfig(proxy=)
 =  crawler.arun(url=)

```

Use an authenticated proxy with :
```
 crawl4ai.async_configs import BrowserConfig
proxy_config = {
  : ,
  : ,
  : 
}
browser_config = BrowserConfig(proxy_config=proxy_config)
 =  crawler.arun(url=)

```

Example using a proxy rotation service and updating dynamically:
```
 crawl4ai.async_configs  BrowserConfig
  ():
  # Your proxy rotation logic here
   {: }
browser_config = BrowserConfig()
  AsyncWebCrawler(config=browser_config)  crawler:
  # Update proxy for each request
   url  urls:
    proxy =  get_next_proxy()
    browser_config.proxy_config = proxy
    result =  crawler.arun(url=url, config=browser_config)

```

