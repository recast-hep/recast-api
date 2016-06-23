import recastapi

def user(user_id = None):
    """Lists user information.
    
    Args:
        id: Optional, if provided will return data of a single user.
    Returns:
        JSON object containing all data that could be retrieved.
    
    """
    single_user = '/{}'.format(user_id) if user_id else ''
    url = '{}{}'.format(recastapi.ENDPOINTS['USERS'], single_user)
    return recastapi.get(url)

def user_data():
    """Lists user given his ORCID ID
    
    Args:
        None
    Returns:
        JSON object
    """
    if not recastapi.ORCID_ID:
        print '-'*60
        print "No ORCID ID and ACCESS TOKEN provide"
        print "Please provide an ORCID ID"
        raise RuntimeError
    url = '{}?where=orcid_id=="{}"'.format(recastapi.ENDPOINTS['USERS'], recastapi.ORCID_ID)
    return recastapi.get(url)
