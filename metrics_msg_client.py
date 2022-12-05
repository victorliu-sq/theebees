import grpc
import metrics_msg_pb2
import metrics_msg_pb2_grpc

def newMetricsRequest():
    req = metrics_msg_pb2.MetricsRequest(metrics="hello")
    return req

def run():
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = metrics_msg_pb2_grpc.QueryManagerStub(channel)
        metrics_req = newMetricsRequest()
        response = stub.QueryMetrics(metrics_req)
        print(response)

        
if __name__ == "__main__":
    # metrics_req = newMetricsRequest()
    # print(metrics_req)
    run()