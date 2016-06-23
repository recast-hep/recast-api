import recastapi
import recastapi.request.get as request_get
from termcolor import colored
import yaml

print colored('Request view')

request_id = 1

response = request_get.parameter(request_id, 1)

print colored(yaml.safe_dump(response, 
                             default_flow_style=False),
              'green')

print len(response)

    
