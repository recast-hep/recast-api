import recastapi
import recastapi.request
from termcolor import colored
import yaml
import datetime

#Fill variable of recatapi.ORCID_ID and recastapi.ACCESS_TOKEN
#recastapi.ORCID_ID =
#recastapi.ACCESS_TOKEN = 



print colored('Request data', 'yellow')

request_data = {
    'analysis_id': 2,
    'title': "Test request from API 2",
    'description_model': 'model',
    'reason_for_request': 'A test from API SDK',
    'additional_information': 'Just testing if I can see this request from the frontend',
    'file_path': 'setup.py',
    'parameter_value': 1.1,
    'parameter_title': 'API test'
}

print colored(yaml.safe_dump(request_data,
                             default_flow_style=False),
              'yellow')

response = recastapi.request.create(
    analysis_id = request_data['analysis_id'],
    title = request_data['title'],
    description_model = request_data['description_model'],
    reason_for_request = request_data['reason_for_request'],
    additional_information = request_data['additional_information'],
    file_path = request_data['file_path'],
    parameter_value = request_data['parameter_value'],
    parameter_title = request_data['parameter_title']
    )

print colored('Response', 'green')
print colored(yaml.safe_dump(response,
                             default_flow_style=False),
              'green')

