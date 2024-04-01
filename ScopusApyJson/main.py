__all__ = ['build_scopus_df_from_api',
          ]

def build_scopus_df_from_api(doi_list):
    '''The function `build_scopus_df_from_api` gets, for each of the DOI 
    in the DOI list "doi_list", the hierarchical dict of the data returned by 
    the function 'get_doi_json_data_from_api'. Then it builts the dataframes resulting 
    from the hierarchical dicts parsing using the function `parse_json_data_to_scopus_df`.
    Finally, it concatenates these dataframe to a single dataframe.
    
    Args:
        doi_list (list): The list of DOI (str) for the Scopus API request.
        
    Returns:
        (pandas.core.frame.DataFrame): The concatenation of the dataframes resulting 
    from the hierarchical dicts parsing for each DOI of the list "doi_list".
    
    '''
    # 3rd party imports
    import pandas as pd
    
    # Local library imports
    from ScopusApyJson.GLOBALS import SELECTED_SCOPUS_COLUMNS_NAMES
    from ScopusApyJson.api_manager import get_doi_json_data_from_api
    from ScopusApyJson.json_parser import parse_json_data_to_scopus_df
    
    if not isinstance(doi_list, list): doi_list = [doi_list]
    scopus_df_list = []
    api_scopus_df = pd.DataFrame(columns = SELECTED_SCOPUS_COLUMNS_NAMES)
    for idx, doi in enumerate(doi_list):        
        api_json_data, request_status = get_doi_json_data_from_api(doi)        
        if request_status == "Empty":
            print(f'DOI {doi} not found in Scopus database')
        elif request_status == "False":
            print('Authentication failed: please check availability of authentication keys')
        elif request_status == "Timeout":
            print('Request timeout: please check web access')
        else:
            print(f'Resquest successful for DOI {doi}')           
            scopus_df = parse_json_data_to_scopus_df(api_json_data)
            scopus_df_list.append(scopus_df)
            api_scopus_df = pd.concat(scopus_df_list, axis = 0)
    
    return api_scopus_df
