import os
import requests as httprequest
import json
import recastapi

def createUser(name, email, orcid_id=''):
    payload = {
        'name':name,
        'email':email,
        'orcid_id':orcid_id,
        }
    postbody = '&'.join(['='.join(x) for x in payload.iteritems()])
    url = '{}/'.format(recastapi.ENDPOINTS['USERS'])
    return recastapi.post(url, payload)

def user(id = None):
    single_user = '/{}'.format(id) if id else ''
    url = '{}{}'.format(recastapi.ENDPOINTS['USERS'], single_user)
    r = httprequest.get(url)
    return recastapi.get(url)

def userData():
    if not recastapi.ORCID_ID:
        print '-'*60
        print "No ORCID ID and ACCESS TOKEN provide"
        print "Please provide an ORCID ID"
        raise RuntimeError
    url = '{}?where=orcid_id=="{}"'.format(recastapi.ENDPOINTS['USERS'], recastapi.ORCID_ID)
    print url
    return recastapi.get(url)
    
                          
