import os
import requests as httprequest
import json
from werkzeug import secure_filename
from boto3.session import Session
import recastapi
import uuid
from termcolor import colored
import urllib
"""Request functionalities.

"""

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

def user_request(username):
  pass

def download_file(basic_request_id, download_path=None):
  """Downloads the zip file associated with a basic request.
  
  Args: 
      basic_request_id: ID of the basic request associated with a file.
      donwload_path: User specified download path(optional), if not
                   provided, file takes original file_name.
  Returns:
      JSON object containing the metadata of the file, and file downloaded saved on disk.
  """
  files_urls = '{}?where=basic_request_id=="{}"'.format(
    recastapi.ENDPOINTS['FILES'], basic_request_id)
  
  file_ids = []
  responses = []
  url_response = recastapi.get(files_urls)
  if len(url_response['_items']) < 2 and not len(url_response['_items']) == 0:
    url = ('{}/{}'.format(recastapi.ENDPOINTS['FILES'],
                          url_response['_items'][0]['id']))
    response = recastapi.get(url)
    link = response['file_link']
    if link:
      zip_file = urllib.URLopener()
      zip_file.retrieve(link, download_path or response['original_file_name'])
      response['file_path'] = download_path or response['original_file_name']
      print colored('Successfully downloaded file {}'.format(
          download_path), 'green')
    else:
      response['file_path'] = ''
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
        zip_file = urllib.URLopener()
        zip_file.retrieve(link, file_path)
        response['file_path'] = file_path
        print colored('Successfully downloaded file {}'.format(
            file_path), 'green')
      else:
        response['file_path'] = ''
        print colored('Failed to download file {}'.format(file_path), 'red')
        print colored('\t Please check if this request is associated with a file', 'red')


      responses.append(response)
  return responses

def download(request_id, point_request_index=0, basic_request_index=0, download_path=None):
  """Downloads file associated with a given request, index through point and basic requests.

  Args:
      request_id: ID of the request.
      point_request_index: index of the point request 0..N-1.
      basic_request_index: index of basic request 0..M-1.
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
                              download_path)
  return response

def download_all(request_id, download_path=None):
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
        
      r = download_file(response_basic['id'], download_path=None)
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
    print colored('Point request index: {} -- {}'.format(i, point_response), 'green')
    
    url_basic_request = '{}?where=point_request_id=="{}"'.format(
      recastapi.ENDPOINTS['BASIC_REQUESTS'], point_response['id'])

    response_basic_request = recastapi.get(url_basic_request)
    
    for j, basic_response in enumerate(response_basic_request['_items']):
      print colored('\t *Basic request index: {} -- {}'.format(j, basic_response), 'yellow')
      

def create(analysis_id, description_model, reason_for_request,
           additional_information, status="Incomplete",
           file_path=None, parameter_value=None, parameter_title=None):
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
    parameter_point_response = add_parameter_point(request_response['id'],
                                                  parameter_value,
                                                  parameter_title,
                                                  file_path)
    request_response['parameter_point'] = parameter_point_response

  return request_response

def add_parameter_point(request_id, parameter_value, parameter_title=None, filename=None):
  """Add a parameter point to a request.

  Usually called automatically after create analysis
  Args:
      request_id: ID of the request to be associated to this parameter point.
      parameter_value: Value of the scan parameter.
      parameter_title: Optional title of the scan parameter.
      filename: Optional file path to file to associate to this parameter point.
      
  Returns:
      JSON object with data added

  """
  request_data = request(request_id)
  point_request = add_point_request(request_id)
  basic_request = add_basic_request(point_request['id'])
  parameter_value = (parameter_value)

  parameter_payload = {
    'point_request_id': point_request['id'],
    'value': float(parameter_value),
    'title': parameter_title
    }

  parameter_url = '{}/'.format(recastapi.ENDPOINTS['PARAMETER_POINTS'])
  parameter_response = recastapi.post(parameter_url, json=parameter_payload)
  parameter_response['basic_request'] = basic_request
  parameter_response['point_request'] = point_request

  if filename:
    print colored(basic_request, 'red')
    file_response = upload_file(request_id, basic_request['id'], filename)
    parameter_response['file'] = file_response

  return parameter_response

def upload_file(request_id, basic_request_id, filename):
  """Uploads zip file and associates it with a request and basic request.
  
  Args:
      request_id: ID of the request to be associated to this file.
      basic_request_id: ID of the basic request to be associated.
      filename: Path to file to be uploaded.
      
  Returns:
      JSON object

  """
  file_uuid = str(uuid.uuid1())
  request_data = request(request_id)
  payload = {
    'file_name': file_uuid,
    'zenodo_file_id': None,
    'original_file_name': filename,
    'basic_request_id': basic_request_id,
    }
  
  files = {'file': open(filename, 'rb')}
  url = '{}/'.format(recastapi.ENDPOINTS['FILES'])
  file_response = recastapi.post(url, data=payload, files=files,
                                 params = {'deposition_id': request_data['zenodo_deposition_id']})
  return file_response
  
def add_point_request(request_id):
  """Adds point request
  
  Args:
      request_id: ID of the request.
      
  Returns:
      JSON object
  """
  user = recastapi.user.userData()
  user = user['_items'][0]
  payload = {
    'requester_id': user['id'],
    }
  print colored(payload, 'yellow')
  url = '{}/'.format(recastapi.ENDPOINTS['POINT_REQUESTS'])
  return recastapi.post(url, data=payload)
  
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
