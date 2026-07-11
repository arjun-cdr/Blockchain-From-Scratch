import hashlib
import json
import time


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Combines block data into a string, encodes it to bytes,
        and returns the SHA-256 hexadecimal hash string.
        """

        # Step 1: Turning the transactions list into a standardized string using json.dumps
        tx_string = json.dumps(self.transactions, sort_keys=True)

        # Step 2: Combine the data fields into one single string. (Concatenating)
        data_to_hash = (
            str(self.index) + tx_string + str(self.timestamp) + str(self.previous_hash)
        )

        # Step 3: Passing the data_to_hash string to hashlib.sha256()
        hex_output = hashlib.sha256(data_to_hash.encode()).hexdigest()

        return hex_output
                

    def print_block(self):
        print(f"-------Block#{self.index}-------")
        print(f"Timestamp : {self.timestamp}")
        print(f"Transactions : ")
        for tx in self.transactions:
            print(f"{tx['sender']} -> {tx['receiver']} : {tx['amount']}")
        print(f"Current hash : {self.hash}")
        print(f"Previous hash : {self.previous_hash}")
        print("-" * 35)

blockchain = []

# GENESIS BLOCK
genesis_txs = [{"sender": "System", "receiver": "Arjun", "amount": 100}]
genesis_block = Block(0, genesis_txs, 0)
blockchain.append(genesis_block)

# Next blocks
tx1 = [
    {"sender": "Arjun", "receiver": "Avinash", "amount": 10},
    {"sender": "Avinash", "receiver": "Arjun", "amount": 50},
    {"sender": "Shruti", "receiver": "Arjun", "amount": 1000},
]
block1 = Block(1, tx1, genesis_block.hash)
blockchain.append(block1)

tx2 = [
    {"sender": "Messi", "receiver": "Ronaldo", "amount": 0},
    {"sender": "Ronaldo", "receiver": "Neymar", "amount": 50},
    {"sender": "Suarez", "receiver": "Zlatan", "amount": 1000},
]
block2 = Block(2, tx2, block1.hash)
blockchain.append(block2)


# displaying output through iteration
for block in blockchain:
    block.print_block()
