import os
import requests as httprequest
import json
import recastapi

def create(name, email, orcid_id=None):
    """create a new user.

    Args:
        name: First and last name of the user.
        email: Email of the user.
        orcid_id: ORCID ID of the user.

    Returns:
        JSON object with added data.
    """
    payload = {
        'name':name,
        'email':email,
        'orcid_id':orcid_id,
        }
    postbody = '&'.join(['='.join(x) for x in payload.iteritems()])
    url = '{}/'.format(recastapi.ENDPOINTS['USERS'])
    return recastapi.post(url, payload)

def user(id = None):
    """Lists user information.
    
    Args:
        id: Optional, if provided will return data of a single user.
    Returns:
        JSON object containing all data that could be retrieved.
    
    """
    single_user = '/{}'.format(id) if id else ''
    url = '{}{}'.format(recastapi.ENDPOINTS['USERS'], single_user)
    r = httprequest.get(url)
    return recastapi.get(url)

def userData():
    """Lists user given his ORCID ID
    
    Args:
        None
    Returns:
        JSON object
    """
    if not recastapi.ORCID_ID:
        print '-'*60
        print "No ORCID ID and ACCESS TOKEN provide"
        print "Please provide an ORCID ID"
        raise RuntimeError
    url = '{}?where=orcid_id=="{}"'.format(recastapi.ENDPOINTS['USERS'], recastapi.ORCID_ID)
    return recastapi.get(url)
    
                          
