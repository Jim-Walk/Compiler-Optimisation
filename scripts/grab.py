#!/lustre/sw/anaconda/anaconda3-5.1.0/bin/python3


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

