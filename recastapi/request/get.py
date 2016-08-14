import recastapi
import recastapi.user.get
from termcolor import colored
import urllib
import yaml

def request(uuid=None,
            analysis_id=None,
            query='?max_results=1000&page=1'):
    """List request depending on criteria
       If all variables are none all requests returned


    :param uuid: ID of the request(optional)
    :param analysis_id: Analysis ID to query. Returns all requests associated to the analysis

    :return: JSON object
    """
    if analysis_id and uuid:
        print "*"*60
        print "Cannot fetch analysis and uuid simultaneously"
        print "Please provide either an analysis or uuid"
        raise RuntimeError

    elif uuid:
        single_request = '/{}'.format(uuid)
        url = '{}{}'.format(recastapi.ENDPOINTS['REQUESTS'], single_request)
        response = recastapi.get(url)
        return response

    elif analysis_id:
        analysis_str = '?where=analysis_id=="{}"'.format(analysis_id)
        url = '{}{}'.format(recastapi.ENDPOINTS['REQUESTS'], analysis_str)
        response = recastapi.get(url)
        return response['_items']

    else:
        url = '{}{}'.format(recastapi.ENDPOINTS['REQUESTS'], query)
        response = recastapi.get(url)
        return response['_items']

def query(query=None):
    """ function for customized query """

    url = '{}{}'.format(recastapi.ENDPOINTS['REQUESTS'], query)
    response = recastapi.get(url)
    if response.has_key('_items'):
        return response['_items']
    else:
        return response


def parameter(request_id,
              parameter_index=None):
    """Returns list of parameters or single parameter

    :param request_id: the request ID to query
    :param parameter_index: starting from 0
    """

    parameters_url = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'],
        request_id
    )
    parameter_responses = recastapi.get(parameters_url)

    if not parameter_index and not parameter_index == 0:
        #No parameter index given, return all
        for i, parameter in enumerate(parameter_responses['_items']):
            parameter['coordinates'] = get_coordinate(parameter['id'])
            parameter['files'] = archives(request_id=request_id,
                                          parameter_index=i,
                                          basic_index=None)

        return parameter_responses['_items']

    if parameter_index >= 0 and parameter_index < len(parameter_responses['_items']):
        # if the parameter index is defined
        parameter_responses['_items'][parameter_index]['coordinates'] = get_coordinate(
            parameter_responses['_items'][parameter_index]['id'])

        parameter_responses['_items'][parameter_index]['files'] = archives(
            request_id=request_id,
            parameter_index=parameter_index,
            basic_index=None)

        return parameter_responses['_items'][parameter_index]

    else:
        #parameter index not found
        print '-'*60
        print "Exception in user code:"
        print "\t ****** Pameter index not found"
        print '\n'
        raise RuntimeError


def coordinate(request_id, parameter_index=0, coordinate_index=None):
    """Returns list of coordinates given a parameter index and request_id \
              or single coordinate


    :param request_id: ID of the request
    :param parameter_index: index of the parameter
    :param coordinate_index: index of the coordinate.
                            `if` none given returns list of coordinate
    :return: JSON object
    """
    if not parameter_index and not parameter_index ==0:
        print '-'*60
        print "Exception in user code:"
        print "\t ****** Parameter index not valid"
        print '\n'
        raise RuntimeError

    response = parameter(request_id = request_id,
                         parameter_index = parameter_index)

    if not coordinate_index and not coordinate_index == 0:
        #No coordinate index given, return all coords.
        return response['coordinates']

    if coordinate_index < len(response['coordinates'])  and coordinate_index >= 0:
        #return coords index
        return response['coordinates'][coordinate_index]
    else:
        print '-'*60
        print "Exception in user code:"
        print "\t ******* Coordinate index out of bounds"
        print '\n'
        raise RuntimeError

def basic_request(basic_request_id):
    """" Returns basic JSON. """
    url = '{}/{}'.format(recastapi.ENDPOINTS['BASIC_REQUESTS'], basic_request_id)
    response = recastapi.get(url)
    return response

def point_request(point_request_id):
    url = '{}/{}'.format(recastapi.ENDPOINTS['POINT_REQUESTS'],point_request_id)
    return recastapi.get(url)

def point_requests_for_scan(scan_requests_id):
    filtered_point_url = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'],
        scan_requests_id
    )
    return recastapi.get(filtered_point_url)

def basic_requests_for_point(point_request_id):
    basic_url = '{}?where=point_request_id=="{}"'.format(
                        recastapi.ENDPOINTS['BASIC_REQUESTS'],
                        point_request_id)
    return recastapi.get(basic_url)

def archives(request_id, point_index=0, basic_index=None):
    """ Returns list of files given the request id and parameter index

    :param request_id: ID of the request
    :param parameter_index: index of the parameter point
    :param basic_index: index of the basic request


    :return: JSON object `or` list if basic_index is None
    """
    if not parameter_index and not point_index ==0:
        print '-'*60
        print "Exception in user code:"
        print "\t ******* Parameter index not valid"
        print '\n'
        raise RuntimeError

    points_of_scan = point_requests_for_scan(request_id)

    #check if we have the right parameter_index
    if point_index > len(points_of_scan['_items']):
        print '-'*60
        print "Excepton in user code:"
        print "\t ********* Parameter index out of bound"
        print '\n'
        raise RuntimeError

    point_request_id = points_of_scan['_items'][point_index]['id']
    basic_responses = basic_requests_for_point(point_request_id)

    if basic_index is None:
        #return all basic request index
        basic_responses = []
        for i, basic in enumerate(basic_response['_items']):
            response = download(request_id=request_id,
                                point_request_index=point_index,
                                basic_request_index=i,
                                download_path=None,
                                dry_run=True)

            basic_responses.append(response)
        return basic_responses

    else:
        #return single indexed basic request
        basic_response = download(request_id=request_id,
                                  point_request_index=parameter_index,
                                  basic_request_index=basic_index,
                                  download_path=None,
                                  dry_run=True)
        return basic_response


def get_coordinate(point_request_id):
    """ Private function

    """
    coordinate_url = '{}?where=point_request_id=="{}"'.format(
        recastapi.ENDPOINTS['PARAMETER_POINTS'],
        point_request_id
    )

    coordinate_responses = recastapi.get(coordinate_url)
    return coordinate_responses['_items']


def user_request(username):
    pass

def download_file(basic_request_id, download_path=None, dry_run=False):
    """ Worker function that actually downloads file


    :param basic_request_id: ID of the basic request associated with a file.
    :param donwload_path: User specified download path(optional), if not
                   provided, file takes original file_name.
    :param dry_run: whether to download file or not. If false link of file provided
                    in response object


    :return: JSON object containing the metadata of the file, and file downloaded saved on disk.
    """
    local_path_key_name = 'local_path' #path of the downloaded file on local machine
    files_urls = '{}?where=basic_request_id=="{}"'.format(
        recastapi.ENDPOINTS['FILES'], basic_request_id)

    responses = None
    url_response = recastapi.get(files_urls)

    if len(url_response['_items']) == 1:
        # File exist
        url = ('{}/{}'.format(recastapi.ENDPOINTS['FILES'],
                              url_response['_items'][0]['id']))
        response = recastapi.get(url)
        link = response['file_link']
        if link:
            if not dry_run:
                zip_file = urllib.URLopener()
                zip_file.retrieve(link, download_path or response['original_file_name'])
                response['local_path_key_name'] = download_path or response['original_file_name']
                print colored('Successfully downloaded file {}'.format(
                    download_path or response['original_file_name']), 'green')
            else:
                print colored('File link: {}'.format(
                    response['file_link']), 'green')
        else:
            response[local_path_key_name] = None
            print colored('Failed to download file {}'.format(
                download_path or response['original_file_name']), 'red')
            print colored('\t Please check if this request is associated with a file', 'red')
        responses = response

    elif len(url_response['_items']) == 0:
        # No files for this basic request
        print colored('No files for this basic request', 'red')

    else:
        # File length greater than 1 (this should never happen)
        print colored('BASIC REQUEST ERROR', 'red')
    return responses

def download(request_id,
             point_request_index=0,
             basic_request_index=0,
             download_path=None,
             dry_run=False):
    """Downloads file associated with a given request, index through point and basic requests.


    :param request_id: ID of the request.
    :param point_request_index: index of the point request 0..N-1.
    :param basic_request_index: index of basic request 0..M-1.
    :param dry_run: whether to download file or not


    :return: JSON object with metadata of files downloaded on disk.
    """
    print colored('Downloading....', 'cyan')
    print colored('Request: {}.\n\t Point request index: {}. \n\t\t Basic request index: {}.'
                  .format(request_id, point_request_index, basic_request_index), 'cyan')

    url_point_request = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)

    response_point_request = recastapi.get(url_point_request)
    if point_request_index > len(response_point_request['_items'])-1:
        print colored('ERR: Point request index out of range. Max range is {}'.format(
            len(response_point_request['_items'])), 'red')
        return

    url_basic_request = '{}?where=point_request_id=="{}"'.format(
        recastapi.ENDPOINTS['BASIC_REQUESTS'],
        response_point_request['_items'][point_request_index]['id'])

    response_basic_request = recastapi.get(url_basic_request)

    if basic_request_index > len(response_basic_request['_items'])-1:
        print colored('ERR: Basic request index out of range. Max range is {}'.format(
            len(response_basic_request['_items'])), 'red')
        return

    response = download_file(response_basic_request['_items'][basic_request_index]['id'],
                              download_path, dry_run)
    return response

def download_all(request_id, download_path=None, dry_run=False):
    """Downloads all files associated with a given request.


    :param request_id: ID of the request to query.
    :param download_path: Filename of the files(still have to come up with logical)
                  naming convention. Currently, files are downloaded with their original
                  file name in the current directory
    :param dry_run: whether to download file or not

    :return: JSON object with metadata of files downloaded on disk
    """
    url_point_request = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    # Get all point requests
    response_point_request = recastapi.get(url_point_request)

    responses = []
    for response in response_point_request['_items']:

        url_basic_request = '{}?where=point_request_id=="{}"'.format(
            recastapi.ENDPOINTS['BASIC_REQUESTS'], response['id'])
        # Get all basic requests
        response_basic_request = recastapi.get(url_basic_request)

        for response_basic in response_basic_request['_items']:

            if download_path:
                """Have to set download path, otherwise files will be overwritten """
                pass

            r = download_file(response_basic['id'], download_path=None, dry_run=dry_run)
            responses.append(r)

    return responses

def tree(request_id):
    """ Prints request tree, including the number of
        coordinates for each parameter


    :param request_id: ID of the request
    """

    print colored('Tree for REQUEST: {}'.format(request_id), 'green')

    url_point_request = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    response_point_request = recastapi.get(url_point_request)

    for i, point_response in enumerate(response_point_request['_items']):

        for j in range(1):
            print "\n"

        print colored("Parameter: {}".format(i), 'green')


        url_coordinate ='{}?where=point_request_id=="{}"'.format(
            recastapi.ENDPOINTS['PARAMETER_POINTS'], point_response['id'])
        response_coordinate = recastapi.get(url_coordinate)

        for j in range(4):
            print colored("\t\t |", 'red')

        print colored("\t\t - coordinates: {}".format(
                len(response_coordinate['_items'])),
                      'red')


        url_basic_request = '{}?where=point_request_id=="{}"'.format(
            recastapi.ENDPOINTS['BASIC_REQUESTS'], point_response['id'])
        response_basic_request = recastapi.get(url_basic_request)

        for j in range(4):
            print colored("\t\t |", 'yellow')

        print colored("\t\t - archives: {}".format(
            len(response_basic_request['_items'])),
            'yellow')
