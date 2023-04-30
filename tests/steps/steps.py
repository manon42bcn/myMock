from behave import given, then, when, step
import requests
import subprocess
   
@step('Using "{server}" as endpoint')
def set_endpoint(context, server):
    context.endpoint = server

@step('Working with "{mode}" mode')
def set_server_mode(context, mode):
    context.mode = mode
    if mode == 'mockurl':
        context.endpoint = context.endpoint + '/mockurl'

@step('Using {method} method to ask {code} as mocked code')
@step('Using {method} method')
def set_request(context, method, code=None):
    context.req_method = method
    if code is not None:
        set_code_to_request(context, code)

@step('Ask {code} as mocked code')
def set_code_to_request(context, code):
    context.req_code = code
    if context.mode == 'mockurl':
        request_mockurl(context)
    else:
        request_mockserver(context)

@step('I get the requested code')
def check_requested_code(context):
    assert int(context.req_code) == int(context.response.status_code),\
        f'Differences between requests [{context.req_code}] and response code [{context.response.status_code}]'

        
def request_mockurl(context):
    if context.req_method == 'GET':
        context.response = requests.get(f'{context.endpoint}/{context.req_code}')
    elif context.req_method == 'POST':
        context.response = requests.post(f'{context.endpoint}/{context.req_code}')

def request_mockserver(context, code):
    pass