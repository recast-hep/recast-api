import os
import requests as httprequest
import json
import recastapi

def user_response(username):
  r = httprequest.get('{}/responses.json?pagesize=100000&username={}'.format(BASEURL,username))
  resonses = json.loads(r.content)
  return resonses

def response(id = None):
  single_response = '/{}'.format(id) if id else ''
  url = '{}{}'.format(recastapi.ENDPOINTS['RESPONSES'], single_response)
  return recastapi.get(url)

def addResponse(request_id, model_id):
  payload = {
    'scan_request_id': request_id,
    'model_id': model_id,
    }
  url = '{}/'.format(recastapi.ENDPOINTS['RESPONSES'])
  return recastapi.post(url, payload)


def addPointResponse(lumi_weighted_efficiency, luminosity,
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
    'scan_response_id': response_id,
    'point_request_id': point_request_id,
    }
  url = '{}/'.format(recastapi.ENDPOINTS['POINT_RESPONSES'])
  return recastapi.post(url, payload)

def addBasicResponse(efficiency, luminosity, lower_1sig, upper_1sig,
                     lower_2sig, upper_2sig, lower_1sig_rate, upper_1sig_rate,
                     lower_2sig_rate, upper_2sig_rate, signal_template,
                     log_likelihood, reference_cross_section, model_id,
                     point_response_id, basic_request_id):
  payload = {
    'overall_efficiency': overall_efficiency,
    'nominal_luminosity': luminosity,
    'lower_1sig_limit_on_cross_section': lower_1sig,
    'upper_1sig_limit_on_cross_section': upper_1sig,
    'lower_2sig_limit_on_cross_section': lower_2sig,
    'upper_2sig_limit_on_cross_section': upper_2sig,
    'lower_1sig_limit_on_rate': lower_1sig_rate,
    'upper_1sig_limit_on_rate': upper_1sig_rate,
    'lower_2sig_limit_on_rate': lower_2sig_rate,
    'upper_2sig_limit_on_rate': upper_2sig_rate,
    'signal_template': signal_template,
    'log_likelihood_at_reference': log_likelihood,
    'reference_cross_section': reference_cross_section,
    'model_id': model_id,
    'point_response_id': point_response_id,
    'basic_request_id': basic_request_id,
    }
  url = '{}/'.format(recastapi.ENDPOINTS['BASIC_REQUESTS'])
  return recastapi.post(url, payload)

def addHistogram(file_name, file_path, histo_name, histo_path,
                 point_response_id, basic_response_id):
  payload = {
    'file_name': file_name,
    'file_path': file_path,
    'histo_name': histo_name,
    'histo_path': histo_path,
    'point_response_id': point_response_id,
    'basic_response_id': basic_response_id,
    }
  url = '{}/'.format(recastapi.ENDPOINTS['HISTOGRAMS'])
  return recastapi.post(url, payload)
