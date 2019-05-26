import argparse
import os.path


def is_valid_file(parser, arg):
    if os.path.exists(arg):
        parser.error("The file %s is exist!" % arg)
    else:
        return arg


parser = argparse.ArgumentParser(description='Grep on python')
parser.add_argument('file_path',
                    help='path to file, where you wanna search to',
                    metavar="FILE", type=lambda x: is_valid_file(parser, x))

args = parser.parse_args()

with open(args.file_path, "w") as file_to_write:
    while os.path.getsize(args.file_path) < 1000000000:
        file_to_write.write("some something on some somewhere\nSomewhere not here though\nsome other thing around\n")
    file_to_write.write("Expression that i search")

print(os.path.getsize(args.file_path))
