from flask import Flask, request

app = Flask(__name__)
mempool = []

@app.route("/add", methods = ['POST'])
def add_to_server():
    incoming_data = request.get_json()
    mempool.append(incoming_data)
    return {"status" : "Successfully received data from Server 1 (Node A)"} 
    
@app.route("/")
def return_data():
    return {"data received": mempool}
    
if __name__ ==  "__main__":
    app.run(host = '127.0.0.1',port=5001, debug = True)