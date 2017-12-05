import asyncio
import unittest

from asyncrequests import get

from . import UnitTestBase

class TestGet(unittest.TestCase, UnitTestBase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def basics(self, resp):
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['status'], "success")
        self.assertEqual(isinstance(resp.headers, dict), True)
        self.assertEqual(resp.json['method'], "GET")

    async def get_simple(self, future):
        resp = await get('%s/' % self.server_addr)
        future.set_result(resp)

    def test_get_simple(self):
        future = asyncio.Future()
        asyncio.ensure_future(self.get_simple(future))
        self.loop.run_until_complete(future)
        resp = future.result()
        self.basics(resp)

    async def get_query_parameter(self, future):
        resp = await get('%s/?test=arg_test' % self.server_addr)
        future.set_result(resp)

    def test_get_query_parameter(self):
        future = asyncio.Future()
        asyncio.ensure_future(self.get_query_parameter(future))
        self.loop.run_until_complete(future)
        resp = future.result()
        self.basics(resp)
        self.assertEqual(resp.json['args'], [{"test":"arg_test"}])