import os.path
import time
import multiprocessing as mp
import re


class FileMultiproc():

    def __init__(self, args, regular_expression):

        self.re_object = regular_expression

        self.file_path = args.file_path

        self.is_exclude_search = args.is_exclude_search

    def process_file(self):
        start_of_search = time.time()

        # init objects
        cores = mp.cpu_count()
        pool = mp.Pool(cores)
        jobs = []

        # create jobs
        for chunkStart, chunkSize in self.chunkify():
            jobs.append(
                pool.apply_async(self.process_wrapper, (chunkStart, chunkSize)))

        # wait for all jobs to finish
        for job in jobs:
            job.get()

        end_of_search = time.time()

        print('Time wasted ', end_of_search - start_of_search)

        # clean up
        pool.close()

    def process_wrapper(self, chunk_start, chunk_size):
        with open(self.file_path) as f:
            f.seek(chunk_start)
            for line in f.read(chunk_size).splitlines():
                if not self.is_exclude_search and self.re_object.search(line):
                    print('\033[1m' + re.sub('[\t\n\r\f\v]', '', line))
                elif self.is_exclude_search and not self.re_object.search(line):
                    print('\033[1m' + re.sub('[\t\n\r\f\v]', '', line))

    def chunkify(self, size=1024*1024):
        file_end = os.path.getsize(self.file_path)
        with open(self.file_path, 'r') as f:
            chunk_end = f.tell()
            while True:
                chunk_start = chunk_end
                f.seek(f.tell() + size, 0)
                f.readline()
                chunk_end = f.tell()
                yield chunk_start, chunk_end - chunk_start
                if chunk_end > file_end:
                    break
