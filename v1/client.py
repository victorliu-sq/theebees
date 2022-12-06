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
    print(results)
    # requested_metrics = ws[1].split(",")
    # results = {}
    # for m in requested_metrics:
    #     if m == "cpu":
    #         results[m] = [] 
    #     else:
    #         results[m] = {}
    # print(metrics)
    # Get the response
    # response = sendRequest(ws[1]).json()
    # for metric_name in requested_metrics:
    #     print()
    #     print(metric_name, ":")
    #     print("====================================================")
    #     print(response[metric_name])
    #     print("====================================================")

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