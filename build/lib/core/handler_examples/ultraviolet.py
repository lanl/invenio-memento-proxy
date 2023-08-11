import StringIO
import logging
import json
import requests

#import re
#from lxml import etree

from core.handler_baseclass import Handler


__author__ = "Lyudmila Balakireva"

class UltravioletHandler(Handler):
    def json_extract(obj, key):
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

        #self.datere = re.compile('http://webarchive.loc.gov/[a-zA-Z0-9]+/([0-9]+)/.+')
    def get_key(url):    
        key = None
        url_split = s.split("/")
        for i in url_split:
           if i == "records":
               j = url_split.index(i)
               key = url_split[j+1]
        return key    

    def get_all_mementos(self, requri):
        changes = []
        #s = "https://127.0.0.1:5000/records/ykean-hxp73/files/JCDL2023.pdf "

        #s = "https://127.0.0.1:5000/records/ykean-hxp73/files"
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
               if j+1<count-1:
                 file = url_split[j+1]
               
               rest =  "/"+url_split[j]+"/"+ file
        vurl="https://ultraviolet.library.nyu.edu/api/records/%s/versions" % (key)

        #surl="https://127.0.0.1:5000/search?q=parent.id%S&f=allversions%3Atrue&l=list&p=1&s=1000000&sort=version"%(parent)

        print(vurl) 
        print(file)
        #http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        #response = http.request('GET', vurl )
        #data = response.data
        #params = {}
        #resp = requests.get(vurl, params=params)
        resp = requests.get(vurl,verify=False)
        print(data)
        #h_values=json_extract(resp.json(), 'hits')
        #print(h_values)
        s_values=json_extract(resp.json(), 'self_html')
        f_values=s_values
        if rest!= None:
           f_values = [x + rest for x in s_values]
           print(f_values)
        u_values=json_extract(resp.json(), 'updated')
        u_values = [x[0:x.find(".")]  for x in u_values]
        print(u_values)
        #c_values=json_extract(resp.json(), 'created')
        #print(c_values)
        #schema_dict = dict(zip(s_values, u_values))
        
        for loc in f_values:
        #   if loc j = 
            k=f_values.index(loc)
            print(k)
            print(loc)
            print(u_values[k])
            changes.append((loc, u_values[k]))
        
        return changes
    
