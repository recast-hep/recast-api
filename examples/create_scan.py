import recastapi.request.write

scanrequest = recastapi.request.write.scan_request(3,'my new scan request', 'my description', 'my reason', 'my addiional information')

points = [
    (125.0,650.0),
    (125.0,750.0),
    (130.0,650.0),
    (130.0,750.0),
]

point_requests = []
basic_requests = []
for x in points:
    pr = recastapi.request.write.point_request_with_coords(scanrequest['id'],{'m_higgs':x[0],'mA':x[1]})
    point_requests += [{'point':x,'id':pr['id']}]
    br = recastapi.request.write.basic_request_with_archive(pr['id'],'actualrequests/point125_13TeV.zip')
    basic_requests += [{'point':x,'id':br['id']}]


import json
json.dump({
    'scan_id': scanrequest['id'],
    'point_requests': point_requests,
    'basic_requests': basic_requests
    },open('mynewscan.json','w')
)
