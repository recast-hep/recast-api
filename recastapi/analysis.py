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
  
def create(owner_id, title, collaboration, 
                   e_print, journal, doi, inspire_url, 
                   description, run_condition_id):
  """Create a new analysis given the run_condition id
      owner_id
      collaboration: ALICE, ATLAS,CMS...
      .
      .
      .
  """
  collaboration.toUpperCase()
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
  postbody = '&'.join(['='.join(x) for x in payload.iteritems()])
  return recastpi.post(url, payload)
  
def create(owner_id, title, collaboration,
                   e_print, journal, doi, inspire_url, 
                   description, run_condition_name, run_condition_description):
  """Create a new analysis and Run Condition
     see createAnalysis(...)
     .
     .
     .
  """
  
  r_condition_payload = {
    'name': run_condition_name,
    'description': run_condition_description,
    }
  r_condition_url = '{}/'.format(recastapi.ENDPOINTS['RUN_CONDITIONS'])

  r_condition_response =  recastapi.post(url, r_condition_payload)
  run_condition_id = r_condition_response['id']

  return create(owner_id, title, collaboration,
                 e_print, journal, doi, inspire_url,
                 description, run_condition_id)
