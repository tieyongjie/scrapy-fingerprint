import asyncio
import random

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.conf import get_config
from twisted.internet.defer import Deferred
from curl_cffi.requests import AsyncSession


def as_deferred(f):
    return Deferred.fromFuture(asyncio.ensure_future(f))


class FingerprintMiddleware(object):
    def __init__(self, user, password, server, proxy_port):
        self.user = user
        self.password = password
        self.server = server
        self.proxy_port = proxy_port
        if self.user:
            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host": self.server,
                "port": self.proxy_port,
                "user": self.user,
                "pass": self.password,
            }
            self.proxies = {
                'http': proxyMeta,
                'https': proxyMeta,
            }
        else:
            self.proxies = None

    @classmethod
    def from_crawler(cls, crawler):
        user = crawler.settings.get('PROXY_USER')
        password = crawler.settings.get('PROXY_PASS')
        server = crawler.settings.get('PROXY_HOST')
        proxy_port = crawler.settings.get('PROXY_PORT')
        s = cls(user=user, password=password, server=server, proxy_port=proxy_port)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        pass

    async def _process_request(self, request, spider):
        fingerprint_meta = request.meta.get('fingerprint') or {}
        impersonate = fingerprint_meta.get("impersonate", random.choice(
            ["chrome99", "chrome101", "chrome110", "edge99", "edge101", "chrome107"]))
        # impersonate = "chrome107"
        async with AsyncSession() as s:
            if fingerprint_meta.get("method") == "GET":
                response = await s.get(request.url, impersonate=impersonate, proxies=self.proxies,
                                       timeout=fingerprint_meta.get("timeout", 60))
            else:
                data = fingerprint_meta.get("data")
                response = await s.post(request.url, impersonate=impersonate, data=data, proxies=self.proxies,
                                        timeout=fingerprint_meta.get("timeout", 60))
            html = response.text
            response = HtmlResponse(
                request.url,
                # status=response.status,
                # headers=response.headers,
                body=str.encode(html),
                encoding='utf-8',
                request=request
            )
            return response

    def process_request(self, request, spider):
        return as_deferred(self._process_request(request, spider))
