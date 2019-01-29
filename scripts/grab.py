#!/lustre/sw/anaconda/anaconda3-5.1.0/bin/python3

import Data_group
import os

# Returns an int representation of the time
# in milliseconds
# originally in for 0m0.0s
def parse_time(string):
    time_str = string.strip().split()[1]
    mins_and_secs, milli_sec_str = time_str.split(".")
    mins, secs = [int(x) for x in mins_and_secs.split("m")]
    secs = secs + mins * 60
    milli_secs = int(milli_sec_str[:-1:])
    milli_secs = milli_secs + secs * 1000
    return milli_secs






os.chdir('../coptbenchmarks2013')

for folder in os.listdir():
    if (not os.path.isfile(folder)):
        print('Entering ', folder)
        times = int(0)
        for i in list(range(1,11)):
            fname = folder + "/" + str(i) + ".dat"
            with open(fname, "r") as f:
                lines = f.readlines()
                times += parse_time(lines[-3])

        avg = times/10
        print(avg)

