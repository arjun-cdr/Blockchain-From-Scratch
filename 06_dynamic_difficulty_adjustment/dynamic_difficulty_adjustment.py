# Concept : If blocks are mined too fast, the system automatically increases the difficulty (e.g., changing the target from 000 to 0000). If they take too long, it lowers the difficulty.
import hashlib
import json
import time

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        # Nonce
        self.nonce = 0
        self.hash = ""  # No need to calculate hash on initialization

    def calculate_hash(self):
        """
        Combines block data into a string, encodes it to bytes,
        and returns the SHA-256 hexadecimal hash string.
        """

        # Step 1: Turning the transactions list into a standardized string using json.dumps
        tx_string = json.dumps(self.transactions, sort_keys=True)

        # Step 2: Combine the data fields into one single string. (Concatenating)
        data_to_hash = (
            str(self.index)
            + tx_string
            + str(self.timestamp)
            + str(self.previous_hash)
            + str(self.nonce)
        )

        # Step 3: Passing the data_to_hash string to hashlib.sha256()
        hex_output = hashlib.sha256(data_to_hash.encode()).hexdigest()

        return hex_output

    def mine_block(self, difficulty):
        
        """Increments the nonce until the block's hash starts
        with the required number of leading zeros.
        """
        target = "0" * difficulty
        self.hash = self.calculate_hash()
        
        print(f"Mining Block #{self.index} (Target: {'0'*difficulty}...)")
        print(f"Difficulty : {difficulty}")
        start_time = time.time()
        
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
            
        end_time = time.time()
        time_taken = end_time - start_time 
        
        print(f"Block Mined in {time_taken:.4f}s.\nNonce found : {self.nonce}\nTime Taken : {time_taken}")
        print(f"Current difficulty : {difficulty}")
        print(f"Final Hash : {self.hash}")
        print("-"*30)
        return time_taken
    

blockchain = []
current_difficulty = 4
target_mine_time = 0.5

print("--- Starting Dynamic Difficulty Simulation ---")

# GENESIS BLOCK
genesis_txs = [{"sender": "System", "receiver": "Arjun", "amount": 100}]
genesis_block = Block(0, genesis_txs, "0")
time_spent = genesis_block.mine_block(current_difficulty)
blockchain.append(genesis_block)

if(time_spent < target_mine_time):
    current_difficulty += 1
else:
    if current_difficulty >= 2:
        current_difficulty -=1

# Next blocks
tx1 = [
    {"sender": "Arjun", "receiver": "Avinash", "amount": 10},
    {"sender": "Avinash", "receiver": "Arjun", "amount": 50},
    {"sender": "Shruti", "receiver": "Arjun", "amount": 1000},
]
block1 = Block(1, tx1, genesis_block.hash)
block1.mine_block(current_difficulty)
blockchain.append(block1)
