# scrapy-fingerprint

## Description
Scrapy - fingerprint is based on [curl_cffi] (https://github.com/yifeikong/curl_cffi), which is used in the packaging of scrapy TLS or JA3 fingerprints of simulated browser requests

**github**:https://github.com/tieyongjie/scrapy-fingerprint



## Installation

```bash
pip install scrapy_fingerprint
```

## Usage

After creating the scrapy project, add the proxy by adding the following configuration in settings.py

```python
# proxy 链接配置
PROXY_HOST = 'http-dynamic-S02.xiaoxiangdaili.com'
PROXY_PORT = 10030
PROXY_USER = '******'
PROXY_PASS = '******'
```

And you also need to enable download handler in `DOWNLOAD_HANDLERS` in settings.py

```bash
DOWNLOAD_HANDLERS = {
    'http': ('scrapy_fingerprint.fingerprint_download_handler.'
             'FingerprintDownloadHandler'),
    'https': ('scrapy_fingerprint.fingerprint_download_handler.'
              'FingerprintDownloadHandler'),
}
```

You can use FingerprintRequest to make a request with a browser fingerprint

```python
yield FingerprintRequest(url=url, callback=self.parse)
```

You can also add impersonate in FingerprintRequest

```python
import scrapy

yield scrapy.Request(url, callback=self.parse, meta={"impersonate": "chrome107"})
```

impersonate **defaults** to random browser fingerprints

