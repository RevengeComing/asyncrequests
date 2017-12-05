from .__version__ import __version__

from httptools import parse_url

def default_user_agent(name="python-asyncrequests"):
    """
    Return a string representing the default user agent.
    :rtype: str
    """
    return '%s/%s' % (name, __version__)

def default_headers():
    """
    Return a dict representing default headers.

    :rtype: dict
    """
    return {
        'User-Agent': default_user_agent(),
        'Accept-Encoding': ', '.join(('gzip', 'deflate')),
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

def get_parsed_url(url):
    if not isinstance(url, bytes):
        url = bytes(url.encode('utf8'))
    return parse_url(url)