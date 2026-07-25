from flask import Flask, request

PEERS = set()
my_port = '127.0.0.1:5000'
app = Flask(__name__)
@app.route("/nodes/register", methods = ['GET', 'POST'])
def extract_list_of_peers():
    nodes = request.get_json().get("nodes")
    
    if not nodes:
        return "Invalid data provided", 400
    
    for node in nodes:
        if node not in PEERS and my_port:
            PEERS.add(node)
            
    return {"SUCCESS": "NEW NODE REGISTERED", "total list of registered peers": PEERS}
