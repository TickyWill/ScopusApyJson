"""
config.py docs
A custom config json is stored in the two  following directories:
      ~/AppData/Roaming/api_scopus_config.json  and  contains user api scopus keys
      .ScopusApyJson/api_scopus_config.json   contain the default setting 
If the user's api_scopus_config.json configuration file exits it  will be used. Otherwise a user's configuration file Pvcharacterization.yaml 
will be created in the user's ~/AppData/Roaming.
The modification of the config variables will be stored in the Pvcharacterization.yaml stor in the user's WORRKING_DIR folder.

"""

__all__ = ['API_CONFIG_DICT',
           'API_CONFIG_PATH',
           'API_RESULTS_PATH',
           'PARSED_SCOPUS_COLUMNS_NAMES',
           'SELECTED_SCOPUS_COLUMNS_NAMES',
          ]


def get_config_dir():

    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    adapted from : https://stackoverflow.com/questions/19078969/python-getting-appdata-folder-in-a-cross-platform-way
    """
    # Standard library imports
    import sys
    from pathlib import Path
    
    home = Path.home()

    if sys.platform == 'win32':
        return home / Path('AppData/Roaming')
    elif sys.platform == 'linux':
        return home / Path('.local/share')
    elif sys.platform == 'darwin':
        return home / Path('Library/Application Support')

def _dump_json(file_path, json_dict):
    # Standard library imports
    import json
    
    with open(file_path, 'w') as file:
        json.dump(json_dict, file, indent=4)
    
def _check_api_keys(API_CONFIG_DICT):
    # Standard library imports
    import warnings
      
    dict_apikey    = API_CONFIG_DICT["apikey"]
    dict_insttoken = API_CONFIG_DICT["insttoken"]
    if (dict_apikey ==  "PAST_APIKEY_HERE") or (dict_insttoken == "PAST_INSTTOKEN_HERE"):
        message  = "Authentication keys are not yet defined (required).\n"
        warnings.warn(message)
        API_CONFIG_DICT["apikey"]    = input("Enter your authentication key (obtained from http://dev.elsevier.com):")
        API_CONFIG_DICT["insttoken"] = input("your institution token provided by Elsevier support staff:")
        _dump_json(API_CONFIG_PATH, API_CONFIG_DICT)     

def _config_ScopusApyJson_key(json_file_name):
    # Standard library imports
    import json
    import os.path
    from pathlib import Path
    
    # Reads the default json_file_name config file
    pck_config_path = Path(__file__).parent / Path('CONFIG') / Path(json_file_name)
    pck_config_date = os.path.getmtime(pck_config_path)
    with open(pck_config_path) as file:
        json_config_dict = json.load(file)
        
    # Sets the json_config_dict according to the status of the local config file        
    local_config_dir_path  = get_config_dir() / Path('ScopusApyJson')
    local_config_file_path = local_config_dir_path  / Path(json_file_name)
    
    if os.path.exists(local_config_file_path):
        # Local json_file_name config file exists
        local_config_date = os.path.getmtime(local_config_file_path)
        if local_config_date > pck_config_date:
            # Local config file is more recent than package one
            # thus json_config_dict is defined by the local config file
            with open(local_config_file_path) as file:
                json_config_dict = json.load(file)
        else:
            # Local config file is less recent than package one
            # thus package config file overwrite the local config file 
            # and json_config_dict is kept at default values
            _dump_json(local_config_file_path, json_config_dict)
    else:
        # Local json_file_name config file does not exist
        # thus package config file is used to create a local config file
        # to be filled by the user
        # and json_config_dict is kept at default values
        if not os.path.exists(get_config_dir() / Path('ScopusApyJson')):
            os.makedirs(get_config_dir() / Path('ScopusApyJson'))
        _dump_json(local_config_file_path, json_config_dict)      
    
    return json_config_dict, local_config_file_path


API_CONFIG_DICT, API_CONFIG_PATH = _config_ScopusApyJson_key('api_scopus_config.json')
_check_api_keys(API_CONFIG_DICT)

scopus_column_names_dict, _   = _config_ScopusApyJson_key('scopus_col_names.json')

PARSED_SCOPUS_COLUMNS_NAMES   = list(scopus_column_names_dict.keys())

SELECTED_SCOPUS_COLUMNS_NAMES = [k for k,v in scopus_column_names_dict.items() if v] 

# To be removed
# API_RESULTS_PATH example for windows: API_RESULTS_PATH = r"C:\Users\<my_user_id>\<my_api_scopus_folder>")
API_RESULTS_PATH = "path/to/results_directory"
#API_RESULTS_PATH = r"C:\Users\AC265100\Documents\BiblioMeter_App\Scopus_api_test"

# List of all columns that can be extracted from the results of a query on the scopus website
# This list is only informative to user 
FULL_SCOPUS_COLUMNS_NAMES = ["Authors","Author full names","Author(s) ID","Title","Year",
                             "Source title","Volume","Issue","Art. No.","Page start","Page end",
                             "Page count","Cited by","DOI","Link","Affiliations","Authors with affiliations","Abstract",
                             "Author Keywords","Index Keywords","Molecular Sequence Numbers","Chemicals/CAS",
                             "Tradenames","Manufacturers","Funding Details","Funding Texts",
                             "References","Correspondence Address","Editors","Publisher","Sponsors",
                             "Conference name","Conference date","Conference location","Conference code",
                             "ISSN","ISBN","CODEN","PubMed ID","Language of Original Document",
                             "Abbreviated Source Title","Document Type","Publication Stage","Open Access","Source","EID",]

# List of columns among 'FULL_SCOPUS_COLUMNS_NAMES' columns list that are not parsed in the 'json_parser' module 
# This list is only informative to user 
UNPARSED_SCOPUS_COLUMNS_NAMES = ["Molecular Sequence Numbers","Chemicals/CAS","Tradenames","Manufacturers",
                                "Funding Details","Funding Texts","Sponsors",]

# List of columns among the 'FULL_SCOPUS_COLUMNS_NAMES' list that are parsed in the 'json_parser' module 
#PARSED_SCOPUS_COLUMNS_NAMES = ["Authors","Author full names","Author(s) ID","Title","Year",
#                               "Source title","Volume","Issue","Art. No.","Page start","Page end",
#                               "Page count","Cited by","DOI","Link","Affiliations","Authors with affiliations","Abstract",
#                               "Author Keywords","Index Keywords","References","Correspondence Address","Editors","Publisher",
#                               "Conference name","Conference date","Conference location","Conference code",
#                               "ISSN","ISBN","CODEN","PubMed ID","Language of Original Document",
#                               "Abbreviated Source Title","Document Type","Publication Stage","Open Access","Source","EID",]
