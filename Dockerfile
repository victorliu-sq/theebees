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

RUN uname -r

RUN apt-get update

RUN apt-get upgrade

RUN apt-get dist-upgrade

# llvm verion 6  version can cause make fail 
RUN apt-get install -y bison build-essential cmake flex git libedit-dev \
  libllvm12 llvm-12-dev libclang-12-dev python zlib1g-dev libelf-dev libfl-dev python3-distutils

# install prometheus client
# -y => yes
RUN apt-get install -y python3-pip

RUN pip install prometheus-client

# install bcc
WORKDIR /
RUN git clone https://github.com/iovisor/bcc.git
RUN mkdir bcc/build
WORKDIR  bcc/build
RUN cmake ..
RUN make
RUN  make install
RUN cmake -DPYTHON_CMD=python3 ..

#install bpftrace
RUN apt-get install -y bpftrace

# WSL
# install linux header
# RUN apt-get install –y linux-headers-5.10.147+
# RUN apt-get install -y linux-headers-gcp
RUN git clone https://github.com/microsoft/WSL2-Linux-Kernel.git

WORKDIR WSL2-Linux-Kernel

RUN export KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2

# openssl/bio.h: No such file or directory
RUN apt-get install libssl-dev

# /bin/sh: 1: bc: not found
RUN apt-get install bc

# BTF: .tmp_vmlinux.btf: pahole (pahole) is not available
RUN apt install -y dwarves

RUN apt-get install -y fakeroot build-essential crash kexec-tools makedumpfile kernel-wedge

# RUN make KERNELRELEASE=$KERNELRELEASE defconfig

RUN cp Microsoft/config-wsl .config \
# enable modules
&& echo 'CONFIG_BPF=y' >> .config \
&& echo 'CONFIG_BPF_SYSCALL=y' >> .config \
&& echo 'CONFIG_BPF_JIT=y' >> .config

RUN make KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 -j 4

RUN make KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 modules -j 4

# arch/x86/Makefile:142: CONFIG_X86_X32 enabled but no binutils support
# bug fix: KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2
RUN make KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 oldconfig -j 4
RUN make KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 modules_prepare -j 4

RUN make -t KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 menuconfig
 
RUN make KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 modules_install

# install bpf tool
# WORKDIR /WSL2-Linux-Kernel/tools/bpf/bpftool

# RUN make

# No such file or directory: '/sys/kernel/debug/kprobes/blacklist'
# WORKDIR /WSL2-Linux-Kernel/kernel/debug

# RUN make

# CMD ["mount -t debugfs debugfs /sys/kernel/debug"]

# at the root
WORKDIR /

COPY cpudist.py .

CMD [ "python3", "./cpudist.py", "-p", "12", "-e", "1" ]