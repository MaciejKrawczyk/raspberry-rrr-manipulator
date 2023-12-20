import requests

url = "http://localhost:5000/update_variable"
data = {
    "name": "var1",
    "value": "new value 1"
}

response = requests.post(url, data=data)

print(response.text)