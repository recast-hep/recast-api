import recastapi
import recastapi.request.post
import yaml
import os

parameter_names = ('a', 'b')
parameter_points = [(1,1), (1,2), (2,1), (2,2)]
files = {(1,1):'samples/file11.zip', (1,2):'samples/file12.zip', (2,1):'samples/file21.zip',(2,2):'samples/file22.zip'}
request_id = 4

request_ids = []

recastapi.ORCID_ID = os.environ.get('RECASTAPI_ORCID_ID', '')
recastapi.ACCESS_TOKEN = os.environ.get('RECASTAPI_ACCESS_TOKEN', '')

for parameter in parameter_points:

    print 'add point request for {}'.format(dict(zip(parameter_names, parameter)))
    coordinates = dict(zip(parameter_names, parameter))
    point_response_id = None
    for i, name in enumerate(parameter_names):

        if i == 0:
            #First point, create a new point request
            point_response = recastapi.request.post.parameter(request_id=request_id,
                                                              coordinate_value=coordinates[name],
                                                              coordinate_title=name)
            point_response_id = point_response['id']
        else:
            coordinate_response = recastapi.request.post.coordinate(parameter_id=point_response_id,
                                                                   coordinate_name=name,
                                                                   coordinate_value=coordinates[name])

    print 'Successfully added parameter: {}, with ID {}'.format(parameter, point_response['id'])
    request_ids.append(point_response['id'])

request_mapping = dict(zip(parameter_points, request_ids))
                       
print 'Uploading files ...'
for coordinates, filename in files.iteritems():

    point_request_id = request_mapping[coordinates]
    file_response = recastapi.request.post.upload_file(parameter_id=point_request_id,
                                                       filename=filename)
    print 'Successfully uploaded file {}'.format(filename)

