# Block Class that stores an index, a timestamp, a list of transactions, and a pointer to the previous block
import time

class Block:
    
    def __init__(self, index, transactions, previous):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous = previous
        
    def print_block(self):
        
        "prints the summary of the block"
        
        print(f"---Block #{self.index}---")
        print(f"Timestamp : {self.timestamp}")
        print(f"Transactions : {self.transactions}")
        print(f"Previous Hash : {self.previous}")
        print("-" * 20)
        
# This list represents our local blockchain database ledger        
blockchain = []

#Genseis (initial) transaction and block being appended to Blockchain list as blocks
genesis_txs = [{"sender": "System", "receiver": "Arjun", "amount": 100}]
genesis_block = Block(index = 0, transactions =genesis_txs, previous = 0)

blockchain.append(genesis_block)

# Next blocks
tx1 = [{"sender": "Arjun", "receiver": "Avinash", "amount": 10},{"sender": "Avinash", "receiver": "Arjun", "amount": 50},{"sender": "Shruti", "receiver": "Arjun", "amount": 1000}]
block1 = Block(1, tx1, "asd123")
blockchain.append(block1)

tx2 = [{"sender": "Messi", "receiver": "Ronaldo", "amount": 0},{"sender": "Ronaldo", "receiver": "Neymar", "amount": 50},{"sender": "Suarez", "receiver": "Zlatan", "amount": 1000}]
block2 = Block(2, tx2, "asd1234567")
blockchain.append(block2)


for block in blockchain:
    block.print_block()
