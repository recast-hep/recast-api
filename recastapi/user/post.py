import recastapi

def user(name, email, orcid_id=None):
    """create a new user.

    Args:
        name: First and last name of the user.
        email: Email of the user.
        orcid_id: ORCID ID of the user.

    Returns:
        JSON object with added data.
    """
    payload = {
        'name':name,
        'email':email,
        'orcid_id':orcid_id,
        }
    url = '{}/'.format(recastapi.ENDPOINTS['USERS'])
    return recastapi.post(url, payload)
