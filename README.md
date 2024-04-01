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

doi_list = ["doi/10.1016/j.fuproc.2022.107223",]
scopus_df = saj.build_scopus_df_from_api(doi_list)
scopus_df.to_excel(<your_fullpath_file.xlsx), index = False)
```
**for more exemples refer to** [ScopusApyJson-exemples](https://github.com/TickyWill/ScopusApyJson/Demo_ScopusApyJson.ipynb).


# Release History
- 1.0.0 first release
- 1.1.0 check of fields availability when parsing the request response


# Meta
	- authors : BiblioAnalysis team

Distributed under the [MIT license](https://mit-license.org/)
