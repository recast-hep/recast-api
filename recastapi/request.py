import os
import requests as httprequest
import json
from werkzeug import secure_filename
from boto3.session import Session
import recastapi
import uuid
from termcolor import colored
import urllib

def request(uuid = None, maxpage = 100000):
  single_analysis = '/{}'.format(uuid) if uuid else ''
  url = '{}{}'.format(recastapi.ENDPOINTS['REQUESTS'], single_analysis)
  return recastapi.get(url)

def user_request(username):
  pass

def download_file(basic_request_id, download_path=None):
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
  
def create(analysis_id, description_model, reason_for_request,
           additional_information, status="Incomplete",
           file_path=None, parameter_value=None, parameter_title=None):
  """
     create a request
          
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
  """Add a parameter point to a request
      usually called automatically after create analysis

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
  user = recastapi.user.userData()
  user = user['_items'][0]
  payload = {
    'requester_id': user['id'],
    }
  print colored(payload, 'yellow')
  url = '{}/'.format(recastapi.ENDPOINTS['POINT_REQUESTS'])
  return recastapi.post(url, data=payload)
  
def add_basic_request(point_request_id):
  user = recastapi.user.userData()
  user = user['_items'][0]
  payload = {
    'requester_id': user['id'],
    'point_request_id': point_request_id,
    }
  url = '{}/'.format(recastapi.ENDPOINTS['BASIC_REQUESTS'])
  return recastapi.post(url, data=payload)

def update_status(request_id, status):
  pass
