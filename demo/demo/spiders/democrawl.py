import scrapy

class DemocrawlSpider(scrapy.Spider):
    name = "democrawl"
    allowed_domains = []
    def start_requests(self):
        url = "https://tls.browserleaks.com/json"
        yield scrapy.Request(url=url, callback=self.parse, meta={"impersonate": "chrome110"})

    def parse(self, response):
        print(response.text)
