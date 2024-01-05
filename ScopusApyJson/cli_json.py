def cli_json():    
    from argparse import ArgumentParser, Namespace

    parser = ArgumentParser()
    parser.add_argument('file',help='json file to parse', type=str)
    args : Namespace = parser.parse_args()
    print(args.file)
    
if __name__=='__main__':
   cli_json()