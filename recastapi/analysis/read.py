import recastapi

def analysis(analysis_id = None):
    """List analysis given uuid or all analyses.

    :param uuid: analysis_id.

    :return: JSON object containing all analyses retrieved.
    """

    single_analysis = '/{}'.format(analysis_id) if analysis_id is not None else ''
    url = '{}{}'.format(recastapi.ENDPOINTS['ANALYSIS'], single_analysis)
    responses = recastapi.get(url)
    if responses.has_key('_items'):
        return responses['_items']
    else:
        return responses
