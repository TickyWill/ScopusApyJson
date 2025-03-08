"""A template of the config json file named "api_scopus_config.json" is stored
in the ".ScopusApyJson/CONFIG" folder. The user's "api_scopus_config.json"
should be located in the user's folder returned by the function `_get_config_dir`
and the user is invited to fill this file with its scopus api authentication keys.

If the user's "api_scopus_config.json" file exits in this user's folder,
it will be used.
Otherwise, a copy of the template file of the ".ScopusApyJson/CONFIG"
folder of the ScopusApyJson package will be automatically created in the user's
folder in order to be filled with the user's scopus api authentication keys.
"""

__all__ = ['API_CONFIG_DICT',
           'API_CONFIG_PATH',
           'ELS_LINK',
           'PARSED_SCOPUS_COLUMNS_NAMES',
           'SELECTED_SCOPUS_COLUMNS_NAMES',
          ]

# Standard library imports
import json
import os.path
import sys
import warnings
from pathlib import Path


# Header of the query for the Scopus API
ELS_LINK = "https://api.elsevier.com/content/abstract/"


# Internal functions to build the Globals
def _get_config_dir():
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    adapted from : ("https://stackoverflow.com/questions/19078969/"
    "python-getting-appdata-folder-in-a-cross-platform-way")
    """
    home = Path.home()

    if sys.platform=='win32':
        app_data_path = home / Path('AppData/Roaming')
    elif sys.platform=='darwin':
        app_data_path = home / Path('Library/Application Support')
    else:
        app_data_path = home / Path('.local/share')
    return app_data_path


def _dump_json(file_path, json_dict):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(json_dict, file, indent=4)


def _check_api_keys(config_path, config_dict):
    dict_apikey = config_dict["apikey"]
    dict_insttoken = config_dict["insttoken"]
    apikey_undef = dict_apikey in  ["PAST_APIKEY_HERE", ""]
    insttoken_undef = dict_insttoken in ["PAST_INSTTOKEN_HERE", ""]
    if apikey_undef or insttoken_undef:
        message = "Authentication keys are not yet defined (required).\n"
        warnings.warn(message)
        config_dict["apikey"] = input(("Enter your authentication key "
                                       "(obtained from http://dev.elsevier.com):"))
        config_dict["insttoken"] = input(("your institution token provided "
                                          "by Elsevier support staff:"))
        _dump_json(config_path, config_dict)
    return config_dict


def _config_saj_dict(json_file_name):
    # Reads the default json_file_name config file
    pck_config_path = Path(__file__).parent / Path('CONFIG') / Path(json_file_name)
    pck_config_date = os.path.getmtime(pck_config_path)
    with open(pck_config_path, encoding="utf-8") as file:
        json_config_dict = json.load(file)

    # Sets the json_config_dict according to the status of the local config file
    local_config_dir_path  = _get_config_dir() / Path('ScopusApyJson')
    local_config_file_path = local_config_dir_path  / Path(json_file_name)

    if os.path.exists(local_config_file_path):
        # Local json_file_name config file exists
        local_config_date = os.path.getmtime(local_config_file_path)
        if local_config_date > pck_config_date:
            # Local config file is more recent than package one
            # thus json_config_dict is defined by the local config file
            with open(local_config_file_path, encoding="utf-8") as file:
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
        if not os.path.exists(_get_config_dir() / Path('ScopusApyJson')):
            os.makedirs(_get_config_dir() / Path('ScopusApyJson'))
        _dump_json(local_config_file_path, json_config_dict)

    return json_config_dict, local_config_file_path

# Getting the authentication key and the institution token
# through the json file 'api_scopus_config.json'
# stored in the folder ".ScopusApyJson/CONFIG"
config_dict, config_path = _config_saj_dict('api_scopus_config.json')
API_CONFIG_DICT = _check_api_keys(config_path, config_dict)
API_CONFIG_PATH = config_path

# Getting the names of the selected scopus columns by the user
# through the json file "scopus_col_names.json"
# stored in the folder ""~/AppData/Roaming/ScopusApyJson" of the user
scopus_column_names_dict, _ = _config_saj_dict('scopus_col_names.json')
PARSED_SCOPUS_COLUMNS_NAMES = list(scopus_column_names_dict.keys())[1:]
SELECTED_SCOPUS_COLUMNS_NAMES = [k for k,v in scopus_column_names_dict.items() if v][1:]
