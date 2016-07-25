import recastapi
from termcolor import colored
import urllib

def response(uuid=None,
             request_id=None,
             query='?max_results=1000&page=1'):
    """ List response depending on criteria.
        If all args are None alll responses returned.

    :param uuid: Response ID to query(optional). Returns a single request with the ID
    :param request_id: Request ID of request to query(optional). Returns request
                     associated to response
    :param query: additional query 

    :return: JSON object       
    """
    
    if uuid and request_id:
        print "*"*60
        print "Cannot fetch request and uuid simultaneously"
        print "Please provide either a request ID or uuid"
        raise RuntimeError

    elif uuid:
         single_response = '/{}'.format(uuid)
         url = '{}{}'.format(recastapi.ENDPOINTS['RESPONSES'], single_response)
         response = recastapi.get(url)
         return response

    elif request_id:
        request_str = '?where=scan_request_id=="{}"'.format(request_id)
        url = '{}{}'.format(recastapi.ENDPOINTS['RESPONSES'], request_str)
        print url
        response = recastapi.get(url)
        if len(response) == 0:
            return None
        else:
            return response['_items'][0]

    else:
        url = '{}{}'.format(recastapi.ENDPOINTS['RESPONSES'], query)
        response = recastapi.get(url)
        return response
         
def parameter(request_id, parameter_index):
    """ Gets the parameter response given an index
    
    :param request_id: ID of request
    :param parameter_index: index of the parameter
    
    :return: JSON object
    """

    # get parameter ID
    parameter_url = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    parameter_response = recastapi.get(parameter_url)

    if parameter_index > len(parameter_response['_items'])-1:
        # index does not exist
        print '-'*60
        print "Exception in user code:"
        print "\t ******* parameter index out of bounds"
        print "\n"
        raise RuntimeError

    parameter_id = parameter_response['_items'][parameter_index]['id']

    # check for parameter response

    response_url = '{}?where=point_request_id="{}"'.format(
        recastapi.ENDPOINTS['POINT_RESPONSES'], parameter_id)
    response = recastapi.get(response_url)

    if len(response['_items']) == 0:
        # No parameter response found
        print '-'*60
        print "Exception in user code:"
        print "\t ****** No parameter response found"
        print '\n'
        raise RuntimeError
    
    return response['_items'][0]
        
def point_response_by_id(point_request_id):
    """ returns point response JSON given point request id. """
    
    url = '{}?where=point_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINTS_RESPONSES'], point_request_id)
    response = recastapi.get(url)
    if len(response['_items']) > 1:
        raise Exception('Duplicated data! Internal Server error')
    if not response['_items']:
        raise Exception('No record found!')
    return response['_items'][0]
    
def basic(request_id, parameter_index, basic_index):
    """ Gets the basic response

    :param request_id: ID of the request
    :param parameter_index: ID of the parameter
    :param basic_index: ID of the basic response
    
    :return: JSON object
    """

    # get parameter ID
    parameter_url = '{}?where=scan_request_id=="{}"'.format(
        recastapi.ENDPOINTS['POINT_REQUESTS'], request_id)
    parameter_response = recastapi.get(parameter_url)

    if parameter_index > len(parameter_response['_items'])-1:
        # index out of bounds
        print '-'*60
        print "Exception in user code:"
        print "\t ******** parameter index out of bounds"
        print '\n'
        raise RuntimeError

    parameter_id = parameter_response['_items'][parameter_index]['id']

    # get basic request
    basic_url = '{}?where=point_request_id=="{}"'.format(
        recastapi.ENDPOINTS['BASIC_REQUESTS'], parameter_id)
    basic_response = recastapi.get(basic_url)

    if basic_index > len(basic_response['_items'])-1:
        # basic index out of bounds
        print '-'*60
        print "Exception in user code:"
        print "\t ******* basic index out of bounds"
        print '\n'
        raise RuntimeError

    basic_id = basic_response['_items'][basic_index]['id']

    # finally fetch the basic response
    response_url = '{}?where=basic_request_id=="{}"'.format(
        recastapi.ENDPOINTS['BASIC_RESPONSES'], basic_id)
    response = recastapi.get(response_url)

    if len(response['_items']) == 0:
        # No basic response found
        print '-'*60
        print "Exception in user code:"
        print "\t ******** No basic response found for the indices"
        print '\n'
        raise RuntimeError

    return response['_items'][0]
    
def user_response(username):
    """Lists all responses associated to a user.      
    """       
    #r = httprequest.get('{}/responses.json?pagesize=100000&username={}'.format(BASEURL,username))
    #responses = json.loads(r.content)
    #return responses
    pass


def download_file(basic_response_id, download_path=None, dry_run=False):
    """Downloads response file to user specified path.
    
    :param basic_response_id: ID of the basic response
    :param download_path: Used specified filename
    :param dry_run: whether to download file or not

    :return: JSON object
    
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
    

    :param response_id: ID of the response.
    :param point_response_index: index of the point request 0..N-1.
    :param basic_response_index: index of the basic request 0..M-1.
    :param download_path: User specified download filename `if` none keeps original name
    :param dry_run: whether to download file or not
    
    :return: JSON object with metadata of files downloaded on disk.
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

def tree(response_id):
    """Prints response tree, nested with point and basic response.
    
    :param response_id: ID of the response
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

