from asyncio import get_event_loop

from .connection import Connection
from .models import Request

class Session():

    def __init__(self):
        self.loop = get_event_loop()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    async def request(self, method, url,
            data=None, headers=None, cookies=None, files=None,
            timeout=None, allow_redirects=True, proxies=None,
            stream=None, verify=None, cert=None, json=None):
        """Constructs a :class:`Request <Request>`, sends it.
        Returns :class:`Response <Response>` object.
        """
        req = Request(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            cookies=cookies,
        )

        return await self.send(req)

    async def get(self, url, **kwargs):
        """Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: asyncrequests.Response
        """
        return await self.request('GET', url, **kwargs)

    async def options(self, url, **kwargs):
        return self.request('OPTIONS', url, **kwargs)

    async def head(self, url, **kwargs):
        pass

    async def post(self, url, **kwargs):
        pass

    async def put(self, url, **kwargs):
        pass

    async def patch(self, url, **kwargs):
        pass

    async def delete(self, url, **kwargs):
        pass

    async def send(self, request, **kwargs):
        """Send a given Request.

        :rtype: asyncrequests.Response
        """
        with Connection(request) as connection:
            return await connection.send_request()

    def close(self):
        pass