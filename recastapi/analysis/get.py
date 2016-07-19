import recastapi

def analysis(uuid = None):  
    """List analysis given uuid or all analyses.
        
    :param uuid: analysis_id.
    
    :return: JSON object containing all analyses retrieved.
    """
    
    single_analysis = '/{}'.format(uuid) if uuid else ''
    url = '{}{}'.format(recastapi.ENDPOINTS['ANALYSIS'], single_analysis)
    responses = recastapi.get(url)
    if responses.has_key('_items'):
        return responses['_items']
    else:
        return responses
    
def query(query=None):
    """ customized query. """
    url = '{}{}'.format(recastapi.ENDPOINTS['REQUESTS'], query)
    response = recastapi.get(url)
    if response.has_key('_items'):
        return response['_items']
    else:
        return response
    
