# Memento Proxy for Invenio
Make your web resources [Memento](http://www.mementoweb.org) compliant in a few easy steps.

The Memento framework enables datetime negotiation for web resources. Knowing the URI of a Memento-compliant web resource, a user can select a date and see what it was like around that time.


## Introduction

In order to support Memento, a web server must obviously have accessible archives of its online resources. And it must also have a piece of software that handles the datetime negotiation according to the Memento protocol for those resources.




From now on, this documentation will refer to the web server where resources and archives are as the **web server** and to the Memento TimeGate datetime negotiation server as the **TimeGate**.

* Suppose you have a web resource accessible in a web server by some URI. We call the resource the **Original Resource** and refer to its URI as **URI-R**.
* Suppose a web server has a snapshot of what this URI-R looked like in the past. We call such a snapshot a **Memento** and we refer to its URI as **URI-M**. There could be many snapshots of URI-R, taken at different moments in time, each with their distinct URI-Ms.
The Mementos do not necessary need to be in the same web server as the Original Resources.


There are only two steps to make such resource Memento compliant.

## Step 1: Setting up Invenio Proxy

# Setup

The Invenio proxy software is downloaded, installed and run from within a Python Virtual Environment.
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


The uWsgi configuration file for a proxy is `timegate.ini` in the `./timegate/conf` folder.
Edit directories relevant to your installation path
```bash
# home of vertual env
home = /data/venv/timegate/
# directory for project install
chdir = /home/ludab/invenio-memento-proxy

# python path
pythonpath = /data/venv/timegate/lib/python3.8/site-packages
```
To start a proxy,

```bash
$ source /data/venv/timegate/bin/activate
$ uwsgi --http :9999 -s /tmp/mysock.sock --module timegate.application --callable application --virtualenv /home/ludab/timegate/
```

Test that service is working:
```bash
curl   http://localhost:9999/timemap/link/https://data.caltech.edu/api/records/tds5b-9rs75/files/README.txt 
```
The invenio handler configured for caltech example. Adapt your installation 
go to ./invenio-memento-proxy/timegate/examples
and change baseurl to your invenio installation

```bash
baseurl = "https://data.caltech.edu/"
```
To configure service under nginx
Change  uWsgi configuration file for a proxy : `timegate.ini` in the `./timegate/conf` folder.
```bash
daemonize = /data/var/logs/timegate/caltech.log                                                                                                                                                                                        
pidfile = /data/var/run/timegate/caltech.pid
```
Change to hostname in config.ini in the `./timegate/conf` folder.
```bash
host = http://localhost/
```
Add section to nginx config:
```bash
location / {
                include uwsgi_params;
                uwsgi_pass unix:///data/var/run/timegate/caltech.sock;
        }
```        
To start a proxy,

```bash
$ source /data/venv/timegate/bin/activate
$ uwsgi   --module timegate.application --callable application --virtualenv /home/ludab/timegate/
```
To restart or stop a proxy,
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
