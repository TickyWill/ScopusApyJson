def cli_doi():

    # Standard library imports
    from argparse import ArgumentParser, Namespace
    from pathlib  import Path  
    
    # 3rd party imports
    import pandas as pd
    
    # Local library imports
    import ScopusApyJson as saj
    from ScopusApyJson.demo import build_scopus_df_from_api    
    
    parser = ArgumentParser()
    parser.usage = '''Usage cli_doi -d <doi1 doi2 ...>  -o <results folder path>
    1- Get the json data through scopus api request for each DOI of a list of DOIs. 
    2- Saves the results in a csv file in the folder <results folder path> (default: your homedir).
    '''
    
    parser.add_argument('-d',
                        '--doi',
                        help='doi to parse',
                        type=str,
                        nargs='+',
                        required=True)

    parser.add_argument('-o', '--output',
                        nargs='?', 
                        help='output path for the results')
    
    args : Namespace = parser.parse_args()
    
    if args.output is None:
        out_path = Path.home()
        print(f'Default output directory : {out_path}')
    else:
        out_path = args.output
        print(f'Option and command-line argument given: "-o {out_path}"')
    
    doi_list = args.doi
    api_scopus_df = build_scopus_df_from_api(doi_list)
    output_file = out_path / Path('scopus_result.csv')
    api_scopus_df.to_csv(output_file,
                         header = True,
                         index = False,
                         sep = ',')
    print(f"The results have been saved in the file: {output_file}")
    

def cli_json():    
    from argparse import ArgumentParser, Namespace

    parser = ArgumentParser()
    parser.add_argument('file',help='json file to parse', type=str)
    args : Namespace = parser.parse_args()
    print(args.file)
    
