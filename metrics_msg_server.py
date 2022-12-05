import grpc
import metrics_msg_pb2
import metrics_msg_pb2_grpc
from concurrent import futures

class QueryManagerServicer(metrics_msg_pb2_grpc.QueryManagerServicer):
    def QueryMetrics(self, request, context):
        # return super().QueryMetrics(request, context)
        return metrics_msg_pb2.MetricsResponse(data="welcome")

def main():
    thread_pool = futures.ThreadPoolExecutor(max_workers=5)
    server = grpc.server(thread_pool)
    QMS = QueryManagerServicer()
    metrics_msg_pb2_grpc.add_QueryManagerServicer_to_server(QMS, server)
    print("Server Starts")
    server.add_insecure_port('localhost:8888')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    main()