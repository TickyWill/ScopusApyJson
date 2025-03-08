#!/usr/bin/env python

# Standard library imports
from os import path
from setuptools import setup, find_packages

# Reading the content of the "README.md" file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Reading the content of the "requirements.txt" file
with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().strip().split('\n')

# Setting the setup parameters
setup(name = 'ScopusApyJson',
      version = '1.1.3',
      description = 'Python modules for parsing the response to a Scopus API request',
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      include_package_data = True,
      license = 'MIT',
      classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research'
        ],
      keywords = 'Metadata parsing, Scopus request, API management',
      install_requires = install_requires,
      entry_points = {
        'console_scripts': [
                            'cli_doi = ScopusApyJson.CLI.cli:cli_doi',
                            'cli_json = ScopusApyJson.CLI.cli:cli_json'
                            ],
         },
      author = 'BiblioAnalysis team',
      author_email = 'francois.bertin7@wanadoo.fr, amal.chabli@orange.fr',
      url = 'https://github.com/TickyWill/ScopusApyJson',
      packages = find_packages(),
      )
