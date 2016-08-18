import os
BASEURL = os.environ.get('RECAST_APIURL','http://recast-frontend-beta.cern.ch:81/')

ENDPOINTS = {
    'USERS': BASEURL + 'users',
    'RUN_CONDITIONS': BASEURL + 'run_conditions',
    'ANALYSIS': BASEURL + 'analysis',

    'SCAN_REQUESTS': BASEURL + 'scan_requests',
    'POINT_REQUESTS': BASEURL + 'point_requests',
    'POINT_COORDINATES': BASEURL + 'point_coordinates',
    'BASIC_REQUESTS': BASEURL + 'basic_requests',
    'REQUEST_ARCHIVES': BASEURL + 'request_archives',

    'SCAN_RESPONSES': BASEURL + 'scan_responses',
    'POINT_RESPONSES': BASEURL + 'point_responses',
    'BASIC_RESPONSES': BASEURL + 'basic_responses',
    'RESPONSE_ARCHIVES': BASEURL + 'response_archives'
}


ORCID_ID = os.environ.get('RECAST_ORCID','')
ACCESS_TOKEN = os.environ.get('RECAST_APITOKEN','')
allowed_extension = '.zip'
