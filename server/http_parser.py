import urllib.parse


class HttpRequest:
    def __init__(self):
        self.method = None
        self.url = None
        self.http_version = None
        self.headers = None

    @staticmethod
    def url_parse(uri):
        if '%' not in uri:
            return uri

        hex_synmb = '0123456789ABCDEFabcdef'

        uri = uri.encode()

        res = []
        chunks = uri.split(b'%')

        res.append(chunks[0])

        hex_char = {(first+second).encode(): bytes.fromhex(first+second)
                    for first in hex_synmb
                    for second in hex_synmb}

        for i in range(1, len(chunks)):
            chunk = chunks[i][:2]
            res.append(hex_char[chunk].decode('utf-8'))
            res.append(chunks[i][2:])

        return ''.join(res)


    @staticmethod
    def url_remove_params(url):
        try:
            ind = url.index('?')
        except ValueError:
            return url

        return url[:ind]

    def parse(self, http_request):
        http_request_str = http_request.decode()
        http_path, *headers_str = http_request_str.split('\r\n')
        self.method, self.url, self.http_version = http_path.split()

        self.url = self.url_remove_params(self.url)

        self.url = urllib.parse.unquote(self.url)
        # self.url = self.url_parse(self.url)

        print(self.url)

        self.headers = {}

        for header in headers_str:
            if not header:
                continue

            key, value = header.split(':', 1)
            self.headers[key.strip()] = value.strip()

        # self.headers = {header.split(':')[0].strip(): header.split(':')[1].strip() for header in headers_str if header}
