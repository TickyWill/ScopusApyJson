"""Functions for Scopus API management with request based on DOI."""

__all__ = ['get_doi_json_data_from_api',]

# Standard library imports
import json

# 3rd party imports
import requests
from requests.exceptions import Timeout

# Internal imports
import ScopusApyJson.saj_globals as saj_g


def _set_els_doi_api(MyScopusKey, MyInstKey, doi):
    """The internal function `_set_els_doi_api` sets, for the DOI 'doi', 
    the query 'els_api' according to the Scopus API usage 
    which header is given by the global 'ELS_LINK'.
    
    Args:
        MyScopusKey (str): The user's authentication key.
        MyInstKey (str): The user's institution token.
        doi (str): The publication DOI for which the Scopus API \
        will provide information. 
    Returns:
        (str): The query for the passed DOI according to the scopus \
        api usage.
    """
    # Setting the query
    query_header = saj_g.ELS_LINK
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
    the response to the query 'els_api' built using the `_set_els_doi_api` 
    internal function .

    It passes to this function the user's authentication key 'MyScopusKey' 
    and the user's institutional token 'MyInstKey' given by the 'api_config_dict' 
    dict. 
    It also increments the number of requests performed by the user. The number 
    is updated in the dict 'api_config_dict' at key 'api_uses_nb'.

    Args:
        doi (str): The publication DOI for which the Scopus API will provide data.
        api_config_dict (dict): The dict wich values are the user's authentication \
        key, the user's institutional token and the number of requests performed.
        timeout (int): The maximum waiting time in seconds for request answer.
    Returns:
        (tup): The tup composed by the hierarchical-dict response \
        to the query and the updated 'api_config_dict' dict.
    """
    # Initializing parameters
    response_dict = None
    response = None
    response_status = "False"

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
        if any(x==response.status_code for x in [204, 404]):
            response_status = "Empty"
        else:
            response_status = "True"
            response_dict = response.json()
        # Updating api_uses_nb in config_dict
        api_config_dict["api_uses_nb"] = api_uses_nb + 1

    return response_dict, api_config_dict, response_status


def _update_api_config_json(api_config_path, api_config_dict):
    with open(api_config_path, 'w', encoding="utf-8") as f:
        json.dump(api_config_dict, f, indent = 4)


def get_doi_json_data_from_api(doi, timeout = None):
    """The function `get_doi_json_data_from_api` gets, for the DOI 'doi', 
    the json-serialized response to the Scopus API request using 
    the internal function `_get_json_from_api`.
    It passes to this function the user's dict 'API_CONFIG_DICT'. 
    It also updates the API configuration json file with the modified 
    dict 'API_CONFIG_DICT' returned by this function.
    
    Args:
        doi (str): The publication DOI for which the Scopus API \
        will provide data.
        timeout (int): The maximum waiting time in seconds \
        for request answer (default: 10).
    Returns:
        (dict): The hierarchical dict of the data returned \
        by the internal function '_get_json_from_api'.
    """
    if not timeout:
        timeout = 10

    # Getting api json data
    return_tup = _get_json_from_api(doi, saj_g.API_CONFIG_DICT,
                                    timeout)
    doi_json_data, api_config_dict, request_status = return_tup

    # Updatting api config json with number of requests
    _update_api_config_json(saj_g.API_CONFIG_PATH,
                            api_config_dict)

    return doi_json_data, request_status
