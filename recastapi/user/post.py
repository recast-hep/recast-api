import recastapi

def user(name, email, orcid_id=None):
    """create a new user.


    :param name: First and last name of the user.
    :param email: Email of the user.
    :param orcid_id: ORCID ID of the user.

    :return: JSON object with added data.
    """
    payload = {
        'name':name,
        'email':email,
        'orcid_id':orcid_id,
        }
    url = '{}/'.format(recastapi.ENDPOINTS['USERS'])
    return recastapi.post(url, payload)
