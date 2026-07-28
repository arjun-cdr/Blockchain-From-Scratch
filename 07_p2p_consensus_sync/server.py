from flask import Flask, jsonify, request
import requests
import time
import json
import hashlib
import argparse

# Initialize Flask
app = Flask(__name__)

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        tx_string = json.dumps(self.transactions, sort_keys=True)
        data_to_hash = str(self.index) + tx_string + str(self.timestamp) + str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(data_to_hash.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

# Chain Validator
def is_chain_valid(chain_to_check):
    for i in range(1, len(chain_to_check)):
        current_block = chain_to_check[i]
        previous_block = chain_to_check[i-1]
            
        # Rule 1: Check if the chain link is broken
        if current_block["previous_hash"] != previous_block["hash"]:
            return False
        
        # Rule 2: Check if Proof of Work was actually done
        if not current_block["hash"].startswith(difficulty):
            return False
    return True 


# Global Node States
blockchain = []
difficulty = 3
pending_transactions = []
PEERS = set()

# Bootstrapping: Auto-mine Genesis Block right on startup
genesis_block = Block(0, [{"data": "Genesis Ledger Initialized"}], "0")
genesis_block.mine_block(difficulty)
blockchain.append(genesis_block)

tx1 = [
    {"sender": "Arjun", "receiver": "Avinash", "amount": 10},
    {"sender": "Avinash", "receiver": "Arjun", "amount": 50},
    {"sender": "Shruti", "receiver": "Arjun", "amount": 1000},
]
block1 = Block(1, tx1, genesis_block.hash)
block1.mine_block(difficulty)
blockchain.append(block1)

# Route-1 Building chain end-point and VIEWING CHAIN
@app.route("/chain", methods = ['GET'])
def get_chain():
    """
    Iterates through the global 'blockchain' list.
    Extracts each block's properties into a normal dictionary.
    Appends that dictionary to the 'chain_data' list.
    """
    chain_data = []
    
    for block in blockchain:
        chain_data.append({'index': block.index, 
                           'hash' : block.hash, 
                           'transactions': block.transactions, 
                           'previous_hash' : block.previous_hash,
                           'timestamp': block.timestamp, 
                           'nonce' : block.nonce})
    return jsonify({"chain":chain_data,"length" : len(chain_data)})

# Route-2 Adds new transactions
@app.route("/transactions/new", methods = ['GET','POST'])
def new_transaction():
    """
    Grabs incoming data using request.get_json().
    Extracts 'sender', 'receiver', and 'amount'.
    Appends this transaction dictionary to the 'pending_transactions' list.
    """
    tx_data = request.get_json()
    new_tx = {
        'sender' : tx_data['sender'],
        'receiver' : tx_data['receiver'],
        'amount' : tx_data['amount']
    }
    pending_transactions.append(new_tx)  #appends to global list (pending pool)
    
    return jsonify({"message":"Transaction added !!"})

# Route-3 Mine pending transactions
@app.route("/mine", methods = ['GET'])
def mine():
    """
    Ensure pending_transactions is not empty.
    Get the last block in the chain: last_block = blockchain[-1]
    Create a new Block instance, mine it, and append it to blockchain.
    Clear the pending_transactions list.
    """
    
    global pending_transactions, blockchain
    if len(pending_transactions) != 0:
        last_block = blockchain[-1]
        if isinstance(last_block, dict):
            last_hash = last_block["hash"]
        else:
            last_hash = last_block.hash
        new_block = Block(
            index = len(blockchain),
            transactions=pending_transactions,
            previous_hash=last_hash
        )
        new_block.mine_block(difficulty)
        blockchain.append(new_block)
        pending_transactions=[]
        
    return jsonify({"message": "New block successfully forged!"})

# Register PEERS
@app.route("/nodes/register", methods = ['POST'])
def extract_list_of_peers():
    nodes = request.get_json().get("nodes")
    
    if not nodes:
        return "Invalid data provided", 400
    
    for node in nodes:
        if node not in PEERS and node not in str(args.port) :
            PEERS.add(node)
            
    return {"SUCCESS": "NEW NODE REGISTERED", "total list of registered peers": list(PEERS)}

# P2P CONSESUS SYNC
@app.route("/nodes/sync", methods = ["GET", "POST"])
def resolve():
    global blockchain
    longest_chain = None
    max_length = len(blockchain)
    chain_was_replaced = False
    
    for peer in PEERS:
        try:
            response = requests.get(f"{peer}/chain")
            if response.status_code == 200:
                chain = response.json()["chain"]
                length = response.json()["length"]
                
                if length > max_length and blockchain.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        except requests.exceptions.RequestException:
            continue
    if longest_chain != None:
        blockchain = longest_chain
        chain_was_replaced = True
    if chain_was_replaced == True:
        return "Local Chain was replaced with the longer valid chain", 200
    else:
        return "Local Chain is already authoritative; no update needed", 200

parser = argparse.ArgumentParser(description="Start network server on a custom port.")
parser.add_argument("-p","--port", type=int, default = 5000)
args = parser.parse_args()

if __name__ ==  "__main__":
    app.run(host = '127.0.0.1',port = args.port)
