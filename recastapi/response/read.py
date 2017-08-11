import recastapi
import recastapi.user.read
from termcolor import colored
import urllib
import yaml
import json

def scan_response(scan_response_id =  None, scan_request_id = None):
    """List request depending on criteria
       If all variables are none all requests returned
    :param uuid: ID of the request(optional)
    :param analysis_id: Analysis ID to query. Returns all requests associated to the analysis

    :return: JSON object
    """
    if (scan_response_id is None) and (scan_request_id is None):
        response = recastapi.get(recastapi.ENDPOINTS['SCAN_RESPONSES'])
        return response['_items']

    if (scan_response_id is not None) and (scan_request_id is not None):
        raise RuntimeError('Cannot fetch scan_response_id and scan_request_id simultaneously')

    elif scan_response_id is not None:
        url = '{}/{}'.format(recastapi.ENDPOINTS['SCAN_RESPONSES'], scan_response_id)
        response = recastapi.get(url)
        return response

    elif scan_request_id is not None:
        selection_str = '?where=scan_request_id=="{}"'.format(scan_request_id)
        url = '{}{}'.format(recastapi.ENDPOINTS['SCAN_RESPONSES'], selection_str)
        response = recastapi.get(url)
        assert(len(response['_items']) < 2)
        if not response['_items']:
            return None
        return response['_items'][0]

def point_response(point_response_id =  None, point_request_id = None):
    """" Returns basic JSON. """
    if (point_response_id is None) and (point_request_id is None):
        response = recastapi.get(recastapi.ENDPOINTS['POINT_RESPONSES'])
        return response['_items']

    if (point_response_id is not None) and (point_request_id is not None):
        raise RuntimeError('Cannot fetch point_response_id and point_request_id simultaneously')

    elif point_response_id is not None:
        url = '{}/{}'.format(recastapi.ENDPOINTS['POINT_RESPONSES'], point_response_id)
        response = recastapi.get(url)
        return response

    elif point_request_id is not None:
        selection_str = '?where=point_request_id=="{}"'.format(point_request_id)
        url = '{}{}'.format(recastapi.ENDPOINTS['POINT_RESPONSES'], selection_str)
        response = recastapi.get(url)
        assert(len(response['_items']) < 2)
        if not response['_items']:
            return None
        return response['_items'][0]

def basic_response(basic_response_id =  None, basic_request_id_filter = None, description_filter = None):
    """" Returns basic JSON. """

    query = {}
    if description_filter:
        query.update(description = description_filter)
    if basic_request_id_filter:
        query.update(basic_request_id = basic_request_id_filter)
    if basic_response_id:
        query.update(id = basic_response_id)

    query = 'where={}'.format(json.dumps(query))

    print query

    url = '{}/?{}'.format(recastapi.ENDPOINTS['BASIC_RESPONSES'],query)
    response = recastapi.get(url)

    if basic_response_id:
        return response['_items'][0]
    else:
        return response['_items']

def response_archive(basic_response_id = None, basic_request_id = None, filename = None):
    if basic_response_id is None:
        basic_response_id = recastapi.response.read.basic_response(basic_request_id = basic_request_id )['id']

    selection_str = '?where=basic_response_id=="{}"'.format(basic_response_id)
    url = '{}{}'.format(recastapi.ENDPOINTS['RESPONSE_ARCHIVES'], selection_str)
    response = recastapi.get(
        url
    )
    archives = response['_items']
    assert len(archives)<2
    return archives[0] if archives else None
