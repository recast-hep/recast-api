import os
import requests as httprequest
import json
import recastapi

"""
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
"""

def create(analysis_id, subscription_type, description, 
           requirements, notifications=[], authoritative='False'):
  user = recastapi.user.userData()
  payload = {
    'subscription_type': subscription_type,
    'description': description,
    'requirements': requirements,
    'notification': ','.join(notifications),
    'authoritative': authoritative,
    'subscriber_id': user['id'],
    'analysis_id': analysis_id,
    }
  url = '{}/'.format(recastapi.ENDPOINTS['SUBSCRIPTIONS'])
  return recastapi.post(url, payload)


def unsubscribe(analysis_id=None):
  pass

def my_subscriptions():
  if not recastapi.ORCID_ID:
    print "Can't list your subscriptions."
    print "Please provide an ORCID_ID and ACCESS_TOKEN"
    raise RuntimeError
  user = recastapi.user.userData()
  id = user['_items'][0]['id']
  url = '{}?where=subscriber_id=="{}"'.format(recastapi.ENDPOINTS['SUBSCRIPTIONS'], id)
  return recastapi.get(url)
  
