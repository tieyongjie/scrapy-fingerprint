from scrapy import Request
import copy


class FingerprintRequest(Request):
    """
    Scrapy ``Request`` subclass providing additional arguments
    """

    def __init__(self, url, callback=None, method: str = "GET", timeout=None, meta=None, data=None,
                 impersonate=None,
                 *args, **kwargs):
        """
        :param url: request url
        :param callback: callback
        :param wait_for: wait for some element to load, also supports dict
        :param method: Request mode, such as get、post, default is get
        """
        # use meta info to save args
        meta = copy.deepcopy(meta) or {}
        fingerprint_meta = meta.get('fingerprint') or {}
        self.timeout = fingerprint_meta.get('timeout') if fingerprint_meta.get(
            'timeout') is not None else timeout
        self.data = fingerprint_meta.get('data') if fingerprint_meta.get(
            'data') is not None else data
        self.method = fingerprint_meta.get('method') if fingerprint_meta.get('method') is not None else str(
            method).upper()
        self.impersonate = fingerprint_meta.get('impersonate') if fingerprint_meta.get(
            'impersonate') is not None else impersonate
        fingerprint_meta = meta.setdefault('fingerprint', {})
        fingerprint_meta['method'] = self.method
        fingerprint_meta['timeout'] = self.timeout
        fingerprint_meta["data"] = self.data
        fingerprint_meta["impersonate"] = self.impersonate
        super().__init__(url, callback, meta=meta, *args, **kwargs)
