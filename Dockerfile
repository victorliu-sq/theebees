# # python3 --version
# FROM python:3.8.10

# # RUN mkdir -p /app
# # WORKDIR /app

# # COPY hello_world.py ./hello_word.py
# COPY ./cpudist.py ./cpudist.py

# # CMD ["python3", "./hello_word.py"]
# CMD ["python3", "./cpudist.py"]

FROM ubuntu:20.04 as build
ENV  DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN apt-get upgrade

# install linux header
RUN apt-get install -y linux-headers-gcp

# install prometheus client
# -y => yes
RUN apt-get install -y python3-pip

RUN pip install prometheus-client
# llvm verion 6  version can cause make fail 
RUN apt-get install -y bison build-essential cmake flex git libedit-dev \
  libllvm12 llvm-12-dev libclang-12-dev python zlib1g-dev libelf-dev libfl-dev python3-distutils

RUN git clone https://github.com/iovisor/bcc.git
RUN mkdir bcc/build
WORKDIR  bcc/build
RUN cmake ..
RUN make
RUN  make install
RUN cmake -DPYTHON_CMD=python3 .. # build python3 binding

WORKDIR /usr/sbin/

# RUN pip3 install prometheus_client

COPY cpudist.py .
CMD [ "python3", "./cpudist.py" ]