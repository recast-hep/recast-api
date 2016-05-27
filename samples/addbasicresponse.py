import recastapi
import recastapi.response
from termcolor import colored
import yaml
import datetime

#Fill variable of recatapi.ORCID_ID and recastapi.ACCESS_TOKEN
recastapi.ORCID_ID =
recastapi.ACCESS_TOKEN =

response = recastapi.response.add_basic_response('basicresponse.yaml', 'setup.py')


print colored('Response', 'green')
print colored(yaml.safe_dump(response,
                             default_flow_style=False),
              'green')

