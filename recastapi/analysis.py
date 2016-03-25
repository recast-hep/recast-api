import os
import requests as httprequest
import json
import recastapi

def analysis(uuid = None):
  """List analysis given uuid or all analyses
  Usage::
       >>> analysis()
       
       >>> returns json object
  """
  single_analysis = '/{}'.format(uuid) if uuid else ''
  url = '{}{}'.format(recastapi.ENDPOINTS['ANALYSIS'], single_analysis)
  return recastapi.get(url)
  
def create(title, collaboration,
           e_print, journal, doi, inspire_url, 
           description, run_condition_name, run_condition_description):
  """Create a new analysis and Run Condition
      collaboration: ALICE, ATLAS,CMS...
      .
      .
      .
  """
  r_condition_payload = {
    'name': run_condition_name,
    'description': run_condition_description,
    }
  r_condition_url = '{}/'.format(recastapi.ENDPOINTS['RUN_CONDITIONS'])

  r_condition_response =  recastapi.post(r_condition_url, r_condition_payload)
  run_condition_id = r_condition_response['id']

  owner = recastapi.user.userData()
  owner_id = owner['_items'][0]['id']
  collaboration.upper()

  payload = {
    'owner_id':owner_id,
    'title':title,
    'collaboration':collaboration,
    'e_print':e_print,
    'journal':journal,
    'doi':doi,
    'inspire_URL':inspire_url,
    'description':description,
    'run_condition_id':run_condition_id,
  }
  url = '{}/'.format(recastapi.ENDPOINTS['ANALYSIS'])
  return recastapi.post(url, payload)
