# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup

class PricesGetter:
    def __init__(self):
        requests.packages.urllib3.disable_warnings()

    def get_prices(self, item):
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

        return prices[0], prices[-1]

    @staticmethod
    def parse_tb(item):
        url = "https://s.taobao.com/search"
        payload = {"q":item, "s":"1", "ie":"utf8"}
        resp = PricesGetter.request_data(url, payload)
        prices = [float(x) for x in re.findall(r'"view_price":"([^"]+)"', resp.text, re.I)]
        prices.sort()

        return prices[0], prices[-1]

    @staticmethod
    def parse_dd(item):
        url = "http://search.dangdang.com"
        payload = {"key":item, "act":"input"}
        resp = PricesGetter.request_data(url, payload)
        bs = BeautifulSoup(resp.text, "lxml")
        prices = [float(x.contents[0][1:]) for x in bs.find_all("span", class_="search_now_price")]
        prices.sort()

        return prices[0], prices[-1]

    @staticmethod
    def parse_sn(item):
        pass

    @staticmethod
    def parse_ymx(item):
        pass

    @staticmethod
    def debug(resp):
        f = open("debug.txt", "w", encoding="utf-8")
        f.write(resp.text)
        f.close()