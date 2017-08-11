import recastapi
import recastapi.analysis
import recastapi.user
import recastapi.subscription
import recastapi.request

from termcolor import colored

recastapi.ORCID_ID = ''
recastapi.ACCESS_TOKEN = ''

print colored('Start by printing data in DB. i.e. GET requests', 'red')

print colored('Analysis GET METHOD', 'green')
print recastapi.analysis.analysis()

print colored('User GET METHOD', 'green')
print recastapi.user.user()

print colored('Request GET METHOD', 'green')
print recastapi.request.request()

print colored('Adding data into DB, POST METHODS', 'red')

print colored('Add Analaysis POST METHOD', 'green')
print recastapi.analysis.create(title='test adding analysis from SDK',
                                collaboration='CMS',
                                doi='1211.121121',
                                inspire_id='1234',
                                arxiv_id='56780',
                                cds_id='938472',
                                description='this is a test',
                                run_condition_name='Name of this run condition',
                                run_condition_description='and finally the description')

print colored('Adding Request POST METHOD', 'green')
response =  recastapi.request.create(analysis_id=1,
                                     description_model='A simple description',
                                     reason_for_request='Give me a reason for this request',
                                     additional_information='some additional info',
                                     file_path='./setup.py',
                                     parameter_value=20.2,
                                     parameter_title='example parameter',
                                     status='Incomplete')

                                
print colored(response, 'yellow')
print colored('Adding point request', 'green')

print recastapi.request.add_parameter_point(request_id=11, parameter_value=10, filename='setup.py')

print colored('Downloading file', 'green')
print recastapi.request.download_file(1, './setup.txt')
