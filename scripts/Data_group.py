import os, sys
import random
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

class Data_group():
    # A list of all ten times, the 11th
    # value is the average
    times = []
    # Dictionary of all flags, flags which are on are set to true
    flags = {}
    # history contains dictionary record of active flags and their runtimes
    bench = ""
    fitness = 0

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
                flg_str += (flag + " ")
        return flg_str

    def set_flags(self, flgs):
        self.flags = flgs

    def add_times(self, res):
        self.times = res
        avg = sum(self.times)//len(self.times)
        self.times += [avg]

    # Calculate fitness after saving run time
    # return inverse average time as we want better 
    # solutions to have higher fitness
    def set_fitnesss(self, fit):
        self.fitness = fit

    def mutate(self):
        for flag in self.flags:
            if random.random() < 0.05:
                self.flags[flag] = not self.flags[flag]


    def emit_make(self):
        make_cmd = 'make CC=gcc CFLAGS=\"' + self.get_flags() +'\"'
        self.emit_clean()
        with Popen(make_cmd, shell=True, stderr=STDOUT, stdout=PIPE,
                   preexec_fn=os.setsid) as process:
            try:
                output = process.communicate(timeout=300)[0]
                # return true or false depending if compile was
                # successful
                return process.returncode == 0
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


def make_data_group(bench):
    dg = Data_group(bench)
    return dg
