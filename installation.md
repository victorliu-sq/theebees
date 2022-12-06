# Install Flask

```shell
sudo pip install Flask
sudo pip install flask-restful
```



# install gRPC

```shell
# install: protobuf, grpcio, grpcio-tools
# use sudo to install all pip because the worker needs to run kprobes
sudo apt install protobuf-compiler
sudo pip install protobuf
sudo pip install grpcio
sudo pip install grpcio-tools

# not generate pb2.py correctly => there are 3 file in total
python3 -m grpc_tools.protoc -I $(PROTO_DIR) --python_out=. --pyi_out=. --grpc_python_out=. $(PROTO_DIR)/metrics_msg.proto 

sudo pip install protobuf
sudo pip install grpcio
sudo pip install grpcio-tools
```

