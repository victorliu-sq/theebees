import grpc
import json
# it will run this file automatically
# import jx_cpu_kprobe
from subprocess import call
from threading import Thread
import sys
# v2_grpc_server
import v2_grpc_server
# specify port and database for current worker
import argparse

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
    "n1": "7777",
    "n2": "8888",
    "n3": "9999",
}

class UserAgent():
    def run_cpu_kprobe(self):
        # set pid to 3327 and interval to 1
        db_path = node2db[args.Node]
        # notice that we do not need " " if pass args through string
        flag_db_path = "-d" + db_path
        # set pid to 3327 and interval to 1
        call(["python3", "kprobes/jx_cpu_kprobe.py", flag_db_path])
    

if __name__ == '__main__':
    port = node2port[args.Node]
    db_path = node2db[args.Node]
    ua = UserAgent()
    thread_cpu_collector = Thread(target=ua.run_cpu_kprobe)
    thread_cpu_collector.start()
    v2_grpc_server.runGRPCServer(port)
    thread_cpu_collector.join()
