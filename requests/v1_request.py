import requests

base = "http://127.0.0.1:5000/"

response = requests.get(base + "cpu")
print(response.json())