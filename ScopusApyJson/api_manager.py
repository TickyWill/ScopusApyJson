__all__ = ['get_doi_json_data_from_api',]

def _set_els_doi_api(MyScopusKey, MyInstKey, doi):
    """The internal function `_set_els_doi_api` sets, for the DOI 'doi', 
    the query 'els_api' according to the Scopus API usage 
    which header is given by the global 'ELS_LINK'.
    
    Args:
        MyScopusKey (str): The user's authentication key.
        MyInstKey (str): The user's institution token.
        doi (str): The publication DOI for which the Scopus API will provide information. 
        
    Returns:
        (str): The query for the passed DOI according to the scopus api usage.
        
    """ 
    # Local imports
    import ScopusApyJson.GLOBALS as saj_globals
    
    # Setting the query  
    query_header = saj_globals.ELS_LINK
    query = doi + '?'

    # Building the HAL API
    els_api = query_header \
            + query \
            + '&apikey='    + MyScopusKey \
            + '&insttoken=' + MyInstKey \
            + '&httpAccept=application/json'
    
    return els_api


def _get_json_from_api(doi, api_config_dict, timeout):
    """The internal function `_get_json_from_api` gets, for the DOI 'doi', 
    the response to the query 'els_api' built using the internal function `_set_els_doi_api`.
    It passes to this function the user's authentication key 'MyScopusKey' and the user's 
    institutional token 'MyInstKey' given by the dict 'api_config_dict'. 
    It also increments the number of requests performed by the user. The number is updated 
    in the dict 'api_config_dict' at key 'api_uses_nb'.
    
    Args:
        doi (str): The publication DOI for which the Scopus API will provide data.
        api_config_dict (dict): The dict wich values are the user's authentication key, the user's 
        institutional token and the number of requests performed.
        timeout (int): The maximum waiting time in seconds for request answer.
        
    Returns:
        (tup): The tup composed by the hierarchical-dict response
        to the query and the updated 'api_config_dict' dict.
    """    
   
    # 3rd party library imports
    import requests
    from requests.exceptions import Timeout
    
    # Initializing parameters
    response_dict = None
    
    # Setting client authentication keys
    MyScopusKey = api_config_dict["apikey"]
    MyInstKey   = api_config_dict["insttoken"]
    api_uses_nb = api_config_dict['api_uses_nb']

    # Setting Elsevier API
    els_api = _set_els_doi_api(MyScopusKey, MyInstKey, doi)

    # Get the request response
    try:
        response = requests.get(els_api, timeout = timeout)   
    except Timeout:
        response_status = "Timeout"
    else:
        if response == False: # response.status_code <200
            response_status = "False"
        else:
            if response.status_code in [204, 404]:
                response_status = "Empty"
            else:
                response_status = "True"
                response_dict = response.json()

        # Updating api_uses_nb in config_dict
        api_config_dict["api_uses_nb"] = api_uses_nb + 1
    
    return (response_dict, api_config_dict, response_status)


def _update_api_config_json(api_config_path, api_config_dict):
    # Standard library imports
    import json
    
    with open(api_config_path, 'w') as f:
        json.dump(api_config_dict, f, indent = 4)
        
        
def get_doi_json_data_from_api(doi, timeout = None):
    """The function `get_doi_json_data_from_api` gets, for the DOI 'doi', 
    the json-serialized response to the Scopus API request using 
    the internal function `_get_json_from_api`.
    It passes to this function the user's dict 'API_CONFIG_DICT'. 
    It also updates the API configuration json file with the modified 
    dict 'API_CONFIG_DICT' returned by this function.
    
    Args:
        doi (str): The publication DOI for which the Scopus API will provide data.
        timeout (int): The maximum waiting time in seconds for request answer (default: 10).
        
    Returns:
        (dict): The hierarchical dict of the data returned by the internal function '_get_json_from_api'.
        
    """ 
    
    # Local imports
    import ScopusApyJson.GLOBALS as saj_globals
    
    if not timeout : timeout = 10
    
    # Getting api json data
    doi_json_data, API_CONFIG_DICT, request_status = _get_json_from_api(doi, saj_globals.API_CONFIG_DICT, timeout)
    
    # Updatting api config json with number of requests
    _update_api_config_json(saj_globals.API_CONFIG_PATH, saj_globals.API_CONFIG_DICT)
    
    return (doi_json_data, request_status)