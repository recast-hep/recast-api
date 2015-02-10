BASEURL = 'http://recast.perimeterinstitute.ca/dev/api'

import os
import requests as httprequest
import json

def request(uuid = None, maxpage = 100000):
  single_analysis = '/{}'.format(uuid) if uuid else ''
  r = httprequest.get('{}/recast-request{}.json?pagesize={}'.format(BASEURL,single_analysis,maxpage))
  analyses = json.loads(r.content)
  return (analyses[0] if uuid else analyses)

def accept(uuid, username):
  r = httprequest.post('{}/recast-request/{}/accept.json?username={}'.format(BASEURL,uuid,username))
  if not r.ok:
    print "http request failed for payload: ".format(postbody)
    print r.reason
    print r.content
    raise RuntimeError
  return json.loads(r.content)['response-uuid']

def add_parameter_point(uuid,username,description,nevents,xsec,filename):
  h = {
       'Content-Length': '1388402',
       'Content-Type': 'multipart/form-data',
       'Accept-Encoding': 'gzip, deflate',
       'Accept': '*/*',
       'User-Agent': 'python-requests/2.3.0 CPython/2.7.6 Darwin/14.0.0'
       }

  urlstring ='{}/recast-request/{}/add-parameter-point.json/?'.format(BASEURL,uuid)
  additionalparams = 'username={}&parameter_point={}&number_of_events={}&cross_sections={}&filename={}'.format(
                      username,description,nevents,xsec,filename)

  full_url =  urlstring+additionalparams
  r = httprequest.post(full_url,data=open(filename),headers=h)
  return r
  
def create(username,analysisuuid,model_type,title,predefined_model,reason,audience,activate,subscribers):
  payload = {'username':username,
            'model-type': model_type,
            'analysis-uuid': analysisuuid,
            'title': title,
            'predefined-model': predefined_model,
            'reason-for-request': reason,
            'audience': audience,
            'activate': '1' if activate else '0',
            'subscribers': ','.join(subscribers)}
  
  
  r = httprequest.post('{}/recast-request.json'.format(BASEURL),data=payload)
  if not r.ok:
    print "http request failed for payload: ".format(postbody)
    print r.reason
    print r.content
    raise RuntimeError
  return r