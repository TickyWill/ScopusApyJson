__all__ = ['get_doi_json_data_from_api',]

def _set_els_doi_api(MyScopusKey, MyInstKey, doi):
    """
    """ 
    # Setting the query
    ELS_LINK = "https://api.elsevier.com/content/abstract/"
    
    query_header = ELS_LINK
    query = doi + '?'

    # Building the HAL API
    els_api = query_header \
            + query \
            + '&apikey='    + MyScopusKey \
            + '&insttoken=' + MyInstKey \
            + '&httpAccept=application/json'
    
    return els_api


def _get_json_from_api(api_doi, api_config_dict):
    '''
    '''
    # Standard library imports
    import json as json
    import requests
    from requests.exceptions import Timeout
    
    # Setting client authentication keys
    MyScopusKey = api_config_dict["apikey"]
    MyInstKey   = api_config_dict["insttoken"]
    api_uses_nb = api_config_dict['api_uses_nb']

    # Setting Elsevier API
    els_api = _set_els_doi_api(MyScopusKey, MyInstKey, api_doi)
    
    # Initializing parameters
    response_dict = None

    # Get the request response
    try:
        response = requests.get(els_api, timeout = 10)   
    except Timeout:
        print('The request timed out')
    else:
        if response == False: # response.status_code <200 or > 400
            print('Resource not found')
        else:
            print(f'Resquest successful for {api_doi}')
            if response.status_code == 204:
                print('No content')
            else:            
                response_dict = response.json()
                
        # Updating api_uses_nb in config_dict
        api_config_dict["api_uses_nb"] = api_uses_nb + 1
    
    return response_dict


def _update_api_config_json(api_config_path, api_config_dict):
    # Standard library imports
    import json as json
    
    with open(api_config_path, 'w') as f:
        json.dump(api_config_dict, f, indent = 4)
        
        
def get_doi_json_data_from_api(api_doi, api_config_path):
    # Standard library imports
    import json as json
    
    # 3rd party imports
    import pandas as pd
    
    # Globals imports
    from ScopusApyJson.GLOBALS import API_CONFIG_DICT
    from ScopusApyJson.GLOBALS import API_CONFIG_PATH
    
    # Getting api json data
    api_json_data = _get_json_from_api(api_doi, API_CONFIG_DICT)
    
    # Updatting api config json with number of requests
    _update_api_config_json(API_CONFIG_PATH, API_CONFIG_DICT)
    
    return api_json_data