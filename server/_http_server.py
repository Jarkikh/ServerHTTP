from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from server.handler import Handler
from server.http_parser import HttpRequest


class Server(TCPServer):
    message_separator = b'\r\n\r\n'

    def __init__(self, config):
        super().__init__()
        self.config = config
        Handler.configure(self.config.get('document_root'))

    async def handle_stream(self, stream, address):
        while True:
            try:
                request = await stream.read_until(self.message_separator)
            except StreamClosedError:
                stream.close(exc_info=True)
                return
            try:
                r = HttpRequest()
                r.parse(request)
                handler = Handler(r)

                response = handler.get_response()

                await stream.write(response)
                stream.close()
            except StreamClosedError:
                stream.close(exc_info=True)
                return
