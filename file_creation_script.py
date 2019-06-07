import argparse
import os.path
import time
import multiprocessing as mp


def multiproc_writing(file, steps_count):
    start_of_search = time.time()

    # init objects
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    jobs = []

    for i in range(1, cores):
        jobs.append(pool.apply_async(process_writning, (i,)))

    # wait for all jobs to finish
    for job in jobs:
        job.get()

    end_of_search = time.time()

    print('Time wasted ', end_of_search - start_of_search)


def process_writning(i: int):
    while os.path.getsize(args.file_path) < 500000000*i:
        file_to_write.write("some something on some somewhere\nSomewhere not here though\nsome other thing around\n")
    file_to_write.write("Expression that i search")


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
    multiproc_writing(file_to_write, 4)

print(os.path.getsize(args.file_path))
