__all__ = ['API_CONFIG_PATH',
           'API_RESULTS_PATH',
           'PARSED_SCOPUS_COLUMNS_NAMES',
           'SELECTED_SCOPUS_COLUMNS_NAMES',
          ]

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