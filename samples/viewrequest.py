import recastapi
import recastapi.request
from termcolor import colored
import yaml

print colored('Request view')

request_id = 1

response = recastapi.request.request(request_id)

print colored(yaml.safe_dump(response, 
                             default_flow_style=False),
              'green')

response2 = recastapi.request.request_tree(request_id)
    
