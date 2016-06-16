import recastapi
from termcolor import colored
import urllib
import yaml
import uuid


def response(id = None):
    """Lists all responses.
    
    """
    single_response = '/{}'.format(id) if id else ''
    url = '{}{}'.format(recastapi.ENDPOINTS['RESPONSES'], single_response)
    return recastapi.get(url)
    
def user_response(username):
    """Lists all responses associated to a user.      
    """       
    #r = httprequest.get('{}/responses.json?pagesize=100000&username={}'.format(BASEURL,username))
    #responses = json.loads(r.content)
    #return responses
    pass

def create(request_id, model_id=None):
    """create response.
    
    """
    payload = {
        'scan_request_id': request_id,
        'model_id': model_id
    }
    
    url = '{}/'.format(recastapi.ENDPOINTS['RESPONSES'])
    return recastapi.post(url, json=payload)

	
def add_parameter_response(yaml_file, scan_response_id, point_request_id, filename):

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
	
def add_basic_response(yaml_file, point_response_id, basic_request_id, filename):

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

def download_file(basic_response_id, download_path=None, dry_run=False):
    """Downloads response file to user specified path.
    
    """
    local_path_key_name = 'local_path' #path of the downloaded file on local machine
    files_urls = '{}?where=basic_response_id=="{}"'.format(
        recastapi.ENDPOINTS['HISTOGRAMS'], basic_response_id)
    
    responses = []
    url_response = recastapi.get(files_urls)
    if len(url_response['_items']) < 2 and not len(url_response['_items']) == 0:
	url = ('{}/{}'.format(recastapi.ENDPOINTS['HISTOGRAMS'], 
			      url_response['_items'][0]['id']))
	response = recastapi.get(url)
	link = response['file_link']
	if link:
	    if not dry_run:
		zip_file = urllib.URLopener()
		zip_file.retrieve(link, download_path or response['original_file_name'])
		response['file_link'] = download_path or response['original_file_name']
		print colored('Successfully downloaded file {}'.format(
		    download_path), 'green')
	    else:
		print colored('File link: {}'.format(
		    response['file_link']), 'green')
	else:
	    response[local_path_key_name] = None
	    print colored('Faile to download file {}'.format(
		download_path or response['original_file_name']), 'red')
	    print colored('\t Please check if this request is associated with a file', 'red')
	                
	responses.append(response)
    else:
	for i, val in enumerate(url_response['_items']):
	    url = ('{}/{}'.format(recastapi.ENDPOINTS['HISTOGRAMS'],
				  url_response['_items'][i]['id']))	  
	    response = recastapi.get(url)
	    if not download_path:
		file_path= '{}_{}'.format(
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

def download(response_id, 
	     point_response_index=0,
	     basic_response_index=0, 
	     download_path=None,
	     dry_run=False):
    """Downloads file associated with a given request, indexed through point and basic responses.
    
    Args:
    response_id: ID of the response.
    point_response_index: index of the point request 0..N-1.
    basic_response_index: index of the basic request 0..M-1.
    Returns:
    JSON object with metadata of files downloaded on disk.
    """
  
    print colored('Download...', 'cyan')
    print colored('Response: {}.\n\t Point response index: {}.\n\t\t Basic response index: {}.'.format(
	response_id, point_response_index, basic_response_index), 'cyan')

    url_point_response = '{}?where=scan_response_id=="{}"'.format(
	recastapi.ENDPOINTS['POINT_RESPONSES'], response_id)
    
    response_point = recastapi.get(url_point_response)
    if len(response_point['_items']) < point_response_index:
	print colored('ERR: Point response index out range. Max index value is {}'.format(
	    len(response_point['_items'])), 'red')
	return
            
    url_basic_response = '{}?where=point_response_id=="{}"'.format(
	recastapi.ENDPOINTS['BASIC_RESPONSES'],
	response_point['_items'][point_response_index]['id'])
    
    response_basic = recastapi.get(url_basic_response)
  
    if len(response_basic['_items']) < basic_response_index:
	print colored('ERR: Basic response index out of range. Max index value is {}'.format(
	    len(response_basic['_items'])), 'red')
	return
		
    response = download_file(response_basic['_items'][basic_response_index]['id'],
							  download_path, dry_run)
    return response

def response_tree(response_id):
    """Prints response tree, nested with point and basic response.
    
    Args:
    response_id:
    """
    url_point_response = '{}?where=scan_response_id=="{}"'.format(
	recastapi.ENDPOINTS['POINT_RESPONSES'], 
	response_id
    )

    response_point = recastapi.get(url_point_response)
    
    for i, point_response in enumerate(response_point['_items']):
	print colored('Point response index: {} -- {}'.format(i, point_response), 'green')
	
	url_basic_response = '{}?where=point_response_id=="{}"'.format(
	    recastapi.ENDPOINTS['BASIC_RESPONSES'], point_response['id'])
        
	response_basic = recastapi.get(url_basic_response)
	for j, basic_response in enumerate(response_basic['_items']):
	    print colored('\t *Basic response index: {} -- {}'.format(
		j, basic_response), 'yellow')

def add_parameter_response_by_index(yaml_file, request_id, parameter_index, filename):
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
        scan_responses = create(request_id)
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

    return add_parameter_response(yaml_file,
                                  scan_response_id,
                                  point_request_id,
                                  filename)

def add_basic_response_by_index(yaml_file,
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

    return add_basic_response(yaml_file,
                              point_response_id,
                              basic_request_id,
                              filename)
    
    
