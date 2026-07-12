# mines a block with a difficulty that works as a proof of work resulting in variable timestamps 

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
        
        print(f"Mining Block #{self.index} (Target : {target}....) at time : {time.time()}")
        
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
            
        print(f"Block Mined. Nonce found : {self.nonce} at time : {time.time()}")
        print(f"Final Hash : {self.hash}")
        
    def print_block(self):
        print(f"-------Block#{self.index}-------")
        print(f"Timestamp : {self.timestamp}")
        print(f"Transactions : ")
        for tx in self.transactions:
            print(f"{tx['sender']} -> {tx['receiver']} : {tx['amount']}")
        print(f"Current hash : {self.hash}")
        print(f"Previous hash : {self.previous_hash}")
        print("-" * 35)


def tamper_detector(blockchain):
    """
    loops through the blockchain to check for possible tampers(data integrity).
    Returns True if the chain is secure, False if tampered with.
    """
    # starts from index1, since genesis block has no previous
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        # Chain link check
        if current_block.previous_hash != previous_block.hash:
            print(
                f"Chain not linked.Link broken at Block#{current_block.index}  !!!!......"
            )
            return False

    for i in range(1, len(blockchain)):
        current_block = blockchain[i]

        # Internal integrity check
        current_hash = current_block.calculate_hash()
        if current_hash != current_block.hash:
            print(f"WARNING. Data tampered at Block #{current_block.index}!!!!........")
            return False

    print("Blockchain is Secure. ")
    return True


blockchain = []
difficulty = 4

# GENESIS BLOCK
genesis_txs = [{"sender": "System", "receiver": "Arjun", "amount": 100}]
genesis_block = Block(0, genesis_txs, "0")
genesis_block.mine_block(difficulty)
blockchain.append(genesis_block)

# Next blocks
tx1 = [
    {"sender": "Arjun", "receiver": "Avinash", "amount": 10},
    {"sender": "Avinash", "receiver": "Arjun", "amount": 50},
    {"sender": "Shruti", "receiver": "Arjun", "amount": 1000},
]
block1 = Block(1, tx1, genesis_block.hash)
block1.mine_block(difficulty)
blockchain.append(block1)

tx2 = [
    {"sender": "Messi", "receiver": "Ronaldo", "amount": 0},
    {"sender": "Ronaldo", "receiver": "Neymar", "amount": 50},
    {"sender": "Suarez", "receiver": "Zlatan", "amount": 1000},
]
block2 = Block(2, tx2, block1.hash)
block2.mine_block(difficulty)
blockchain.append(block2)
