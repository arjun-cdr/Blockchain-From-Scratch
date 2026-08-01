from flask import Flask, jsonify, request
import time
import json
import hashlib

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

# Initialize Flask
app = Flask(__name__)

# Global Node States
blockchain = []
difficulty = 3

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

# Route-1 Building chain end-point and viewing chain
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

pending_transactions = []
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
        new_block = Block(
            index = len(blockchain),
            transactions=pending_transactions,
            previous_hash=last_block.hash
        )
        new_block.mine_block(difficulty)
        blockchain.append(new_block)
        pending_transactions=[]
        
    return jsonify({"message": "New block successfully forged!"})
    
if __name__ ==  "__main__":
    app.run(host = '127.0.0.1',port=5000)
