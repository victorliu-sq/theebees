from flask import Flask
from flask_restful import Resource, Api
import json
# it will run this file automatically
# import jx_cpu_kprobe
from subprocess import call
from threading import Thread
import sys
import v2_grpc_client

import threading

app = Flask(__name__)
api = Api(app)

# node2port
node2port = {
    "n1": "7777",
    "n2": "8888",
    "n3": "9999",
}

class UserAgent():
    def run_web_server(self):
        app.run(debug=True)

class Metrics(Resource):
    def get(self, metrics_names, nodes):
        # print(metrics_names)
        # print(nodes)
        results = {}
        threads = {}
        for node in nodes.split(","):
            port = node2port[node]
            node_name = node
            # print(node, port)
            thread = threading.Thread(target=v2_grpc_client.SendQueryMetrics, args=(results, metrics_names, node_name, port))
            threads[node] = thread
        for thread in threads.values():
            thread.start()
        for thread in threads.values():
            thread.join()
        print("results is done")
        return results

api.add_resource(Metrics, '/<string:metrics_names>/<string:nodes>')

if __name__ == '__main__':
    app.run(debug=True, port=6000, host='localhost')
