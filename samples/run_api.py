from samples.api import RecastRequest
import recastapi


request_id = 9

if request_id == 0:
    raise Exception('request id not set')

r = RecastRequest(request_id)

recastapi.ORCID_ID = ''
recastapi.ACCESS_TOKEN = ''

r.add_parameter_from_file() #'arg is hardcoded for testing purpose')

r.print_sizes()

r.add_point_response('samples/pointresponse.json', 'samples/file11.zip')

r.print_sizes()


r.dump()

r.print_sizes()
