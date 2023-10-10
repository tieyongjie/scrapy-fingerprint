import asyncio
import random
from time import time
from urllib.parse import urldefrag

import scrapy
from scrapy.http import HtmlResponse
from scrapy.spiders import Spider
from scrapy.http import Response

from twisted.internet.defer import Deferred
from twisted.internet.error import TimeoutError

from curl_cffi.requests import AsyncSession
from curl_cffi import const
from curl_cffi import curl


def as_deferred(f):
    return Deferred.fromFuture(asyncio.ensure_future(f))


class FingerprintDownloadHandler:

    def __init__(self, user, password, server, proxy_port):
        self.user = user
        self.password = password
        self.server = server
        self.proxy_port = proxy_port
        if self.user:
            proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host": self.server,
                "port": self.proxy_port,
                "user": self.user,
                "pass": self.password,
            }
            self.proxies = {
                "http": proxy_meta,
                "https": proxy_meta,
            }
        else:
            self.proxies = None

    @classmethod
    def from_crawler(cls, crawler):
        user = crawler.settings.get("PROXY_USER")
        password = crawler.settings.get("PROXY_PASS")
        server = crawler.settings.get("PROXY_HOST")
        proxy_port = crawler.settings.get("PROXY_PORT")
        s = cls(user=user,
                password=password,
                server=server,
                proxy_port=proxy_port)
        return s

    async def _download_request(self, request):
        async with AsyncSession() as s:
            impersonate = request.meta.get("impersonate") or random.choice([
                "chrome99", "chrome101", "chrome110", "edge99", "edge101",
                "chrome107"
            ])

            timeout = request.meta.get("download_timeout") or 30

            try:
                response = await s.request(
                    request.method,
                    request.url,
                    data=request.body,
                    headers=request.headers.to_unicode_dict(),
                    proxies=self.proxies,
                    timeout=timeout,
                    impersonate=impersonate)
            except curl.CurlError as e:
                if e.code == const.CurlECode.OPERATION_TIMEDOUT:
                    url = urldefrag(request.url)[0]
                    raise TimeoutError(
                        f"Getting {url} took longer than {timeout} seconds."
                    ) from e
                raise e

            response = HtmlResponse(
                request.url,
                encoding=response.encoding,
                status=response.status_code,
                # headers=response.headers,
                body=response.content,
                request=request
            )
            return response

    def download_request(self, request: scrapy.Request,
                         spider: Spider) -> Deferred:
        del spider
        start_time = time()
        d = as_deferred(self._download_request(request))
        d.addCallback(self._cb_latency, request, start_time)

        return d

    @staticmethod
    def _cb_latency(response: Response, request: scrapy.Request,
                    start_time: float) -> Response:
        request.meta["download_latency"] = time() - start_time
        return response
