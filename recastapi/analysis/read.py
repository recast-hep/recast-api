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

def analysis_by_pub_identifier(pubtype, pubid):
    """List analysis given uuid or all analyses.

    :param uuid: analysis_id.

    :return: JSON object containing all analyses retrieved.
    """

    query = None
    if pubtype == 'cds':
        query = 'cds_id=="{}"'.format(pubid)
    elif pubtype == 'arxiv':
        query = 'arxiv_id=="{}"'.format(pubid)
    elif pubtype == 'inspire':
        query = 'inspire_id=="{}"'.format(pubid)
    elif pubtype == 'recast':
        query = 'id=="{}"'.format(pubid)
    else:
        raise NotImplementedError()

    url = '{}{}'.format(recastapi.ENDPOINTS['ANALYSIS'], '?where={}'.format(query))
    responses = recastapi.get(url)

    if not responses['_items']:
        return None

    return responses['_items'][0]
