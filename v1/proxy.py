import requests
from typing import List, Mapping

class ClientProxy():
    def __init__(self, node2addr) -> None:
        # dictionary of {node_name : ip:port} 
        self.node2addr = node2addr
    
    def broadcastRequests(self, nodes:str, metrics:str):
        results = {}
        for node in nodes.split(","):
            if node in self.node2addr:
                base = self.node2addr[node]
                print(node, base)
                response = requests.get(base + metrics)
                results[node] = response.json()
                print(results[node])
        return results