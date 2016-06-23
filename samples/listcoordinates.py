import recastapi
import recastapi.request.get as request_get
from termcolor import colored
import yaml

print colored('Request view')

request_id = 1

response = request_get.coordinate(request_id, parameter_index=0, coordinate_index=0)


print colored(yaml.safe_dump(response, 
                             default_flow_style=False),
              'green')

    
