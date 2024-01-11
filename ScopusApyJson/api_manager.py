__all__ = ['get_doi_json_data_from_api',]

def _set_els_doi_api(MyScopusKey, MyInstKey, doi):
    """
    """ 
    # Globals imports
    from ScopusApyJson.GLOBALS import ELS_LINK
    
    # Setting the query  
    query_header = ELS_LINK
    query = doi + '?'

    # Building the HAL API
    els_api = query_header \
            + query \
            + '&apikey='    + MyScopusKey \
            + '&insttoken=' + MyInstKey \
            + '&httpAccept=application/json'
    
    return els_api


def _get_json_from_api(doi, API_CONFIG_DICT):
    '''
    '''
    # Standard library imports
    import json    
    
    # 3rd party library imports
    import requests
    from requests.exceptions import Timeout
    
    # Setting client authentication keys
    MyScopusKey = API_CONFIG_DICT["apikey"]
    MyInstKey   = API_CONFIG_DICT["insttoken"]
    api_uses_nb = API_CONFIG_DICT['api_uses_nb']

    # Setting Elsevier API
    els_api = _set_els_doi_api(MyScopusKey, MyInstKey, doi)
    
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
            print(f'Resquest successful for DOI {doi}')
            if response.status_code == 204:
                print('No content')
            else:            
                response_dict = response.json()
                
        # Updating api_uses_nb in config_dict
        API_CONFIG_DICT["api_uses_nb"] = api_uses_nb + 1
    
    return response_dict


def _update_api_config_json(API_CONFIG_PATH, API_CONFIG_DICT):
    # Standard library imports
    import json
    
    with open(API_CONFIG_PATH, 'w') as f:
        json.dump(API_CONFIG_DICT, f, indent = 4)
        
        
def get_doi_json_data_from_api(doi):
    
    # Globals imports
    from ScopusApyJson.GLOBALS import API_CONFIG_DICT
    from ScopusApyJson.GLOBALS import API_CONFIG_PATH
    
    # Getting api json data
    doi_json_data = _get_json_from_api(doi, API_CONFIG_DICT)
    
    # Updatting api config json with number of requests
    _update_api_config_json(API_CONFIG_PATH, API_CONFIG_DICT)
    
    return doi_json_data