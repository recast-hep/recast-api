BASEURL = 'http://recast-rest-api.herokuapp.com'

import os
import requests as httprequest
import json

def user_response(username):
  r = httprequest.get('{}/responses.json?pagesize=100000&username={}'.format(BASEURL,username))
  resonses = json.loads(r.content)
  return resonses


