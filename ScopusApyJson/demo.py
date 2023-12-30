__all__ = ['build_scopus_csv_from_api',
           'build_scopus_csv_from_file',
          ]


def _export_to_check(df, root_path, filename_base):
    """Saves the scopus results extracted using Elsevier-DOI api and 
    the scopus results extracted using scopus-site request 
    in the same file for checking results equivalence."""
    
    # Standard library imports
    from pathlib import Path
    
    # 3rd party imports
    import pandas as pd
    
    # Globals imports
    from ScopusApyJson.GLOBALS import SELECTED_SCOPUS_COLUMNS_NAMES
    
    # Formatting dataframe of Scopus-DOI api results
    df = df.T
    df.reset_index(inplace = True)
    
    # Setting dataframe of scopus-site request
    file_xlsx = root_path / Path(filename_base + '.xlsx')
    dg = pd.read_excel(file_xlsx, header = None)
    
    # Merging the two dataframes
    dh = pd.merge(df, dg, left_index = True, right_index = True)
    dh.drop("0_y", axis = 1, inplace = True)
    dh.rename(columns= {"0_x": "from API", 1: "REF"}, inplace = True)
    
    # Saving de merged dataframe as Excel file
    file_out = root_path / Path(filename_base + '_check.xlsx')
    dh.to_excel(file_out, index = False)
    

def _get_doi_json_data_from_file(file_doi, root_path):
    """
    """
    # Standard library imports
    import json
    from pathlib import Path
    
    file_path = root_path / Path(f'{file_doi}.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        
    return json_data


def build_scopus_csv_from_file(doi_file_list, root_path, check = False):
    """
    """
    # 3rd party imports
    import pandas as pd
    
    # Local library imports
    from ScopusApyJson.json_parser import parse_json_data_to_scopus_df        
    
    if not isinstance(doi_file_list, list): doi_file_list = [doi_file_list]
    scopus_df_list = []
    for idx, doi_file in enumerate(doi_file_list):
        file_json_data = _get_doi_json_data_from_file(doi_file, root_path)
        scopus_df      = parse_json_data_to_scopus_df(file_json_data)
        if check: 
            _export_to_check(scopus_df, root_path, doi_file)
        scopus_df_list.append(scopus_df)
    files_scopus_df = pd.concat(scopus_df_list, axis = 0)
    
    return files_scopus_df


def build_scopus_csv_from_api(api_config_path, api_doi_list):
    """
    """
    # 3rd party imports
    import pandas as pd
    
    # Local library imports
    from ScopusApyJson.api_manager import get_doi_json_data_from_api
    from ScopusApyJson.json_parser import parse_json_data_to_scopus_df
    
    if not isinstance(api_doi_list, list): api_doi_list = [api_doi_list]
    scopus_df_list = []
    for idx, api_doi in enumerate(api_doi_list) :
        api_json_data = get_doi_json_data_from_api(api_doi, api_config_path)
        scopus_df     = parse_json_data_to_scopus_df(api_json_data)
        scopus_df_list.append(scopus_df)
    api_scopus_df = pd.concat(scopus_df_list, axis = 0)
    
    return api_scopus_df