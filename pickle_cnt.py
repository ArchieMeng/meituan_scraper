from pickle import load
import sys


def pickle_count(file_name):
    with open(file_name, 'rb') as rf:
        cnt = 0
        while 1:
            try:
                load(rf)
                cnt += 1
            except EOFError:
                break
    return cnt

if len(sys.argv) > 1:
    for filename in sys.argv[1:]:
        print(pickle_count(filename))
else:
    file_name = input("input pickle file name:")
    print(pickle_count(file_name))