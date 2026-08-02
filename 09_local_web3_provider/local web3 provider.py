import requests
import logging
from flask import Flask
import json

# Initializing Logger
logger = logging.getLogger(__name__)

# Initializing Flask
app = Flask(__name__)

class Web3_Provider:
    
    def __init__(self,node_url = "http://127.0.0.1:5000"):
        
        # Strip trailing slashes to prevent malformed endpoint
        self.node_url = node_url.rstrip("/")
        # Test connection upon initialization
        if not self.is_connected(node_url):
            logger.warning("Warning !!! Unable to reach local node at ", self.node_url)
        
    def is_connected(url):
        try:
            response = requests.head(url, timeout = 5)
            return response.ok
        except requests.RequestException:
            return False
    
    # Private method : The Engine room 
    def __send_request(self, endpoint, methods,  payload = None):
        
        # Combining node url with endpoint 
        target_url = self.node_url + endpoint
        
        try :
            if methods == "POST":
                response = requests.post(target_url, json = payload)
            elif methods == "GET":
                response = requests.get(target_url)
                
            if response.status_code == 200:
                return response.json()
            else:
                print("Node returned status code :", response.status_code)
                return
        
        except Exception as e:
            raise ConnectionError(f"Failed to connect to local node....{e}")
        except TimeoutError:
            raise "Node request timed out...."

    # Fetching the blockchain
    def get_chain(self):
        return self._send_request("/chain", methods = "GET")

    # Fetching Blockchain Length
    def get_block_height(self):
        chain = self.get_chain()
        return len(chain["chain"])

    # Bundles transactions and send it to mempool
    def send_transaction(self, sender, receiver, amount):
        payload = {
            "sender" : sender,
            "receiver" : receiver,
            "amount" : amount
        }
        return self._send_request("/transactions/new", method = "POST", payload = payload)

    # Method to trigger a new Mine-Block
    def trigger_mine(self):
        return self._send_request("/mine", method = "POST")


# Manual Test Script

provider = Web3_Provider("http://127.0.0.1:5000")

if provider.is_connected():
    print("Connected to the node....")
    print(provider.send_transaction("Billy", "Homelander", 8000))
    print(provider.trigger_mine())
    print(provider.get_chain())
    print(provider.get_block_height())

else:
    print("Node is Unreachable.....")
