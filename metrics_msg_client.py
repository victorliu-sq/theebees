import grpc
import metrics_msg_pb2
import metrics_msg_pb2_grpc
import json
import google.protobuf.json_format as json_format

def from_protobuf_cpu_avg(resp:metrics_msg_pb2.MetricsResponse):
    cpu_avg_json = json_format.MessageToJson(resp.cpu_avg)
    cpu_avg = json.loads(cpu_avg_json)["range2usecs"]
    print(cpu_avg)
    return

def from_protobuf_cpu_sum(resp:metrics_msg_pb2.MetricsResponse):
    cpu_sum_json = json_format.MessageToJson(resp.cpu_sum)
    cpu_sum = json.loads(cpu_sum_json)["range2usecs"]
    print(cpu_sum)
    return
       
def from_protobuf_cpu(resp:metrics_msg_pb2.MetricsResponse):
    # print(resp.cpu)
    cpu_json = json_format.MessageToJson(resp.cpu)
    temp_cpu = json.loads(cpu_json)["multipleRange2usecs"]
    # print(temp_cpu)
    cpu = []
    for c in temp_cpu:
        cpu += [c["range2usecs"]]
    
    print(cpu)
        
    # cpu = json.loads(cpu_json)
    
    # for cpu in cpu_arr:
    #     # print(cpu)
    #     temp_cpu_dist = metrics_msg_pb2.CPUDistUint32()
    #     for k, v in cpu.items():
    #         print(k, v)
    #         temp_cpu_dist.range2usecs[k] = v
    #     resp.cpu.append(temp_cpu_dist)

def newMetricsRequest():
    req = metrics_msg_pb2.MetricsRequest(metrics="cpu,cpu_avg,cpu_sum")
    return req

def run():
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = metrics_msg_pb2_grpc.QueryManagerStub(channel)
        metrics_req = newMetricsRequest()
        response = stub.QueryMetrics(metrics_req)
        # from_protobuf_cpu_avg(response)
        # from_protobuf_cpu_sum(response)
        from_protobuf_cpu(response)
        print("hello")
        # print(response)

        
if __name__ == "__main__":
    # metrics_req = newMetricsRequest()
    # print(metrics_req)
    run()