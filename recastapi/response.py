import os
import requests as httprequest
import json
import recastapi
from termcolor import colored
import urllib

def response(id = None):
  single_response = '/{}'.format(id) if id else ''
  url = '{}{}'.format(recastapi.ENDPOINTS['RESPONSES'], single_response)
  return recastapi.get(url)

def user_response(username):
  r = httprequest.get('{}/responses.json?pagesize=100000&username={}'.format(BASEURL,username))
  resonses = json.loads(r.content)
  return resonses

def create(request_id, model_id=None):
  payload = {
    'model_id': model_id
    }
  url = '{}/'.format(recastapi.ENDPOINTS['RESPONSES'])
  return recastapi.post(url, json=payload)


def add_point_response(lumi_weighted_efficiency, luminosity,
                     lower_1sig, upper_1sig, lower_2sig, upper_2sig, 
                     signal_template, log_likelihood, model_id,
                     response_id, point_request_id):
  payload = {
    'lumi_weighted_efficiency': lumi_weighted_efficiency,
    'total_luminosity': luminosity,
    'lower_1sig_limit_on_cross_section_wrt_reference': lower_1sig,
    'upper_1sig_limit_on_cross_section_wrt_reference': upper_1sig,
    'lower_2sig_limit_on_cross_section_wrt_reference': lower_2sig,
    'upper_2sig_limit_on_cross_section_wrt_reference': upper_2sig,
    'merged_signal_template_wrt_reference': signal_template,
    'log_likelihood_at_reference': log_likelihood,
    'model_id': model_id,
    'scan_response_id': response_id
    }
  url = '{}/'.format(recastapi.ENDPOINTS['POINT_RESPONSES'])
  return recastapi.post(url, json=payload)

def add_basic_response(efficiency=None, luminosity=None, lower_1sig=None, upper_1sig=None,
                     lower_2sig=None, upper_2sig=None, lower_1sig_rate=None, upper_1sig_rate=None,
                     lower_2sig_rate=None, upper_2sig_rate=None, log_likelihood=None,
                       reference_cross_section=None, model_id=None,
                     point_response_id=None, basic_request_id=None):
  payload = {
    'overall_efficiency': efficiency,
    'nominal_luminosity': luminosity,
    'lower_1sig_limit_on_cross_section': lower_1sig,
    'upper_1sig_limit_on_cross_section': upper_1sig,
    'lower_2sig_limit_on_cross_section': lower_2sig,
    'upper_2sig_limit_on_cross_section': upper_2sig,
    'lower_1sig_limit_on_rate': lower_1sig_rate,
    'upper_1sig_limit_on_rate': upper_1sig_rate,
    'lower_2sig_limit_on_rate': lower_2sig_rate,
    'upper_2sig_limit_on_rate': upper_2sig_rate,
    'log_likelihood_at_reference': log_likelihood,
    'reference_cross_section': reference_cross_section,
    'model_id': model_id,
    'point_response_id': point_response_id
    }
  url = '{}/'.format(recastapi.ENDPOINTS['BASIC_RESPONSES'])
  return recastapi.post(url, json=payload)

def upload_file(basic_response_id, file_name, 
                point_response_id=None, file_path=None,
                histo_name=None, histo_path=None):
  payload = {
    'file_name': file_name,
    'file_path': file_path,
    'histo_name': histo_name,
    'histo_path': histo_path,
    'point_response_id': point_response_id,
    'basic_response_id': basic_response_id
    }
  files = {'file': open(file_name, 'rb')}
  url = '{}/'.format(recastapi.ENDPOINTS['HISTOGRAMS'])
  return recastapi.post(url, data=payload, files=files)

def download_archive(basic_response_id, download_path=None):
  files_urls = '{}?where=basic_response_id=="{}"'.format(
    recastapi.ENDPOINTS['HISTOGRAMS'], basic_response_id)
  
  file_ids = []
  responses = []
  url_response = recastapi.get(files_urls)
  if len(url_response['_items']) < 2 and not len(url_response['_items']) == 0:
    url = ('{}/{}'.format(recastapi.ENDPOINTS['HISTOGRAMS'], 
                          url_response['_items'][0]['id']))
    response = recastapi.get(url)
    link = response['file_link']
    if link:
      zip_file = urrllib.URLopener()
      zip_file.retrieve(link, download_path or response['original_file_name'])
      response['file_link'] = download_path or response['original_file_name']
      print colored('Successfully downloaded file {}'.format(
          download_path), 'green')
    else:
      response['file_path'] = ''
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
