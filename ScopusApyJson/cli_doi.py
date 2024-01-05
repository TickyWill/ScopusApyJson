def cli_doi():

    # Standard library import
    from argparse import ArgumentParser, Namespace
    from pathlib  import Path  
    
    #Internal import
    from   ScopusApyJson.api_manager import get_doi_json_data_from_api
    
    parser = ArgumentParser()
    parser.usage = '''usage cli_doi doi -k <api-key-pass>
    from a doi get the json article from scopus api
    and buils acsv file in your homedir.
    your api keys must be store in a json file locate at -k <api-key-path
    otherwise the default value is your homedir '''
    parser.add_argument('doi',help='doi to parse', type=str)
    parser.add_argument('-k', '--keyfile', nargs='?', const='arg_was_not_given', help='api keys file, in JSON format')

    args : Namespace = parser.parse_args()

    if args.keyfile is None:
        api_config_path = Path.home()
        print(f'Default api_key_path is set to : {api_config_path}')
    elif args.keyfile == 'arg_was_not_given':
        print('Option given, but no command-line argument: "-k"')
    else:
        api_config_path = args.keyfile
        print(f'Option and command-line argument given: "-k {api_config_path}"')
    
    
    print(args.doi)
    
    #api_json_data = get_doi_json_data_from_api(args.doi, api_config_path)
    
if __name__=='__main__':
   cli_doi()