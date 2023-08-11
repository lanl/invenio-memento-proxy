# Memento Proxy for Invenio
Make your web resources [Memento](http://www.mementoweb.org) compliant in a few easy steps.

The Memento framework enables datetime negotiation for web resources. Knowing the URI of a Memento-compliant web resource, a user can select a date and see what it was like around that time.


## Introduction

In order to support Memento, a web server must obviously have accessible archives of its online resources. And it must also have a piece of software that handles the datetime negotiation according to the Memento protocol for those resources.

But in such datetime negotiation server, only a small proportion of the code is specific to the particular web resources it handles. The main part of logic will be very similar throughout many implementations.


From now on, this documentation will refer to the web server where resources and archives are as the **web server** and to the Memento TimeGate datetime negotiation server as the **TimeGate**.

* Suppose you have a web resource accessible in a web server by some URI. We call the resource the **Original Resource** and refer to its URI as **URI-R**.
* Suppose a web server has a snapshot of what this URI-R looked like in the past. We call such a snapshot a **Memento** and we refer to its URI as **URI-M**. There could be many snapshots of URI-R, taken at different moments in time, each with their distinct URI-Ms.
The Mementos do not necessary need to be in the same web server as the Original Resources.


There are only two steps to make such resource Memento compliant.

## Step 1: Setting up Invenio TimeGate
The first thing to do is to set up the TimeGate for the specific web server.
* Run the TimeGate with your custom Invenio  handler. 


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
