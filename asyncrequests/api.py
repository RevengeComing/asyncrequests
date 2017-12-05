from .session import Session

__all__ = [
    'request', 'get', 'options', 'head', 'post',
    'put', 'patch', 'delete'
]


async def request(method, url, **kwargs):
    with Session() as session:
        return await session.request(method, url, **kwargs)

async def get(url, params=None, **kwargs):
    # kwargs.setdefault('allow_redirects', True)
    return await request('get', url, **kwargs)

async def options(url, **kwargs):
    raise NotImplemented()

async def head(url, **kwargs):
    raise NotImplemented()

async def post(url, data=None, json=None, **kwargs):
    return await request('post', url, data=data, json=json,**kwargs)

async def put(url, data=None, **kwargs):
    raise NotImplemented()

async def patch(url, data=None, **kwargs):
    raise NotImplemented()

async def delete(url, **kwargs):
    raise NotImplemented()