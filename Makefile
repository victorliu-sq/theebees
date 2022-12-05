# make proto
PROTO_DIR = protos

generate:
	python3 -m grpc_tools.protoc -I $(PROTO_DIR) --python_out=. --pyi_out=. --grpc_python_out=. $(PROTO_DIR)/metrics_msg.proto 

clean:
	rm *_pb2.py