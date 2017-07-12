import asyncio
from asyncio import Protocol, get_event_loop
from httptools import parse_url, HttpResponseParser
from httptools.parser.parser import URL

__all__ = [
    'get',
    'post',
    'Client',
]


class Response():
    __slot__ = [
        'body', 'data', 'headers', 'protocol'
    ]

    def __init__(self, data, protocol):
        self.parser = HttpResponseParser(self)
        self.headers = {}
        self.body = b""
        self.data = data
        self.protocol = protocol

    def on_header(self, name, value):
        self.headers[name] = value

    def on_body(self, body):
        if body:
            self.body = self.body + body

    def on_message_complete(self):
        self.protocol.return_event.set()


class ReturnResponseEvent(asyncio.Event):
    pass


class Session(Protocol):
    __all__ = [
        "cookie", "loop", 'resp', 'host', 'return_event'
    ]

    user_agent = "Python AsyncRequests v0.1.0"

    def __init__(self, host, loop=None):
        self.loop = loop or get_event_loop()
        self.host = host
        self.resp = None
        self.cookie = None
        self.return_event = ReturnResponseEvent()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if not self.resp:
            self.resp = Response(data, self)
        self.resp.parser.feed_data(data)

    async def get(self, url, **kwargs):
        """
        url: absolute path of the request.
        params: uri params
        """
        if not isinstance(url, URL):
            pass
        self.clear()
        return await self.request("GET", url, **kwargs)

    async def post(self):
        pass

    async def put(self):
        pass

    async def delete(self):
        pass

    async def request(self, method, url, headers=None,
                      params=None, cookies=None, json=None):            
        self.send_request_line(method, url, params)
        self.send_headers(headers)
        self.send_request_body(params, json)
        await self.return_event.wait()
        return self.resp

    def send_request_line(self, method, url, params):
        self.transport.write(self.generate_request_line(method, url, params))

    def generate_request_line(self, method, url, params):
        url_path = url.path
        if not url.path:
            url_path = b'/'

        if url.query:
            _url = url_path + b"?" + url.query
        elif params and method == "GET":
            _url = url_path + b"?" + "&".join(
                [ ("%s=%s" % (key, value)) for key, value in params.items()]
            ).encode('ascii')
        else:
            _url = url_path

        return ("%s %s HTTP/1.1\r\n" % (method, _url.decode())).encode('ascii')

    def send_headers(self, headers):
        _headers = self.generate_base_headers()
        if headers:
            for key, value in headers:
                _headers[key] = value
        for key, value in _headers.items():
            self.transport.write(("%s: %s\r\n" % (key, value)).encode('ascii'))
        self.transport.write(b'\r\n')

    def generate_base_headers(self):
        headers = {
            "User-Agent": self.user_agent,
            "Host": self.host.decode(),
            "Connection": "Keep-Alive",
        }
        return headers

    def send_request_body(self, data, json):
        if data:
            pass
        elif json:
            pass

    def clear(self):
        self.resp = None
        self.return_event.clear()

    def close(self):
        print("closed")
        self.transport.close()

async def create_session(loop, client=Session):
    pass

async def get(url, loop=None, session_class=Session, *args, **kwargs):
    loop = loop or get_event_loop()
    if not isinstance(url, bytes):
        url = bytes(url.encode('utf8'))
    parsed_url = parse_url(url)
    coro = loop.create_connection(lambda: session_class(parsed_url.host, loop),
                              parsed_url.host, parsed_url.port or 80)
    session = await coro;
    session = session[1]
    resp = await session.get(parsed_url, *args, **kwargs)
    session.close()
    return resp

def post():
    pass