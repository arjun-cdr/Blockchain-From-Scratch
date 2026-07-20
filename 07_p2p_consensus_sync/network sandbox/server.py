from flask import Flask, request

app = Flask(__name__)
mempool = []

@app.route("/add", methods = ['POST'])
def add_to_server():
    incoming_data = request.get_json()
    mempool.append(incoming_data)
    return {"status" : "Successfully received data from Client..."} 
    
@app.route("/")
def return_data():
    return {"data received": mempool}

@app.route("/sync")
def sync_peers():
    target = "http://127.0.0.1:5001/add"
    response = request.post(target, json={"pet":mempool})
    return {"status":"Server Broadcast complete"}
    
if __name__ ==  "__main__":
    app.run(host = '127.0.0.1',port=5000, debug = True)