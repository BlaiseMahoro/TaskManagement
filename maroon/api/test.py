
jsonRequest = {
    'name' : 'MyProject',
    'description': 'Something'
}

request = HttpRequest(jsonRequest)
sendRequest("http://127.0.0.1:8000/api/project/", request)
