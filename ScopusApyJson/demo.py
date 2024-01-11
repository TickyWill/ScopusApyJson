__all__ = ['build_scopus_df_from_api',
          ]

def build_scopus_df_from_api(doi_list):
    """
    """
    # 3rd party imports
    import pandas as pd
    
    # Local library imports
    from ScopusApyJson.api_manager import get_doi_json_data_from_api
    from ScopusApyJson.json_parser import parse_json_data_to_scopus_df
    
    if not isinstance(doi_list, list): doi_list = [doi_list]
    scopus_df_list = []
    for idx, doi in enumerate(doi_list) :
        api_json_data = get_doi_json_data_from_api(doi)
        scopus_df     = parse_json_data_to_scopus_df(api_json_data)
        scopus_df_list.append(scopus_df)
    api_scopus_df = pd.concat(scopus_df_list, axis = 0)
    
    return api_scopus_df
