# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup

class PricesGetter:
    def __init__(self):
        requests.packages.urllib3.disable_warnings()

        self.supported = {"jd":"京东", "tb":"淘宝", "dd":"当当", "tm":"天猫", "ymx":"亚马逊"}

    def get_prices(self, item):
        for func, platform in self.supported.items():
            f = getattr(type(self), "parse_" + func)
            url, payload, prices = f(item)
            link = url +  "?" + "&".join([x + "=" + "%20".join(payload[x].split(" ")) for x in payload.keys()])
            yield platform, prices, link


    @staticmethod
    def request_data(url, payload):
        resp = requests.get(url, params=payload, verify=False)
        bs = BeautifulSoup(resp.text, "lxml")
        return resp, bs

    @staticmethod
    def parse_jd(item):
        url = "https://search.jd.com/search"
        payload = {"keyword":item, "enc":"utf-8"}
        _, bs = PricesGetter.request_data(url, payload)
        prices = [float(x) for x in [each.strong.contents[1].contents[0] for each in bs.find_all("div", class_="p-price")]]
        prices.sort()

        return url, payload, prices

    @staticmethod
    def parse_tb(item):
        url = "https://s.taobao.com/search"
        payload = {"q":item, "s":"1", "ie":"utf8"}
        resp, _ = PricesGetter.request_data(url, payload)
        prices = [float(x) for x in re.findall(r'"view_price":"([^"]+)"', resp.text, re.I)]
        prices.sort()

        return url, payload, prices

    @staticmethod
    def parse_dd(item):
        url = "http://search.dangdang.com"
        payload = {"key":item, "act":"input"}
        _, bs = PricesGetter.request_data(url, payload)
        prices = [float(x.contents[0][1:]) for x in bs.find_all("span", class_="search_now_price")]
        prices.sort()

        return url, payload, prices

    @staticmethod
    def parse_tm(item):
        url = "https://list.tmall.com/search_product.htm"
        payload = {"q":item}
        _, bs = PricesGetter.request_data(url, payload)
        prices = [float(x.em["title"]) for x in bs.find_all("p", class_="productPrice")]
        prices.sort()

        return url, payload, prices

    @staticmethod
    def parse_ymx(item):
        url = "https://www.amazon.cn/s"
        payload = {"field-keywords":item}
        _, bs = PricesGetter.request_data(url, payload)
        prices = []
        temp = ["".join(x.contents[0].split(",")) for x in bs.find_all("span", class_="a-size-base a-color-price s-price a-text-bold")]
        for x in temp:
            for each_price in re.findall(r'[0-9]+\.[0-9]+', x):
                prices.append(float(each_price))

        prices.sort()
        return url, payload, prices


    @staticmethod
    def debug(resp):
        f = open("debug.txt", "w", encoding="utf-8")
        f.write(resp.text)
        f.close()