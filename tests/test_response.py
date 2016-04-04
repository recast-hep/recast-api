import recastapi
import recastapi.analysis
import recastapi.user
import recastapi.subscription
import recastapi.request
import recastapi.response

from termcolor import colored

recastapi.ORCID_ID = ''
recastapi.ACCESS_TOKEN = ''

print colored('Add response POST method', 'red')
response = recastapi.response.create(25)

print colored(response, 'yellow')

print colored('Add basic response', 'green')
response_2 = recastapi.response.add_basic_response(efficiency=10.0,
                                                 basic_request_id=80)

print colored(response_2, 'yellow')

print colored('Uploading file', 'green')
response_3 = recastapi.response.upload_file(basic_response_id=response_2['id'],
                                            file_name='requirements.txt')
print colored(response_3, 'yellow')

print colored('Downloading', 'red')
response_4 = recastapi.response.download_archive(6,
                                                 download_path='downloaded.txt')

print colored(response_4, 'yellow')
