from asyncio import Queue, open_connection

from .models import Response


class Connection():

    def __init__(self, request):
        self.request = request

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    async def send_request(self):
        self.reader, self.writer = await open_connection(self.request.url.host, self.request.port)

        self.writer.write(self.request.req_bytes)
        await self.writer.drain()

        response_data = await self.reader.read()
        r = Response(response_data)
        return r

    def close(self):
        self.writer.close()