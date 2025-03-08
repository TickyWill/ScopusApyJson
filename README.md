# ScopusApyJson
## Description
Python modules for parsing the response to a request through [Scopus Api](https://api.elsevier.com/content/abstract/) based on DOI.

## Installation
Run the following to install:
```python
pip install ScopusApyJson
```

## Usage example
```python
import ScopusApyJson as saj

doi_list = ["doi/10.1016/j.fuproc.2022.107223",
            "doi/10.1109/pvsc48317.2022.9938766"]
scopus_tup = saj.build_scopus_df_from_api(doi_list, timeout = 20, verbose = True)
authy_status = scopus_tup[2]
if authy_status: 
    scopus_df = scopus_tup[0]
    scopus_df.to_excel(<your_fullpath_file1> + ".xlsx", index = False)
    failed_doi_df = scopus_tup[1]
    failed_doi_df.to_excel(<your_fullpath_file2> + ".xlsx", index = False)
else:
    print("Authentication failed: please check availability of authentication keys")
```
**for more exemples refer to** [ScopusApyJson-exemples](https://github.com/TickyWill/ScopusApyJson/Demo_ScopusApyJson.ipynb).


# Release History
- 1.0.0 first release
- 1.1.0 check of fields availability when parsing the request response
- 1.1.1 updated args of build_scopus_df_from_api function
- 1.1.2 Enhanced robusteness of code after pylint scan
- 1.1.3 Updated release history
- 1.1.4 Align release history on PyPi


# Meta
	- authors : BiblioAnalysis team

Distributed under the [MIT license](https://mit-license.org/)
