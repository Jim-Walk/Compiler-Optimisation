def compare(str1, str2):
    arr_1 = str1.split('\n')
    arr_2 = str2.split('\n')

    i = 0
    j = 0
    while i < len(arr1):
        if arr_1[i] == arr_2[i]:
            j = j + 1
        i = i + 1

    return j/i > 0.6

