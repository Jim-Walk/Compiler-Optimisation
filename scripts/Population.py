import random
import Data_group, helpers

class Population():
    pop_size = 0
    live_pool = []
    mating_pool = []
    bench = ""
    history = {}

    def __init__(self, size, benchmark):
        self.pop_size = size
        self.bench = benchmark
        i = 0
        flgs = helpers.read_flags('../flags.txt')
        for i in list(range(0,self.pop_size)):
            self.live_pool.append( Data_group.make_data_group(self.bench) )
            self.live_pool[i].set_flags(helpers.random_flags(flgs))


    def calc_fitnesss(self):
        max_time, min_time = 0, 0

        for i in list(range(0,self.pop_size)):
            if max_time < self.live_pool[i].times[-1]:
                max_time = self.live_pool[i].times[-1]
            if min_time >  self.live_pool[i].times[-1]:
                min_time = self.live_pool[i].times[-1]

        # Those which are faster have a higher fitness
        for i in list(range(0,self.pop_size)):
            self.live_pool[i].set_fitnesss( helpers.change_range( self.live_pool[i].times[-1],
                                                                  min_time, max_time,
                                                                  100, 1 ) )

    # Creates mating pool
    def evaluate(self):
        self.calc_fitnesss()
        self.mating_pool = []
        for i in list(range(0, self.pop_size)):
            j = 0; max_j = self.live_pool[i].fitness
            while j < max_j:
                self.mating_pool.append(self.live_pool[i])
                j += 1

    def save(self):
        for i in list(range(0, self.pop_size)):
            if self.live_pool[i].get_flags() not in self.history:
                self.history[self.live_pool[i].get_flags()] = self.live_pool[i].times

    def crossover(self, dg1, dg2):
        new_flags = {}
        mid = random.randint(0, len(dg1))
        i = 0
        for flag in dg1:
            if i < mid:
                new_flags[flag] = dg1[flag]
            else:
                new_flags[flag] = dg2[flag]
            i += 1
        return new_flags

    def selection(self):
        new_pool = []
        self.save()
        for i in list(range(0, self.pop_size)):
             p1 = self.mating_pool[(random.randint(0, self.pop_size-1))].flags
             p2 = self.mating_pool[(random.randint(0, self.pop_size-1))].flags
             child = self.crossover(p1, p2)
             d = Data_group.make_data_group(self.bench)
             d.set_flags(child)
             d.mutate()
             new_pool.append(d)

        self.live_pool = new_pool

    def write_to_file(self, path):
        fpath = path + self.bench
        best_time = 10000000000
        with open(fpath, 'w+') as f:
            f.write(self.bench)
            f.write('\n')
            for flg in self.history:
                if len(self.history[flg]) > 0:
                    if self.history[flg][-1] < best_time:
                        best_time = self.history[flg][-1]
                w_str = flg + ' ' + str(self.history[flg])
                f.write(w_str)
                f.write('\n')
            w_str = 'The best time is ' + str(best_time)
            f.write(w_str)
            f.write('\n')

def create(size, bench):
    pop = Population(size, bench)
    pop.history = {}
    return pop
