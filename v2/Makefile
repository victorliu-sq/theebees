# make proto
PROTO_DIR = protos

generate:
	python3 -m grpc_tools.protoc -I $(PROTO_DIR) --python_out=. --pyi_out=. --grpc_python_out=. $(PROTO_DIR)/metrics_msg.proto 

clean:
	rm *_pb2.py

runClient:
	python3 ./v2_client.py

runCoordinator:
	python3 ./v2_coordinator.py

runWorker:
	sudo python3 ./v2_worker.py

runWorker1:
	sudo python3 ./v2_worker.py -n n1

runWorker2:
	sudo python3 ./v2_worker.py -n n2

runWorker3:
	sudo python3 ./v2_worker.py -n n3