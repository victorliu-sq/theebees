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

class UserAgent():
    def run_web_server(self):
        app.run(debug=True)

class Metrics(Resource):
    def get(self, metrics_names):
        # print(metrics_names)
        result = v2_grpc_client.runQueryMetrics(metrics_names)
        return result
        # results = {}
        # with open("db/cpu.json", "r") as f:
        #     data = json.load(f)
        #     # print(data["cpu"])
        #     for m in metrics_names.split(","):
        #         results[m] = data[m]
        # print(results)
        # return results

api.add_resource(Metrics, '/<string:metrics_names>')

if __name__ == '__main__':
    app.run(debug=True, port=6000, host='localhost')
