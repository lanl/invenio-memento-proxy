# Memento Proxy for Invenio
Make your web resources [Memento](http://www.mementoweb.org) compliant in a few easy steps.

The Memento framework enables datetime negotiation for web resources. Knowing the URI of a Memento-compliant web resource, a user can select a date and see what it was like around that time.

The Memento protocol is an HTTP extension that allows clients to request a version of a resource as it existed at a specified time in the past. It is specified in RFC 7089.
The Memento protocol works by adding two new headers to HTTP requests and responses:

*  Accept-Datetime: This header is used by the client to specify the desired datetime of the resource.
*  Memento-Datetime: This header is used by the server to indicate the datetime of the resource that is being returned.

The Memento protocol also defines two new types of resources:

*  TimeGate: A TimeGate is a server that can return Mementos of a resource.
*  TimeMap: A TimeMap is a resource that lists the Mementos of another resource.

To use the Memento protocol, a client would first need to find a TimeGate that can return Mementos of the desired resource. 
The client would then send an HTTP request to the TimeGate with the Accept-Datetime header set to the desired datetime. 
The TimeGate would then return a Memento of the resource, or a 404 Not Found response if no Memento exists for the specified datetime.

## Introduction

In order to support Memento, a web server must obviously have accessible archives of its online resources.
And it must also have a piece of software that handles the datetime negotiation according to the Memento protocol for those resources.
The Invenio Memento proxy provide easy way to add TimeGate and TimeMap services to any Invenio installation.


There are only two steps to make such web server Memento compliant.

## Step 1: Setting up Invenio Memento Proxy

# Setup

The Invenio Memento Proxy software is downloaded, installed and run from within a Python Virtual Environment.
```bash

# create virtual env in your custom directory
$ cd /data/venv
$ virtualenv timegate
$ source /data/venv/timegate/bin/activate

# download and install the proxy code within the virtual env
$ cd ~
$ git clone https://~/invenio-memento-proxy
$ cd invenio-memento-proxy
$ python setup.py install
$ deactivate
```

### To start a proxy,

```bash
$ source /data/venv/timegate/bin/activate
$ uwsgi --http :9999 -s /tmp/mysock.sock --module timegate.application --callable application --virtualenv /home/ludab/timegate/
```

### Test that service is working:

```bash
curl   http://localhost:9999/timemap/link/https://data.caltech.edu/api/records/tds5b-9rs75/files/README.txt 

curl -I  http:///localhost:9999/timegate/https://data.caltech.edu/api/records/tds5b-9rs75/files/README.txt
HTTP/1.1 302 FOUND
Server: nginx/1.18.0 (Ubuntu)
Date: Fri, 25 Aug 2023 00:25:35 GMT
Content-Type: text/plain; charset=UTF-8
Content-Length: 0
Connection: keep-alive
Vary: accept-datetime
Location: https://data.caltech.edu/records/tds5b-9rs75/files/README.txt
Link: <https://data.caltech.edu/api/records/tds5b-9rs75/files/README.txt>; rel=original, <http://160.1.118.115/timemap/link/https://data.caltech.edu/api/records/tds5b-9rs75/files/README.txt>; rel=timemap; type=application/link-format, <http://160.1.118.115/timemap/json/https://data.caltech.edu/api/records/tds5b-9rs75/files/README.txt>; rel=timemap; type=application/json, <https://data.caltech.edu/records/tds5b-9rs75/files/README.txt>; rel="first last memento"; datetime="Mon, 03 Jul 2023 19:57:38 GMT"
```

### The default Invenio Memento proxy configured for caltech example.

To adapt to your installation of invenio 
go to ./invenio-memento-proxy/timegate/examples, edit invenio.py 
with baseurl of  your invenio installation

```bash
baseurl = "https://data.caltech.edu/"
```
### To configure service under nginx

Change  hostname in config.ini in the `./timegate/conf` folder.
```bash
host = http://localhost/
```
Add section to nginx config:
```bash
location / {
                #include uwsgi_params;
                #uwsgi_pass unix:///data/var/run/timegate/caltech.sock;
                proxy_pass http://localhost:9999;
		        #proxy_set_header Host $host;
		        #proxy_set_header X-Real_IP $remote_addr;
        }
```        

The also can configure  uWsgi with configuration file  and example of  uWsgi configuration  is `timegate.ini` in the `./timegate/conf` folder.
Adapt  according  to your installation.

```bash
# home of vertual env
home = /data/venv/timegate/
# directory for project install
chdir = /home/ludab/invenio-memento-proxy
daemonize = /data/var/logs/timegate/caltech.log                                                                                                                                                                                        
pidfile = /data/var/run/timegate/caltech.pid
# python path
pythonpath = /data/venv/timegate/lib/python3.8/site-packages
```

To restart or stop a proxy if your configured pid file,
```bash
$ uwsgi --reload /data/var/run/timegate/<proxyname>.pid

$ uwsgi --stop /data/var/run/timegate/<proxyname>.pid
```
## Step 2: Providing the headers
The second thing to do is to provide Memento's HTTP headers at the web server.
* Add HTTP headers required by the Memento protocol to responses from the Original Resource and its Mementos:
  - For the Original Resource, add a "Link" header that points at its TimeGate
  - For each Memento, add a "Link" header that points at the TimeGate
  - For each Memento, add a "Link" header that points to the Original Resource
  - For each Memento, add a Memento-Datetime header that conveys the snapshot datetime


## Requirements
* [Python](https://www.python.org)
* [uWSGI](http://uwsgi-docs.readthedocs.org/en/latest/)



## License
See the [LICENSE]
