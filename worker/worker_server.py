from flask import Flask
from flask_restful import Resource, Api
import json
# it will run this file automatically
# import jx_cpu_kprobe
from subprocess import call
from threading import Thread
import sys

app = Flask(__name__)
api = Api(app)

class UserAgent():
    def run_cpu_kprobe(self):
        # set pid to 3327 and interval to 1
        call(["python3", sys.path[0]+"/"+"jx_cpu_kprobe.py"])
    
    def run_web_server(self):
        app.run(debug=True)

class Metrics(Resource):
    def get(self, req_metrics):
        results = {}
        with open("db/cpu.json", "r") as f:
            data = json.load(f)
            # print(data["cpu"])
            for m in req_metrics.split(","):
                results[m] = data[m]
        print(results)
        return results

api.add_resource(Metrics, '/<string:req_metrics>')

if __name__ == '__main__':
    UserAgentClass = UserAgent()
    thread_cpu_collector = Thread(target=UserAgentClass.run_cpu_kprobe)
    thread_cpu_collector.start()
    app.run(debug=True)
    thread_cpu_collector.join()
