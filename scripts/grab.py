#!/lustre/sw/anaconda/anaconda3-5.1.0/bin/python3

import Data_group
import os

# Returns an int representation of the time
# in milliseconds
# originally in for 0m0.0user or 0.0user
def parse_time(time_str):
    mins_and_secs, milli_sec_str = time_str.split(".")
    if len(mins_and_secs.split("m")) == 2:
        mins, secs = [int(x) for x in mins_and_secs.split("m")]
        secs = secs + mins * 60
    else:
        secs = int(mins_and_secs)
    milli_secs = int(milli_sec_str[:-4:])
    milli_secs = milli_secs + secs * 1000
    return (milli_secs)



def foo():
    for folder in os.listdir():
        if (not os.path.isfile(folder)):
            print('Entering ', folder, end='')
            times = int(0)
            for i in list(range(1,11)):
                fname = folder + "/" + str(i) + ".dat"
                with open(fname, "r") as f:
                    lines = f.readlines()
                    times += parse_time(lines[-3])

            dg = Data_group.make_data_group(times//10, {'-O2':True}, folder)
            dg.save()
            print(" saved average")
