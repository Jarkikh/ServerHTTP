from pathlib import Path

from server.http_response import HttpResponse


class Handler:
    allowed_methods = ['GET', 'HEAD']
    base_dir = None

    @classmethod
    def configure(cls, basedir):
        cls.base_dir = Path(basedir)

    def __init__(self, http_request):
        self.http_request = http_request

    def get_response(self):
        response = HttpResponse()
        if self.http_request.method not in self.allowed_methods:
            response.set_code(405)

        path = (self.base_dir / Path(self.http_request.url[1:])).resolve()

        if not str(path).startswith(str(self.base_dir)):
            response.set_code(403)
            return response.build()

        is_dir = False
        if path.is_dir():
            is_dir = True
            path = path / 'index.html'

        if not path.exists():
            if is_dir:
                response.set_code(403)
            else:
                response.set_code(404)

            return response.build()

        response.set_content_type(path)

        if self.http_request.method == 'HEAD':
            response.set_content_len(path)
            return response.build()

        with path.open('rb') as f:
            response.set_body(f.read())

        return response.build()
