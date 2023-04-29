import time
import json
'''
myFunctions.py:
To include a function that can be used from
templates. Format:
def mock_fnc_<name>(obj):
    your code.
Attributes:
    obj.mock_msg: default message loaded from method responses[]
        from http.client class
    obj.response_content: dict or string containing the response
        builded from template.
    obj.config: dict containing config_filds.json
    obj.mockMode: 'URL' or type of request recieved
        ('POST', 'PUT', 'DELETE', etc.)
'''
'''
DEFAULT FUNCTIONS:
Needed to normal function
'''
def mock_fnc_content_len_json(obj):
    str = json.dumps(obj.response_content)
    return (len(str.encode('utf-8')))

def mock_fnc_content_len(obj):
    return (len(obj.response_content))

def mock_fnc_time(obj):
    return (time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime()))

def mock_fnc_content_len(obj):
    return (str(len(obj.response_content)))

def mock_fnc_default_response(obj):
    return (obj.mock_msg)

def mock_fnc_server(obj):
    return ('MockServer')
'''
END OF DEFAULT FUNCTIONS
'''