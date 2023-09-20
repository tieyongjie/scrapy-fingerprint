# scrapy-fingerprint

## Description
Scrapy - fingerprint is based on [curl_cffi] (https://github.com/yifeikong/curl_cffi), which is used in the packaging of scrapy TLS or JA3 fingerprints of simulated browser requests

**github**:https://github.com/tieyongjie/scrapy-fingerprint



## Installation

```bash
pip install scrapy_fingerprint
```

## Usage

After creating the scrapy project, add the proxy by adding the following configuration in setting.py

```python
# proxy 链接配置
PROXY_HOST = 'http-dynamic-S02.xiaoxiangdaili.com'
PROXY_PORT = 10030
PROXY_USER = '******'
PROXY_PASS = '******'
```

And you also need to enable FingerprintMiddleware in `DOWNLOADER_MIDDLEWARES`:

```bash
'scrapy_fingerprint.fingerprintmiddlewares.FingerprintMiddleware': 543,
```

You can use FingerprintRequest to make a request with a browser fingerprint

```python
yield FingerprintRequest(url=url, callback=self.parse)
```

You can also add impersonate in FingerprintRequest

```python
yield FingerprintRequest(url=url, callback=self.parse,impersonate="chrome107")
```

impersonate **defaults** to random browser fingerprints

POST  request

```python
payload = {}
yield FingerprintRequest(url, method='POST', callback=self.parse,data=json.dumps(payload))
```

