import uuid

class Data_group():
    avg = 0
    flags = {}
    bench = ""
    num_flags = 0

    def __init__(self, average, flegs, benchmark):
        self.avg = average
        self.flags = flegs
        self.bench = benchmark
        self.iden = uuid.uuid4()

    def save(self):
        fname = str(self.num_flags) + "_" + self.bench + "." + str(self.iden)  + ".dat"
        print(fname)
        for flag in self.flags:
            if self.flags[flag]:
                print(flag)
        print(self.avg)

def make_data_group(avg, flags, bench):
    dg = Data_group(avg, flags, bench)
    return dg

a = make_data_group(12, {"-flag": True, "-otherflag": False}, "test-bench")
