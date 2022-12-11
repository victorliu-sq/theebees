

# KProbe

| Name      | Functionality                                                |
| --------- | ------------------------------------------------------------ |
| cpudist   | This measures the time a task spends on or off the CPU, and shows this time s a histogram, optionally per-process. |
| pidpersec | This shows the number of new processes created per second, measured by tracing |



```shell
# run the cpu_kprobe
sudo python3 ./kprobes/jx_cpu_kprobe.py -d kprobes/db/metrics.json

# run the pidpersec_kprobe
sudo python3 ./kprobes/pidpersec.py -d kprobes/db/metrics.json

# run the runqlat_kprobe
sudo python3 ./kprobes/runqlat.py -d kprobes/db/metrics.json
```



some fixed arguments for cpu_kprobe

```python
args.extension = 1
args.pid = 3327
args.interval = 1
# must use extension, interval is 1s, and pid is fixed as 3327
```



# Preprocessing Functions





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

select cpu_avg,pidpersec_avg from n1,n2,n3

select cpu_avg,pidpersec_avg,runqlat_avg,runqlat_sum from n1,n2,n3
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

select cpu_avg,pidpersec_avg from n1,n2,n3

select cpu_avg,pidpersec_avg,runqlat_avg,runqlat_sum from n1,n2,n3
```

