import requests

print("Sending data to server...")
data_to_send = {"pet":"rocky", "name": "Arjun"} 
response = requests.post('http://127.0.0.1:5000/add', json = data_to_send)

print("Connection successsful...")
print("Status Code : ", response.status_code)