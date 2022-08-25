>>> import requests

# GET
>>> r = requests.get('https://jgraber.ch')
>>> r.status_code
200
>>> r.status_code == requests.codes.ok
True
>>> r.text
'<!DOCTYPE html>\r\n<html lang='...

# URL parameter
>>> payload = {'key1': 'value1', 'key2': 'value2'}
>>> r = requests.get('https://httpbin.org/get', params=payload)
>>> r.url
'https://httpbin.org/get?key1=value1&key2=value2'
>>> r.json()
{
    'args': {
        'key1': 'value1', 
        'key2': 'value2'
        }, 
    'headers': {
        'Accept': '*/*', 
        'Accept-Encoding': 'gzip, deflate', 
        'Host': 'httpbin.org', 
        'User-Agent': 'python-requests/2.27.1', 
        'X-Amzn-Trace-Id': 'Root=1-63068b8d-12d628e31969095f64f294be'
        }, 
    'origin': '213.142.178.228', 
    'url': 'https://httpbin.org/get?key1=value1&key2=value2'
}

# Headers

>>> headers = {'user-agent': 'my-app/0.0.1'}
>>> r = requests.get('https://httpbin.org/get', headers=headers) 
>>> r.json()
{
    'args': {}, 
    'headers': {
        'Accept': '*/*', 
        'Accept-Encoding': 'gzip, deflate', 
        'Host': 'httpbin.org', 
        'User-Agent': 'my-app/0.0.1', 
        'X-Amzn-Trace-Id': 'Root=1-63068c4d-069d88c374a297341d678835'}, 
    'origin': '213.142.178.228', 
    'url': 'https://httpbin.org/get'
}


>>> r = requests.get('http://jgraber.ch')  
>>> r.headers
{
    'Date': 'Wed, 24 Aug 2022 20:53:40 GMT', 
    'Content-Type': 'application/json', 
    'Content-Length': '309', 
    'Connection': 'keep-alive', 
    'Server': 'gunicorn/19.9.0', 
    'Access-Control-Allow-Origin': '*', 
    'Access-Control-Allow-Credentials': 'true'
}

>>> r.headers['Server']
'gunicorn/19.9.0'
>>> r.headers['Content-Type'] 
'application/json'

# POST
>>> r = requests.post('https://httpbin.org/post', data={'key': 'value'})
>>> r.json()
{
    'args': {}, 
    'data': '', 
    'files': {}, 
    'form': {'key': 'value'}, 
    'headers': {
        'Accept': '*/*', 
        'Accept-Encoding': 'gzip, deflate', 
        'Content-Length': '9', 'Content-Type': 
        'application/x-www-form-urlencoded', 
        'Host': 'httpbin.org', 
        'User-Agent': 'python-requests/2.27.1', 
        'X-Amzn-Trace-Id': 'Root=1-63068d0a-7104245d043d455c717e2d99'}, 
    'json': None, 
    'origin': '213.142.178.228', 
    'url': 'https://httpbin.org/post'
}

# Follow redirects
>>> r = requests.get('http://jgraber.ch')  
>>> r.status_code == requests.codes.ok    
True
>>> r.is_redirect
False
>>> r.status_code                         
200
>>> r.history
[<Response [301]>]

# Other HTTP methods

>>> r = requests.head('https://httpbin.org/get')
>>> r.text
''
>>> r.status_code
200
>>> r = requests.head('https://httpbin.org/get5') 
>>> r.status_code
404

>>> r = requests.options('https://httpbin.org/get')
>>> r.text
''
>>> r.headers
{
    'Date': 'Wed, 24 Aug 2022 20:55:07 GMT', 
    'Content-Type': 'text/html; charset=utf-8', 
    'Content-Length': '0', 
    'Connection': 'keep-alive', 
    'Server': 'gunicorn/19.9.0', 
    'Allow': 'OPTIONS, GET, HEAD', 
    'Access-Control-Allow-Origin': '*', 
    'Access-Control-Allow-Credentials': 'true', 
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS', 
    'Access-Control-Max-Age': '3600'
}



r = requests.put('https://httpbin.org/put', data={'key': 'value'})
r = requests.delete('https://httpbin.org/delete')

