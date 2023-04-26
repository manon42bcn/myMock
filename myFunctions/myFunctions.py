# from testFIle import Test
import time

def mock_fnc_content_len(obj):
    return (len(obj.response_content))

def mock_fnc_time(obj):
    print (time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime()))
    return (time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime()))