import os
import requests as httprequest
import json
import recastapi

def createUser(name, email, orcid_id):
    payload = {
        'name':name,
        'email':email,
        'orcid_id':orcid_id,
        }
    postbody = '&'.join(['='.join(x) for x in payload.iteritems()])
    url = '{}/'.format(recastapi.ENDPOINTS['USERS'])
    r = httprequest.post(url, data=payload, auth=(recastapi.ORCID_ID, recastapi.ACCESS_TOKEN))
    if not r.ok:
        print "http request failed for payload: {} \t due to".format(postbody)
        print "\t de due to: {}".format(r.reason)
        print r.content
        raise RuntimeError
    return json.loads(r.content)

def user(id = None):
    single_user = '/{}'.format(id) if id else ''
    url = '{}{}'.format(recastapi.ENDPOINTS['USERS'], single_user)
    r = httprequest.get(url)
    users = json.loads(r.content)
    return users

def userData():
    if recastapi.ORCID_ID and recastapi.ACCESS_TOKEN:
        url = '{}'.format(recastapi.ENDPOINTS['USERS'])
        #search eve
        
                          
