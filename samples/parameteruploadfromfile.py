import os
import recastapi
import recastapi.request.post
import yaml

""" Example script to upload several parameter points from a file 
    Set the request ID
    can return a response variable
"""

request_id = 5


f = open('samples/param_data.yaml')
param_data = yaml.load(f)
f.close()

print yaml.dump(param_data, default_style=False)

recastapi.ORCID_ID = os.environ.get('RECASTAPI_ORCID_ID', '')
recastapi.ACCESS_TOKEN = os.environ.get('RECASTAPI_ACCESS_TOKEN', '')

response = []

for parameter in param_data:

    # create a point request/parameter (parent)
    print "Adding parameter for: {}".format(parameter['coordinates'])
    point_response = recastapi.request.post.parameter(request_id=request_id)
    parameter_id = point_response['id']
    
    response.append(point_response)
    response[-1]['coordinate'] = []

    for coordinate in parameter['coordinates']:
        print "\t Adding coordinates: {}".format(coordinate)
        
        coordinate_response = recastapi.request.post.coordinate(
            parameter_id=parameter_id,
            coordinate_name=coordinate['name'],
            coordinate_value=float(coordinate['value'])
            )
        # save coordinate response id
        response[-1]['coordinate'].append(coordinate_response)

    #basic requests
    response[-1]['files'] = []
    for basic in parameter['basicrequests']:
        print "\t Uploading file: {}".format(basic)
        file_response = recastapi.request.post.upload_file(parameter_id=parameter_id,
                                                      filename=basic)
        response[-1]['files'].append(file_response)

    print "\n\n"
