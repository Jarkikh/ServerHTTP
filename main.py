import multiprocessing
import os

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream, StreamClosedError
from tornado.netutil import bind_sockets, add_accept_handler
from tornado.process import fork_processes

from server.handler import Handler
from server.http_parser import HttpRequest

CONF_PATH = '/etc/httpd.conf'

config = {}

with open(CONF_PATH) as f:
    for line in f.readlines():
        key, value = line.split()
        config[key] = value


Handler.configure(config.get('document_root'))


async def handle_stream(stream, address):
    while True:
        try:
            request = await stream.read_until(b'\r\n\r\n')
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


def callback(connection, address):
    stream = IOStream(
        connection,
        max_buffer_size=1024,
        read_chunk_size=512,
    )

    future = handle_stream(stream, address)
    if future is not None:
        IOLoop.current().add_future(
            gen.convert_yielded(future), lambda f: f.result()
        )


def init(sockets):
    print('Starting the server...')
    for socket in sockets:
        add_accept_handler(socket, callback)
    IOLoop.instance().start()
    print('Server has shut down.')


if __name__ == '__main__':
    sockets = bind_sockets(80)

    workers = []
    for i in range(3):
        worker = multiprocessing.Process(target=init, args=(sockets,))
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()
