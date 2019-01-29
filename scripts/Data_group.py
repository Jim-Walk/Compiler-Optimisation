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
        for x in flegs:
            if flegs[x]:
                self.num_flags += 1

    def save(self):
        fname = str(self.num_flags) + "_" + self.bench + "." + str(self.iden) + ".final"
        with open(fname, "w+") as f:
            f.write(str(self.avg))
            f.write('\n')
            for flag in self.flags:
                if self.flags[flag]:
                    f.write(flag)
                    f.write('\n')

def make_data_group(avg, flags, bench):
    dg = Data_group(avg, flags, bench)
    return dg

