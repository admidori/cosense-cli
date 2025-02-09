from cosense.lib.resource import wrapped_resource
from cosense.lib.request import make_request
from functools import partial

class Client(object):
    base_url = "https://scrapbox.io/api/pages"

    def __init__(self, sid=None):
        self.sid = sid

    def __getattr__(self, name, **kwargs):
        if name not in ("get"):
            raise AttributeError
        return partial(self._request, name, **kwargs)

    def _request(self, method, resource, **kwargs):
        url = self._resolve_resource_name(resource)
        return wrapped_resource(make_request(method, url, self.sid, kwargs))

    def _resolve_resource_name(self, name):
        name = name.rstrip("/").lstrip("/")
        return '%s/%s' % (self.base_url, name)
