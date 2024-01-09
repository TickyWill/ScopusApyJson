__all__ = ['api_manager_demo',
           'build_scopus_df_from_api',
           'build_scopus_df_from_json_files',
           'get_doi_json_data_from_file',
           'json_parser_demo',
          ]


def _export_to_check(df, data_path, filename_base, results_path):
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
    file_xlsx = data_path / Path(filename_base + '.xlsx')
    dg = pd.read_excel(file_xlsx, header = None)
    
    # Merging the two dataframes
    dh = pd.merge(df, dg, left_index = True, right_index = True)
    dh.drop("0_y", axis = 1, inplace = True)
    dh.rename(columns= {"0_x": "from API", 1: "REF"}, inplace = True)
    
    # Saving de merged dataframe as Excel file
    file_out = results_path / Path(filename_base + '_check.xlsx')
    dh.to_excel(file_out, index = False)
    

def get_doi_json_data_from_file(file_doi, data_path):
    """
    """
    # Standard library imports
    import json
    from pathlib import Path
    
    file_path = data_path / Path(f'{file_doi}.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        
    return json_data


def build_scopus_df_from_json_files(doi_file_list, data_path, results_path = None):
    """
    """
    # 3rd party imports
    import pandas as pd
    
    # Local library imports
    from ScopusApyJson.json_parser import parse_json_data_to_scopus_df        
    
    if not isinstance(doi_file_list, list): doi_file_list = [doi_file_list]
    scopus_df_list = []
    for idx, doi_file in enumerate(doi_file_list):
        file_json_data = get_doi_json_data_from_file(doi_file, data_path)
        scopus_df      = parse_json_data_to_scopus_df(file_json_data)
        if results_path is not None: 
            _export_to_check(scopus_df, data_path, doi_file, results_path)
        scopus_df_list.append(scopus_df)
    files_scopus_df = pd.concat(scopus_df_list, axis = 0)
    
    return files_scopus_df


def build_scopus_df_from_api(api_config_path, api_doi_list):
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


def api_manager_demo(data_path = None, api_config_path = None, api_results_path = None):
    """
    Args:
        None
    Returns:
        None
    Note:
        The `get_doi_json_data_from_api` function is imported from `api_manager` module 
        of `ScopusApyJson` package.
        The globals "API_CONFIG_PATH" and "API_RESULTS_PATH" are imported from `GLOBALS` 
        module of `ScopusApyJson` package.
    """
    
    # Standard library imports
    import json as json
    import os
    from pathlib import Path
    
    # Local library imports
    from ScopusApyJson.api_manager import get_doi_json_data_from_api
    
    # Globals imports
    from ScopusApyJson.GLOBALS import API_CONFIG_PATH
    from ScopusApyJson.GLOBALS import API_RESULTS_PATH
    
    #Setting results paths
    if not api_config_path: api_config_path = API_CONFIG_PATH 
    if not api_results_path: api_results_path = API_RESULTS_PATH 
    
    # Setting the DATA path where demo files are stored
    if not data_path:
        data_path = os.path.join(os.path.dirname(__file__), "DATA")    

    
    # Setting a dict which values are the DOIs to be used in the api request
    # The dict keys are used to build the file names where will be saved 
    # the json response of the api request
    doi_dic = {"doi_1": "doi/10.1016/j.fuproc.2022.107223",
               "doi_2": "doi/10.1002/aenm.202102687",
               "doi_3": "doi/10.1007/s13399-020-00894-9",
               "doi_4": "doi/10.1063/5.0140495",
               "doi_5": "doi/10.1021/acsphyschemau.3c00002",
               "doi_6": "doi/10.1016/j.ijhydene.2023.08.189",
               "doi_7": "doi/10.1021/acs.est.3c06557",}
    
    for file, doi in doi_dic.items(): 
        # Getting the json response of the api request
        doi_json_data = get_doi_json_data_from_api(doi, api_config_path)
        
        # Saving the json response in a json file
        doi_path = api_results_path / Path(f'{file}.json')
        with open(doi_path, 'w') as f:
            json.dump(doi_json_data, f, indent = 4)
            
            
def json_parser_demo(data_path = None, api_results_path = None, check_status = False):
    """
    Args:
        check_status (bool): If set to True, parsing results are saved 
                             for comparaison with reference results 
                             in the `build_scopus_df_from_json_files` function
                             (default = False).
    Returns:
        None
    Note:
        The `build_scopus_df_from_json_files` internal function of `demo` module is used.
        The global "API_RESULTS_PATH" is imported from `GLOBALS` module of `ScopusApyJson` package.
    """
    
    # Standard library imports
    import os
    from pathlib import Path
    
    # Globals imports
    from ScopusApyJson.GLOBALS import API_RESULTS_PATH
    
    # Setting results paths
    if not api_results_path: api_results_path = API_RESULTS_PATH   
    
    # Setting the DATA path where demo files are stored
    if not data_path:
        data_path = os.path.join(os.path.dirname(__file__), "DATA")
    
    # Setting the list of json files (results of the api requests using DOIs)
    doi_files_list = []        
    try:
        for file_path in os.listdir(data_path):
            file = os.path.join(data_path, file_path) 
            if os.path.isfile(file) and file.endswith(".json"):
                doi_files_list.append(os.path.splitext(os.path.basename(file))[0])
    except FileNotFoundError:
        print(f"The directory {data_path} does not exist")
    except PermissionError:
        print(f"Permission denied to access the directory {data_path}")
    except OSError as e:
        print(f"An OS error occurred: {e}")
    
    # Getting the scopus df resulting from the json files parsing
    scopus_df = build_scopus_df_from_json_files(doi_files_list, data_path, 
                                                api_results_path, check = check_status)
    
    file_name = "demo_scopus"
    out_file_csv = api_results_path / Path(file_name + ".csv")
    scopus_df.to_csv(out_file_csv,
                     header = True,
                     index = False,
                     sep = ',')
    
    out_file_xlsx = api_results_path / Path(file_name + ".xlsx")
    scopus_df.to_excel(out_file_xlsx, index = False)