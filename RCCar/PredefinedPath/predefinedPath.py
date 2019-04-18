import numpy as np
import matplotlib as plt
import sys
import argparse

from createPath import cone_generation
import loadPath

def parse_file_name(file_name):
    f,b='',''
    if not file_name.endswith('.csv'):
        b = '.csv'
    elif not file_name.startswith('data/'):
        f = 'data/'

    path = f + file_name + b
    try:
        open(path, 'w')
        return path
    except:
        print('Illegal file name.')


    path = 'data/'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create path for RCCar.')
    parser.add_argument('-u', action='store_true',help='generate a user defined path')
    parser.add_argument('-f',action='store', nargs=1, help='open specific path file')
    args, rem_args= parser.parse_known_args()
    if args.f and args.u:
        parser.error('Use -n to name a file. -f loads a file already present.')
    elif args.u:
        parser.add_argument('-n',action='store_true', help='name the generated file (default: test_data.csv)')
        args = parser.parse_args(rem_args)
        if args.n:
            file_name = parse_file_name(args.n)
        else:
            file_name = 'data/test_data.csv'
        cone_generation(file_name)
    elif args.f:
        print(args)
        load_data(args)
    # if args.n and not args.u:
    #     parser.error('-n requires -u')
    # if args.u:
    #    cone_generation() 
    # try:
    #     if sys.argv[1] == '-u':
    #         cone_generation()
    #     elif sys.argv[1] == '-f':
    #         try:
    #             file_name = sys.argv[2]
    #         except:
    #             print('-f options used. Please input file name.\nUse -h for help.')
    #     elif sys.argv[1] == '-h':
    #         print('Options:\n\t-u: Specify a new path\n\t-f: Specify file name of path\n\t-h: Get help')
    # except:
    #     pass
    #
    # if file_name
    #
    # path = loadPath(file_name)
