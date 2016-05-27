import recastapi
import recastapi.response
from termcolor import colored
import yaml
import datetime

#Fill variable of recatapi.ORCID_ID and recastapi.ACCESS_TOKEN
recastapi.ORCID_ID = '0000-0001-7618-844X'
#recastapi.ACCESS_TOKEN = 'd4dfe8b-04fa-4797-bee4-57fd84207be0'
recastapi.ACCESS_TOKEN = '7f9b0497-e340-4476-8247-8ab29e84dd9a'

response = recastapi.response.create(1)

print colored('Response', 'green')
print colored(yaml.safe_dump(response,
                             default_flow_style=False),
              'green')

