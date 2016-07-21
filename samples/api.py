import json
import logging
import os
import Queue
import recastapi.request.get
import recastapi.request.post
import recastapi.response.post
import recastapi.response.get
import yaml

class RecastRequest(object):
    """ A helper client stateful class for the Request API endpoint.
    
    Container for a single request, and keeps history of actions performed and state.
    """
    def __init__(self, request_id=None, json_file=None):
        self.input = None
        self.all_responses = []
        self.request_id = request_id
        self.staged_point_request = Queue.Queue()
        self.staged_basic_request = Queue.Queue()

        logging.basicConfig(level=logging.DEBUG,
                            format='[%(levelname)s] %(message)s')
        logging.info('Initialization')
        self.print_sizes()
        if json_file:
            pass
    def print_sizes(self):
        logging.info('point request size: {}'.format(self.staged_point_request.qsize()))
        logging.info('basic request size: {}'.format(self.staged_basic_request.qsize()))
        
    def current_response(self):
        if self.all_responses:
            return self.all_responses[-1]
        logging.warning('Responses empty!')
        #raise Exception('No response yet!')

    def read_file(self, filename):
        """ Reads dumped file and fills queues

        example file format:
        {'request_id':
        'staged_response':
        'staged_basic_response':
        }
        """
        if not os.path.isfile(filename):
            raise Exception('Filename does not exist!')

        f = open(filename)
        data = yaml.load(f)
        f.close()
        try:
            self.request_id = data['request_id']
            response = data['staged_response']
            response_l = response.split(',')
            for i in response_l:
                self.staged_point_request.put(int(i))
            basic = data['staged_basic_response']
            basic_l = basic.split(',')
            for i in basic_l:
                self.staged_basic_request.put(int(i))
        except Exception, e:
            print e
            raise Exception(e)
    
    def dump(self, filename=None):
        """ Writes state of class to file.
        
        """
        if not filename:
            filename = 'file_request_{}.json'.format(self.request_id)
        logging.info('filename: {}'.format(filename))
        data = {}
        data['request_id'] = self.request_id
        staged_response = ''
        while not self.staged_point_request.empty():
            el = self.staged_point_request.get()
            logging.debug('adding {}'.format(el))
            staged_response += '{},'.format(el)
        data['staged_response'] = staged_response

        staged_basic_response = ''
        while not self.staged_basic_request.empty():
            el = self.staged_basic_request.get()
            logging.debug('adding {}'.format(el))
            staged_basic_response += '{},'.format(el)
        data['staged_basic_response'] = staged_basic_response
        logging.info('Content dumped: {}'.format(data))
        with open(filename, 'w') as f:
            json.dump(data, f)
                
    def add_parameter_from_file(self, param_file='samples/param_data.yaml'):
        """ function to add parameters

        saves point_request_id and basic_request_id into a staging area/Queue
        to be used later to add
        """
        f = open(param_file)
        param_data = yaml.load(f)
        f.close()

        response = []

        for parameter in param_data:
            logging.info('Adding parameter for: {}'.format(parameter['coordinates']))
            point_response = recastapi.request.post.parameter(request_id=self.request_id)

            parameter_id = point_response['id']
            logging.debug('Added point request with ID: {}'.format(parameter_id))
            self.staged_point_request.put(parameter_id)
            
            response.append(point_response)
            response[-1]['coordinate'] = []

            for coordinate in parameter['coordinates']:
                logging.info('\t Adding coordinates: {}'.format(coordinate))
                coordinate_response = recastapi.request.post.coordinate(
                    parameter_id=parameter_id,
                    coordinate_name=coordinate['name'],
                    coordinate_value=float(coordinate['value'])
                    )
                logging.debug('Added coordinate with ID: {}'.format(coordinate_response['id']))
                response[-1]['coordinate'].append(coordinate_response)

            response[-1]['files'] = []
            for basic in parameter['basicrequests']:
                logging.info('\t Uploading file: {}'.format(basic))
                file_response = recastapi.request.post.upload_file(parameter_id=parameter_id,
                                                                   filename=basic)
                response[-1]['files'].append(file_response)
                logging.debug('Added archive with ID: {}'.format(file_response['id']))
                self.staged_basic_request.put(file_response['id'])
        logging.debug('Added all files!')
        self.all_responses.append(response)

    def add_point_response(self, response_file, archive):
        """ Adds point response to staged point_request.
        """
        if not self.staged_point_request.empty():
            point_request_id = self.staged_point_request.get()
            response = {}
            logging.info('Creating a scan response')
            scan_response = recastapi.response.post.response(request_id=self.request_id)
            logging.info('Adding a point response to point request id: {}'.format(
                point_request_id))
            response = recastapi.response.post.parameter_response(
                yaml_file=response_file,
                point_request_id=point_request_id,
                scan_response_id=scan_response['id'],
                filename=archive)
            logging.debug('Added point response with ID: {}'.format(response['id']))
            response['scan_response'] = scan_response
            self.all_responses.append(response)
            return True
        logging.error('No staged point request available!')
        return False

    def add_basic_response(self, basic_response_file, archive):
        """ Adds basic response to staged basic_request.

        """
        print 'Function not currently implemented, returning....'
        return
        if not self.staged_basic_request.empty():
            basic_request_id = self.staged_point_request.get()
            response = {}
            # first get the point request id
            logging.debug('checking if basic response has point request id')

    def create_this_request(self, **kwargs):
        """ to create a request for this class.
        
        function used if the request class wasn't assigned id 
        at initialization stage.
        """
        try:
            analysis_id = kwargs['analysis_id']
            title = kwargs['title']
            description_model = kwargs['description_model']
            reason_for_request = kwargs['reason_for_request']
            additional_information = kwargs['additional_information']
            status = kwargs['status']
            file_path = kwargs['file_path']
            parameter_value = kwargs['parameter_value']
            parameter_title = kwargs['parameter_title']
        except Exception, e:
            print e
            print "Data not added"
            return False

        response = recastapi.request.post.request(analysis=analysis,
                                                  title=title,
                                                  description_model=description_model,
                                                  reason_for_request=reason_for_request,
                                                  additional_information=additional_information,
                                                  status=status,
                                                  file_path=file_path,
                                                  parameter_value=parameter_value,
                                                  parameter_title=parmeter_title)
        self.all_responses.append(response)
        return True
