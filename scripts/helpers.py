import random

# Contains misc helper methods

# Compares two strings, returns true if 60% of the lines
# match
def compare(str1, str2):
    arr_1 = str1.split()
    arr_2 = str2.split()

    i = 0
    j = 0
    while i < len(arr_1):
        if arr_1[i] == arr_2[i]:
            j = j + 1
        i = i + 1

    return j/i >= 0.6

# reads in flags from specified path
# returns a dictionary of all flags, with a random
# boolean to indicate if they are on or not
def read_flags(path):
    with open(path, 'r') as flg_f:
        flgs = flg_f.read()
        return flgs.split()

# Returns random true false dict of flags
# from given list of flags
def random_flags(flgs):
    flg_dict = {}
    for flg in flgs:
        flg_dict[flg] = random.random() > 0.5

    return flg_dict

def change_range(n, start1, stop1, start2, stop2):
    val =  ((n-start1) / (stop1-start1)) * (stop2-start2) + start2
    return val
