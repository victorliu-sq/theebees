# Single Probe

```shell
# run the cpu_kprobe
sudo python3 ./kprobes/jx_cpu_kprobe.py -d v1/db1/metrics.json
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
```



# V2

Currently we only support one worker in V2

worker

```shell
make runWorker
```



coordinator

```shell
make runCoordinator
```



client

```shell
# run the client
make runClient
```

