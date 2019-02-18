#!/lustre/sw/anaconda/anaconda3-5.1.0/bin/python3
"""
#!/usr/bin/python3
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
import Data_group, helpers, Population

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
            if not helpers.compare(sample, output.decode('utf-8')) or process.returncode != 0:
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
    count = 0; MAX_ITER = 21
    while count < MAX_ITER:
        fail_count = 0
        population = Population.create(15, "all")
        for folder in listdir():
            if ( not isfile(folder)):

                print('Entering ', folder)
                chdir(folder)
                with open('sample', 'r') as sample_f:
                    sample = sample_f.read()
                    for i in list(range(0, population.pop_size)):
                        results = []
                        chdir('src')
                        if population.live_pool[i].emit_make():
                            chdir('../..')   # now in coptbenchmark2013 root folder
                            proc_num = 3

                            # Now we run the benchmark in parallel to save time
                            process_folders = [folder + "_" + str(x) for x in
                                               range(0,proc_num)]
                            for proc_folder in process_folders:
                                shutil.copytree(folder, proc_folder)

                            pool = ThreadPool(processes=proc_num)
                            results = pool.starmap(run_bench, zip(process_folders,
                                                              repeat(sample)))
                            pool.close()
                            pool.join()

                            #print('Completed execution for group', i)
                            #print(results)
                            # Clean up folders
                            for proc_folder in process_folders:
                                shutil.rmtree(proc_folder)
                            population.live_pool[i].add_times(results)
                            chdir(folder)
                        else:
                            population.live_pool[i].add_times([10000000])
                            chdir('..')
                            fail_count = fail_count + 1
                            # print("failed")

                chdir('..')

        if (count % 5 == 0):
            s = 0
            for datum in population.live_pool:
                if len(datum.times) != 0:
                    s += datum.times[-1]
            s //= population.pop_size

        population.evaluate()
        population.selection()

        if (count % 5 == 0):
            print('Iteration %d, failed compiles %d, history length %d' % (count, fail_count,len(population.history)))
            print('Population average time: %d' % (s))

        count = count + 1

    population.write_to_file('../results/gcc/')

    print('program completed')


main()
