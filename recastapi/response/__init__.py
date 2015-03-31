BASEURL = 'http://recast.perimeterinstitute.ca/dev/api'

import os
import requests as httprequest
import json

def user_response(username):
  r = httprequest.get('{}/recast-response.json?pagesize=100000&username={}'.format(BASEURL,username))
  resonses = json.loads(r.content)
  return resonses

def update(responseuuid,response_file):
  h = {
       'Content-Length': '1388402',
       'Content-Type': 'multipart/form-data',
       'Accept-Encoding': 'gzip, deflate',
       'Accept': '*/*',
       'User-Agent': 'python-requests/2.3.0 CPython/2.7.6 Darwin/14.0.0'
       }

  urlstring ='{}/recast-response/{}/update?'.format(BASEURL,responseuuid)
  additionalparams = 'filename={}'.format(os.path.basename(response_file))
  full_url =  urlstring+additionalparams
  r = httprequest.post(full_url,data=open(response_file),headers=h)
  if not r.ok:
    print r.reason
    print r.content
    raise RuntimeError
  return r
