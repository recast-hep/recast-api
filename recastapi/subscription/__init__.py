BASEURL = 'http://recast.perimeterinstitute.ca/dev/api'

import os
import requests as httprequest
import json

def subscribe(analysisuuid, username, subscriptiontype, requirements, notifications = []):
  assert subscriptiontype in ['provider','observer']
  for notif in notifications:
    assert notif in ['recast_requests','recast_responses','new_subscribers']

  payload = {
    'analysis-uuid':analysisuuid,
    'username':username,
    'subscription-type':subscriptiontype,
    'requirements':requirements,
    'notifications':','.join(notifications)
  }
  postbody = '&'.join(['='.join(x) for x in payload.iteritems()])

  r = httprequest.post('{}/recast-subscription.json'.format(BASEURL), data = payload)
  if not r.ok:
    print "http request failed for payload: ".format(postbody)
    print r.reason
    print r.content
    raise RuntimeError

  return json.loads(r.content)
