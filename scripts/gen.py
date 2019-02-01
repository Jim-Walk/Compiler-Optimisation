#!/usr/bin/python3

"""
#!/lustre/sw/anaconda/anaconda3-5.1.0/bin/python3
This script compiles a benchmarks, with -O3. After
compiling each benchmark, they are ran in parallel
to save time.
"""

from multiprocessing import Pool as ThreadPool
from os import chdir, listdir, system
from os.path import isfile
import shutil, os
import subprocess, time
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from itertools import repeat
import Data_group, helpers

# Run the bench mark in process's folder
# check that it matches well enough
def run_bench(folder, sample):
    chdir(folder)
    run_err = False
    start_time = time.time()
    with Popen('./run.sh', shell=True, stderr=STDOUT, stdout=PIPE,
               preexec_fn=os.setsid) as process:
        try:
            output = process.communicate(timeout=600)[0]
            end_time = time.time()
            if not helpers.compare(sample, output.decode('utf-8')):
                run_err = True
        except TimeoutExpired:
            os.killpg(process.pid, signal.SIGINT)
            output = process.communicate()[0]
            end_time = time.time()
            run_err = True

    ellapsed_time = int( (end_time-start_time)*1000)
    if run_err:
        ellapsed_time *= 1000

    chdir('..')
    return ellapsed_time

def main():

    chdir('../coptbenchmarks2013')
    for folder in listdir():
        if ( not isfile(folder)):

            print('Entering ', folder)
            chdir(folder)
            with open('sample', 'r') as sample_f:
                sample = sample_f.read()
                #flags = [{'-O0':True},{'-O1':True},{'-O2':True},{'-O3':True}]
                flags = [{'-O3':True}]
                dg = Data_group.make_data_group(folder)

                for flag in flags:
                    dg.set_flags(flag)
                    results = None

                    chdir('src')
                    print('Compiling...')
                    if dg.emit_make():
                        chdir('../..')   # now in coptbenchmark2013 root folder
                        process_folders = [folder + "_" + str(x) for x in
                                           range(0,10)]
                        for proc_folder in process_folders:
                            shutil.copytree(folder, proc_folder)

                        # Now we must run the benchmark, in parallel to save time

                        pool = ThreadPool(processes=10)

                        results = pool.starmap(run_bench, zip(process_folders,
                                                          repeat(sample)))
                        pool.close()
                        pool.join()

                        print('Completed execution for ', flag)
                        print(results)
                        # Clean up folders
                        for proc_folder in process_folders:
                            shutil.rmtree(proc_folder)
                        dg.add_times(results)
                        dg.save()
                        chdir(folder)
                    else:
                        chdir('..')
                chdir('..')
                dg.write_to_file('../results/gcc/')
                break

        print('Done')


main()
