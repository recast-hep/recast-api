import os
BASEURL = os.environ.get('RECAST_APIURL','http://recast-frontend-beta.cern.ch:81/')

ENDPOINTS = {
    'USERS': BASEURL + 'users',
    'RUN_CONDITIONS': BASEURL + 'run_conditions',
    'ANALYSIS': BASEURL + 'analysis',
    'REQUESTS': BASEURL + 'requests',
    'POINT_REQUESTS': BASEURL + 'point_requests',
    'PARAMETER_POINTS': BASEURL + 'parameter_points',
    'BASIC_REQUESTS': BASEURL + 'basic_requests',
    'FILES': BASEURL + 'request_archives',
    'SUBSCRIPTIONS': BASEURL + 'subscriptions',
    'RESPONSES': BASEURL + 'responses',
    'POINT_RESPONSES': BASEURL + 'point_responses',
    'BASIC_RESPONSES': BASEURL + 'basic_responses',
    'HISTOGRAMS': BASEURL + 'response_archives'
    }


ORCID_ID = os.environ.get('RECAST_ORCID','')
ACCESS_TOKEN = os.environ.get('RECAST_APITOKEN','')
allowed_extension = '.zip'
