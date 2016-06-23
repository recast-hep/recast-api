import recastapi
import recastapi.user.get
import uuid
from termcolor import colored

def request(analysis_id,
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
    user = recastapi.user.get.user_data()
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
        parameter_response = parameter(request_response['id'],
                                       parameter_value,
                                       parameter_title,
                                       file_path)
        request_response['parameter'] = parameter_response

    return request_response
        
def parameter(request_id,
              coordinate_value=None,
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
    if filename:
        recastapi.file_check(filename)
        
    parameter_response = point_request(request_id)    

    if coordinate_value:
        coordinate_response = coordinate(parameter_response['id'],
                                         coordinate_title,
                                         coordinate_value)
        
        
        parameter_response['coordinate'] = coordinate_response
    

    if filename:
        file_response = upload_file(parameter_response['id'], filename)
        parameter_response['file'] = file_response

    return parameter_response


def coordinate(parameter_id,
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
    recastapi.file_check(filename)
    
    basic_request_response = basic_request(parameter_id)
    basic_request_id = basic_request_response['id']
    
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
    basic_request_response['metadata'] = file_response
    return basic_request_response
  
def point_request(request_id):
    """Adds point request
    
    Args:
        request_id: ID of the request.
    
    Returns:
       JSON object
    """
    user = recastapi.user.get.user_data()
    user = user['_items'][0]
    payload = {
        "scan_request_id": request_id,
        "requester_id": user['id'],
    }
    
    print colored(payload, 'yellow')
    url = '{}'.format(recastapi.ENDPOINTS['POINT_REQUESTS'])
    return recastapi.post(url, json=payload)
    
def basic_request(point_request_id):
    """Adds basic request
    
    Args:
        point_request_id: ID of the point request
      
    Returns:
       JSON object
    """
    user = recastapi.user.get.user_data()
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


def coordinate_by_index(request_id,
                            parameter_index,
                            coordinate_name,
                            coordinate_value):
    """Adds coordinate to a give parameter 
    Args:
        request_id: request ID
        parameter_index: value of the coordinate
        coordinate_name: name of the coordinate
        coordinate_value: value
    Returns: 
        JSON
    """
               
    #get the parameter id
    parameter_url = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    parameters = recastapi.get(parameter_url)

    if parameter_index > len(parameters['_items'])-1:
        print "*"*60
        print "Parameter index out of bounds"
        print "The request has ", len(parameters['_items']), " parameters"
        raise RuntimeError

    parameter_id = parameter_index['_items'][parameter_index]['id']    

    return coordinate(parameter_id=parameter_id,
                      coordinate_name=coordinate_name,
                      coordinate_value=coordinate_value)


def upload_file_by_index(request_id, parameter_index, filename):
    """ Uploads zip file given the parameter index

    """
    recastapi.file_check(filename)

    #get parameter id
    parameter_url = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    parameters = recastapi.get(parameter_url)

    if parameter_index > len(parameters['_items'])-1:
        print "*"*60
        print "Parameter index out of bounds"
        print "The request has ", len(parameters['_items']), " parameters"
        raise RuntimeError

    parameter_id = parameter_index['_items'][parameter_index]['id']

    return upload_file(parameter_id=parameter_id,
                       filename=filename)

