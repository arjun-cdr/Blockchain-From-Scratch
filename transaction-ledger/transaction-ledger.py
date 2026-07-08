#Global ledger - Transaction tracking history
ledger =[]

#determines balance of the sender
def get_balance(username):
    balance = 0
    for tx in ledger:
        if tx.get("sender") == username:
            balance -= tx.get("amount")
        if tx.get("receiver") == username:
            balance += tx.get("amount")
    return balance
    
#adds new tracnsaction to the ledger        
def add_transaction(sender, receiver, amount):
    if sender != "System":
        curr_balance = get_balance(sender)
        if curr_balance < amount:
            print(f"Error: Insufficient funds. {sender} only has {curr_balance} tokens")
            return False
        
    #new transaction           
    new_tx = {
        "sender" : sender,
        "receiver" : receiver,
        "amount" : amount
    }
    
    ledger.append(new_tx)
    print(f"Success: {sender} sent {amount} to {receiver}")
    return True

print("-----------Running Blockchain Ledger tests-----------")

add_transaction("System","Alice",100)
print(f"Alice - balance :: {get_balance('Alice')}, Expected (100)")

add_transaction("Alice","Bob",70)
print(f"Alice - balance :: {get_balance('Alice')}, Expected (30)")
print(f"Bob - balance :: {get_balance('Bob')}, Expected (70)")

add_transaction("Alice","John",10)
print(f"Alice - balance :: {get_balance('Alice')}, Expected (20)")
print(f"John - balance :: {get_balance('John')}, Expected (10)")

tx_status =add_transaction("Bob","Jack", 80)
print(f"Transaction status : {tx_status}..Expected False/true")
print(ledger)
