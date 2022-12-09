from flask import Flask
from flask_restful import Resource, Api
import json
# it will run this file automatically
# import jx_cpu_kprobe
from subprocess import call
from threading import Thread
import sys
import v2_grpc_client

app = Flask(__name__)
api = Api(app)

# node2port
node2port = {
    "n1": "7777",
    "n2": "8888",
    "n3": "9999",
}

node2db = {
    "n1":"db1/metrics.json",
    "n2":"db2/metrics.json",
    "n3":"db3/metrics.json"
}

class UserAgent():
    def run_web_server(self):
        app.run(debug=True)

class Metrics(Resource):
    def get(self, metrics_names, nodes):
        # print(metrics_names)
        # print(nodes)
        result = {}
        for node in nodes.split(","):
            port = node2port[node]
            node_name = node
            # print(node, port)
            result[node] = v2_grpc_client.runQueryMetrics(metrics_names, node_name, port)
        print("result is done")
        return result

api.add_resource(Metrics, '/<string:metrics_names>/<string:nodes>')

if __name__ == '__main__':
    app.run(debug=True, port=6000, host='localhost')
