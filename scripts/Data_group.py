import os
import sys
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

class Data_group():
    # A list of all ten times, the 11th
    # value is the average
    times = []
    # Dictionary of all flags, flags which are on are set to true
    flags = {}
    # history contains dictionary record of active flags and their runtimes
    history = {}
    bench = ""

    def __init__(self, benchmark):
        self.bench = benchmark

    # save most recent runtime to history, append
    # average non zero value to end of list
    def save(self):
        avg = sum(self.times)//len(self.times)
        self.history[self.get_flags()] = self.times + [avg]

    # Return a string of all activated flags
    def get_flags(self):
        flg_str = ""
        for flag in self.flags:
            if self.flags[flag]:
                flg_str += flag
        return flg_str

    def add_times(self, res):
        self.times = res

    def write_to_file(self, path):
        fpath = path + self.bench
        with open(fpath, 'w+') as f:
            f.write(self.bench)
            f.write('\n')
            for flg in self.history:
                w_str = flg + ' ' + str(self.history[flg])
                f.write(w_str)
                f.write('\n')

    def emit_make(self):
        make_cmd = 'make CC=gcc CFLAGS=' + self.get_flags()
        self.emit_clean()
        with Popen('./run.sh', shell=True, stderr=STDOUT, stdout=PIPE,
                   preexec_fn=os.setsid) as process:
            try:
                output = process.communicate(timeout=600)[0]
                return True
            except TimeoutExpired:
                os.killpg(process.pid, signal.SIGINT)
                output = process.communicate()[0]
                return False

    def emit_clean(self):
        with Popen('make clean', shell=True, stderr=STDOUT, stdout=PIPE,
                   preexec_fn=os.setsid) as process:
            try:
                output = process.communicate(timeout=600)[0]
            except TimeoutExpired as e:
                os.killpg(process.pid, signal.SIGINT)
                print("CATASTROPHIC ERROR - UNABLE TO CLEAN", file=sys.stderr)
                print(e, file=sys.stderr)
                output = process.communicate()[0]
                exit()

    def set_flags(self, flgs):
        self.flags = flgs

def make_data_group(bench):
    dg = Data_group(bench)
    return dg
