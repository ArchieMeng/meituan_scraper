import pickle
import os

FILE_NAME = 'words.pickle'


def iter_data(file_name):
    with open(file_name, 'rb') as rf:
        while 1:
            try:
                data = pickle.load(rf)
                yield data
            except EOFError:
                break
if __name__ == '__main__':
    id_set = set()
    for file in os.listdir('.'):
        if file.endswith('.pickle'):
            i = 0
            for shop in iter_data(file):
                id_set.add(shop['id'])
                i += 1
            print(file[:-7].replace('_', '\t'), "\t", i)
    print(len(id_set))
