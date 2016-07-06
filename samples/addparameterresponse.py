import os
import recastapi
import recastapi.response

""" Example script to upload a parameter response using parameter indices
"""

request_id = 1
parameter_index = 1
filename = 'samples/file11.zip'
yaml_file = 'pointresponse.json'

recastapi.ORCID_ID = os.environ.get('RECASTAPI_ORCID_ID', '')
recastapi.ACCESS_TOKEN = os.environ.get('RECASTAPI_ACCESS_TOKEN', '')



response = recastapi.response.add_parameter_response_by_index(yaml_file=yaml_file,
                                                              request_id=request_id,
                                                              parameter_index=parameter_index,
                                                              filename=filename)

print response
