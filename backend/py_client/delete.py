import requests

product_id = input("What is the product ID you want to use: \n")

# Validate if the input is a valid integer
try:
    product_id = int(product_id)
except ValueError:
    print(f"{product_id} is not a valid ID.")
    exit()

# Proceed only if a valid ID is provided
if product_id:
    endpoint = f"http://127.0.0.1:8000/api/products/{product_id}/delete/"
    
    try:
        get_response = requests.delete(endpoint)  # Making the DELETE request
        # Checking if the status code is 204 (No Content, successful deletion)
        if get_response.status_code == 204:
            print("Product deleted successfully.")
        elif get_response.status_code == 404:
            print("Product not found.")
        else:
            print(f"Failed to delete the product. Status code: {get_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
