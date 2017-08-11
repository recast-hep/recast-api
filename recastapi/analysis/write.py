import recastapi
import recastapi.user.read

def analysis(title,
             collaboration,
             doi,
             arxiv_id,
             inspire_id,
             cds_id,
             description,
             run_condition_name,
             run_condition_description):
    """Create a new analysis and Run Condition.

    :param title: Title of the analysis.
    :param collaboration: Choice among: ALICE, ATLAS, CMS, .
    :param doi:  Digital Object Identifier
    :param inspire_id: INSPIRE Record identifier
    :param arxiv_id: link.
    :param description: A detailed description of the analysis.
    :param run_condition_name: Name of the run condition.
    :param run_condition_descprition: Detailed description of the run condition.

    :return: JSON object containing data that has been added into DB.
    """
    run_condition_payload = {
        'name': run_condition_name,
        'description': run_condition_description,
    }
    run_condition_url = '{}/'.format(recastapi.ENDPOINTS['RUN_CONDITIONS'])
    run_condition_response =  recastapi.post(run_condition_url, run_condition_payload)
    run_condition_id = run_condition_response['id']

    owner = recastapi.user.read.this_user()
    owner_id = owner['id']
    collaboration.upper()

    payload = {
        'owner_id':owner_id,
        'title':title,
        'collaboration':collaboration,
        'doi':doi,
        'arxiv_id':arxiv_id,
        'inspire_id':inspire_id,
        'cds_id':cds_id,
        'description':description,
        'run_condition_id':run_condition_id,
        }
    url = '{}/'.format(recastapi.ENDPOINTS['ANALYSIS'])
    return recastapi.post(url, payload)
