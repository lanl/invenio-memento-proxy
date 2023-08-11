from __future__ import print_function
import StringIO
import logging
import json
import requests
import logging

from errors.timegateerrors import HandlerError
#import re
#from lxml import etree

from core.handler_baseclass import Handler


__author__ = "Lyudmila Balakireva"
baseurl = "https://data.caltech.edu/"
#change to your invenio install
#baseurl = https://ultraviolet.library.nyu.edu/"

class InvenioHandler(Handler):

    def __init__(self):
        Handler.__init__(self)

    def json_extract(self,obj, key):
        """Recursively fetch values from nested JSON."""
        arr = []
    
        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr
    
        values = extract(obj, arr, key)
        return values

        
    def get_key(url):    
        key = None
        url_split = s.split("/")
        for i in url_split:
           if i == "records":
               j = url_split.index(i)
               key = url_split[j+1]
        return key    

    def get_all_mementos(self, requri):
    
        """Gets all mementos for the given request URI.

        Args:
        requri: The request URI.

        Returns:
        A list of tuples, where each tuple contains the location uri of the memento and
        the timestamp of the memento.
        """
        changes = []
        
        res=requests.head(requri,verify=False)
        if res.status_code >= 400:
           raise HandlerError(
                "Resource not found, empty response from API", 404)

        key = None
        file = None
        rest = None
        parentkey = None
        url_split = requri.split("/")
        count = len(url_split)
        print(count) 
        for i in url_split:
           if i == "records":
               j = url_split.index(i)
               key = url_split[j+1]
           if  i == "files":
               j = url_split.index(i)
               file=""
               if j+1<count:
                 file = url_split[j+1]
               
               rest =  "/"+url_split[j]+"/"+ file
               logging.info("rest %s" % rest)
               print (rest)
        vurl=baseurl+"/api/records/%s/versions" % (key)

        

        print (vurl) 
        
        print (file)
        
        resp = requests.get(vurl,verify=False)
        data = resp.json()
        print (data)
        s_values = self.json_extract(data,'self_html')
        f_values=s_values
        if rest!= None:
           f_values = [x + rest for x in s_values]
           print(f_values)
        #u_values = self.json_extract(data,'updated')
        u_values = self.json_extract(data,'created')
        u_values = [x[0:x.find(".")]  for x in u_values]
        print(u_values)
        
        
        for loc in f_values:
        #   if loc j = 
            k=f_values.index(loc)
            print(k)
            print(loc)
            print(u_values[k])
            resp = requests.head(loc,verify=False)
            if resp.status_code < 400:
               changes.append((loc, u_values[k]))
        
        return changes
    
