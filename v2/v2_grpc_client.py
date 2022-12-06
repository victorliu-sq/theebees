import grpc
import metrics_msg_pb2
import metrics_msg_pb2_grpc
import json
import google.protobuf.json_format as json_format

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

def newMetricsRequest():
    req = metrics_msg_pb2.MetricsRequest(metrics="cpu,cpu_avg,cpu_sum")
    return req

def runQueryMetrics(metrics_names):
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = metrics_msg_pb2_grpc.QueryManagerStub(channel)
        metrics_req = newMetricsRequest()
        response = stub.QueryMetrics(metrics_req)
        result = {}
        for metric_name in metrics_names.split(","):
            if metric_name == "cpu_avg":
                result[metric_name] = from_protobuf_cpu_avg(response)
            elif metric_name == "cpu_sum":
                result[metric_name] = from_protobuf_cpu_sum(response)
            elif metric_name == "cpu":
                result[metric_name] = from_protobuf_cpu(response)
        return result
        # from_protobuf_cpu(response)
        # print("hello")
        # print(response)

        
if __name__ == "__main__":
    # metrics_req = newMetricsRequest()
    # print(metrics_req)
    metrics_req = "cpu,cpu_avg,cpu_sum"
    runQueryMetrics(metrics_req)