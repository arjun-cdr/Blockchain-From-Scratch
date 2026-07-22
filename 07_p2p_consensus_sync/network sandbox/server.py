from flask import Flask, request
import requests

app = Flask(__name__)
mempool = []

@app.route("/add", methods = ['POST'])
def add_to_server():
    incoming_data = request.get_json()
    mempool.append(incoming_data)
    return {"status" : "Successfully received data from Server 2 (Node B)"} 
    
@app.route("/")
def return_data():
    return {"data received": mempool}

@app.route("/sync")
def sync_peers():
    target = "http://127.0.0.1:5001/add"
    response = requests.post(target, json={"data":mempool})
    if response.status_code==200:
        return {
        "status":"Server Broadcast complete",
        "node_2_reply": response.json(),
        }
    else:
        return{
        "status":"Server Broadcast Incomplete",
        "status_code": response.status_code(),
        }
    
if __name__ ==  "__main__":
    app.run(host = '127.0.0.1',port=5000, debug = True)