def cli_doi():

    # Standard library import
    from argparse import ArgumentParser, Namespace
    from pathlib  import Path  
    
    # Third party imports
    import pandas as pd
    
    # Internal import
    from   ScopusApyJson.demo import build_scopus_df_from_api
    
    parser = ArgumentParser()
    parser.usage = '''usage cli_doi doi -k <api-key-pass>
    from a doi get the json article from scopus api
    and buils acsv file in your homedir.
    your api keys must be store in a json file locate at -k <api-key-path
    otherwise the default value is your homedir '''
    #parser.add_argument('doi',help='doi to parse', type=str)
    parser.add_argument('-d',
                        '--doi',
                        help='doi to parse',
                        type=str,
                        nargs='+',
                        required=True)
    parser.add_argument('-k', '--keyfile',
                        nargs='?', 
                        help='api keys file, in JSON format')
    parser.add_argument('-o', '--output',
                        nargs='?', 
                        help='output path for the results')
    args : Namespace = parser.parse_args()

    if args.keyfile is None:
        api_config_path = Path.home()
        print(f'Default api_key_path is set to : {api_config_path}')
    else:
        api_config_path = args.keyfile
        print(f'Option and command-line argument given: "-k {api_config_path}"')
    
    if args.output is None:
        out_path = Path.home()
        print(f'Default output directory : {out_path}')
    else:
        out_path = args.output
        print(f'Option and command-line argument given: "-o {out_path}"')
    
    for doi in args.doi:
        print(doi)
    
        
        
    #api_scopus_df = build_scopus_df_from_api(api_config_path, api_doi_list)
    #output_file = out_path / Path('scopus_result.csv')
    #api_scopus_df.to_csv()
    

def cli_json():    
    from argparse import ArgumentParser, Namespace

    parser = ArgumentParser()
    parser.add_argument('file',help='json file to parse', type=str)
    args : Namespace = parser.parse_args()
    print(args.file)
    
