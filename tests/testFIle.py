import requests
import json

url = 'http://localhost:8000/mockserver'
with open('test.json', 'r') as fd:
    data = json.load(fd)

data['header']['Content-Length'] = str(len(json.dumps(data['content']).encode('utf-8')))
response = requests.post(url, json=data['content'], headers=data['header'])
print(response)
