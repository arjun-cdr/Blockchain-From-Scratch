import requests

print("Sending requests to server...")
response = requests.get('http://127.0.0.1:5000/')

print("Connection successsful...")
print("Status Code : ", response.status_code)
print("Data Received : ", response.json())