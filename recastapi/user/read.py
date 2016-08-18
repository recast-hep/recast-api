import recastapi
def user(user_id = None):
    """Lists user information.

    :param id: Optional, if provided will return data of a single user.
    :return: JSON object containing all data that could be retrieved.
    """
    single_user = '/{}'.format(user_id) if user_id is not None else ''
    url = '{}{}'.format(recastapi.ENDPOINTS['USERS'], single_user)
    return recastapi.get(url)

def this_user():
    """Lists user given his ORCID ID
    :return: JSON object
    """
    if not recastapi.ORCID_ID:
        raise RuntimeError('No ORCID ID set')
    url = '{}?where=orcid_id=="{}"'.format(recastapi.ENDPOINTS['USERS'], recastapi.ORCID_ID)
    return recastapi.get(url)['_items'][0]
