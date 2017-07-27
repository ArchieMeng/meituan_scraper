from meituan_api import MeiTuanAPIManager
import pickle
from time import time
from threading import Thread, Semaphore
from collections import defaultdict

thread_sem = Semaphore(10)
id_set = defaultdict(set)


def fetch_and_dump(lat, lng):
    with thread_sem:
        t1 = time()
        fetcher = MeiTuanAPIManager(lat=lat, lng=lng)
        print('{},{} fetcher initialization times:'.format(lat, lng), time() - t1, 's')
        t2 = time()
        for main_category in fetcher.get_all_category()[1:]:
            print(main_category['code'], main_category['name'])
            for sub_category in main_category['sub_category_list'][1:]:
                print('\t', sub_category['code'], sub_category['name'])
                shops = fetcher.get_shops_in_category(main_category['code'], sub_category['code'])
                category_name = '_'.join(
                    [
                        main_category['name'].replace('/', 'or').replace('\x08', ''),
                        sub_category['name'].replace('/', 'or').replace('\x08', '')
                    ]
                )
                for shop in shops:
                    if shop['id'] not in id_set[category_name]:
                        id_set[category_name] += {shop['id']}
                        shop['category'] = {
                            'name': main_category['name'],
                            'code': main_category['code']
                        }
                        shop['sub_category'] = {
                            'name': sub_category['name'],
                            'code': sub_category['code']
                        }
                        with open(category_name + '.pickle', 'a+b') as wf:
                            pickle.dump(shop, wf, protocol=pickle.HIGHEST_PROTOCOL)
        print('task {},{} done with '.format(lat, lng), time() - t2, 's')


def get_category_shops_by_location():
    locations = []
    with open('geo_location.txt', 'r') as rf:
        for line in rf:
            if line:
                locations.append(tuple(line.replace('\n','').split(',')))
    threads = []
    for location in locations:
        print(location)
        thread = Thread(target=fetch_and_dump, args=location, daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    with open('下午茶_水果.pickle', 'rb') as rf:
        shop = pickle.load(rf)
    for k in shop:
        print(k, shop[k])