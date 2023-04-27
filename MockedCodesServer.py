import logging
import json
import http.server
import socketserver
from http.client import responses
import argparse
import sys
import inspect
import myFunctions.myFunctions as mF

log = logging.getLogger('http_logger')
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f"HTTPmockStatus.log")
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

class MyMockServer(http.server.SimpleHTTPRequestHandler):
    '''
    at init: load personalized functions
    and init superclass
    '''
    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config', None)
        imF = dir(mF)
        try:
            self.myFnc = {key: getattr(mF, key) \
                            for key in imF \
                            if inspect.isfunction(getattr(mF, key)) \
                            and key.startswith('mock_fnc_')}
        except:
            error_msg('External functions could not be found. '
                      'myFunctions/myFunctions.py should be present '
                      'even if is empty file')
        super().__init__(*args, **kwargs)

    def sender(self):
        self.send_response(int(self.mock_code))
        if len(self.header_content):
            for key, value in self.header_content.items():
                self.send_header(key, value)
        self.end_headers()
        if isinstance(self.response_content, dict):
            rsp = json.dumps(self.response_content)
            log.warning(f'HOLA {rsp.encode()}')
            self.wfile.write(rsp.encode())
        else:
            self.wfile.write(bytes(self.response_content, "UTF-8"))

    def do_mockurl(self):
        '''
        Build mock response for mockurl
        functionality
        '''
        log.info('MOCK-URL request.')
        self.template = self.config['templates']['URL']
        self.mockMode = 'URL'
        self.mock_req = self.path.split('/')[-1]
        self.checkMockCode()
        self.template_response()
        self.template_header()
        self.to_send()

    def get_requested_code(self):
        '''
        Get requested code(s) using config file
        and search it at request
        '''
        result = self.config['templates'][self.mockMode]['request']
        for field in self.config[self.mockMode]['request_field']:
            if isinstance(result, dict):
                result = result.get(field, {})
            elif isinstance(result, list):
                result = [x.get(field, {}) for x in result]
        return (result)

    def do_mockserver(self):
        '''
        Build mock response for mockserver
        functionality.
        '''
        log.info('MOCK-SERVER request mode')
        self.template = self.config['templates'][self.command]
        self.mockMode = self.command
        self.mock_req = self.get_requested_code()
        self.checkMockCode()
        self.req_header = json.dumps(dict(self.headers))
        len = int(self.headers.get('Content-Length', 0))
        request_data = self.rfile.read(len)
        self.req_data = request_data.decode('utf-8')

    def template_response(self):
        '''
        Build body response using template.
        If a mock_fnc_ is founded will be called
        '''
        self.response_content = {}
        for key, value in self.template['response']['data'].items():
            self.response_content[key] = self.myFnc[value](self) \
                if value.startswith('mock_fnc_') \
                else value

    def template_header(self):
        '''
        Build header response using template.
        If a mock_fnc_ is founded will be called
        '''
        self.header_content = {}
        for key, value in self.template['response']['header'].items():
            self.header_content[key] = self.myFnc[value](self) \
                if value.startswith('mock_fnc_') \
                else value

    def get_mock_request(self):
        '''
        EVALUATE REQUEST:
        /mockurl/ if request is sended to and url
        with /mockurl/ in path, response will be
        getted and returned using /mockurl/<code>.
        /mockserver in path will evaluate
        all options...  
        '''
        if '/favicon.ico' in self.path:
            return
        if '/mockurl/' in self.path:
            self.do_mockurl()
        if '/mockserver' in self.path:
            self.do_mockserver()
            pass
        pass

    def code_warning(self):
        log.error(f"Code is not present or is out of range {self.mock_code}.")
        self.send_response(501)
        self.end_headers()
        self.wfile.write(b"Code is not present or is out of range.")

    def path_warning(self):
        log.warning(f"Path does not contain 'mockserver'. Default 200 will be sended.")
        self.send_response(501)
        self.end_headers()
        self.wfile.write(b"To get mocked status codes, url shoud include '/mockserver/<code>'")

    def checkMockCode(self):
        try:
            self.mock_code = int(self.mock_req)
            log.info(f"Requested code found {self.mock_code}")
        except:
            return (self.code_warning())
        try:
            self.mock_msg = responses[self.mock_code]
            log.info(f"Default message found {self.mock_msg}")
        except KeyError:
            log.error(f"Requested code is out of range {self.mock_code}")
            return (self.code_warning())

    def to_send(self):
        if isinstance(self.mock_req, list):
            if self.config['multiple_messages']:
                for code in self.mock_req:
                    self.mock_code = code
                    self.sender()
            else:
                self.mock_code = self.mock_req[0]
                self.sender()
        else:
            self.mock_code = self.mock_req
            self.sender()

    def create_response(self, scenario):
        template = self.config
        pass

    def do_GET(self):
        self.get_mock_request()

    def do_POST(self):
        self.get_mock_request()

    def do_PUT(self):
        self.get_mock_request()

    def do_DELETE(self):
        self.get_mock_request()

    def do_PATCH(self):
        self.get_mock_request()

class MyHTTPServer(socketserver.TCPServer):
    def __init__(self, host, port, config):
        self.config = config
        self.server_address = (host, port)
        handlerClass = lambda *args, **kwargs: MyMockServer(*args, **kwargs, config=self.config)
        super().__init__(self.server_address, handlerClass)

def get_parse():
    '''
    Get parse options:
        -c --config: json file containing all config. 
        By default will loud config/config_fields.json
    '''
    parse = argparse.ArgumentParser(exit_on_error=False)
    parse.add_argument('-c', '--config', dest='config', type=str, help='config field file', default='/config/config_fields.json')
    parse.add_argument('-t', '--template', dest='template', type=str, help='template file', default='/config/template.json')
    print(f'{parse.parse_args()}')
    return (vars(parse.parse_args()))

def error_msg(message):
    # To log and exit at fatal error
    log.error(message)
    sys.exit()

if __name__ == '__main__':
    opts = get_parse()
    try:
        with open('config/config_fields.json') as fd:
            config = json.load(fd)
    except:
        log.error('')
    if 'host' in config:
        HOST = config['host']
    else:
        error_msg('Host field missing at config/config_fields.json')

    if 'port' in config:
        try:
            PORT = int(config['port'])
        except ValueError:
            error_msg('Invalid port field at config/config_fields.json')
    else:
        error_msg('Port field missing at config/config_fields.json')

    log.info('Config HOST and PORT successfully loaded from config/config_fields.json')
    try:
        httpd = MyHTTPServer(HOST, PORT, config)
    except:
        error_msg('Failed to start the server, check HOST and PORT configuration')

    log.info(f'Server running at -> {HOST}:{PORT}')
    print(f"Listening at {HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log.warning(f'Server was stopped by user or signal')
        httpd.server_close()
