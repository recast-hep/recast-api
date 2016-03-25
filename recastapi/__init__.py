from settings import *
import requests as httprequest
import traceback, sys
import json

def post(url, data=None):
    response = httprequest.post(url, data=data, auth=(ORCID_ID, ACCESS_TOKEN))
    if not response.ok:
        print '-'*60
        print "Exception in user code:", response.status_code
        print "\t HTTP request failed"
        print "\t due to: {}".format(response.reason)
        print "\t ", response.content
        print "\t data: ", data
        print '\n'
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** exception:"
        traceback.print_tb(exc_type, exc_value, exc_traceback)
        raise RuntimeError
    return json.loads(response.content)
        

def get(url):
    response = httprequest.get(url)
    if not response.ok:
        print '-'*60
        print "Exception in user code:"
        print "\t HTTP request failed"
        print "\t due to: {}".format(response.reason)
        print response.content
        print '\n'
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** exception:"
        traceback.print_tb(exc_type, exc_value, exc_traceback)
        raise RuntimeError
    return json.loads(response.content)
