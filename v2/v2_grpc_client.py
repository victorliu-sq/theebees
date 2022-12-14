import grpc
import metrics_msg_pb2
import metrics_msg_pb2_grpc
import json
import google.protobuf.json_format as json_format
import threading

lock = threading.Lock()

def from_protobuf_cpu_avg(resp:metrics_msg_pb2.MetricsResponse):
    cpu_avg_json = json_format.MessageToJson(resp.cpu_avg)
    cpu_avg = json.loads(cpu_avg_json)["range2usecs"]
    return cpu_avg

def from_protobuf_cpu_sum(resp:metrics_msg_pb2.MetricsResponse):
    cpu_sum_json = json_format.MessageToJson(resp.cpu_sum)
    cpu_sum = json.loads(cpu_sum_json)["range2usecs"]
    return cpu_sum
       
def from_protobuf_cpu(resp:metrics_msg_pb2.MetricsResponse):
    # print(resp.cpu)
    cpu_json = json_format.MessageToJson(resp.cpu)
    temp_cpu = json.loads(cpu_json)["multipleRange2usecs"]
    # print(temp_cpu)
    cpu = []
    for c in temp_cpu:
        cpu += [c["range2usecs"]]
    return cpu

def from_protobuf_pidpersec_avg(resp:metrics_msg_pb2.MetricsResponse):
    pidpersec_avg = resp.pidpersec_avg
    return pidpersec_avg

def from_protobuf_pidpersec_sum(resp:metrics_msg_pb2.MetricsResponse):
    pidpersec_sum = resp.pidpersec_sum
    return pidpersec_sum

def newMetricsRequest(metrics_names, node_name):
    req = metrics_msg_pb2.MetricsRequest(metrics=metrics_names, node_name=node_name)
    return req

def from_protobuf_runqlat_avg(resp:metrics_msg_pb2.MetricsResponse):
    runqlat_avg_json = json_format.MessageToJson(resp.runqlat_avg)
    runqlat_avg = json.loads(runqlat_avg_json)["range2usecs"]
    return runqlat_avg

def from_protobuf_runqlat_sum(resp:metrics_msg_pb2.MetricsResponse):
    runqlat_sum_json = json_format.MessageToJson(resp.runqlat_sum)
    runqlat_sum = json.loads(runqlat_sum_json)["range2usecs"]
    return runqlat_sum

def SendQueryMetrics(results, metrics_names, node_name, port):
    with grpc.insecure_channel('localhost:' + port) as channel:
        # print("Try to get metrics from", port)
        stub = metrics_msg_pb2_grpc.QueryManagerStub(channel)
        metrics_req = newMetricsRequest(metrics_names, node_name)
        # print("Hello1")
        response = stub.QueryMetrics(metrics_req)
        # print("Hello2")
        result = {}
        for metric_name in metrics_names.split(","):
            if metric_name == "cpu_avg":
                result[metric_name] = from_protobuf_cpu_avg(response)
            elif metric_name == "cpu_sum":
                result[metric_name] = from_protobuf_cpu_sum(response)
            elif metric_name == "cpu":
                result[metric_name] = from_protobuf_cpu(response)
            elif metric_name == "pidpersec_avg":
                result[metric_name] = from_protobuf_pidpersec_avg(response)
            elif metric_name == "pidpersec_sum":
                result[metric_name] = from_protobuf_pidpersec_sum(response)
            elif metric_name == "runqlat_avg":
                result[metric_name] = from_protobuf_runqlat_avg(response)
            elif metric_name == "runqlat_sum":
                result[metric_name] = from_protobuf_runqlat_sum(response)
        # print("Hello3")
        lock.acquire()
        results[node_name] = result
        lock.release()

        
if __name__ == "__main__":
    # metrics_req = newMetricsRequest()
    # print(metrics_req)
    metrics_req = "cpu,cpu_avg,cpu_sum"
    SendQueryMetrics(metrics_req)