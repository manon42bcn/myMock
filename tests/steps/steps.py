from behave import given, then, when, step
import requests
import subprocess
import json
import os
   
@step('Using "{server}" as endpoint')
def set_endpoint(context, server):
    context.endpoint = server

@step('Working with "{mode}" mode')
def set_server_mode(context, mode):
    context.mode = mode
    context.endpoint = context.endpoint + '/' + mode

@step('Load "{template}" body as template request')
def load_default_json(context, template):
    base_path = os.path.dirname(__file__)
    template_path = os.path.join(base_path, 'utils/bodyTest.json')
    with open(template_path, 'r') as fd:
        context.template = json.loads(fd.read())

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

def content_length(body_to_send):
    str = json.dumps(body_to_send)
    return (len(str.encode('utf-8')))

def request_mockserver(context):
    context.req_body = dict(context.template['content'])
    context.req_body['message']['messages'][0]['text']['body'] = context.req_code
    context.req_headers = context.template['header']
    context.req_headers['Content-Length'] = str(content_length(context.req_body))
    if context.req_method == 'POST':
        context.response = requests.post(context.endpoint, headers=context.req_headers, json=context.req_body)
    else:
        pass