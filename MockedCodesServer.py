import logging
import http.server
import socketserver
from http.client import responses

log = logging.getLogger('http_logger')
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f"HTTPmockStatus.log")
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def code_warning(self):
        log.error(f"Code is not present or is out of range {self.mock_code}.")
        self.send_response(501)
        self.end_headers()
        self.wfile.write(b"Code is not present or is out of range.")

    def path_warning(self):
        log.warning(f"Path does not contain 'mockserver'. Default 200 will be sended.")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"To get mocked status codes, url shoud include '/mockserver/<code>'")

    def do_GET(self):
        if '/favicon.ico' in self.path:
            return
        log.info(f"GET request: '{self.path}'")
        if '/mockserver/' not in self.path:
            return (self.path_warning())
        self.mock_code = self.path.split('/')[-1]
        try:
            self.mock_code = int(self.mock_code)
            log.info(f"Requested code founded {self.mock_code}")
        except:
            return (self.code_warning())
        try:
            self.mock_msg = responses[self.mock_code]
        except KeyError:
            log.error(f"Requested code is out of range {self.mock_code}")
            return (self.code_warning())
        self.send_response(self.mock_code)
        self.end_headers()
        self.wfile.write(bytes(self.mock_msg, "UTF-8"))

class MyHTTPServer(socketserver.TCPServer):
    def __init__(self, host, port):
        self.server_address = (host, port)
        super().__init__(self.server_address, HTTPRequestHandler)

if __name__ == '__main__':
    HOST, PORT = 'localhost', 8000
    httpd = MyHTTPServer(HOST, PORT)
    log.info(f"Server running at -> {HOST}:{PORT}")
    print(f"Listening at {HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log.warning(f'Server was stopped by user or signal')
