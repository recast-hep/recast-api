import os
import requests as httprequest
import json
from werkzeug import secure_filename
from boto3.session import Session
import recastapi

def request(uuid = None, maxpage = 100000):
  single_analysis = '/{}'.format(uuid) if uuid else ''
  url = '{}{}'.format(recastapi.ENDPOINTS['REQUESTS'], single_analysis)
  r = httprequest.get(url)
  analyses = json.loads(r.content)
  return analyses

def accept(uuid, username):
  pass
  """
  r = httprequest.post('{}/requests/{}/accept.json?username={}'.format(BASEURL,uuid,username))
  if not r.ok:
    print "http request failed for payload"
    print r.reason
    print r.content
    raise RuntimeError
  return json.loads(r.content)['response-uuid']
  """

def add_parameter_point(request_id, parameter_value, filename):
  request_data = request(request_id)
  file_uuid = uuid.uuid1()
  point_request = addPointRequest(response['id'])
  basic_request = addBasicRequest(point_request['id'])
  parameter_payload = {
    'value': parameter_value,
    'point_request_id', point_request['id'],
    }
  parameter_url = '{}/'.format(recastapi.ENDPOINTS['PARAMETER_POINTS'])
  parameter_response = httprequest.post(parmater_url, data=parameter_payload,
                              auth=(recastapi.ORCID_ID, recastapi.ACCESS_TOKEN))

  uploadToAWS(filename, file_uuid)
  zenodo_file_id = uploadToZenodo(request_data['deposition_id'],
                                      file_uuid,
                                      filename)
  file_payload = {
    'file_name': file_name,
    'zenodo_file_id': zenodo_file_id,
    'original_file_name': original_file_name,
    'basic_request_id': basic_request['id']
    }
  file_url = '{}/'.format(recastapi.ENDPOINTS['FILES'])
  file_response = httprequest.post(url, data=payload, 
                                   auth=(recastapi.ORCID_ID, recastapi.ACCESS_TOKEN))
  
def create(analysis_id, description_model, reason_request,
           additional_information, file_path, parameter_value,
           status="Incomplete"):
  """
     create a request
          
  """
  request_uuid = uuid.uuid1()  
  user = userData()
  deposition_id = createZenodoDeposition(user['name'],
                                         user['orcid_id'],
                                         file_uuid,
                                         file_path)
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
  url = '{}/'.format(recastapi.ENDPOINTS['REQUESTS'])
  response = httprequest.post(url, data=payload,
                              auth=(recastapi.ORCID_ID, recastapi.ACCESS_TOKEN))
  
def addPointRequest(request_id):
  user = userData()
  payload = {
    'requester_id': user['id'],
    'scan_request_id': request_id,
    }
  url = '{}/'.format(recastapi.ENDPOINTS['POINT_REQUESTS'])
  response = httprequest.post(url, data=payload, auth=(recastapi.ORCID_ID, recastapi.ACCESS_TOKEN))

def addBasicRequest(point_request_id):
  user = userData()
  payload = {
    'requester_id': user['id'],
    'point_request_id': point_request_id,
    }
  url = '{}/'.format(recastapi.ENDPOINTS['BASIC_REQUESTS'])
  response = httprequest.post(url, data=payload, auth=(recastapi.ORCID_ID, recastapi.ACCESS_TOKEN))
          
def uploadToAWS(zip_file, file_uuid):    
  session = Session(recastapi.AWS_ACCESS_KEY_ID,
                      recastapi.AWS_SECRET_ACCESS_KEY)
  s3 = session.resource('s3')
  data = open(zip_file, 'rb')
  s3.Bucket(recastapi.AWS_S3_BUCKET_NAME).put_object(Key=str(file_uuid), Body=data)

def downloadFile(request_id, download_path=None):
  """ Downloads file from AWS
      

  """
  request_data = request(request_id)
  point_request = httprequest.get('{}/{}'.format(
      recastapi.ENDPOINTS['POINT_REQUESTS'], str(request_id)))
  basic_request = httprequest.get('{}/{}'.format(
      recastapi.ENDPOINTS['BASIC_REQUESTS'], str(point_request['id'])))
  zip_file = httprequest.get('{}/{}'.format(
      recastapi.ENDPOINTS['FILES'], str(basic_request['id'])))
      
  session = Session(recastapi.AWS_ACCESS_KEY_ID, 
                    recastapi.AWS_SECRET_ACCESS_KEY)
  s3 = session.resource('s3')
  out_file = download_path or zip_file['original_file_name']
  s3.Bucket(recastapi.AWS_S3_BUCKET_NAME).download_file(zip_file['file_name'], out_file)

def createZenodoDeposition(request_uuid, username, orcid_id, description):
  url = 'https:zenodo.org/api/deposit/depositions/?access_token={}'.format(
    recastapi.ZENODO_ACCESS_TOKEN)
  description = 'Recast_request: {} Requester: {} ORCID: {} Request_description: {}'.format(
    request_uuid, username,
    orcid_id, description)
  deposition_data = {"metadata":
                       {
      "access_right": "embargoed",
      "upload_type": "dataset",
      "creators": [{"name": "Bora, Christian"}]
      "description": description,
      "title": "Sample title"
      }
                       }
  response = httprequest.post(url, deposition_data)
  if not response.ok:
    print "http request failed for deposition data"
    print response.reason
    print response.content
    raise RuntimeError
  
  return response.json()['id']

def uploadToZenodo(ZENODO_ACCESS_TOKEN, deposition_id, file_uuid, zip_file):
  url = "https://zenodo.org/api/deposit/depositions/{}/files?access_token={}".format(
      deposition_id, ZENODO_ACCESS_TOKEN)
  json_data_file = {"filename": file_uuid}
  files = {'file': open(zip_file), 'rb'}
  response = httprequest.post(url, data=json_data_file, files=files)
  if not response.ok:
    print "http request failed for deposition files"
    print response.reason
    print response.content
    print RuntimeError
    
  return response.json()['id']
  
def publishToZenodo(ZENODO_ACCESS_TOKEN, deposition_id):
  url = "https://zenodo.org/api/deposit/depositions/{}/actions/publish?access_token={}".format(
    deposition_id, ZENODO_ACCESS_TOKEN)
  response = httprequest.post(url)

def updateStatus(request_id, status):
  pass
