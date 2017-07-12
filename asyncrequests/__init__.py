import time
import asyncio
import logging

try:
    import ujson
except:
    import json

from asyncio import Protocol, get_event_loop
from httptools import parse_url, HttpResponseParser
from httptools.parser.parser import URL

__all__ = [
    'get',
    'post',
    'Client',
]

FORMAT = '%(asctime)-15s %(levelname)s -> %(message)s'
logging.basicConfig(format=FORMAT)
arlogger = logging.getLogger('async_requests')

active_session = None

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
        if not isinstance(url, URL):
            pass
        self.clear()
        return await self.request("GET", url, **kwargs)

    async def post(self, url, **kwargs):
        if not isinstance(url, URL):
            pass
        self.clear()
        return await self.request("POST", url, **kwargs)

    async def put(self):
        if not isinstance(url, URL):
            pass
        self.clear()
        return await self.request("POST", url, **kwargs)

    async def delete(self):
        if not isinstance(url, URL):
            pass
        self.clear()
        return await self.request("PUT", url, **kwargs)

    async def request(self, method, url, headers=None,
                      params=None, #cookies=None,
                      body_json=None, data=None):
        self.send_request_line(method, url, params)
        self.send_headers(headers, data, body_json)
        self.send_request_body()
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
        elif params:
            _url = url_path + b"?" + "&".join(
                [ ("%s=%s" % (key, value)) for key, value in params.items()]
            ).encode('ascii')
        else:
            _url = url_path

        return ("%s %s HTTP/1.1\r\n" % (method, _url.decode())).encode('ascii')

    def send_headers(self, headers, data, body_json):
        _headers = self.generate_base_headers(data, body_json)
        if headers:
            for key, value in headers:
                _headers[key] = value
        for key, value in _headers.items():
            self.transport.write(("%s: %s\r\n" % (key, value)).encode('ascii'))
        self.transport.write(b'\r\n')

    def generate_base_headers(self, data, body_json):
        headers = {
            "User-Agent": self.user_agent,
            "Host": self.host.decode(),
            "Connection": "Keep-Alive",
        }
        if data or body_json:
            if data:
                self.body_params = "&".join(["%s=%s" % (key, value) for key, value in data.items()])
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
            elif body_json:
                self.body_params = json.dumps(body_json)
                headers['Content-Type'] = 'application/json'
            headers['Content-Length'] = len(self.body_params)

        return headers

    def send_request_body(self):
        self.transport.write(self.body_params.encode('utf8'))

    def clear(self):
        self.resp = None
        self.return_event.clear()

    def close(self):
        self.transport.close()


def get_parsed_url(url):
    if not isinstance(url, bytes):
        url = bytes(url.encode('utf8'))
    return parse_url(url)

async def do_connect(protocol, host, port, try_times=None, loop=None):
    tried_times = 0
    try_times = 1 if try_times == None else try_times
    while tried_times != try_times:
        try:
            loop = loop or get_event_loop()
            coro = loop.create_connection(protocol, host, port or 80)
            session = await coro
            return session
        except OSError:
            tried_times += 1
            if tried_times != try_times:
                print("Server not up retrying in 3 seconds...")
                await asyncio.sleep(3)
            else:
                return

async def get(url, loop=None, session_class=Session, *args, **kwargs):
    parsed_url = get_parsed_url(url)
    session = await do_connect(lambda: session_class(parsed_url.host, loop),
                               parsed_url.host, parsed_url.port or 80,
                               try_times=kwargs.get('try_times'),
                               loop=loop)
    if session == None:
        raise ConnectionRefusedError("Can't connect to server ...")
    else:
        resp = await session[1].get(parsed_url, *args, **kwargs)
        return resp

async def post(url, loop=None, session_class=Session, *args, **kwargs):
    parsed_url = get_parsed_url(url)
    session = await do_connect(lambda: session_class(parsed_url.host, loop),
                               parsed_url.host, parsed_url.port or 80,
                               try_times=kwargs.get('try_times'),
                               loop=loop)
    if session == None:
        raise ConnectionRefusedError("Can't connect to server ...")
    else:
        resp = await session[1].post(parsed_url, *args, **kwargs)
        return resp