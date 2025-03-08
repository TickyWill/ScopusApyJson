"""Functions for building Scopus data through the API based on DOI."""

__all__ = ['build_scopus_df_from_api',]

# 3rd party imports
import pandas as pd

# Local imports
import ScopusApyJson.saj_globals as saj_g
from ScopusApyJson.api_manager import get_doi_json_data_from_api
from ScopusApyJson.json_parser import parse_json_data_to_scopus_df


def build_scopus_df_from_api(doi_list, timeout = None, verbose = False):
    """The function `build_scopus_df_from_api` gets, for each of the DOI 
    in the DOI list "doi_list", the hierarchical dict of the data returned by 
    the function `get_doi_json_data_from_api`.

    Then, it builts the dataframes resulting from the hierarchical dicts parsing 
    using the function `parse_json_data_to_scopus_df`. 
    Finally, it concatenates these dataframe to a single dataframe.

    Args:
        doi_list (list): The list of DOI (str) for the Scopus API request.
        timeout (int): The maximum waiting time in seconds for request answer.
    Returns:
        ((pandas.core.frame.DataFrame, pandas.core.frame.DataFrame, bool)): Tuple where first term \
        is the concatenation of the dataframes resulting from the hierarchical dicts parsing \
        for each DOI of the list "doi_list", second term is the dataframe giving the failed DOIs \
        with the reasons of their fail and third term is equal to False if the authentication \
        to the scopus database failed.
    """
    if not isinstance(doi_list, list):
        doi_list = [doi_list]
    scopus_df_list = []
    failed_num = 0
    authy_status = False
    failed_doi_df = pd.DataFrame(columns = ["DOI","Fail reason"])
    api_scopus_df = pd.DataFrame(columns = saj_g.SELECTED_SCOPUS_COLUMNS_NAMES)
    for _, doi in enumerate(doi_list):
        api_json_data, request_status = get_doi_json_data_from_api(doi, timeout = timeout)
        if request_status == "False":
            authy_status = False
            if verbose:
                print(('Authentication failed: please check availability'
                       ' of authentication keys'))
            break
        authy_status = True
        if request_status == "Empty":
            if verbose:
                print(f'DOI {doi} not found in Scopus database')
            failed_doi_df.loc[failed_num, "DOI"] = doi
            failed_doi_df.loc[failed_num, "Fail reason"] = "Not found"
            failed_num += 1
        elif request_status == "Timeout":
            if verbose:
                print('Request timeout: please check web access')
            failed_doi_df.loc[failed_num, "DOI"] = doi
            failed_doi_df.loc[failed_num, "Fail reason"] = "Timeout"
            failed_num += 1
        else:
            if verbose:
                print(f'Request successful for DOI {doi}')
            scopus_df = parse_json_data_to_scopus_df(api_json_data)
            scopus_df_list.append(scopus_df)
            api_scopus_df = pd.concat(scopus_df_list, axis = 0)

    return api_scopus_df, failed_doi_df, authy_status
