import recastapi
from termcolor import colored
import uuid
import yaml


def response(request_id, model_id=None):
    """create response.
    
    """
    payload = {
        'scan_request_id': request_id,
        'model_id': model_id
    }
    
    url = '{}/'.format(recastapi.ENDPOINTS['RESPONSES'])
    return recastapi.post(url, json=payload)
	
def parameter_response(yaml_file, scan_response_id, point_request_id, filename):

    recastapi.file_check(filename)
    
    f = open(yaml_file)
    data_map = yaml.load(f)
    f.close()
    
    try:
	payload = {
	    'lower_1sig_expected_CLs': float(data_map['lower_1sig_expected_CLs']),
	    'lower_2sig_expected_CLs': float(data_map['lower_2sig_expected_CLs']),
	    'expected_CLs': float(data_map['expected_CLs']),
	    'upper_1sig_expected_CLs': float(data_map['upper_1sig_expected_CLs']),
	    'upper_2sig_expected_CLs': float(data_map['upper_2sig_expected_CLs']),
	    'observed_CLs': float(data_map['observed_CLs']),
            'log_likelihood_at_reference': float(data_map['log_likelihood_at_reference']),
            'scan_response_id': int(scan_response_id),
            'point_request_id': int(point_request_id)
	}
    except Exception, e:
	print "*"*60
	print "YAML file not correctly formatted: ", e
	print "-"*60
	raise RuntimeError
    
    print payload
    url = '{}/'.format(recastapi.ENDPOINTS['POINT_RESPONSES'])
    response = recastapi.post(url, json=payload)
    
    if filename:
	response['metadata'] = upload_file(filename, point_response_id=response['id'])
        	
    return response
	
def basic_response(yaml_file, point_response_id, basic_request_id, filename):

    recastapi.file_check(filename)
    
    f = open(yaml_file)
    data_map = yaml.load(f)
    f.close()
    
    try:
	payload = {
	    'lower_1sig_expected_CLs': float(data_map['lower_1sig_expected_CLs']),
	    'lower_2sig_expected_CLs': float(data_map['lower_2sig_expected_CLs']),
	    'expected_CLs': float(data_map['expected_CLs']),
	    'upper_1sig_expected_CLs': float(data_map['upper_1sig_expected_CLs']),
	    'upper_2sig_expected_CLs': float(data_map['upper_2sig_expected_CLs']),
	    'observed_CLs': float(data_map['observed_CLs']),
            'log_likelihood_at_reference': float(data_map['log_likelihood_at_reference']),
	    'point_response_id': int(point_response_id),
            'basic_request_id': int(basic_request_id)
	}
    except Exception, e:
	print "*"*60
	print "YAML file not correctly formatted: ", e
	print "-"*60
	raise RuntimeError

    url = '{}/'.format(recastapi.ENDPOINTS['BASIC_RESPONSES'])
    response = recastapi.post(url, json=payload)
    
    if filename:
	response['metadata'] = upload_file(filename, basic_response_id=response['id'])
        
    return response

def upload_file(filename,
	        point_response_id=None,
		basic_response_id=None):
    """Uploads response file 
    
    Double check how the filename of response will be provided
    i.e. common name or uuid?
    """
    recastapi.file_check(filename)

    if not point_response_id and not basic_response_id:
        print "*"*60
        print "No point response ID or basic response ID given"
        raise RuntimeError

    if point_response_id and basic_response_id:
        print "*"*60
        print "Point response ID and basic response ID"
        print "Please provide either a point response ID and a basic response ID"
        raise RuntimeError
    
    file_uuid = str(uuid.uuid1()) # how will response provi
    if point_response_id:		
	payload = {
	    'file_name': file_uuid,
	    'original_file_name': filename,
	    'point_response_id': point_response_id
	}
    elif basic_response_id:
	payload = {
	    'file_name': file_uuid,
	    'original_file_name': filename,
	    'basic_response_id': basic_response_id
	}
    else:
	print "*"*60
	print "Either a point response ID or basic response ID needs to be provided"
	raise RuntimeError
	
    files = {'file': open(filename, 'rb')}
    url = '{}/'.format(recastapi.ENDPOINTS['HISTOGRAMS'])
    return recastapi.post(url, data=payload, files=files)

def parameter_response_by_index(yaml_file, request_id, parameter_index, filename):
    """Adds Point response/Parameter response given the request id and parameter index
        index with reference from 0
    Args: 
        yaml_file: file containing the data of the response
        request_id: request id
        parameter_index: index of the parameter
    """
    recastapi.file_check(filename)

    # Query scan responses check if the response has already been created
    scan_response_url = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['RESPONSES'], request_id)
    scan_responses = recastapi.get(scan_response_url)

    if len(scan_responses['_items']) == 0:
        # make new scan response if none is associated to the request
        scan_responses = response(request_id)
        #scan_response_id = scan_responses['id']
    else:
        scan_response_id = scan_responses['_items'][0]['id']

    # get the point request id
    # Query the point request for a given request_id get the index in the list
    point_request_url = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    point_requests = recastapi.get(point_request_url)    

    if parameter_index > len(point_requests['_items'])-1:
        print "*"*60
        print "Parameter index out of bounds"
        print "The request has ", len(point_requests['_items']), "elements"
        raise RuntimeError

    point_request_id = point_requests['_items'][parameter_index]['id']

    return parameter_response(yaml_file,
                              scan_response_id,
                              point_request_id,
                              filename)

def basic_response_by_index(yaml_file,
                            request_id,
                            parameter_index,
                            basic_index,
                            filename):
    """ Add basic response given the request id, parameter index, and basic index
    Args:
        yaml_file: file containing basic response data
        request_id: associate request id
        parameter_index: index of the parameter
        basic_index: index of the basic response
    Returns:
        JSON object
    """
    recastapi.file_check(filename)
    
    # Find the point_response_id
    point_request_url = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    point_requests = recastapi.get(point_request_url)

    if parameter_index > len(point_requests['_items'])-1:
        print "*"*60
        print "Parameter index out of bounds"
        print "The request has ", len(point_requests['_items']), " elements"
        raise RuntimeError

    point_request_id = point_requests['_items'][parameter_index]['id']

    # Find the point response
    point_response_url = '{}?where=point_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_RESPONSES'], point_request_id)
    point_responses = recastapi.get(point_response_url)

    if len(point_responses['_items']) < 1:
        print "*"*60
        print "No Parameter response found!"
        print "Please add a Parameter response before a Basic response"
        raise RuntimeError

    point_response_id = point_responses['_items'][0]['id']

    #Find the basic request
    basic_request_url = '{}?where=point_request_id=="{}"'.format(
        recastapi.ENDPOINTS['BASIC_REQUESTS'], point_request_id)
    basic_requests = recastapi.get(basic_request_url)

    if basic_index > len(basic_requests['_items'])-1:
        print "*"*60
        print "Basic index out of bounds"
        print "The parameter has ", len(basic_requests['_items']), " basic elements"
        raise RuntimeError

    basic_request_id = basic_requests['_items'][basic_index]['id']

    return basic_response(yaml_file,
                          point_response_id,
                          basic_request_id,
                          filename)
