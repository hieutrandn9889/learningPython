import requests

x = requests.get('https://httpbin.org/get')
print(x.status_code)  # 200 means OK
print(x.headers['Content-Type'])  # application/json; charset=utf-8
print(x.headers['Content-Length'])  # Length of the response content
print(x.headers['Server'])  # Server information
print(x.encoding)  # utf-8

if x.status_code == 200:
    print("Success!")
elif x.status_code == 404:
    print("Not Found!")

print(x.elapsed) # Time taken to get the response
print(x.cookies)  # Cookies set by the server

x = requests.get('https://httpbin.org/get', params={'key1': 'value1', 'key2': 'value2'})