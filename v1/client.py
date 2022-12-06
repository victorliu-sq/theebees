import requests
import os
import proxy

base = "http://127.0.0.1:5000/"

def sendRequest(metrics):
    response = requests.get(base + metrics)
    return response

def parse(command:str, p:proxy.Proxy):
    metrics = {
        "cpu": False,
        "cpu_sum": False,
        "cpu_avg": False,
    }
    # first str should be select
    ws = command.split(" ")
    if ws[0] != "select":
        print("first command should be [select]")
        return
    
    if ws[2] != "from":
        print("second command should be [select]")
        return
    # metrics to select
    metrics_names = ws[1]
    nodes = ws[3]
    # broadcast requests to nodes
    results = p.broadcastRequests(nodes, metrics_names)
    for node in nodes.split(","):
        print()
        print("********************", node, "********************")
        # print(results[node])
        requested_metrics = metrics_names.split(",")
        # Get the metrics for each node
        for metric_name in requested_metrics:
            print()
            print(metric_name, ":")
            print("====================================================")
            print(results[node][metric_name])
            print("====================================================")

def run_node():
    node2addr = {
        "n1" : "http://127.0.0.1:6000/",
        "n2" : "http://127.0.0.1:6100/",
        "n3" : "http://127.0.0.1:6200/",
    }
    p = proxy.Proxy(node2addr)
    existing = 0
    while(1):
        try:
            print("Please input your command:")
            command = input()
            parse(command, p)
        except KeyboardInterrupt:
            existing = 1

        if existing:
            exit()

def main():
    run_node()

if __name__ == "__main__":
    main()