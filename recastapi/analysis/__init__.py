BASEURL = 'http://recast.perimeterinstitute.ca/dev/api'

import os
import requests as httprequest
import json

def analysis(uuid = None):
  single_analysis = '/{}'.format(uuid) if uuid else ''
  r = httprequest.get('{}/recast-analysis{}.json'.format(BASEURL,single_analysis))
  analyses = json.loads(r.content)
  return (analyses[0] if uuid else analyses)
  
def createAnalysis(username,title,collaboration,e_print,journal,doi,inspire_url,description):
  payload = {
    'username':username,
    'title':title,
    'collaboration':collaboration,
    'e_print':e_print,
    'journal':journal,
    'doi':doi,
    'inspire_url':inspire_url,
    'description':description,
  }
  postbody = '&'.join(['='.join(x) for x in payload.iteritems()])
  r = httprequest.post('{}/recast-analysis.json'.format(BASEURL), data = payload)
  if not r.ok:
    print "http request failed for payload: ".format(postbody)
    print r.reason
    print r.content
    raise RuntimeError
  return json.loads(r.content)
  