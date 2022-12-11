import grpc
import metrics_msg_pb2
import metrics_msg_pb2_grpc
from concurrent import futures
import json
import google.protobuf.json_format

node2db = {
    "n1":"db1/metrics.json",
    "n2":"db2/metrics.json",
    "n3":"db3/metrics.json"
}

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

def to_protobuf_pidpersec_avg(pidpersec_avg, resp: metrics_msg_pb2.MetricsResponse):
    resp.pidpersec_avg = pidpersec_avg

def to_protobuf_pidpersec_sum(pidpersec_sum, resp: metrics_msg_pb2.MetricsResponse):
    resp.pidpersec_sum = pidpersec_sum

def to_protobuf_runqlat_avg(runqlat_avg, resp:metrics_msg_pb2.MetricsResponse):
    for k, v in runqlat_avg.items():
       resp.runqlat_avg.range2usecs[k] = v
    # print(resp.runqlat_avg.range2usecs)

def to_protobuf_runqlat_sum(runqlat_sum, resp:metrics_msg_pb2.MetricsResponse):
    # print("Hello")
    for k, v in runqlat_sum.items():
        print(k, v)
        resp.runqlat_sum.range2usecs[k] = v
    # print(resp.runqlat_sum.range2usecs)

class QueryManagerServicer(metrics_msg_pb2_grpc.QueryManagerServicer):        
    def QueryMetrics(self, request, context):
        # open db/cpu.json and read metrics
        metrics_resp = metrics_msg_pb2.MetricsResponse()
        # results = {}
        db_path = node2db[request.node_name]
        print(db_path)
        with open(db_path, "r") as f:
            data = json.load(f)
            # print(data["cpu"])
            for m in request.metrics.split(","):
                # print(m)
                if m not in data:
                    continue
                if m == "cpu_avg":
                    to_protobuf_cpu_avg(data[m], metrics_resp)
                elif m == "cpu_sum":
                    to_protobuf_cpu_sum(data[m], metrics_resp)
                elif m == "cpu":
                    to_protobuf_cpu(data[m], metrics_resp)
                elif m == "pidpersec_avg":
                    to_protobuf_pidpersec_avg(data[m], metrics_resp)
                elif m == "pidpersec_sum":
                    to_protobuf_pidpersec_sum(data[m], metrics_resp)
                elif m == "runqlat_avg":
                    to_protobuf_runqlat_avg(data[m], metrics_resp)
                elif m == "runqlat_sum":
                    to_protobuf_runqlat_sum(data[m], metrics_resp)
                # print(metrics_resp)
        return metrics_resp
    

def runGRPCServer(port):
    thread_pool = futures.ThreadPoolExecutor(max_workers=5)
    server = grpc.server(thread_pool)
    QMS = QueryManagerServicer()
    metrics_msg_pb2_grpc.add_QueryManagerServicer_to_server(QMS, server)
    print("Server Starts")
    server.add_insecure_port('localhost:' + port)
    server.start()
    server.wait_for_termination()

def main():
    runGRPCServer()

if __name__ == "__main__":
    main()