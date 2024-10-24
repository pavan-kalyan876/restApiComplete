import requests

endpoint = "http://127.0.0.1:8000/api/products/2/update"
data = {"title": "hello my friend", "price": "129.00"}
get_response = requests.put(endpoint, json=data)
print(get_response.json())
 