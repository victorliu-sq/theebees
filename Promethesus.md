# Prometheus

## Download Prometheus





# Prometheus Client

install python library

```python
pip install prometheus_client

sudo python3 ./cpudist.py -p 12 -e 1
```





# Prometheus Server

Ask the server to monitor the metrics of client

```shell
# in prometheus.yml
ADD
- job_name: "oncpu_count"

    static_configs:
      - targets: ["localhost:8080"]


# "oncput_count" is name of Count/Gauge/Sum/Histogram
# [local:host8080] is port of prometheus client
```



Run Prometheus Server and Client



Check if prometheus server has started to monitor in **STATUS** => **TARGETS**
