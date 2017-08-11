import recastapi.request.read
import recastapi.user.read
import uuid
import os

def scan_request(analysis_id,
                 title,
                 description_model,
                 reason_for_request,
                 additional_information,
                 status="Incomplete",
                 ):
    """Creates a new request

    :param analysis_id: ID of the analysis.
    :param description_model: Detailed description of the model to use.
    :param reason_for_request: Reason for submitting this request.
    :param additional_information: Any other additional information associated to this request.
    :param status: Defaults to Incomplete.

    :return: JSON object with data added
    """
    user = recastapi.user.read.this_user()

    payload = {
        'requester_id': user['id'],
        'title': title,
        'reason_for_request': reason_for_request,
        'additional_information': additional_information,
        'analysis_id': analysis_id,
        'description_of_model': description_model,
        'status': status,
    }
    url = '{}/'.format(recastapi.ENDPOINTS['SCAN_REQUESTS'])
    post_response = recastapi.post(url, data=payload)
    return post_response

def point_request(scan_request_id):
    """Adds point request
    :param request_id: ID of the request.
    :return: JSON object
    """
    user = recastapi.user.read.this_user()
    payload = {
        "scan_request_id": scan_request_id,
        "requester_id": user['id'],
    }
    url = '{}'.format(recastapi.ENDPOINTS['POINT_REQUESTS'])
    return recastapi.post(url, json=payload)

def coordinate(name,value,point_request_id):
    payload = {
        "point_request_id": point_request_id,
        "title":name,
        "value":value
    }
    url = '{}'.format(recastapi.ENDPOINTS['POINT_COORDINATES'])
    return recastapi.post(url, json=payload)


def point_request_with_coords(scan_request_id,coordinate_map):
    pr = point_request(scan_request_id)
    for k,v in coordinate_map.iteritems():
        coordinate(k,float(v),pr['id'])
    return pr

def basic_request(point_request_id,request_format):
    """Adds basic request
    :param point_request_id: ID of the point request
    :return: JSON object
    """
    user = recastapi.user.read.this_user()
    payload = {
        'request_format': request_format,
        'requester_id': user['id'],
        'point_request_id': point_request_id,
    }
    url = '{}/'.format(recastapi.ENDPOINTS['BASIC_REQUESTS'])
    return recastapi.post(url, data=payload)

def basic_request_with_archive(point_request_id,filename,request_format):
    br = basic_request(point_request_id,request_format)
    request_archive(br['id'],filename)
    return br

def request_archive(basic_request_id, filename = None):
    payload = {
        'basic_request_id': basic_request_id,
        'original_file_name': os.path.basename(filename),
    }

    files = {'file': open(filename, 'rb')} if filename else {}
    url = '{}/'.format(recastapi.ENDPOINTS['REQUEST_ARCHIVES'])
    basic_request_archive = recastapi.post(
        url,
        data=payload,
        files=files,
    )
    return basic_request_archive
