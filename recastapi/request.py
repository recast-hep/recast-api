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

def accept(uuid, username):
  pass
  """
  r = httprequest.post('{}/requests/{}/accept.json?username={}'.format(BASEURL,uuid,username))
  return json.loads(r.content)['response-uuid']
  """
  
def create(analysis_id, description_model, reason_request,
           additional_information, file_path, parameter_value,
           status="Incomplete"):
  """
     create a request
          
  """
  request_uuid = uuid.uuid1()  
  user = recastapi.user.userData()
  user = user['_items'][0]
  deposition_id = createZenodoDeposition(user['name'],
                                         user['orcid_id'],
                                         request_uuid,
                                         reason_request)
  payload = {
    'requester_id': user['id'],
    'reason_for_request': reason_request,
    'additional_information': additional_information,
    'analysis_id': analysis_id,
    'zenodo_deposition_id': deposition_id,
    'uuid': request_uuid,
    'description_of_model': description_model,
    'status': status,
    }
  print colored(payload, 'green')
  url = '{}/'.format(recastapi.ENDPOINTS['REQUESTS'])
  request_response = recastapi.post(url, data=payload)
  #  add_parameter_point(request_response['id'], parameter_value, file_path)
  return request_response

def downloadFile(request_id, download_path=None):
  """ Downloads file from AWS
      
  """
  request_data = request(request_id)

  point_request_url = '{}?where=scan_request_id=="{}"'.format(
    recastapi.ENDPOINTS['POINT_REQUESTS'], str(request_id))
  point_request = recastapi.get(point_request_url)

  basic_request_url = '{}?where=point_request_id=="{}"'.format(
    recastapi.ENDPOINTS['BASIC_REQUESTS'], str(point_request['_items'][0]['id']))
  basic_request = recastapi.get(basic_request_url)

  zip_file_url = '{}?where=basic_request_id=="{}"'.format(
    recastapi.ENDPOINTS['FILES'], str(basic_request['_items'][0]['id']))  
  zip_file = recastapi.get(zip_file_url)
  zip_file = zip_file['_items'][0]
      
  session = Session(recastapi.AWS_ACCESS_KEY_ID, 
                    recastapi.AWS_SECRET_ACCESS_KEY)
  s3 = session.resource('s3')
  out_file = download_path or zip_file['original_file_name']
  s3.Bucket(recastapi.AWS_S3_BUCKET_NAME).download_file(zip_file['file_name'], out_file)
  print colored('Successfully downloaded file {}'.format(out_file), 'green')
  return zip_file

def add_parameter_point(request_id, parameter_value, filename):
  """Add a parameter point to a request
      usually called automatically after create analysis

  """
  
  request_data = request(request_id)
  file_uuid = uuid.uuid1()
  point_request = addPointRequest(request_id)
  basic_request = addBasicRequest(point_request['id'])
  parameter_value = float(parameter_value)*1.0
  parameter_payload = {
    "value": parameter_value,
    'point_request_id': point_request['id'],
    }
  parameter_url = '{}/'.format(recastapi.ENDPOINTS['PARAMETER_POINTS'])
  parameter_response = recastapi.post(parameter_url, data=parameter_payload)

  uploadToAWS(filename, file_uuid)
  zenodo_file_id = uploadToZenodo(request_data['deposition_id'],
                                      file_uuid,
                                      filename)
  file_payload = {
    'file_name': file_name,
    'zenodo_file_id': zenodo_file_id,
    'original_file_name': original_file_name,
    'basic_request_id': basic_request['id'],
    }
  file_url = '{}/'.format(recastapi.ENDPOINTS['FILES'])
  file_response = recastapi.post(url, data=payload)
  
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
          
def uploadToAWS(zip_file, file_uuid):    
  session = Session(recastapi.AWS_ACCESS_KEY_ID,
                      recastapi.AWS_SECRET_ACCESS_KEY)
  s3 = session.resource('s3')
  data = open(zip_file, 'rb')
  s3.Bucket(recastapi.AWS_S3_BUCKET_NAME).put_object(Key=str(file_uuid), Body=data)
  print colored('Successfully uploaded file {} to server'.format(out_file), 'green')

def createZenodoDeposition(username, orcid_id, request_uuid, description):
  url = 'https://zenodo.org/api/deposit/depositions/?access_token={}'.format(
    recastapi.ZENODO_ACCESS_TOKEN)
  description = 'Recast_request: {} Requester: {} ORCID: {} Request_description: {}'.format(
    request_uuid, username,
    orcid_id, description)
  headers = {"Content-Type": "application/json"}
  deposition_data = {"metadata":
                       {
      "access_right": "embargoed",
      "upload_type": "dataset",
      "creators": [{"name": "Bora, Christian"}],
      "description": description,
      "title": "Sample title"
      }
                       }
  #return recastapi.post(url, deposition_data)['id']
  response = httprequest.post(url, data=json.dumps(deposition_data), headers=headers)
  print ":"*100
  print response
  return response.json()['id']

def uploadToZenodo(ZENODO_ACCESS_TOKEN, deposition_id, file_uuid, zip_file):
  url = "https://zenodo.org/api/deposit/depositions/{}/files?access_token={}".format(
      deposition_id, ZENODO_ACCESS_TOKEN)
  json_data_file = {"filename": file_uuid}
  files = {'file': open(zip_file, 'rb')}
  response = httprequest.post(url, data=json_data_file, files=files)
  return response.json()['id']
    
  
def publishToZenodo(ZENODO_ACCESS_TOKEN, deposition_id):
  url = "https://zenodo.org/api/deposit/depositions/{}/actions/publish?access_token={}".format(
    deposition_id, ZENODO_ACCESS_TOKEN)
  response = httprequest.post(url)
  return response

def updateStatus(request_id, status):
  pass
