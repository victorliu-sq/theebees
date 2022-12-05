# install proto





# compile proto

```shell
protoc --python_out=proto protos/metrics_msg.proto
# (1) protoc => protocompiler
# (2) --python_out => python RPC
# (3) proto => output_dir
# (4) proto/msg.proto => input_dir
```



# install gRPC

```shell
#install: protobuf, grpcio, grpcio-tools
sudo apt install protobuf-compiler
pip install protobuf
pip install grpcio
pip install grpcio-tools

# not generate pb2.py correctly
pip install --no-binary :all: grpcio --ignore-installed
```

