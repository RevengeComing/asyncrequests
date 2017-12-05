import json
import urllib.parse

from httptools import HttpResponseParser
# from httptools.parser.parser import URL

from .utils import get_parsed_url, default_headers


class Request():
    """A user-created :class:`Request <Request>` object.

    Used to prepare a :class:`PreparedRequest <PreparedRequest>`, which is sent to the server.

    :param method: HTTP method to use.
    :param url: URL to send.
    :param headers: dictionary of headers to send.
    :param files: dictionary of {filename: fileobject} files to multipart upload.
    :param data: the body to attach to the request. If a dictionary is provided, form-encoding will take place.
    :param json: json for the body to attach to the request (if files or data is not specified).
    :param params: dictionary of URL parameters to append to the URL.
    :param auth: Auth handler or (user, pass) tuple.
    :param cookies: dictionary or CookieJar of cookies to attach to this request.

    Usage::

      >>> import asyncrequests
      >>> req = asyncrequests.Request('GET', 'http://httpbin.org/get')
      >>> req.prepare()
      <PreparedRequest [GET]>
    """

    def __init__(self,
            method=None, url=None, headers=None, files=None, data=None,
            params=None, auth=None, cookies=None, json=None):

        # Default empty dicts for dict params.
        data = [] if data is None else data
        files = [] if files is None else files
        headers = {} if headers is None else headers
        params = {} if params is None else params

        self.method = method
        self.url_string = url
        self.url = get_parsed_url(url)
        self.headers = headers
        self.files = files
        self.data = data
        self.json = json
        self.cookies = cookies
        self.params = params

        self.prepare()

    # @property
    # def data(self):
    #     """
    #     Generating bytes that should be sent to target server as request

    #     :rtype: bytes
    #     """
    #     return bdata

    @property
    def port(self):
        if self.url.port:
            return self.url.port
        elif not self.url.port and self.url.schema == b"http":
            return 80
        elif not self.url.port and self.url.schema == b"https":
            return 443

    @property
    def _line(self):
        """
        Generate request line

        :rtype: bytes
        """
        url_path = self.url.path

        if not self.url.path:
            url_path = b'/'

        if self.url.query:
            _url = url_path + b"?" + self.url.query
        
        elif self.params:
            _url = url_path + b"?" + "&".join(
                [ ("%s=%s" % (key, value)) for key, value in params.items()]
            ).encode('ascii')
        
        else:
            _url = url_path

        return ("%s %s HTTP/1.1\r\n" % (self.method, _url.decode())).encode('ascii')

    def set_default_headers(self):
        for key, val in default_headers().items():
            self.headers.setdefault(key, val)
    
    @property
    def _headers(self):
        h = b''
        for key, val in self.headers.items():
            h += ("%s: %s\r\n" % (key, val)).encode()
        return h

    def set_body(self):
        self.body = b""
        if self.method == "POST":
            if self.headers.get('Content-Type') == "application/x-www-form-urlencoded":
                if isinstance(self.data, dict):
                    self.body += urllib.parse.urlencode(self.data).encode('ascii')
                elif isinstance(self.data, str):
                    data = urllib.parse.parse_qs(self.data)
                    self.body += urllib.parse.urlencode(data).encode('ascii')
            elif self.headers.get('Content-Type') == "application/json":
                pass
            elif self.headers.get('Content-Type') == "multipart/form-data":
                pass

    def set_content_length(self):
        content_length = len(self.body)
        if content_length > 0:
            self.headers['Content-Length'] = len(self.body)

    @property
    def _body(self):
        return b"\r\n" + self.body + b"\r\n"

    def set_content_type(self):
        has_data = False;has_json = False;has_files = False
        if self.data: has_data = True
        elif self.json: has_json = True
        if self.files: has_files = True
        if has_data and has_files:
            self.headers['Content-Type'] = 'multipart/form-data'
        elif has_data:
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        elif has_json:
            self.headers['Content-Type'] = 'application/json'
        # print(has_json, has_data, has_files)

    @property
    def req_bytes(self):
        b = self._line
        b += self._headers
        b += self._body
        return b

    def prepare(self):
        self.set_default_headers()
        self.set_content_type()
        self.set_body()
        self.set_content_length()

    def __repr__(self):
        return '<Request [%s]>' % (self.method)


class Response():
    __slot__ = [
        # '_content', 'status_code', 'headers', 'url', 'history',
        # 'encoding', 'reason', 'cookies', 'elapsed', 'request'
        'body', 'data', 'headers'
    ]

    def __init__(self, data):
        parser = HttpResponseParser(self)
        self.headers = {}
        self.body = b""
        self.data = data
        parser.feed_data(self.data)
        self.status_code = parser.get_status_code()

    def on_header(self, name, value):
        self.headers[name.decode()] = value.decode()

    def on_body(self, body):
        if body:
            self.body = self.body + body

    @property
    def text(self):
        return self.body.decode()

    @property
    def json(self):
        return json.loads(self.text)