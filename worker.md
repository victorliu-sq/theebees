install some dependencies for Flask

```shell
# count lines of code
find . -name '*.py' | xargs wc -l

# install Flask
pip install -U Flask
sudo pip3 install Flask
# install Falsk_Restful
pip install Flask-RESTful
sudo pip3 install Flask_Restful
```



run kprobe for cpu_dist

```shell
sudo python3 ./cpu_dist/jx_cpu_kprobe.py -p 3327 -e 1
```



run the server

```
python3 worker/worker_server.py
```



run the 

```shell
python3 requests/v1_request.py
```

