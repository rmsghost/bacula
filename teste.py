import requests, json
import json

def req():
    response = requests.get('http://172.26.228.140:16686/trace/c1c6ede47f9c0e5d')
    print(response)
    data = response
    print(data)
    teste = 'oi'
    
    return (data, teste)


x = req()
print (x[1])