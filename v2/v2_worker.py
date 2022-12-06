import grpc
import json
# it will run this file automatically
# import jx_cpu_kprobe
from subprocess import call
from threading import Thread
import sys
# v2_grpc_server
import v2_grpc_server


class UserAgent():
    def run_cpu_kprobe(self):
        # set pid to 3327 and interval to 1
        call(["python3", "kprobes/jx_cpu_kprobe.py"])
    

if __name__ == '__main__':
    ua = UserAgent()
    thread_cpu_collector = Thread(target=ua.run_cpu_kprobe)
    thread_cpu_collector.start()
    v2_grpc_server.runGRPCServer()
    thread_cpu_collector.join()
