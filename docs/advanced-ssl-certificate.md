The class encapsulates an SSL certificate’s data and allows exporting it in various formats (PEM, DER, JSON, or text). It’s used within whenever you set in your . 
```
 :
  """
  Represents an SSL certificate with methods to export in various formats.
  Main Methods:
  - from_url(url, timeout=10)
  - from_file(file_path)
  - from_binary(binary_data)
  - to_json(filepath=None)
  - to_pem(filepath=None)
  - to_der(filepath=None)
  ...
  Common Properties:
  - issuer
  - subject
  - valid_from
  - valid_until
  - fingerprint
  """

```

  1. You certificate fetching in your crawl by: 
  2. After , if is present, it’s an instance of . 
  3. You can basic properties (issuer, subject, validity) or them in multiple formats.


Manually load an SSL certificate from a given URL (port 443). Typically used internally, but you can call it directly if you want:
Load from a file containing certificate data in ASN.1 or DER. Rarely needed unless you have local cert files:
Initialize from raw binary. E.g., if you captured it from a socket or another source:
After obtaining a instance (e.g. from a crawl), you can read:
1. - E.g. `{"CN": "My Root CA", "O": "..."}` 2. - E.g. 3. - NotBefore date/time. Often in ASN.1/UTC format. 4. - NotAfter date/time. 5. - The SHA-256 digest (lowercase hex). - E.g. 
Once you have a object, you can or it:
  * Returns a JSON string containing the parsed certificate fields. 
  * If is provided, saves it to disk instead, returning .


```
json_data = cert.to_json() 
cert.to_json() # writes file, returns None

```

  * Returns a PEM-encoded string (common for web servers). 
  * If is provided, saves it to disk instead.


```
pem_str = cert.to_pem()       
cert.to_pem()   

```

  * Returns the original DER (binary ASN.1) bytes. 
  * If is specified, writes the bytes there instead.


  * If you see a method like , it typically returns an OpenSSL-style textual representation. 
  * Not always needed, but can help for debugging or manual inspection.


## 5. Example Usage in Crawl4AI
Below is a minimal sample showing how the crawler obtains an SSL cert from a site, then reads or exports it. The code snippet:
```
import asyncio
import os
 crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
async def ():
  tmp_dir = 
  os.(tmp_dir, exist_ok=True)
  config = (
    fetch_ssl_certificate=True,
    cache_mode=CacheMode.BYPASS
  )
  async with () as crawler:
    result = await crawler.(, config=config)
    if result.success and result.ssl_certificate:
      cert = result.ssl_certificate
      # . Basic Info
      (, cert.issuer.(, ))
      (, cert.valid_until)
      (, cert.fingerprint)
      # . Export
      cert.(os.path.(tmp_dir, ))
      cert.(os.path.(tmp_dir, ))
      cert.(os.path.(tmp_dir, ))
if __name__ == :
  asyncio.(())

```

## 6. Notes & Best Practices
1. : internally uses a default socket connect and wraps SSL. 2. : The certificate is loaded in ASN.1 (DER) form, then re-parsed by . 3. : This does validate the certificate chain or trust store. It only fetches and parses. 4. : Within Crawl4AI, you typically just set in ; the final result’s is automatically built. 5. : If you need to store or analyze a cert, the and are quite universal.
  * is a convenience class for capturing and exporting the from your crawled site(s). 
  * Common usage is in the field, accessible after setting . 
  * Offers quick access to essential certificate details (, , ) and is easy to export (PEM, DER, JSON) for further analysis or server usage.


Use it whenever you need into a site’s certificate or require some form of cryptographic or compliance check.
