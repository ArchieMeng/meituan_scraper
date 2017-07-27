import requests
import json
from time import sleep
from collections import defaultdict


class MeiTuanAPIManager:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) '
                      'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    }
    MOBILE_PAGE = 'http://i.waimai.meituan.com/home'
    QUERY_PAGE = 'http://i.waimai.meituan.com/ajax/v6/poi/filter'
    CATEGORY_URL = 'http://i.waimai.meituan.com/ajax/v6/poi/getfilterconditions'

    TOKEN = 'eJxVjEFrg0AUhP/LO/RS0X3quiqEYrEHQ7TY3XoJPZitmKVZE K2MZb 927AQ/t48M0Mw3zDuXiHFIm9xAEzWk0JkhApDWKGD'
    'sj/WUJtbXducki3SYwOY HbLXixfos0iJw4sskf6Yf2b53CVmBvzCn1POVeWqVb5epOmc92cOVRe/uj7h4OrVkFvksi4tPw7j'
    'D0K8TYZUkUMwYOgF3Swi5ZfixsF5qFo oHSKFbT4KrqRBP91g1YsP5darEjpdzNpd5ga/ya82ZxGoj6pJJMs5Z0FyeT0p6JSfa'
    'jHlTZ/3jNalpCD /nCdTEA=='

    def __init__(self, lat=32.060344, lng=118.790281, proxies=None):
        self.lat = lat
        self.lng = lng

        query_params = {
            'lat': self.lat,
            'lng': self.lng,
        }

        self.xhr_session = requests.Session()
        self.proxies = proxies
        initial_response = None
        while not initial_response:
            try:
                initial_response = self.xhr_session.request(
                    method='get',
                    url=MeiTuanAPIManager.MOBILE_PAGE,
                    params=query_params,
                    headers=MeiTuanAPIManager.HEADERS,
                    proxies=proxies
                )
            except Exception as e:
                print(e)
            sleep(5)
        self.uuid = initial_response.cookies['w_uuid']

    def get_shops(self, lat=None, lng=None, index=1):
        """
        get shops by location and index
        :param lat: latitude, string or float is preferred
        :param lng: longitude, string or float is preferred
        :param index: page_index, int
        :return: a dict of json response
        """
        lat, lng = lat if lat else self.lat, lng if lng else self.lng
        data = {
            'platform': 3,
            'partner': 4,
            'page_index': index,
            'apage': 1,
            'uuid': self.uuid
        }
        query_params = {
            'lat': lat,
            'lng': lng,
            '_token': MeiTuanAPIManager.TOKEN
        }

        response = self.xhr_session.post(
            url=MeiTuanAPIManager.QUERY_PAGE,
            params=query_params,
            headers=MeiTuanAPIManager.HEADERS,
            data=data,
            proxies=self.proxies
        )

        json_obj = json.loads(response.text)
        return json_obj

    def get_all_shops(self, lat=None, lng=None):
        """
        get all shops nearby by given location
        :param lat:

        latitude
        :param lng:

        longitude
        :return:

        a generator of shops
        """
        lat, lng = lat if lat else self.lat, lng if lng else self.lng
        result = {'data': {'poi_has_next_page': True}}
        i = 0
        while result['data']['poi_has_next_page']:

            result = self.get_shops(lat=lat, lng=lng, index=i)
            while result['code'] != 0:
                print(result)
                sleep(5)
                result = self.get_shops(lat=lat, lng=lng, index=i)
            for shop in result['data']['poilist']:
                yield shop
            i += 1
            sleep(2)

    def get_category_page(self, category1, category2=0, index=0):
        query_params = {
            'category_type': category1,
            'second_category_type': category2,
            '_token': MeiTuanAPIManager.TOKEN
        }

        data = {
            'platform': 3,
            'partner': 4,
            'page_index': index,
            'apage': 1,
            'uuid': self.uuid
        }

        response = self.xhr_session.post(
            url=MeiTuanAPIManager.QUERY_PAGE,
            params=query_params,
            headers=MeiTuanAPIManager.HEADERS,
            data=data,
            proxies=self.proxies
        )
        return json.loads(response.text)

    def get_shops_in_category(self, category1, category2=0):
        """
        get all shops in a specific category

        :param category1:

        code of category1
        :param category2:

        code of category2
        :return:

        a generator of shops
        """
        result = {'data': {'poi_has_next_page': True}}

        i = 0
        while result['data']['poi_has_next_page']:
            result = self.get_category_page(category1, category2, i)
            while result['code'] != 0:
                print(result)
                sleep(5)
                result = self.get_category_page(category1, category2, i)
            for shop in result['data']['poilist']:
                yield shop
            i += 1
            sleep(2)

    def get_all_category(self):
        response = self.xhr_session.post(
            url=MeiTuanAPIManager.CATEGORY_URL,
            data={
                'navigate_type': 910,
                'first_category_type': 910,
                'second_category_type': 0
            },
            proxies=self.proxies
        )
        text = response.text
        json_obj = json.loads(text)

        return json_obj['data']['category_filter_list']


