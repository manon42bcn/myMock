import jsonschema
from myMock.MockedCodesServer import *
from myMock.ConfigCheck import schema_template, schema_config
import os

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
    set_logger(opts)
    '''
    Load config file and check
    config structure
    '''
    try:
        base_path = os.path.dirname(__file__)
        print(f'BASE {base_path}')
        with open(f'{base_path}/{opts["config"]}') as fd:
            config = json.load(fd)
    except Exception as e:
        log.error(f'Error loading config file. Detailed exception {e}')
    
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
    my_functions_loader()
    try:
        httpd = MyHTTPServer(HOST, PORT, config)
    except Exception as e:
        error_msg(f'Failed to start the server. Detailed exception: {e}')

    log.info(f'Server running at -> {HOST}:{PORT}')
    print(f"Listening at {HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log.warning(f'Server was stopped by user or signal')
        httpd.server_close()
