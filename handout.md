# Single Probe

```shell
# run the cpu_kprobe
sudo python3 ./kprobes/jx_cpu_kprobe.py -d kprobes/db/metrics.json

```

```python
args.extension = 1
args.pid = 3327
args.interval = 1
# must use extension, interval is 1s, and pid is fixed as 3327
```



# V1

worker

- the worker will run a Flask server in its main function and run a user agent in another thread (attach a kprobe, extract information and store it in db)
- each worker has 1 specific port number and 1 database to store the extracted metrics 

```shell
make runWorker1
make runWorker2
make runWorker3
```



client

```shell
# run the client
make runClient

# input a command
select cpu_avg,cpu_sum from n1,n2,n3
# metrics_name will be "cpu_avg,cpu_sum"
# nodes will be "n1,n2,n3"

select cpu_avg from n1,n2,n3

select cpu_avg,cpu_sum from n1,n3
```



# V2

worker

```shell
make runWorker1
make runWorker2
make runWorker3
```



coordinator

```shell
make runCoordinator
```



client

```shell
# run the client
make runClient


# operations
select cpu_avg from n1,n2,n3

select cpu_avg,cpu_sum from n1,n3
```



# Job

write 2 kprobes into kprobes 



# Problem

No time for evaluation
