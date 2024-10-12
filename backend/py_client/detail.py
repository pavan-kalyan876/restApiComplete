import requests

endpoint = "http://127.0.0.1:8000/api/products/2/"  # Adjusted URL
get_response = requests.get(endpoint)

# Check if the request was successful
print(get_response.json())
