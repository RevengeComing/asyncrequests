import logging
import asyncio
import asyncrequests

loop = asyncio.get_event_loop()
logging.getLogger('async_requests').setLevel(logging.DEBUG)

async def start(loop):
    resp = await asyncrequests.get('http://127.0.0.1:5000', body_json={"test":'1243'})
    print(resp.body)
    print(resp.headers)
    resp2 = await asyncrequests.get('http://127.0.0.1:5000', data={"test":'1243'})
    print(resp2.body)
    resp3 = await asyncrequests.get('http://127.0.0.1:5000', params={"test":'1243'})
    print(resp3.body)
    loop.stop()

loop.run_until_complete(start(loop))
loop.run_forever()