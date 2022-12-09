import requests
import os
import json

base = "http://127.0.0.1:6000/"

def printResults(results, nodes, metrics_names):
    for node in nodes.split(","):
        print()
        print("********************", node, "********************")
        # print(results[node])
        # Get the metrics for each node
        for metric_name in metrics_names.split(","):
            print()
            print(metric_name, ":")
            print("====================================================")
            print(results[node][metric_name])
            print("====================================================")

def sendRequest(metrics, nodes):
    response = requests.get(base + metrics + "/" + nodes)
    return response

def parse(command):
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
    
    requested_metrics = ws[1].split(",")
    results = {}
    for m in requested_metrics:
        if m == "cpu":
            results[m] = [] 
        else:
            results[m] = {}
    results = sendRequest(metrics_names, nodes).json()
    printResults(results, nodes, metrics_names)

def run_node():
    existing = 0
    while(1):
        try:
            print("Please input your command:")
            command = input()
            parse(command)
        except KeyboardInterrupt:
            existing = 1

        if existing:
            exit()

def main():
    run_node()

if __name__ == "__main__":
    main()