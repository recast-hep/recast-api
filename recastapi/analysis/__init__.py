BASEURL = 'http://recast.perimeterinstitute.ca/dev/api'

import os
import requests as httprequest
import json

def analysis(uuid = None):
  single_analysis = '/{}'.format(uuid) if uuid else ''
  r = httprequest.get('{}/recast-analysis{}.json'.format(BASEURL,single_analysis))
  analyses = json.loads(r.content)
  return (analyses[0] if uuid else analyses)