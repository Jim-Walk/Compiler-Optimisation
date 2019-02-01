#!/lustre/sw/anaconda/anaconda3-5.1.0/bin/python3

"""
This class is responsible for running the benchmark,
and checking its output
"""


import os, signal

from subprocess import Popen, PIPE, TimeoutExpired, STDOUT


class Runner():
    sample = ""
    bench = ""

    def check_correctness(output):
        with open('sample', 'r') as f:
             boolean = levin-dist(f.read(), output)
        return boolean

    def gen_sample(bench):
        os.chdir(bench)
        with Popen('./run.sh', shell=True, stderr=STDOUT, stdout=PIPE,
                   preexec_fn=os.setsid) as process:
            try:
                output = process.communicate(timeout=600)[0]
            except TimeoutExpired:
                os.killpg(process.pid, signal.SIGINT)
                output = process.communicate()[0]

        check_correctness(output.decode('utf-8'))

        os.chdir('..')
        sample = bench + '/sample'
        with open(sample, 'w+') as f:
            f.write(output.decode('utf-8'))

