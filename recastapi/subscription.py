import recastapi


def create(analysis_id,
           subscription_type,
           description, 
           requirements,
           notifications=[],
           authoritative=False):     
    """Creates a subscription.
    

    :param analysis: ID of the analysis
    :param subscription_type: provider or observer
    :param description: description of subscription
    :param requirements: requirements
    :param notification: recast_requests or recast_responses or new subscribers
    :param authoritative: True or False
    
    :return: JSON object
    """
    
    assert subscription_type in ['provider', 'observer']
    for notif in notifications:
        assert notif in ['recast_requests', 'recast_responses', 'new_subscribers']
        
        
    user = recastapi.user.userData()
    payload = {
        'subscription_type': subscription_type,
        'description': description,
        'requirements': requirements,
        'notification': ','.join(notifications),
        'authoritative': authoritative,
        'subscriber_id': user['_items'][0]['id'],
        'analysis_id': analysis_id,
    }
    url = '{}/'.format(recastapi.ENDPOINTS['SUBSCRIPTIONS'])
    return recastapi.post(url, payload)


def unsubscribe(subscription_id):
    """Deletes subscription.
  
    TO-DO: check if the user is allowed to delete the subscription
    
    :param subscription_id: ID of the subscription
    """
    url = '{}/{}'.format(recastapi.ENDPOINTS['SUBSCRIPTIONS'],
                        subscription_id)
    return recastapi.delete(url)
  

def my_subscriptions():
    """Lists your subscriptions.
    
    """
    if not recastapi.ORCID_ID:
        print "Can't list your subscriptions."
        print "Please provide an ORCID_ID and ACCESS_TOKEN"
        raise RuntimeError        
    user = recastapi.user.userData()
    user_id = user['_items'][0]['id']
    url = '{}?where=subscriber_id=="{}"'.format(recastapi.ENDPOINTS['SUBSCRIPTIONS'], user_id)
    return recastapi.get(url)
  
