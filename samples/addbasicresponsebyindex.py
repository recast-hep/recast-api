import os
import recastapi
import recastapi.response

"""Example script to upload a basic response using basic and parameter indices """

request_id = 1
parameter_index = 1
basic_index = 10
yaml_file = 'basicresponse.yaml'
filename = 'samples/file11.zip'

recastapi.ORCID_ID = os.environ.get('RECASTAPI_ORCID_ID', '')
recastapi.ACCESS_TOKEN  = os.environ.get('RECASTAPI_ACCESS_TOKEN', '')

response = recastapi.response.add_basic_response_by_index(yaml_file=yaml_file,
                                                          request_id=request_id,
                                                          parameter_index=parameter_index,
                                                          basic_index=basic_index,
                                                          filename=filename)

print response
