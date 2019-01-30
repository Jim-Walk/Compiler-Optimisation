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

    # save most recent runtime to history
    def save(self):
        self.times += sum(self.times)//len(self.times)
        self.history[self.get_flags()] = [times]

    # Return a string of all activated flags
    def get_flags(self):
        flg_str = ""
        for flag in self.flags:
            if self.flags[flag]:
                flg_str += flag
        return flg_str

    def add_times(self, res):
        self.times = res

    def write_to_file(self):
        with open(self.bench, 'w+') as f:
            for flg in self.flags:
                w_str = flg + self.flags[flg]
                f.write(w_str)
                f.write('\n')

    def emit_make(self):
        make_cmd = 'make CC=icc CFLAGS=' + self.get_flags()
        os.system(make_cmd)

    def set_flags(self, flgs):
        self.flags = flgs

def make_data_group(bench):
    dg = Data_group(bench)
    return dg
