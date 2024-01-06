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
           'GLOBAL_KEYS',
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


def _config_ScopusApyJson_key():

    # Standard library imports
    import os.path
    from pathlib import Path

    # 3rd party imports
    import json
    
    # Reads the default api_scopus_config.json config file
    path_config_file = Path(__file__).parent / Path('DATA/scopus_api_keys/api_scopus_config.json')
    date1 = os.path.getmtime(path_config_file)
    with open(path_config_file) as file:
        json_dict = json.load(file)
        
    # Overwrite if a local api_scopus_config.json config file otherwise create it.
         
    local_config_path = get_config_dir() / Path(r'ScopusApyJson/api_scopus_config.json')
    
    if os.path.exists(local_config_path):
        date2 = os.path.getmtime(local_config_path)
        if date2>date1:
            with open(local_config_path) as file:
                json_dict = json.load(file)
        else:
            with open(local_config_path, 'w') as file:
                json.dump(json_dict, file, indent=4)
    else:
        if not os.path.exists(get_config_dir() / Path('ScopusApyJson')):
            os.makedirs(get_config_dir() / Path('ScopusApyJson'))
        with open(local_config_path, 'w') as file:
            json.dump(json_dict, file, indent=4)
       
    return json_dict

GLOBAL_KEYS = _config_ScopusApyJson_key()


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