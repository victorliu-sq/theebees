sudo apt-get update

sudo apt-get upgrade

sudo apt-get dist-upgrade

sudo apt-get install -y bison build-essential cmake flex git libedit-dev \
  libllvm12 llvm-12-dev libclang-12-d

sudo apt-get install -y python3-pip

sudo pip install prometheus-client

sudo git clone https://github.com/iovisor/bcc.git
sudo mkdir bcc/build
WORKDIR  bcc/build
sudo cmake ..
sudo make
sudo  make install
sudo cmake -DPYTHON_CMD=python3 ..

sudo apt-get install -y bpftrace

sudo git clone https://github.com/microsoft/WSL2-Linux-Kernel.git

cd WSL2-Linux-Kernel

sudo export KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2

sudo apt-get install libssl-dev

sudo apt-get install bc

sudo apt install -y dwarves

sudo apt-get install -y fakeroot build-essential crash kexec-tools makedumpfile kernel-wedge

sudo make KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 -j 4

sudo make KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 modules -j 4

sudo make KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 oldconfig -j 4
sudo make KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 modules_prepare -j 4

sudo make -t KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 menuconfig
 
sudo make KERNELRELEASE=5.10.102.1-microsoft-standard-WSL2 modules_install
