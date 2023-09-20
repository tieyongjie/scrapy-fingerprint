import scrapy

from scrapy_fingerprint.request import FingerprintRequest


class DemocrawlSpider(scrapy.Spider):
    name = "democrawl"
    allowed_domains = []
    def start_requests(self):
        url = "https://tls.browserleaks.com/json"
        yield FingerprintRequest(url=url, callback=self.parse, impersonate="chrome110")

    def parse(self, response):
        print(response.text)
