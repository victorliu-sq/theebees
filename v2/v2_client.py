import requests
import os
import json

base = "http://127.0.0.1:6000/"

def sendRequest(metrics):
    response = requests.get(base + metrics)
    return response

def parse(command):
    # first str should be select
    ws = command.split(" ")
    if ws[0] != "select":
        print("first command should be [select]")
        return
    
    # metrics to select
    requested_metrics = ws[1].split(",")
    results = {}
    for m in requested_metrics:
        if m == "cpu":
            results[m] = [] 
        else:
            results[m] = {}
    response = sendRequest(ws[1]).json()
    print(type(response))
    for metric_name in requested_metrics:
        print()
        print(metric_name, ":")
        print("====================================================")
        print(response[metric_name])
        print("====================================================")

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