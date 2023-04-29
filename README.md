myMock Server  

myMock Server
=============

Manuel Porras Ojeda 
- [github](https://github.com/manon42bcn/myMock) 
- [linkedin](https://www.linkedin.com/in/manuelporrasojeda/) 
- [email](mailto:manuelporrasojeda@gmail.com)
--------------------------------------------------------------

### Mock server is a simple Python-based mock server to simulate REST API endpoints, providing mocked responses or URL and REQUESTS.

**Disclaimer!** This is an ongoing project! I started it as a way to understand how mock tests should be, how servers-endpoints-api works and to improve my python skills. If is useful to you, go to linkedin and comment... or just say hello by email! Please, don't cheat yourself, if you will use this project put my name somewhere ;-D

Prerequisites

*   Python 3.6+
*   jsonschema 3.2.0
*   http.server
*   socketserver
*   argparse

### Getting started

To get started with the mock server, you can follow these steps:

*   Clone the repository: $> git clone git@github.com:manon42bcn/myMock.git
*   Install the required packages by running pip install -r requirements.txt
*   Define your configuration file in JSON format, following the schema of the schema\_config.json file (Check Config section for details)
*   Start the server by running python myMockServer.py
    Options:*   \-d --debug: To activate all logs.
    *   \-c --config path/to/file.json: To load your configuration
*   The server will now be running and listening for requests.
*   in your browser go to http:yourhost:port and you will see a html version of this file.

### How it works?

The mock server provides two modes: MOCKURL and MOCKSERVER. To get a mocked code, you only have to make a request to the host and port where myMock is running.

### Mockurl mode.

MOCKURL mode simulates a URL endpoint. You have set your endpoint as **http:yourhost:port/mockurl/\[code\]** and you will get **\[code\]** as HTTP status code.

### Mockserver mode.

MOCKURL mode simulates a URL endpoint. and the SERVER mode simulates a full server.

### Get a response, not just the HTTP status code.

You can define what you want to recieve as a response, not only the status code. At config/config\_file.json you will find a default model of a config file (make a copy to use it like a model, config\_file.json it will be used as a default configuration)

The structure of the config file is:

*   host(str):Name of the host where myMock will be running
*   port(int):Port number where myMock will be listen
*   multiple\_messages(bool): myMock server will respose multiple code petitions at one request
*   error\_code(int): Code sended where an error on request will be founded
*   error\_range(array->int): Min and Max codes that will be considered as error codes.
*   error\_list(bool): A detailed list of codes that will be considered as error codes.
*   NOTE: Error list and error range will be use to implement new features in the future
*   GET, POST, PUT, DELETE, PATCH(json): container request\_field(array->str).**request\_field** should be de path to the field that include the desired code to response.
    
    e.g. Your request look like this:
    
    \[ "messages": \[  
    "message": \[  
    "question": \[  
    "phrase": \[  
    "305"  
    \]  
    \]  
    \]  
    \]
    
    Your request\_field should be: \['messages', 'message', 'question', 'phrase'\]
    
    That way, when you make a request with that body, myMock will detect 305 as a desired HTTP response code.
    
*   templates(json):that should include a template for each behaviour (GET, POST, PUT, DELETE, PATCH) that sould include (Go to /config/config\_fiels.json to used as reference):
    
    *   Name of behaviour(json):
        *   case(request, response, error)
            *   header(json): key -> value that shoul be recieved or include at headers responses
            *   data(json): key -> value that shoul be recieved or include at body responses
    
    **Important:** you can use literal strings as value to each field at header or data, but you can also go to myFunctions.py and code a function using attibutes of MyMockServer class. To use personalized functions your should call it **mock\_fnc\_\[name\]** and include that name as string at value.
    
    e.g: At POST->response->header->Random-Number-Field you need a field that include a random number. After include a function named "mock\_fnc\_random", you include POST->response->header->Random-Number-Field: "mock\_fnc\_random" and myMock will get the return of the function as its value.
    

### Comming soon:

Right now i'm working on:

*   clean code
*   docker version
*   include some tests

### DISCLAIMER: 
The materials and information provided in this repository are offered "as is" and without warranties of any kind, either express or implied. The user assumes all responsibility and risk for the use of this repository and any files contained herein. This repository may contain inaccuracies or errors and we do not warrant the accuracy or completeness of the materials or information provided. In no event shall the authors or contributors of this repository be liable for any damages or losses arising out of or in connection with the use or inability to use this repository or any of its contents. By using this repository, you agree to these terms and conditions.