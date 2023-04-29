import logging
import json
import jsonschema
import http.server
import socketserver
from http.client import responses
import argparse
import sys
import inspect
import myFunctions.myFunctions as mF
from ConfigCheck import schema_config, schema_template

'''
Loaded functions from myFunctions.py
as a global var
'''
myLoadedFunctions = {}
class MyMockServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        '''
        at init: load personalized functions
        and init superclass
        '''
        self.config = kwargs.pop('config', None)
        self.myFnc = myLoadedFunctions
        super().__init__(*args, **kwargs)

    def get_mock_request(self):
        '''
        Starts workflow for different mock
        request options.
        '''
        if '/favicon.ico' in self.path:
            return
        if '/mockurl/' in self.path:
            self.do_mockurl()
        if '/mockserver' in self.path:
            self.do_mockserver()

    def do_mockurl(self):
        '''
        Build mock response for mockurl
        option
        '''
        log.info('MOCK-URL request mode detected')
        self.mockMode = 'URL'
        self.template = self.config['templates']['URL']
        self.req_header = dict(self.headers.items())
        self.mock_req = [self.path.split('/')[-1]]
        self.to_send()

    def do_mockserver(self):
        '''
        Build mock response for mockserver
        option.
        '''
        log.info('MOCK-SERVER request mode detected')
        self.mockMode = self.command
        log.debug(f'Loading template to {self.mockMode}')
        self.template = self.config['templates'][self.command]
        self.req_header = dict(self.headers.items())
        len = int(self.req_header.get('Content-Length', 0))
        request_data = self.rfile.read(len)
        self.req_data = json.loads(request_data.decode('utf-8'))
        self.mock_req = self.get_requested_code()
        self.to_send()

    def get_requested_code(self):
        '''
        Get requested code(s) using config file
        and search it at request
        '''
        result = self.req_data
        for field in self.config[self.mockMode]['request_field']:
            if isinstance(result, dict):
                result = result.get(field, {})
            elif isinstance(result, list):
                result = [x.get(field, {}) for x in result]
        log.debug(f'Asked codes founded at request {result}')
        return (result)

    def cfg_response(self):
        if self.config['error_list']:
            if self.mock_code in self.config['error_list']:
                self.mock_rsp = 'error'
            else:
                self.mock_rsp = 'response'
        else:
            if self.mock_code >= self.config['error_range'][0] and self.mock_code <= self.config['error_range'][1]:
                self.mock_rsp = 'error'
            else:
                self.mock_rsp = 'response'
        log.debug(f'Response will be set as: {self.mock_rsp}')

    def template_response(self):
        '''
        Build body response using template.
        If a mock_fnc_ is founded will be called
        '''
        log.debug('Load info from template to build a response content')
        self.response_content = {}
        for key, value in self.template[self.mock_rsp]['data'].items():
            self.response_content[key] = self.myFnc[value](self) \
                if value.startswith('mock_fnc_') \
                else value

    def template_header(self):
        '''
        Build header response using template.
        If a mock_fnc_ is founded will be called
        '''
        log.debug('Load info from template to build a response headers')
        self.header_content = {}
        for key, value in self.template[self.mock_rsp]['header'].items():
            self.header_content[key] = self.myFnc[value](self) \
                if value.startswith('mock_fnc_') \
                else value

    def to_send(self):
        '''
        Prepare response or responses to send
        if multi message is allowed
        '''
        if self.config['multiple_messages']:
            log.debug('Multiple mocked request option is true')
            for code in self.mock_req:
                self.mock_code = code
                self.sender()
        else:
            log.debug('Multiple mocked request option is false')
            self.mock_code = self.mock_req[0]
            self.sender()

    def snd_header(self):
        if len(self.header_content):
            for key, value in self.header_content.items():
                self.send_header(key, value)
        self.end_headers()
        log.debug('Headers sended')

    def sender(self):
        '''
        Response sender
        '''
        self.checkMockCode()
        self.cfg_response()
        self.template_response()
        self.template_header()
        self.send_response(self.mock_code, responses[self.mock_code])
        log.debug(f'Responde sended code: {self.mock_code} - msg: {responses[self.mock_code]}')
        if len(self.header_content):
            for key, value in self.header_content.items():
                self.send_header(key, value)
        self.end_headers()
        log.debug(f'Headers sended {self.header_content}')
        if isinstance(self.response_content, dict):
            rsp = json.dumps(self.response_content)
            self.wfile.write(rsp.encode())
        else:
            self.wfile.write(bytes(self.response_content, "UTF-8"))
        log.debug('Body response sended')

    def checkMockCode(self):
        '''
        Response code checker.
        Request can be casted to int and
        is in a valid HTTP status code
        range
        '''
        try:
            self.mock_code = int(self.mock_code)
            log.debug(f"Requested code found {self.mock_code}")
        except:
            return (self.code_warning())
        try:
            self.mock_msg = responses[self.mock_code]
            log.debug(f"Default message found {self.mock_msg}")
        except KeyError:
            log.error(f"Requested code is out of range {self.mock_code}")
            return (self.code_warning())


    def code_warning(self):
        log.error(f"Code is not present or is out of range {self.mock_req}.")
        self.send_error(self.config["error_code"])
        self.end_headers()
        rsp = json.dumps({"content": "Requested mock error"})
        self.wfile.write(rsp.encode())

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

def my_functions_loader():
    imF = dir(mF)
    rst = {}
    try:
        log.debug('Loading my functions from myFunctions.py')
        rst = {key: getattr(mF, key) \
                            for key in imF \
                            if inspect.isfunction(getattr(mF, key)) \
                            and key.startswith('mock_fnc_')}
    except:
        error_msg('External functions could not be found. '
                    'myFunctions/myFunctions.py should be present '
                    'even if is empty file')
    return (rst)

def get_parse():
    '''
    Get parse options:
        -c --config: json file containing all config.
        By default will loud config/config_fields.json
        -d --debug: active debug mode. By default log
        level is setted as WARNING
    '''
    parse = argparse.ArgumentParser(exit_on_error=False)
    parse.add_argument('-c', '--config', dest='config', type=str, help='config field file', default='config/config_fields.json')
    parse.add_argument('-d', '--debug', help='activate debug mode', action='store_true')
    return (vars(parse.parse_args()))

def error_msg(message):
    '''
    Log and exit at fatal error
    '''
    log.error(message)
    sys.exit()

def check_config_file(config_file, log):
    '''
    Check config file structure.
    Template check is not working properly
    '''
    try:
        jsonschema.validate(config_file, schema_config)
        log.info('Valid config file base')
    except jsonschema.exceptions.ValidationError as e:
        error_msg(f'Error on base json config file Error: {e}')
    for key, elem in config_file['templates'].items():
        try:
            jsonschema.validate(elem, schema_template)
            log.info(f'Valid template {key} loaded')
        except jsonschema.exceptions.ValidationError as e:
            error_msg(f'Error on base template {key} json config file Error: {e}')


if __name__ == '__main__':
    '''
    Get parsed configuration and
    star logger
    '''
    opts = get_parse()
    log = logging.getLogger('http_logger')
    if opts['debug']:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARNING)
    file_handler = logging.FileHandler(f"HTTPmockStatus.log")
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    '''
    Load config file and check
    config structure
    '''
    try:
        with open(opts['config']) as fd:
            config = json.load(fd)
    except:
        log.error('Error loading config file')
        
    check_config_file(config, log)
    log.info(f'config file loaded from {opts["config"]}')
    '''
    Start server
    '''
    HOST = config['host']
    PORT = config['port']
    '''
    Load functions from myFunctions.py
    '''
    myLoadedFunctions = my_functions_loader()
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
