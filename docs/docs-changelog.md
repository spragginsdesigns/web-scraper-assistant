You signed in with another tab or window. to refresh your session. You signed out in another tab or window. to refresh your session. You switched accounts on another tab or window. to refresh your session.
  * You must be signed in to change notification settings


1089 lines (827 loc) · 48 KB
1089 lines (827 loc) · 48 KB
All notable changes to Crawl4AI will be documented in this file.
The format is based on , and this project adheres to .
## [0.4.267] - 2025 - 01 - 06
  * : Introduced a utility function to resolve for asyncio subprocesses on Windows. (, )
  * : Added a method to determine if a page requires scrolling before taking actions in . ()


  * : Updated the version from to . ()
  * : Enhanced scrolling methods in by adding a parameter for better control. ()
  * : Updated the example to reflect the latest API changes and better illustrate features. ()
  * : 
    * Added Windows-specific instructions for handling asyncio event loops. ()


  * : Removed outdated and unused code for markdown generation in . ()


  * **Page Closing to Prevent Memory Leaks** : 
    * : Added a block to ensure pages are closed when no is provided.
    * : Prevents memory leaks caused by lingering pages after a crawl.
    * : 
```
:
  # If no session_id is given we should close the page
    .:
     .()
```

  * : Modified in to return all matching elements instead of just the first one, ensuring comprehensive extraction. ()
  * : Added robust error handling to ensure scrolling proceeds safely even if a configuration is missing. ()


  * : Added to for better development environment consistency. ()


  *     * SSL certificate validation options in extraction strategies
    * Enhanced response status code handling with retry logic
  *     * New content filtering system with regex support
    * Advanced chunking strategies for large content
  *   * 

  *     * Optimized selector compilation with caching
    * Enhanced memory management for large documents
  *     * More detailed error messages and categorization


  * Old field computation method using 
  * Direct browser manipulation without proper SSL handling


  * Legacy extraction patterns without proper error handling
  * Direct DOM manipulation without sanitization


  * Memory leaks in large document processing
  * Incorrect handling of nested JSON structures
  * Performance bottlenecks in parallel processing


  * Improved input validation and sanitization


#### **New Parameters and Attributes Added**
  * : Enables text-only mode, disables images, JavaScript, and GPU-related features for faster, minimal rendering.
  * : Optimizes the browser by disabling unnecessary background processes and features for efficiency.
  * : Dynamically adjusts based on mode (default values: 800x600 for , 1920x1080 otherwise).
  * : Adds browser-specific flags for mode.
  * : Dynamically adjusts the viewport to the content size for accurate rendering.


  * Added : Dynamically computed based on or custom configuration.
  * Enhanced support for and by adding specific browser arguments to reduce resource consumption.


  * : 
    * Scrolls through the entire page while dynamically detecting content changes.
    * Ensures scrolling stops when no new dynamic content is loaded.


  * Added method: 
    * Creates a new browser session and assigns a unique ID.
    * Supports persistent and non-persistent contexts with full compatibility for cookies, headers, and proxies.


#### **Improved Content Loading and Adjustment**
  * : 
    * Automatically adjusts viewport to match content dimensions.
    * Includes scaling via Chrome DevTools Protocol (CDP).
  * Enhanced content loading: 
    * Waits for images to load and ensures network activity is idle before proceeding.


  * Improved error handling and detailed logging for: 


  * Removed hardcoded viewport dimensions in multiple places, replaced with dynamic values (, ).
  * Removed commented-out and unused code for better readability.


  * Reduced resource usage in by disabling unnecessary browser features such as extensions, background timers, and sync.
  * Improved compatibility for different browser types (, , ).


  * Changed schema reference for : 
    * This likely ensures better compatibility with the class and its JSON schema.


  * Improved extraction instruction for schema-based LLM strategies.


  1. : 
     * Focuses on minimal resource usage by disabling non-essential browser features.
  2. : 
     * Optimizes browser for performance by disabling background tasks and unnecessary services.
  3. : 
     * Ensures the entire content of a page is crawled, including dynamic elements loaded during scrolling.
  4. : 
     * Automatically resizes the viewport to match content dimensions, improving compatibility and rendering accuracy.
  5. : 
     * Simplifies session handling with better support for persistent and non-persistent contexts.


  * Fixed potential viewport mismatches by ensuring consistent use of and throughout the code.
  * Improved robustness of dynamic content loading to avoid timeouts and failed evaluations.


#### 1. Introduced PruningContentFilter (Dec 01, 2024) (Dec 01, 2024)
A new content filtering strategy that removes less relevant nodes based on metrics like text and link density.
  * : Enhancement of content filtering capabilities.


```
Implemented effective pruning algorithm with comprehensive scoring.
```

  * : Improved documentation regarding new features.


```
Updated to include usage and explanation for the PruningContentFilter.
```

  * : Expanded documentation for users.


```
Added detailed section explaining the PruningContentFilter.
```

#### 2. Added Unit Tests for PruningContentFilter (Dec 01, 2024) (Dec 01, 2024)
Comprehensive tests added to ensure correct functionality of PruningContentFilter
  * : Increased test coverage for content filtering strategies.


```
Created test cases for various scenarios using the PruningContentFilter.
```

#### 3. Enhanced BM25ContentFilter tests (Dec 01, 2024) (Dec 01, 2024)
Extended testing to cover additional edge cases and performance metrics.
  * : Improved reliability and performance assurance.


```
Added tests for new extraction scenarios including malformed HTML.
```

#### 4. Updated Examples (Dec 01, 2024) (Dec 01, 2024)
Altered examples in documentation to promote the use of PruningContentFilter alongside existing strategies.
  * : Enhanced usability and clarity for new users.
  * Revised example to illustrate usage of PruningContentFilter.


  1. Enhanced Docker Support (Nov 29, 2024) 
     * Improved GPU support in Docker images.
     * Dockerfile refactored for better platform-specific installations.
     * Introduced new Docker commands for different platforms: 


  * Enhanced README.md to improve user guidance and installation instructions.
  * Added installation instructions for Playwright setup in README.
  * Created and updated examples in to be more useful and user-friendly.
  * Bumped version number in to 0.3.746.


  * Streamlined application structure: 
    * Removed static pages and related code from which might affect existing deployments relying on static content.


  * Developed method in to streamline post-installation setup tasks.
  * Refined migration processes in with enhanced logging for better error visibility.
  * Updated to support local and hub services for different architectures, enhancing build and deploy capabilities.
  * Refactored example test cases in to facilitate comprehensive testing.


Updated README with new docker commands and setup instructions. Enhanced installation instructions and guidance.
Added post-install script functionality. Introduced method for automation of post-installation tasks.
Improved migration logging. Refined migration processes and added better logging.
Refactored docker-compose for better service management. Updated to define services for different platforms and versions.
Updated version number. Bumped version number to 0.3.746.
Enhanced example scripts. Uncommented example usage in async guide for user functionality.
Refactored code to improve maintainability. Streamlined app structure by removing static pages code.
  * Improved ManagedBrowser configuration with dynamic host/port
  * Implemented fast HTML formatting in web crawler
  * Enhanced markdown generation with a new generator class
  * Improved sanitization and utility functions
  * Added contributor details and pull request acknowledgments
  * Updated documentation for clearer usage scenarios
  * Adjusted tests to reflect class name changes


Added new contributors and pull request details. Updated community contributions and acknowledged pull requests.
Version update. Bumped version to 0.3.743.
Improved ManagedBrowser configuration. Enhanced browser initialization with configurable host and debugging port; improved hook execution.
Optimized HTML processing. Implemented 'fast_format_html' for optimized HTML formatting; applied it when 'prettiify' is enabled.
Enhanced markdown generation strategy. Updated to use DefaultMarkdownGenerator and improved markdown generation with filters option.
Refactored markdown generation class. Renamed DefaultMarkdownGenerationStrategy to DefaultMarkdownGenerator; added content filter handling.
Enhanced utility functions. Improved input sanitization and enhanced HTML formatting method.
Improved documentation for hooks. Updated code examples to include cookies in crawler strategy initialization.
Refactored tests to match class renaming. Updated tests to use renamed DefaultMarkdownGenerator class.
This changelog details the updates and changes introduced in Crawl4AI version 0.3.74. It's designed to inform developers about new features, modifications to existing components, removals, and other important information.
  * Users can now specify download folders using the parameter in the constructor or the method. If not specified, downloads are saved to a "downloads" folder within the directory.
  * File download tracking is integrated into the object. Successfully downloaded files are listed in the attribute, providing their paths.
  * Added parameter to the crawler strategies (defaults to ). If set to True you can add JS code and parameter for file download.


```
 
 
   
   
  ():
    ..(.(), , )
  .(, )
    (
    , 
    , 
    
  )  :
       .(
      ,
      

        if (downloadLink) { downloadLink.click(); }
,
       # To ensure download has started
    )
     .:
      ()
         .:
        ()
.(())
```

  * Introduced the strategy (and its implementation ) for extracting relevant content from web pages, replacing Fit Markdown and other content cleaning strategy. This new strategy leverages the BM25 algorithm to identify chunks of text relevant to the page's title, description, keywords, or a user-provided query.
  * The flag in the content scraper is used to filter content based on title, meta description, and keywords.


```
   
 .  
  (, ):
    ()  :
      ()
       .(, , )
    (.) # Or result.fit_markdown for the markdown version
    (.) # Or result.fit_html to show HTML with only the filtered content
.((, ))
```

### 3. Raw HTML and Local File Support
  * Added support for crawling local files and raw HTML content directly.
  * Use the prefix for local file paths.
  * Use the prefix for raw HTML strings.


```
  (, , ):
          
    
     .()
   .:
    ()
    (.)
# Example usage with local file and raw HTML
  ():
    ()  :
    
     (
      , ..(), 
    )
    
     (, "<h1>Raw Test</h1><p>This is raw HTML.</p>")
    
.(())
```

  * New asynchronous crawler strategy implemented using Playwright.
  * class introduced for improved browser session handling, offering features like persistent browser sessions between requests (using parameter) and browser process monitoring.
  * Updated to tf-playwright-stealth for enhanced stealth capabilities.


### 5. API Server & Cache Improvements
  * Added CORS support to API server.
  * Cache database updated to store response headers and downloaded files information. It utilizes a file system approach to manage large content efficiently.
  * New, more efficient caching database built using xxhash and file system approach.
  * Introduced enum (, , , , ) and parameter in AsyncWebCrawler for fine-grained cache control. This replaces , , , and .


  * Removed legacy cache control flags: , , , , and . These have been superseded by .


  * API server now requires an API token for authentication, configurable with the environment variable. This enhances API security.
  * Added synchronous crawl endpoint for immediate result retrieval, and direct crawl endpoint bypassing the task queue.


  * The synchronous version of is being phased out. While still available via , it will eventually be removed. Transition to is strongly recommended. Boolean cache control flags in are also deprecated, migrate to using the parameter. See examples in the "New Features" section above for correct usage.


  * Resolved issue with browser context closing unexpectedly in Docker. This significantly improves stability, particularly within containerized environments.
  * Fixed memory leaks associated with incorrect asynchronous cleanup by removing the method and ensuring the browser context is closed explicitly using context managers.
  * Improved error handling in . More detailed error messages and suggestions for debugging will minimize frustration when running into unexpected issues.
  * Fixed issue with incorrect text parsing in specific HTML structures.


### Example of migrating to the new CacheMode:
## [0.3.74] - November 13, 2024
  1. (Nov 14, 2024)
     * Added capability for users to specify download folders
     * Implemented file download tracking in crowd result object
  2. (Nov 14, 2024)
     * Introduced Relevance Content Filter as an improvement over Fit Markdown
     * Implemented BM25 algorithm for content relevance matching
  3. **Local File and Raw HTML Support** (Nov 13, 2024)
     * Added support for processing local files
     * Implemented raw HTML input handling in AsyncWebCrawler
  4. (Nov 12, 2024)
     * Implemented new async crawler strategy using Playwright
     * Introduced ManagedBrowser for better browser session handling
     * Added support for persistent browser sessions
     * Updated from playwright_stealth to tf-playwright-stealth
  5. 

## [0.3.731] - November 13, 2024
  * Support for raw HTML and local file crawling via URL prefixes ('raw:', 'file://')
  * Browser process monitoring for managed browser instances
  * Screenshot capability for raw HTML and local file content
  * Response headers storage in cache database
  * New flag for optional markdown generation


  * Switched HTML parser from 'html.parser' to 'lxml' for ~4x performance improvement
  * Optimized BeautifulSoup text conversion and element selection
  * Pre-compiled regular expressions for better performance
  * Response headers now stored alongside HTML in cache


  * method from AsyncPlaywrightCrawlerStrategy to prevent async cleanup issues


  * Issue #256: Added support for crawling raw HTML content
  * Issue #253: Implemented file:// protocol handling
  * Missing response headers in cached results
  * Memory leaks from improper async cleanup


## [v0.3.731] - 2024-11-13 Changelog for Issue 256 Fix
  * Fixed: Browser context unexpectedly closing in Docker environment during crawl operations.
  * Removed: method from AsyncPlaywrightCrawlerStrategy to prevent unreliable asynchronous cleanup, ensuring - browser context is closed explicitly within context managers.
  * Added: Monitoring for ManagedBrowser subprocess to detect and log unexpected terminations.
  * Updated: Dockerfile configurations to expose debugging port (9222) and allocate additional shared memory for improved browser stability.
  * Improved: Error handling and resource cleanup processes for browser lifecycle management within the Docker environment.


  *     * Added comprehensive system diagnostics tool
    * Available through package hub and CLI
    * Provides automated troubleshooting and system health checks
    * Includes detailed reporting of configuration issues
  *     * Released complete Docker implementation for API server
    * Added comprehensive documentation for Docker deployment
  *     * Added support for user-controlled browser instances
    * Implemented class for better browser lifecycle management
    * Added ability to connect to existing Chrome DevTools Protocol (CDP) endpoints
    * Introduced user data directory support for persistent browser profiles
  *     * Added HTML tag preservation feature during markdown conversion
    * Introduced configurable tag preservation system
    * Improved pre-tag and code block handling
    * Added support for nested preserved tags with attribute retention


  *     * Added flag to ignore body visibility for problematic pages
    * Improved browser process cleanup and management
    * Enhanced temporary directory handling for browser profiles
    * Added configurable browser launch arguments
  *     * Implemented connection pooling for better performance
    * Added retry logic for database operations
    * Improved error handling and logging
    * Enhanced cleanup procedures for database connections
  *     * Added memory and CPU monitoring
    * Implemented dynamic task slot allocation based on system resources


  *     * Moved version management to dedicated _version.py file
    * Improved error handling throughout the codebase
    * Enhanced logging system with better error reporting
    * Reorganized core components for better maintainability


  * Fixed issues with browser process termination
  * Improved handling of connection timeouts
  * Enhanced error recovery in database operations
  * Fixed memory leaks in long-running processes


  * Updated core dependencies with more flexible version constraints
  * Added new development dependencies for testing


  * Changed default browser handling behavior
  * Modified database connection management approach
  * Updated API response structure for better consistency


When upgrading to v0.3.73, be aware of the following changes:
  1.      * Review Docker documentation for new deployment options
     * Update environment configurations as needed
  2. If using custom browser management:
     * Update browser initialization code to use new ManagedBrowser class
  3.      * Check custom database queries for compatibility with new connection pooling
     * Update error handling to work with new retry logic
  4.      * Run doctor command for system diagnostics: 
     * Review generated reports for potential issues
     * Follow recommended fixes for any identified problems


This commit introduces several key enhancements, including improved error handling and robust database operations in , which now features a connection pool and retry logic for better reliability. Updates to the README.md provide clearer instructions and a better user experience with links to documentation sections. The file has been refined to include additional directories, while the async web crawler now utilizes a managed browser for more efficient crawling. Furthermore, multiple dependency updates and introduction of the class enhance text extraction capabilities.
  * preserve_tags: Added support for preserving specific HTML tags during markdown conversion.
  * Smart overlay removal system in AsyncPlaywrightCrawlerStrategy: 
    * Automatic removal of popups, modals, and cookie notices
    * Detection and removal of fixed/sticky position elements
    * Cleaning of empty block elements
  * Enhanced screenshot capabilities: 
    * Improved screenshot handling with existing page context
    * Better error handling with fallback error images
  * New URL normalization utilities: 
    * function for consistent URL formatting
    * function for better link classification
  * Custom base directory support for cache storage: 
    * Allows specifying alternative locations for folder


  * Link handling improvements: 
    * Improved handling of special URL protocols
    * Support for anchor links and protocol-relative URLs
  * Configuration refinements: 
    * Streamlined social media domain list
    * More focused external content filtering
  * LLM extraction strategy: 
    * Added support for separate API base URL via parameter
    * Better handling of base URLs in configuration


  * Screenshot functionality: 
    * Resolved issues with screenshot timing and context
    * Improved error handling and recovery
  * Link processing: 
    * Fixed URL normalization edge cases
    * Better handling of invalid URLs
    * Improved error messages for link processing failures


  * The overlay removal system uses advanced JavaScript injection for better compatibility
  * URL normalization handles special cases like mailto:, tel:, and protocol-relative URLs
  * Screenshot system now reuses existing page context for better performance
  * Link processing maintains separate dictionaries for internal and external links to ensure uniqueness


  * New class: 
    * Smart content extraction based on text density and element scoring
    * Automatic removal of boilerplate content
    * DOM tree analysis for better content identification
    * Configurable thresholds for content detection
  * Advanced proxy support: 
    * Added option for authenticated proxy connections
    * Support for username/password in proxy configuration
  * New content output formats: 
    * : Optimized markdown output with main content focus
    * : Clean HTML with only essential content


  * Image source detection: 
    * Support for multiple image source attributes (, , , etc.)
    * Automatic fallback through potential source attributes
    * Smart handling of srcset attribute
  * External content handling: 
    * Made external link exclusion optional (disabled by default)
    * Improved detection and handling of social media links
    * Better control over external image filtering


  * Image extraction reliability with multiple source attribute checks
  * External link and image handling logic for better accuracy


  * The new uses configurable thresholds for customization
  * Proxy configuration now supports more complex authentication scenarios
  * Content extraction process now provides both regular and optimized outputs


  * Added support for parsing Base64 encoded images in WebScrapingStrategy


  * Forked and integrated a customized version of the html2text library for more control over Markdown generation
  * New configuration options for controlling external content: 
    * Ability to exclude all external links
    * Option to specify domains to exclude (default includes major social media platforms)
    * Control over excluding external images


  * Improved Markdown generation process: 
    * Added fine-grained control over character escaping in Markdown output
    * Enhanced handling of code blocks and pre-formatted text
  * Updated method to use a shorter sleep time (0.5 seconds instead of 500)
  * Enhanced flexibility in with a more generic function


  * Optimized content scraping and processing for better efficiency
  * Enhanced error handling and logging in various components


  * The customized html2text library is now located within the crawl4ai package
  * New configuration options are available in the file for external content handling
  * The class has been updated to accommodate new external content exclusion options


  * New chunking strategies: 
    * : Allows for overlapping chunks of text, useful for maintaining context between chunks.
    * Enhanced : Improved to handle edge cases and last chunks more effectively.


  * Updated in config to 2048 tokens (2^11) for better compatibility with most LLM models.
  * Improved method to use a shorter sleep time (0.5 seconds instead of 500), significantly reducing wait time when closing the crawler.
  * Enhanced flexibility in : 
    * Now uses a more generic function, allowing for easier swapping of embedding models.


  * Addressed potential issues with the sliding window chunking strategy to ensure all text is properly chunked.


  * Added more comprehensive docstrings to chunking strategies for better code documentation.
  * Removed hardcoded device setting in , now using the automatically detected device.
  * Added a new example in for generating a knowledge graph from crawled content.


These updates aim to provide more flexibility in text processing, improve performance, and enhance the overall capabilities of the crawl4ai library. The new chunking strategies, in particular, offer more options for handling large texts in various scenarios.
  1.      * Updated version number from 0.3.7 to 0.3.71.
  2.      * Added option to AsyncPlaywrightCrawlerStrategy for delayed browser closure.
     * Improved context creation with additional options: 
       * Added a cookie to enable cookies by default.
  3.      * Enhanced error messages in AsyncWebCrawler's method.
     * Updated error reporting format for better visibility and consistency.
  4.      * Commented out automatic page and context closure in method to potentially improve performance in certain scenarios.


  * Updated quickstart notebook: 
    * Changed installation command to use the released package instead of GitHub repository.


  * Minor code refactoring and cleanup.


  1.      * Implemented for improved bot detection avoidance.
     * Added for fine-tuned control over stealth parameters.
  2.      * New option to mimic human-like interactions (mouse movements, clicks, keyboard presses).
  3.      * Added option to modify navigator properties, further improving bot detection evasion.
  4.      * New parameter to extract and integrate iframe content into the main page.
  5.      * Support for choosing between Chromium, Firefox, and WebKit browsers.
  6.      * Added support for including links in Markdown content, by definin g a new flag in method.


  1.      * Enhanced error reporting in WebScrapingStrategy with detailed error messages and suggestions.
     * Added console message and error logging for better debugging.
  2.      * Improved image dimension updating and filtering logic.
  3.      * Added support for custom viewport sizes.
     * Implemented delayed content retrieval with parameter.
  4.      * Adjusted default semaphore count for parallel crawling.


  * Fixed an issue where the HTML content could be empty after processing.


  * Added new example demonstrating the use of user simulation and navigator override features.


  * Refactored code for better maintainability and readability.
  * Updated browser launch arguments for improved compatibility and performance.


  * : Introduced parameter to allow waiting before retrieving HTML content. 
    * Useful for pages with delayed content loading.
  * : function now uses (default 60 seconds) instead of a fixed 30-second timeout. 
    * Provides better handling for slow-loading pages.
  * : Set (in milliseconds) when calling .


  * Added support for different browser types (Chromium, Firefox, WebKit).
  * Users can now specify the browser type when initializing AsyncWebCrawler.
  * : Set or when initializing AsyncWebCrawler.


  * Added ability to capture screenshots during crawling.
  * Useful for debugging and content verification.
  * : Set when calling .


### 4. Enhanced LLM Extraction Strategy
  * Added support for multiple LLM providers (OpenAI, Hugging Face, Ollama).
  * : Added support for passing extra arguments to LLM providers via parameter.
  * : Users can now pass custom headers to the extraction strategy.
  * : Specify the desired provider and custom arguments when using .


  * New feature to process and extract content from iframes.
  * : Set in the crawl method.


  * Allows retrieval of content after a specified delay, useful for dynamically loaded content.
  * : Access after crawling.


  * : Now accepts arbitrary keyword arguments, passed directly to the crawler strategy.
  * Allows for more customized setups.


  * Enhanced image handling in WebScrapingStrategy.
  * Added filtering for small, invisible, or irrelevant images.
  * Improved image scoring system for better content relevance.
  * Implemented JavaScript-based image dimension updating for more accurate representation.


  * Automatic database schema updates ensure compatibility with the latest version.


#### 4. Enhanced Error Handling and Logging
  * Improved error messages and logging for easier debugging.


  * Improved handling of base64 encoded images.


  * function now supports additional arguments for more customized API calls to LLM providers.


  * Fixed an issue where image tags were being prematurely removed during content extraction.


  * Updated with examples of: 
    * Using custom headers in LLM extraction.
    * Different LLM provider usage (OpenAI, Hugging Face, Ollama).


  * Refactored code for better maintainability, flexibility, and performance.
  * Enhanced type hinting throughout the codebase for improved development experience.
  * Expanded error handling for more robust operation.


These updates significantly enhance the flexibility, accuracy, and robustness of crawl4ai, providing users with more control and options for their web crawling and content extraction tasks.
Enhance AsyncWebCrawler with smart waiting and screenshot capabilities
  * Implement smart_wait function in AsyncPlaywrightCrawlerStrategy
  * Add screenshot support to AsyncCrawlResponse and AsyncWebCrawler
  * Improve error handling and timeout management in crawling process
  * Fix typo in CrawlResult model (responser_headers -> response_headers)


Significant improvements in text processing and performance:
  * 🚀 : Removed dependency on spaCy model for text chunk labeling in cosine extraction strategy.
  * 🤖 : Implemented text sequence classification using a transformer model for labeling text chunks.
  * ⚡ : Improved model loading speed due to removal of spaCy dependency.
  * 🔧 : Laid groundwork for potential complete removal of spaCy dependency in future versions.


These changes address issue #68 and provide a foundation for faster, more efficient text processing in Crawl4AI.
Major improvements in functionality, performance, and cross-platform compatibility! 🚀
  * 🐳 : Significantly improved Dockerfile for easy installation on Linux, Mac, and Windows.
  * 🌐 : Launched our first official image on Docker Hub for streamlined deployment.
  * 🔧 : Removed dependency on ChromeDriver, now using Selenium's built-in capabilities for better compatibility.
  * 🖼️ : Implemented ability to generate textual descriptions for extracted images from web pages.
  * ⚡ : Various improvements to enhance overall speed and performance.


A big shoutout to our amazing community contributors:
  * for developing the textual description extraction feature.
  * for creating the first official Docker Hub image and fixing Dockerfile errors.
  * for identifying Selenium's new capabilities, helping us reduce dependencies.


Your contributions are driving Crawl4AI forward! 🙌
Minor improvements for a more maintainable codebase:
  * 🔄 Fixed typos in and to improve code readability
  * 🔄 Removed directory from to keep our repository clean and organized


These changes may seem small, but they contribute to a more stable and sustainable codebase. By fixing typos and updating our settings, we're ensuring that our code is easier to maintain and scale in the long run.
A slew of exciting updates to improve the crawler's stability and robustness! 🎉
  * 💻 : Resolved the Windows "charmap" error by adding UTF encoding.
  * 🛡️ : Implemented MaxRetryError exception handling in LocalSeleniumCrawlerStrategy.
  * 🧹 : Improved input sanitization and handled encoding issues in LLMExtractionStrategy.
  * 🚮 : Removed existing database file and initialized a new one.


💡 In this release, we've bumped the version to v0.2.73 and refreshed our documentation to ensure you have the best experience with our project.
  * Supporting website need "with-head" mode to crawl the website with head.
  * Fixing the installation issues for setup.py and dockerfile.


This release brings exciting updates and improvements to our project! 🎉
  * 📚 : Our documentation has been revamped to reflect the latest changes and additions.
  * 🚀 : We've added support for three new modes in setup.py: default, torch, and transformers. This enhances the project's flexibility and usability.
  * 🐳 : The Docker file has been updated to ensure seamless compatibility with the new modes and improvements.
  * 🕷️ **Temporary Solution for Headless Crawling** : We've implemented a temporary solution to overcome issues with crawling websites in headless mode.


These changes aim to improve the overall user experience, provide more flexibility, and enhance the project's performance. We're thrilled to share these updates with you and look forward to continuing to evolve and improve our project!
**Improved Error Handling and Performance** 🚧
  * 🚫 Refactored to handle exceptions and provide better error messages, making it more robust and reliable.
  * 💻 Optimized the function in for improved performance, reducing potential bottlenecks.
  * 💻 Updated with the latest changes, ensuring consistency and accuracy.
  * 🚫 Migrated to to resolve Chrome driver download issues, providing a smoother user experience.


These changes focus on refining the existing codebase, resulting in a more stable, efficient, and user-friendly experience. With these improvements, you can expect fewer errors and better performance in the crawler strategy and utility functions.
  * Speed up twice the extraction function.


  * Fix issue #19: Update Dockerfile to ensure compatibility across multiple platforms.


  * Added five important hooks to the crawler: 
    * on_driver_created: Called when the driver is ready for initializations.
    * before_get_url: Called right before Selenium fetches the URL.
    * after_get_url: Called after Selenium fetches the URL.
    * before_return_html: Called when the data is parsed and ready.
    * on_user_agent_updated: Called when the user changes the user_agent, causing the driver to reinitialize.
  * Added an example in in the example folder under the docs.
  * Enhancement issue #24: Replaced inline HTML tags (e.g., DEL, INS, SUB, ABBR) with textual format for better context handling in LLM.
  * Maintaining the semantic context of inline tags (e.g., abbreviation, DEL, INS) for improved LLM-friendliness.
  * Updated Dockerfile to ensure compatibility across multiple platforms (Hopefully!).


  * Fix issue #22: Use MD5 hash for caching HTML files to handle long URLs


You can’t perform that action at this time. 
