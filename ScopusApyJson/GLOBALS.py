"""
config.py docs
A custom config json is stored in the two  following directories:
      ~/AppData/Roaming/api_scopus_config.json  and  contains user api scopus keys
      .ScopusApyJson/api_scopus_config.json   contain the default setting 
If the user's api_scopus_config.json configuration file exits it  will be used. Otherwise a user's configuration file Pvcharacterization.yaml 
will be created in the user's ~/AppData/Roaming.
The modification of the config variables will be stored in the Pvcharacterization.yaml stor in the user's WORRKING_DIR folder.

"""

__all__ = ['API_CONFIG_PATH',
           'API_RESULTS_PATH',
           'API_KEYS_DICT',
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

def _check_api_keys(json_config_dict):
    status = True   
    dict_apikey    = json_config_dict["apikey"]
    dict_insttoken = json_config_dict["insttoken"]
    if (dict_apikey ==  "PAST_APIKEY_HERE") or (dict_insttoken == "PAST_INSTTOKEN_HERE"):
        status = False
    return status        

def _config_ScopusApyJson_key():

    # Standard library imports
    import json
    import os.path
    from pathlib import Path
    
    # Reads the default api_scopus_config.json config file
    pck_config_path = Path(__file__).parent / Path('DATA/scopus_api_keys/api_scopus_config.json')
    pck_config_date = os.path.getmtime(pck_config_path)
    with open(pck_config_path) as file:
        json_config_dict = json.load(file)
        
    # Sets the json_config_dict according to the status of the local config file        
    local_config_dir_path = get_config_dir() / Path('ScopusApyJson')
    local_config_file_path = local_config_dir_path  / Path('api_scopus_config.json')
    
    if os.path.exists(local_config_file_path):
        # Local api_scopus_config.json config file exists
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
            with open(local_config_file_path, 'w') as file:
                json.dump(json_config_dict, file, indent=4)
    else:
        # Local api_scopus_config.json config file does not exist
        # thus package config file is used to create a local config file
        # to be filled by the user
        # and json_config_dict is kept at default values
        if not os.path.exists(get_config_dir() / Path('ScopusApyJson')):
            os.makedirs(get_config_dir() / Path('ScopusApyJson'))
        with open(local_config_file_path, 'w') as file:
            json.dump(json_config_dict, file, indent=4)
    
    api_keys_status = _check_api_keys(json_config_dict)
    if not  api_keys_status:
        message  = f"Api keys not yet defined."
        message += f"Please fill the config file:"
        message += f"{local_config_file_path}"
        raise ValueError(message)       
    
    return json_config_dict

API_KEYS_DICT = _config_ScopusApyJson_key()


# Paths to be set by user 
    # API_CONFIG_PATH example for windows: API_CONFIG_PATH = r"C:\Users\<my_user_id>\<my_config_folder>\api_scopus_config.json")
API_CONFIG_PATH = "path/to/api_scopus_config.json"
#API_CONFIG_PATH = r"C:\Users\AC265100\Documents\BiblioMeter_App\Scopus_api_test\api_scopus_config.json"
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


# List of columns among the 'FULL_SCOPUS_COLUMNS_NAMES' list that are parsed in the 'json_parser' module 
PARSED_SCOPUS_COLUMNS_NAMES = ["Authors","Author full names","Author(s) ID","Title","Year",
                               "Source title","Volume","Issue","Art. No.","Page start","Page end",
                               "Page count","Cited by","DOI","Link","Affiliations","Authors with affiliations","Abstract",
                               "Author Keywords","Index Keywords","References","Correspondence Address","Editors","Publisher",
                               "Conference name","Conference date","Conference location","Conference code",
                               "ISSN","ISBN","CODEN","PubMed ID","Language of Original Document",
                               "Abbreviated Source Title","Document Type","Publication Stage","Open Access","Source","EID",]


# List of scopus columns to be kept among the 'PARSED_SCOPUS_COLUMNS_NAMES' list in the final dataframe 
# This list has to be set by the user
SELECTED_SCOPUS_COLUMNS_NAMES = ["Authors","Author full names","Author(s) ID","Title","Year",
                                 "Source title","Volume","Issue","Art. No.","Page start","Page end",
                                 "Page count","Cited by","DOI","Link","Affiliations","Authors with affiliations",
                                 "Author Keywords","Index Keywords","References","Correspondence Address",
                                 "Editors","Publisher","ISSN","ISBN","CODEN","PubMed ID","Language of Original Document",
                                 "Abbreviated Source Title","Document Type","Publication Stage","Open Access","Source","EID",]


# List of columns among 'FULL_SCOPUS_COLUMNS_NAMES' columns list that are not parsed in the 'json_parser' module 
# This list is only informative to user 
UNPARSED_SCOPUS_COLUMNS_NAMES = ["Molecular Sequence Numbers","Chemicals/CAS","Tradenames","Manufacturers",
                                "Funding Details","Funding Texts","Sponsors",]