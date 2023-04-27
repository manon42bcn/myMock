import time

def mock_fnc_content_len(obj):
    return (len(obj.response_content))

def mock_fnc_time(obj):
    print (time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime()))
    return (time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime()))

def mock_fnc_content_len(obj):
    return (len(obj.response_content))

def mock_fnc_default_response(obj):
    return (obj.mock_msg)

def mock_fnc_server(obj):
    return ('MockServer')