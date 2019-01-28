#!/lustre/sw/anaconda/anaconda3-5.1.0/bin/python3

"""  icc-gen.py
This script compiles a benchmarks, with -O3. After
compiling each benchmark, they are ran in parallel
to save time. Output is stored in 10 .dat files
"""

from multiprocessing import Pool as ThreadPool
from os import chdir, listdir, system
from os.path import isfile

def run_bench(cmd):
    system('chmod +x run.sh')
    exec_string = '(time ./run.sh) &> ' + str(cmd) + '.dat'
    system(exec_string)
    return cmd

def edit_make(f):
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    for line in lines:
        if "gcc" in line and "#" not in line:
            f.write('CC=icc\n')
        elif '-O0' in line:
            nl = ""
            for char in line:
                if char == '0':
                    nl = nl + '3'
                else:
                    nl = nl + char
            f.write(nl)

        else:
            f.write(line)

def main():

    chdir('../coptbenchmarks2013')
    my_array = list(range(1,11))
    for folder in listdir():
        if ( not isfile(folder)):
            print('Entering ', folder)
            chdir(folder + "/src")
            with open('Makefile', 'r+') as Makefile:
                edit_make(Makefile)

            print('Compiling...')
            system('make')
            chdir('..')

            # Now we must run the benchmark, in parallel to save time

            pool = ThreadPool(processes=10)

            results = pool.map(run_bench, my_array)
            pool.close()
            pool.join()

            print('Completed execution for ', folder)
            print(results)
            results = []
            chdir('..')


    print('Done')


main()
