from flask import Flask
from flask_restful import Resource, Api
import json
# it will run this file automatically
# import jx_cpu_kprobe
from subprocess import call
from threading import Thread
# specify a port
import argparse
import sys
from collections import defaultdict

app = Flask(__name__)
api = Api(app)

# specify port for current worker

parser = argparse.ArgumentParser(
    description="Summarize on- and off-CPU time per task as a histogram.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

parser.add_argument("-n", "--Node", help="Specify the node for  the worker")

args = parser.parse_args()

# node2db and node2port
node2db = {
    "n1":"db1/metrics.json",
    "n2":"db2/metrics.json",
    "n3":"db3/metrics.json"
}

node2port = {
    "n1": 6000,
    "n2": 6100,
    "n3": 6200,
}

class UserAgent():
    def run_cpu_kprobe(self):
        # set pid to 3327 and interval to 1
        db_path = node2db[args.Node]
        # notice that we do not need " " if pass args through string
        flag_db_path = "-d" + db_path
        # print(flag_db_path)
        call(["python3", "kprobes/jx_cpu_kprobe.py", flag_db_path])
    
    def run_pidpersec_kprobe(self):
        # set pid to 3327 and interval to 1
        db_path = node2db[args.Node]
        # notice that we do not need " " if pass args through string
        flag_db_path = "-d" + db_path
        # print(flag_db_path)
        call(["python3", "kprobes/pidpersec_kprobe.py", flag_db_path])
    
    def run_web_server(self):
        app.run(debug=True)

class Metrics(Resource):
    def get(self, req_metrics):
        results = {}
        db_path = node2db[args.Node]
        print("Hello")
        with open(db_path, "r") as f:
            data = json.load(f)
            for m in req_metrics.split(","):
                # print(data[m])
                results[m] = data[m]
        # print(results)
        return results

api.add_resource(Metrics, '/<string:req_metrics>')

if __name__ == '__main__':
    db_path = node2db[args.Node]
    data = {}
    with open(db_path, "w") as f:
        data["cpu_avg"] = defaultdict(float)
        data["cpu_sum"] = defaultdict(int)
        data["cpu"] = []
        data["pidpersec_avg"] = 0.0
        data["pidpersec_sum"] = 0
        json.dump(data, f)
    
    ua = UserAgent()
    thread_cpu_collector = Thread(target=ua.run_cpu_kprobe)
    thread_pidpersec_collector = Thread(target=ua.run_pidpersec_kprobe)
    thread_cpu_collector.start()
    thread_pidpersec_collector.start()
    port = node2port[args.Node]
    
    app.run(debug=True, port=port, host='localhost')
    thread_cpu_collector.join()
    thread_pidpersec_collector.join()
