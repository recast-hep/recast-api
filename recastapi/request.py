import recastapi
import recastapi.user
import uuid
from termcolor import colored
import urllib
import yaml
import json
import os

def request(uuid = None, maxpage = 100000):
    """Lists all requests.
    Args:
        uuid: ID of the request(optional)
    Returns:
       JSON object
    """
    single_analysis = '/{}'.format(uuid) if uuid else ''
    url = '{}{}'.format(recastapi.ENDPOINTS['REQUESTS'], single_analysis)
    return recastapi.get(url)

def parameter(request_id,
              parameter_index=None):
    '''Returns list of parameters or single parameter
    Args:
        request_id: the request ID to query
        parameter_index: starting from 0
    '''
    
    parameters_url = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'],
        request_id
    )
    parameter_responses = recastapi.get(parameters_url)

    if not parameter_index and not parameter_index == 0:
        for i, parameter in enumerate(parameter_responses['_items']):
            parameter['coordinates'] = get_coordinate(parameter['id'])
            parameter['file'] = download(request_id=request_id,
                                         point_request_index=i,
                                         basic_request_index=0,
                                         download_path=None,
                                         dry_run=True
                                     )                               
        return parameter_responses['_items']
    
    if parameter_index >= 0 and parameter_index < len(parameter_responses['_items']):
        # if the parameter index is defined
        parameter_responses['_items'][parameter_index]\
            ['coordinates'] = get_coordinate(
                parameter_responses['_items'][parameter_index]['id'])

        parameter_responses['_items'][parameter_index]\
            ['file'] = download(
                request_id = request_id,
                point_request_index = parameter_index,
                basic_request_index = 0,
                dry_run=True
            )
        
        return parameter_responses['_items'][parameter_index]
    else:
        #parameter index not found
        print '-'*60
        print "Exception in user code:"
        print "\t ****** Pameter index not found"
        print '\n'
        raise RuntimeError
        

def coordinate(request_id, parameter_index=0, coordinate_index=None):
    '''Returns list of coordinates given a parameter index and request_id \
              or single coordinate
    if
    '''
    if not parameter_index and not parameter_index ==0:
        print '-'*60
        print "Exception in user code:"
        print "\t ****** Parameter index not valid"
        print '\n'
        raise RuntimeError

    response = parameter(request_id = request_id,
                         parameter_index = parameter_index,
                     )    

    if not coordinate_index and not coordinate_index == 0:
        return response['coordinates']
        
    if coordinate_index < len(response['coordinates'])  and coordinate_index >= 0:
        return response['coordinates'][coordinate_index]
    else:
        print '-'*60
        print "Exception in user code:"
        print "\t ******* Coordinate index not found"
        print '\n'
        raise RuntimeError

def get_coordinate(point_request_id):
    coordinate_url = '{}?where=point_request_id=="{}"'.format(
        recastapi.ENDPOINTS['PARAMETER_POINTS'],
        point_request_id
    )
    
    coordinate_responses = recastapi.get(coordinate_url)
    return coordinate_responses['_items']
    
              
def user_request(username):
    pass

def download_file(basic_request_id, download_path=None, dry_run=False):  
    """Downloads the zip file associated with a basic request.
    
    Args: 
      basic_request_id: ID of the basic request associated with a file.
      donwload_path: User specified download path(optional), if not
                   provided, file takes original file_name.
    Returns:
      JSON object containing the metadata of the file, and file downloaded saved on disk.
    """
	local_path_key_name = 'local_path' #path of the downloaded file on local machine
    files_urls = '{}?where=basic_request_id=="{}"'.format(
        recastapi.ENDPOINTS['FILES'], basic_request_id)
  
    responses = []
    url_response = recastapi.get(files_urls)
    if len(url_response['_items']) < 2 and not len(url_response['_items']) == 0:
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
            print colored('\t Please check if this request is associted with a file', 'red')
        responses.append(response)
    else:
        for i, val in enumerate(url_response['_items']):
            url = ('{}/{}'.format(recastapi.ENDPOINTS['FILES'],
                                  url_response['_items'][i]['id']))
            response = recastapi.get(url)
            if not download_path:
                file_path = '{}_{}'.format(
                    response['_items'][i]['original_file_name'], str(i))
            else:
                file_path = '{}_{}'.format(download_path, str(i))
        
            link = response['file_link']
            if link:
                if not dry_run:
                    zip_file = urllib.URLopener()
                    zip_file.retrieve(link, file_path)
                    response[local_path_key_name] = file_path
                    print colored('Successfully downloaded file {}'.format(
                        file_path), 'green')
            else:
                response[local_path_key_name] = None
                print colored('Failed to download file {}'.format(file_path), 'red')
                print colored('\t Please check if this request is associated with a file', 'red')
                
                
            responses.append(response)
    return responses

def download(request_id,
             point_request_index=0,
             basic_request_index=0, 
             download_path=None, 
             dry_run=False):
    """Downloads file associated with a given request, index through point and basic requests.
    
    Args:
        request_id: ID of the request.
        point_request_index: index of the point request 0..N-1.
        basic_request_index: index of basic request 0..M-1.
        dry_run: True - let's you get the file link in the json and does not download file
    Returns:
       JSON object with metadata of files downloaded on disk.
    """
    print colored('Downloading....', 'cyan')
    print colored('Request: {}.\n\t Point request index: {}. \n\t\t Basic request index: {}.'.format(
        request_id, point_request_index, basic_request_index), 'cyan')
    url_point_request = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    
    response_point_request = recastapi.get(url_point_request)
    if len(response_point_request['_items']) < point_request_index:
        print colored('ERR: Point request index out of range. Max range is {}'.format(
            len(response_point_request['_items'])), 'red')
        return
        
    url_basic_request = '{}?where=point_request_id=="{}"'.format(
        recastapi.ENDPOINTS['BASIC_REQUESTS'],
        response_point_request['_items'][point_request_index]['id'])
    
    response_basic_request = recastapi.get(url_basic_request)
    
    if len(response_basic_request['_items']) < basic_request_index:
        print colored('ERR: Basix request index out of range. Max range is {}'.format(
            len(response_basic_request['_items'])), 'red')
        return
        
    response = download_file(response_basic_request['_items'][basic_request_index]['id'],
                              download_path, dry_run)
    return response

def download_all(request_id, download_path=None, dry_run=False):
    """Downloads all files associated with a given request.
    
    Args:
        request_id: ID of the request to query.
        download_path: Filename of the files(still have to come up with logical)
                  naming convention. Currently, files are downloaded with their original
                  file name in the current directory
    Returns:
        JSON object with metadata of files downloaded on disk
    """
    url_point_request = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    
    response_point_request = recastapi.get(url_point_request)
    
    responses = []
    for response in response_point_request['_items']:
    
        url_basic_request = '{}?where=point_request_id=="{}"'.format(
            recastapi.ENDPOINTS['BASIC_REQUESTS'], response['id'])
        
        response_basic_request = recastapi.get(url_basic_request)
    
        for response_basic in response_basic_request['_items']:
      
            if download_path:
                """Have to set download path, otherwise files will be overwritten """
                pass
        
            r = download_file(response_basic['id'], download_path=None, dry_run=dry_run)
            responses.append(r)
      
    return responses

def request_tree(request_id):
    """ Prints request tree, including point request, basic_request
    
    Args:
        request_id
    
    """
    print "Request ID: ", request_id
    url_point_request = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    response_point_request = recastapi.get(url_point_request)
    
    for i, point_response in enumerate(response_point_request['_items']):
        print colored('Point request index: {} -- {}'
                      .format(i, yaml.safe_dump(point_response,
                                            default_flow_style=False)),
                      'green')
    
        url_basic_request = '{}?where=point_request_id=="{}"'.format(
            recastapi.ENDPOINTS['BASIC_REQUESTS'], point_response['id'])
        
        response_basic_request = recastapi.get(url_basic_request)
    
        for j, basic_response in enumerate(response_basic_request['_items']):
            print colored('>>>>>> (*) Basic request index: {} -- {}'
                          .format(j, yaml.safe_dump(basic_response, 
                                                    default_flow_style=False)),
                          'yellow')
      

def create(analysis_id,
           title,
           description_model,
           reason_for_request,
           additional_information,
           status="Incomplete",
           file_path=None,
           parameter_value=None,
           parameter_title=None):
    """Creates a request.
    
    Args:
        analysis_id: ID of the analysis.
        description_model: Detailed description of the model to use.
        reason_for_request: Reason for submitting this request.
        additional_information: Any other additional information associated to this request.
        status: Defaults to Incomplete.
        file_path: File to be associated with this request, optional variable.
        parameter_value: Value of the scan parameter, optional.
        parameter_title: Optional title of the parameter title.
      
    Returns:
       JSON object with data added
    """
    request_uuid = str(uuid.uuid1())
    user = recastapi.user.userData()
    user = user['_items'][0]
    
    payload = {
        'requester_id': user['id'],
        'title': title,
        'reason_for_request': reason_for_request,
        'additional_information': additional_information,
        'analysis_id': analysis_id,
        'zenodo_deposition_id': None,
        'uuid': request_uuid,
        'description_of_model': description_model,
        'status': status,
    }
    print colored(payload, 'green')
    url = '{}/'.format(recastapi.ENDPOINTS['REQUESTS'])
    request_response = recastapi.post(url, data=payload)
    
    if file_path and parameter_value:
        parameter_response = add_parameter(request_response['id'],
                                                 parameter_value,
                                                 parameter_title,
                                                 file_path)
        request_response['parameter'] = parameter_response

    return request_response
        
def add_parameter(request_id,
                  coordinate_value,
                  coordinate_title=None,
                  filename=None):
    """Add a parameter point to a request.

    Usually called automatically after create analysis
    Args:
        request_id: ID of the request to be associated to this parameter point.
        coordinate_value: Value of the scan coordinate.
        parameter_title: Optional title of the scan title.
        filename: Optional file path to file to associate to this parameter point.
      
    Returns:
       JSON object with data added
    
    """
    parameter_response = add_point_request(request_id)

    
    coordinate_response = add_coordinate(parameter_response['id'],
                                         coordinate_title,
                                         coordinate_value)

                                         
    parameter_response['coordinate'] = coordinate_response
    

    if filename:
        file_response = upload_file(parameter_response['id'], filename)
        parameter_response['file'] = file_response

    return parameter_response

def add_coordinate(parameter_id,
                   coordinate_name,
                   coordinate_value):
    '''Adds coordinate given parameter id.
        
    Args: 
        parameter_id: analogous to point_request_id.
        coordinate_value: value of the coordinate.
        coordinate_name: name of the coordinate.
    Returns:
        JSON object with added data
    '''
    coordinate_payload = {
        'point_request_id': parameter_id,
        'title': coordinate_name,
        'value': float(coordinate_value)        
    }
    
    coordinate_url = '{}/'.format(recastapi.ENDPOINTS['PARAMETER_POINTS'])
    coordinate_response = recastapi.post(coordinate_url,
                                         json=coordinate_payload)
    return coordinate_response


def upload_file(parameter_id, filename):
    """Uploads zip file and associates it with a request and basic request.
  
    Args:
        request_id: ID of the request to be associated to this file.
        basic_request_id: ID of the basic request to be asso
        filename: Path to file to be uploaded.
      
    Returns:
        JSON object
    
    """
	if not os.path.isfile(filename):
		raise IOException('File does not exist: {}'.format(filename))

    basic_request = add_basic_request(parameter_id)
    basic_request_id = basic_request['id']
    
    file_uuid = str(uuid.uuid1())

    #get request ID, so deposition can be retrieved
    point_request_url = '{}/{}'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'],
        parameter_id)
    point_response = recastapi.get(point_request_url)

    request_id = point_response['scan_request_id']
    
    request_url = '{}/{}'.format(
        recastapi.ENDPOINTS['REQUESTS'],
        request_id
    )
    request_response = recastapi.get(request_url)
    deposition_id = request_response['zenodo_deposition_id']

    payload = {
        'file_name': file_uuid,
        'zenodo_file_id': None,
        'original_file_name': filename,
        'basic_request_id': basic_request_id,
    }
  
    files = {'file': open(filename, 'rb')}
    url = '{}/'.format(recastapi.ENDPOINTS['FILES'])
    file_response = recastapi.post(
        url, 
        data=payload, 
        files=files,
        params = {'deposition_id': deposition_id}
    )
    basic_request['metadata'] = file_response
    return basic_request
  
def add_point_request(request_id):
    """Adds point request
    
    Args:
        request_id: ID of the request.
    
    Returns:
       JSON object
    """
    user = recastapi.user.userData()
    user = user['_items'][0]
    paxyload = {
        "scan_request_id": request_id,
        "requester_id": user['id'],
    }
    
    print colored(payload, 'yellow')
    url = '{}'.format(recastapi.ENDPOINTS['POINT_REQUESTS'])
    return recastapi.post(url, json=payload)
    
def add_basic_request(point_request_id):
    """Adds basic request
    
    Args:
        point_request_id: ID of the point request
      
    Returns:
       JSON object
    """
    user = recastapi.user.userData()
    user = user['_items'][0]
    payload = {
        'requester_id': user['id'],
        'point_request_id': point_request_id,
    }
    url = '{}/'.format(recastapi.ENDPOINTS['BASIC_REQUESTS'])
    return recastapi.post(url, data=payload)
    
def update_status(request_id, status):
    """Updates status of the request.

    Args: 
        request_id: ID of the request to be updated
    Returns:
       JSON object
    """
    pass
