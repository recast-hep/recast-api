import recastapi
import recastapi.user.read
from termcolor import colored
import urllib
import yaml

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

def basic_response(basic_response_id =  None, basic_request_id = None):
    """" Returns basic JSON. """

    if (basic_response_id is None) and (basic_request_id is None):
        response = recastapi.get(recastapi.ENDPOINTS['BASIC_RESPONSES'])
        return response['_items']

    if (basic_response_id is not None) and (basic_request_id is not None):
        raise RuntimeError('Cannot fetch basic_response_id and basic_request_id simultaneously')

    elif basic_response_id is not None:
        url = '{}/{}'.format(recastapi.ENDPOINTS['BASIC_RESPONSES'], basic_response_id)
        response = recastapi.get(url)
        return response

    elif basic_request_id is not None:
        selection_str = '?where=basic_request_id=="{}"'.format(basic_request_id)
        url = '{}{}'.format(recastapi.ENDPOINTS['BASIC_RESPONSES'], selection_str)
        response = recastapi.get(url)
        assert(len(response['_items']) < 2)
        if not response['_items']:
            return None
        return response['_items'][0]

# def point_request_of_scan(scan_request_id, point_request_index=None):
#     """Returns list of point requests or single point reqeusts
#     :param scan_request_id: the request ID to query
#     :param point_request_index: starting from 0
#     """
#     point_req_url = '{}?where=scan_request_id=="{}"'.format(
#         recastapi.ENDPOINTS['POINT_REQUESTS'],
#         scan_request_id
#     )
#     point_api_response = recastapi.get(point_req_url)
#
#     if point_request_index is None:
#         return point_api_response['_items']
#
#     if point_request_index in range(len(point_api_response['_items'])):
#         point_api_response['_items'][point_request_index]
#         return point_api_response['_items'][point_request_index]
#     else:
#         raise RuntimeError('Pameter index out of bounds')
#
# def coordinate(point_request_id, coordinate_index=None):
#     """Returns list of coordinates given a parameter index and request_id
#     or single coordinate
#
#     :param request_id: ID of the request
#     :param parameter_index: index of the parameter
#     :param coordinate_index: index of the coordinate.
#                             `if` none given returns list of coordinate
#     :return: JSON object
#     """
#
#     filtered_coordinate_url = '{}?where=point_request_id=="{}"'.format(
#         recastapi.ENDPOINTS['POINT_COORDINATES'],
#         point_request_id
#     )
#
#     filtered_coordinate_response = recastapi.get(filtered_coordinate_url)
#
#     if coordinate_index is None:
#         #No coordinate index given, return all coords.
#         return filtered_coordinate_response['_items']
#
#     if coordinate_index in range(len(filtered_coordinate_response['_items'])):
#         #return coords index
#         return filtered_coordinate_response['_items'][coordinate_index]
#     else:
#         raise RuntimeError('Coordinate index out of bounds')
#
#
# def basic_request_for_point(point_request_id):
#     basic_url = '{}?where=point_request_id=="{}"'.format(
#                         recastapi.ENDPOINTS['BASIC_REQUESTS'],
#                         point_request_id)
#     return recastapi.get(basic_url)
#
# def request_archive(archive_id):
#     archive_url = '{}/{}'.format(recastapi.ENDPOINTS['REQUEST_ARCHIVES'], archive_id)
#     archive_url_response = recastapi.get(archive_url)
#     return archive_url_response
#
# def request_archive_for_request(basic_request_id, download_path = None, dry_run = False):
#     files_url = '{}?where=basic_request_id=="{}"'.format(recastapi.ENDPOINTS['REQUEST_ARCHIVES'], basic_request_id)
#     files_url_response = recastapi.get(files_url)
#     links =  [request_archive(x['id'])['file_link'] for x in files_url_response['_items']]
#     if len(links) > 1:
#         raise RuntimeError('more than one request archive? not downloading...')
#     link = links[0]
#     if dry_run:
#         return link
#     else:
#         if download_path:
#             download_file(link,download_path)
#         else:
#             raise RuntimeError('no download path given')
#
# def download_file(file_url, download_path):
#     """ Worker function that actually downloads file"""
#     zip_file = urllib.URLopener()
#     zip_file.retrieve(file_url, download_path or response['original_file_name'])
