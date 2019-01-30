import uuid
import os

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
        i = 0
        sum_times = 0
        for time in self.times:
            if time != 0:
                sum_times += times
                i += 1

        times = self.times sum_times//i
        self.history[self.get_flags()] = times

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
        print(make_cmd)
        os.system('make clean')
        os.system(make_cmd)

    def set_flags(self, flgs):
        self.flags = flgs

def make_data_group(bench):
    dg = Data_group(bench)
    return dg
