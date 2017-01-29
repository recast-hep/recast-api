import json
import recastapi.response.write
data = json.load(open('mynewscan.json'))

scan_id =  data['scan_id']

responsefiles = {
    (125.0,650.0):'file11.zip',
    (125.0,750.0):'file12.zip',
    (130.0,650.0):'file21.zip',
    (130.0,750.0):'file22.zip',
}



pr_data = {tuple(x['point']):x['id'] for x in data['point_requests']}
br_data = {tuple(x['point']):x['id'] for x in data['basic_requests']}

scan_response = recastapi.response.write.scan_response(scan_id)
scan_response_id = scan_response['id']
for i,(coords,prid) in enumerate(pr_data.iteritems()):
    brid = br_data[coords]
    filename = responsefiles[coords]
    x = recastapi.response.write.point_response(scan_response_id,prid,{'lower_2sig_expected_CLs':5+i/10.0})
    point_response_id = x['id']
    recastapi.response.write.basic_response_with_archive(point_response_id,brid,responsefiles[coords],{'lower_2sig_expected_CLs':6+i/10.0})
    print coords,i
