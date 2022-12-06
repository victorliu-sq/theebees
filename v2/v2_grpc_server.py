import grpc
import metrics_msg_pb2
import metrics_msg_pb2_grpc
from concurrent import futures
import json
import google.protobuf.json_format

def to_protobuf_cpu_avg(cpu_avg, resp:metrics_msg_pb2.MetricsResponse):
    for k, v in cpu_avg.items():
       resp.cpu_avg.range2usecs[k] = v

def to_protobuf_cpu_sum(cpu_sum, resp:metrics_msg_pb2.MetricsResponse):
    for k, v in cpu_sum.items():
       resp.cpu_sum.range2usecs[k] = v
       
def to_protobuf_cpu(cpu_arr, resp:metrics_msg_pb2.MetricsResponse):
    for cpu in cpu_arr:
        # print(cpu)
        temp_cpu_dist = metrics_msg_pb2.CPUDistUint32()
        for k, v in cpu.items():
            print(k, v)
            temp_cpu_dist.range2usecs[k] = v
        resp.cpu.multiple_range2usecs.append(temp_cpu_dist)

class QueryManagerServicer(metrics_msg_pb2_grpc.QueryManagerServicer):
    def QueryMetrics(self, request, context):
        # open db/cpu.json and read metrics
        metrics_resp = metrics_msg_pb2.MetricsResponse()
        # results = {}
        with open("db/cpu.json", "r") as f:
            data = json.load(f)
            # print(data["cpu"])
            for m in request.metrics.split(","):
                if m not in data:
                    continue
                if m == "cpu_avg":
                    to_protobuf_cpu_avg(data[m], metrics_resp)
                elif m == "cpu_sum":
                    to_protobuf_cpu_sum(data[m], metrics_resp)
                elif m == "cpu":
                    to_protobuf_cpu(data[m], metrics_resp)
            print(metrics_resp)
                # elif m == "cpu":
                # results[m] = data[m]
        # print(results)
        # print(request.metrics)
        print("hello")
        return metrics_resp

def runGRPCServer():
    thread_pool = futures.ThreadPoolExecutor(max_workers=5)
    server = grpc.server(thread_pool)
    QMS = QueryManagerServicer()
    metrics_msg_pb2_grpc.add_QueryManagerServicer_to_server(QMS, server)
    print("Server Starts")
    server.add_insecure_port('localhost:8888')
    server.start()
    server.wait_for_termination()

def main():
    runGRPCServer()

if __name__ == "__main__":
    main()