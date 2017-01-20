from settings import ORCID_ID, ACCESS_TOKEN, ENDPOINTS, BASEURL, allowed_extension
import requests as httprequest
import traceback, sys
import json as json_obj
import yaml
import os
import logging
log = logging.getLogger(__name__)

SSL_VERIFY = yaml.load(os.environ['RECAST_SSL_VERIFY'])

def print_failure(response):
    print '-'*60
    print "", response.status_code
    print "\t HTTP request failed"
    print "\t url was {}".format(response.url)
    print "\t due to: {}".format(response.reason)
    print "\t ", response.content
    print '\n'
    exc_type, exc_value, exc_traceback = sys.exc_info()

    print "*** exception:"
    traceback.print_tb(exc_type, exc_value, exc_traceback)
    raise RuntimeError('Exception in user code')

def file_check(filename):
    if not os.path.isfile(filename):
	raise Exception('File does not exit: {}'.format(filename))

    if not filename.endswith(allowed_extension):
        print "File extension not allowed"
        raise RuntimeError

def post(url, data=None, params=None, files=None, json=None):
    response = httprequest.post(url,
                                data=data,
                                auth=(ORCID_ID, ACCESS_TOKEN),
                                params=params,
                                files=files,
                                json=json,
                                verify = SSL_VERIFY)
    if not response.ok:
        print_failure(response)
    return json_obj.loads(response.content)

def get(url, params=None):
    response = httprequest.get(url, params=params,verify = SSL_VERIFY)
    if not response.ok:
        print_failure(response)
    return json_obj.loads(response.content)

def delete(url):
    response = httprequest.delete(url, verify = SSL_VERIFY)
    if not response.ok:
        print_failure(response)

    return json_obj.loads(response.content)

def put(url, data=None):
    response = httprequest.put(url, auth=(ORCID_ID, ACCESS_TOKEN), json = data, verify = SSL_VERIFY)
    if not response.ok:
        print_failure(response)

    return json_obj.loads(response.content)

def patch(url, data=None, files = None):
    response = httprequest.patch(url, auth=(ORCID_ID, ACCESS_TOKEN), json = data, files = files, verify = SSL_VERIFY)
    if not response.ok:
        print_failure(response)

    return json_obj.loads(response.content)

def patch2(url, data=None, files = None):
    response = httprequest.patch(url, auth=(ORCID_ID, ACCESS_TOKEN), data = data, files = files, verify = SSL_VERIFY)
    if not response.ok:
        print_failure(response)

    return json_obj.loads(response.content)
