#!/lustre/sw/anaconda/anaconda3-5.1.0/bin/python3

"""
This script compiles a benchmarks, with -O3. After
compiling each benchmark, they are ran in parallel
to save time.
"""

from multiprocessing import Pool as ThreadPool
from os import chdir, listdir, system
from os.path import isfile
import subprocess, time
from supbrocess import Popen, PIPE, STDOUT, TimeoutExpired
import Data_group

def run_bench():
    system('chmod +x run.sh')
    start_time = time.time()
    with Popen(benchrun, shell=True, stderr=STDOUT, stdout=PIPE,
               preexec_fn=os.setsid) as process:
        try:
            output = process.communicate(timeout=600)[0]
            end_time = time.time()
        except TimeoutExpired:
            os.killpg(process.pid, signal.SIGINT)
            output = process.communicate()[0]
            end_time = time.time()

    ellapsed_time = int( (end_time-start_time)*1000)
    res_str = res.stdout.decode('utf-8')
    return ellapsed_time

def main():

    chdir('../coptbenchmarks2013')
    for folder in listdir():
        if ( not isfile(folder)):

            print('Entering ', folder)
            chdir(folder)
            flags = [{'-O0':True},{'-O1':True},{'-O2':True},{'-O3':True}]
            dg = Data_group.make_data_group(folder)

            for flag in flags:
                dg.set_flags(flag)
                results = None

                chdir('src')
                print('Compiling...')
                if dg.emit_make():
                    chdir('..')

                    # Now we must run the benchmark, in parallel to save time

                    pool = ThreadPool(processes=10)

                    results = pool.map(run_bench)
                    pool.close()
                    pool.join()

                    print('Completed execution for ', flag)
                    dg.add_times(results)
                    dg.save()
                else:
                    chdir('..')
            dg.write_to_file('../results/gcc/')

    print('Done')


main()
