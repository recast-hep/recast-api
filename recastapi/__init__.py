from settings import *
import requests as httprequest
import traceback, sys
import json as json_obj

def post(url, data=None, params=None, files=None, json=None):
    print "-*"*30
    try:
        print type(data['value'])
    except Exception, e:
        pass
    print data
    print json
    response = httprequest.post(url, 
                                data=data, 
                                auth=(ORCID_ID, ACCESS_TOKEN), 
                                params=params,
                                files=files,
                                json=json)
    print response
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
    return json_obj.loads(response.content)
        

def get(url, params=None):
    response = httprequest.get(url, params=params)
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
    return json_obj.loads(response.content)
