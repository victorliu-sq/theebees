import requests
import threading

class ClientProxy():
    def __init__(self, node2addr) -> None:
        # dictionary of {node_name : ip:port} 
        self.node2addr = node2addr
        self.lock = threading.Lock()
    
    def broadcastRequests(self, nodes:str, metrics:str):
        results = {}
        threads = {}
        for node in nodes.split(","):
            if node in self.node2addr:
                thread = threading.Thread(target=self.sendRequest, args=(node, metrics, results))
                threads[node] = thread
        for thread in threads.values():
            thread.start()
        for thread in threads.values():
            thread.join()
        return results

    def sendRequest(self, node, metrics, result):
        base = self.node2addr[node]
        self.lock.acquire()
        response = requests.get(base + metrics)
        result[node] = response.json()
        self.lock.release()
        return