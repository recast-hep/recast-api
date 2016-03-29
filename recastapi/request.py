import os
import requests as httprequest
import json
from werkzeug import secure_filename
from boto3.session import Session
import recastapi
import uuid
from termcolor import colored

def request(uuid = None, maxpage = 100000):
  single_analysis = '/{}'.format(uuid) if uuid else ''
  url = '{}{}'.format(recastapi.ENDPOINTS['REQUESTS'], single_analysis)
  return recastapi.get(url)

def download_archive(basic_request_id, download_path=None):
  files_urls = '{}?where=basic_request_id=="{}"'.format(
    recastapi.ENDPOINTS['FILES'], basic_request_id)
  
  file_ids = []
  if len(files_urls['_items']) < 2 and not len(files_urls['_items'] == 0):
    url = ('{}/{}{}'.format(recastapi.ENDPOINTS['FILES'], files_urls['_items'][0]['id']))
    response = recastapi.get(url, params={'download': 1, 'path': download_path})
    print colored('Successfully downloaded file {}'.format(out_file), 'green')
    return response
  else:
    for i, val in enumerate(files_url['_items']):
      url = ('{}/{}{}'.format(recastapi.ENDPOINTS['FILES'], files_urls['_items'][i]['id']))
      if not download_path:
        download_path = '{}_{}'.format(
          files_urls['_items'][i]['original_file_name'], str(i))
      else:
        download_path = '{}_{}'.format(download_path, str(i))
    reponse = recastapi.get(url, params={'download': 1, 'path': download_path})
      print colored('Successfully downloaded file {}'.format(download_path), 'green')
  
def create(analysis_id, description_model, reason_request,
           additional_information, file_path, parameter_value,
           status="Incomplete"):
  """
     create a request
          
  """
  request_uuid = str(uuid.uuid1())
  user = recastapi.user.userData()
  user = user['_items'][0]

  payload = {
    'requester_id': user['id'],
    'reason_for_request': reason_request,
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
  #  add_parameter_point(request_response['id'], parameter_value, file_path)
  return request_response

def add_parameter_point(request_id, parameter_value, filename):
  """Add a parameter point to a request
      usually called automatically after create analysis

  """
  
  request_data = request(request_id)
  file_uuid = str(uuid.uuid1())
  point_request = addPointRequest(request_id)
  basic_request = addBasicRequest(point_request['id'])
  parameter_value = float(parameter_value)*1.0
  parameter_payload = {
    "value": parameter_value,
    'point_request_id': point_request['id'],
    }
  parameter_url = '{}/'.format(recastapi.ENDPOINTS['PARAMETER_POINTS'])
  parameter_response = recastapi.post(parameter_url, data=parameter_payload)

  file_payload = {
    'file_name': file_uuid,
    'zenodo_file_id': None,
    'original_file_name': original_file_name,
    'basic_request_id': basic_request['id'],
    }
  files = {'recast_file': open(filename, 'rb')}
  file_url = '{}/'.format(recastapi.ENDPOINTS['FILES'])
  file_response = recastapi.post(url, data=payload, files=files,
                                 params = {'deposition_id': request_data['zenodo_deposition_id']})
  
def addPointRequest(request_id):
  user = recastapi.user.userData()
  user = user['_items'][0]
  payload = {
    'requester_id': user['id'],
    }
  print colored(payload, 'yellow')
  url = '{}/'.format(recastapi.ENDPOINTS['POINT_REQUESTS'])
  return recastapi.post(url, data=payload)
  
def addBasicRequest(point_request_id):
  user = recastapi.user.userData()
  user = user['_items'][0]
  payload = {
    'requester_id': user['id'],
    'point_request_id': point_request_id,
    }
  url = '{}/'.format(recastapi.ENDPOINTS['BASIC_REQUESTS'])
  return httprequest.post(url, data=payload)

def updateStatus(request_id, status):
  pass
