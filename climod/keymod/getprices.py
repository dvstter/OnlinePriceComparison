# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup

class PricesGetter:
    def __init__(self):
        self.__supported = ["京东", "淘宝", "当当", "苏宁", "国美", "亚马逊"]

        requests.packages.urllib3.disable_warnings()

    def get_supported(self):
        return self.__supported

    def get_prices(self, item):
        for idx in range(len(self.__supported)):
            pass

    @staticmethod
    def request_data(url, payload):
        resp = requests.get(url, params=payload, verify=False)
        return resp

    @staticmethod
    def parse_jd(item):
        url = "https://search.jd.com/search"
        payload = {"keyword":item, "enc":"utf-8"}
        resp = PricesGetter.request_data(url, payload)
        bs = BeautifulSoup(resp.text, "lxml")
        prices = [float(x) for x in [each.strong.contents[1].contents[0] for each in bs.find_all("div", class_="p-price")]]
        prices.sort()
        lowest, highest = prices[0], prices[-1]
        return lowest, highest

    @staticmethod
    def parse_tb(item):
        url = "https://s.taobao.com/search"
        payload = {"q":item, "s":"1", "ie":"utf8"}
        resp = PricesGetter.request_data(url, payload)
        prices = [float(x) for x in re.findall(r'"view_price":"([^"]+)"', resp.text, re.I)]
        prices.sort()
        lowest, highest = prices[0], prices[-1]
        return lowest, highest

    @staticmethod
    def parse_dd(item):
        pass

    @staticmethod
    def parse_sn(item):
        pass

    @staticmethod
    def parse_ymx(item):
        pass