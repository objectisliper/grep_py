import argparse
import re
import os.path
from file_multiprocessing import FileMultiproc


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg  # return an open file handle


parser = argparse.ArgumentParser(description='Grep on python')
parser.add_argument('-v', action='store_true',
                    dest='is_exclude_search',
                    help='Search every substring, exclude write one')
parser.add_argument('search_string',
                    help='an string that you search for')

parser.add_argument('file_path',
                    help='path to file, where you wanna search to',
                    metavar="FILE", type=lambda x: is_valid_file(parser, x))

args = parser.parse_args()

regular_expression_object = re.compile(args.search_string)

FileMultiproc(args, regular_expression_object).process_file()

