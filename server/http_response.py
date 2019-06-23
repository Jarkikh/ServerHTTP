import os
from email.utils import formatdate


class HttpResponse:
    def __init__(self):
        self.http_code = 200
        self.http_status = ''
        self.body = b''
        self.headers = {}

        self._available_statuses = {
            200: 'OK',
            404: 'Not Found',
            403: 'Forbidden',
            405: 'Method Not Allowed'
        }

        self._available_types = {
            '.css': 'text/css',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.html': 'text/html',
            '.js': 'text/javascript',
            '.gif': 'image/gif',
            '.swf': 'application/x-shockwave-flash'
        }

    def _get_default_headers(self):
        headers = {
            'Server': 'Grisha server',
            'Date': formatdate(usegmt=True),
            'Connection': 'closed'
        }

        return headers

    def set_code(self, code):
        self.http_code = code
        self.http_status = self._available_statuses.get(code)

        if self.http_status is None:
            raise Exception('This status code is unavailable')

    def set_body(self, body):
        self.body = body
        self.set_content_len()

    def set_content_len(self, path=None):
        if not path:
            content_len = len(self.body)
        else:
            content_len = os.path.getsize(path)

        self.headers.update({
            'Content-Length': content_len,
        })

    def set_content_type(self, file_name):
        self.headers['Content-Type'] = self._available_types.get(file_name.suffix, 'text/html')

    def set_headers(self, headers):
        self.headers = headers

    def build(self):
        header = f'HTTP/1.1 {self.http_code} {self.http_status}'
        headers = [f'{k}: {v}' for k, v in {**self.headers, **self._get_default_headers()}.items()]
        headers = '\r\n'.join(headers)
        rsponse = header.encode() + b'\r\n' + headers.encode() + b'\r\n\r\n' + self.body
        return rsponse
