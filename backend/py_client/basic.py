import requests

# endpoint = "https://httpbin.org/status/200"
# endpoint = "https://httpbin.org/anything"
endpoint = "http://127.0.0.1:8000/api"

# Sending a POST request with params and JSON data
get_response = requests.post(endpoint,  json={"title": "hello world"})

# print(get_response.text)
# print(get_response.headers)

# Printing the response JSON and status code
print(get_response.json())
#print(get_response.status_code)
