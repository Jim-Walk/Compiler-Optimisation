#!/lustre/sw/anaconda/anaconda3-5.1.0/bin/python3

"""
This script compiles a benchmarks, with -O3. After
compiling each benchmark, they are ran in parallel
to save time. Output is stored in 10 .dat files
"""

from multiprocessing import Pool as ThreadPool
from os import chdir, listdir, system
from os.path import isfile
import subprocess
import grab

def run_bench(cmd):
    system('chmod +x run.sh')
    res = subprocess.run(['time', './run.sh'], stderr=subprocess.STDOUT,
                         stdout=subprocess.PIPE)
    res_str = res.stdout.decode('utf-8')
    ans = res_str.split('\n')[-3].strip()
    ans = ans.split()[0]
    return grab.parse_time(ans)

def main():

    chdir('../coptbenchmarks2013')
    my_array = list(range(1,11))
    for folder in listdir():
        if ( not isfile(folder)):

            flags = [{'-O0':True},{'-O1':True},{'-O2':True},{'-O3':True}]
            dg = make_data_group(folder)

            for flag in flags:
                dg.set_flags(flag)
                print('Entering ', folder)
                chdir(folder + "/src")

                print('Compiling...')
                dg.emit_make()
                chdir('..')

                # Now we must run the benchmark, in parallel to save time

                pool = ThreadPool(processes=10)

                results = pool.map(run_bench, my_array)
                pool.close()
                pool.join()

                print('Completed execution for ', folder)
                dg.add_times(results)
                dg.save()
                results = []
                chdir('..')

        dg.write_to_file()


    print('Done')


main()
