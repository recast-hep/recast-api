import recastapi
import recastapi.request
from termcolor import colored
import yaml

print colored('Request view')

request_id = 1

response = recastapi.request.parameter(request_id, 2)


print colored(yaml.safe_dump(response, 
                             default_flow_style=False),
              'green')


print len(response)

    
