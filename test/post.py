import asyncio
import unittest

from asyncrequests import get, post

from . import UnitTestBase

class TestPost(unittest.TestCase, UnitTestBase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def basics(self, resp):
        self.assertEqual(resp.json['method'], "POST")        

    async def post_simple(self, future):
        resp = await post('%s/' % self.server_addr)
        future.set_result(resp)

    def test_post_simple(self):
        future = asyncio.Future()
        asyncio.ensure_future(self.post_simple(future))
        self.loop.run_until_complete(future)
        resp = future.result()
        self.basics(resp)

    async def post_query_parameter(self, future):
        resp = await post('%s/?test=arg_test' % self.server_addr)
        future.set_result(resp)

    def test_post_query_parameter(self):
        future = asyncio.Future()
        asyncio.ensure_future(self.post_query_parameter(future))
        self.loop.run_until_complete(future)
        resp = future.result()
        self.basics(resp)
        self.assertEqual(resp.json['method'], "POST")
        self.assertEqual(resp.json['args'], [{"test":"arg_test"}])

    async def post_body_parameter(self, future):
        resp = await post('%s/' % self.server_addr, data={'asd':'123'})
        future.set_result(resp)

    def test_parameter_post(self):
        future = asyncio.Future()
        asyncio.ensure_future(self.post_body_parameter(future))
        self.loop.run_until_complete(future)
        resp = future.result()
        self.basics(resp)
        self.assertEqual(resp.json['method'], "POST")
        self.assertEqual(resp.json['body'], [{"asd":"123"}])

    async def json_post(self, future):
        resp = await post('%s/?test=arg_test' % self.server_addr)
        future.set_result(resp)

    def test_json_post(self):
        pass

    async def multipart_post(self, future):
        resp = await post('http://127.0.0.1:5000/?test=arg_test')
        future.set_result(resp)

    def test_multipart_post(self):
        pass