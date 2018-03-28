# coding:utf-8
import requests
import re
from .tools import Tools

class PricesGetter:
    def __init__(self):
        requests.packages.urllib3.disable_warnings()

        self.supported = {"jd":"京东", "tb":"淘宝", "dd":"当当", "tm":"天猫", "ymx":"亚马逊"}

    def get_prices(self, item):
        for func, platform in self.supported.items():
            f = getattr(type(self), "parse_" + func)
            url, payload, prices = f(item)
            link = url +  "?" + "&".join([x + "=" + "%20".join(payload[x].split(" ")) for x in payload.keys()])

            if len(prices) == 0:
                continue

            yield platform, prices, link

    @staticmethod
    def parse_jd(item):
        url = "https://search.jd.com/search"
        payload = {"keyword":item, "enc":"utf-8"}
        resp, bs = Tools.request_data(url, payload)
        prices = []
        # TODO: After updating lxml, "for each in bs.find_all..." can not run
        tmplist = bs.find_all("div", class_="p-price")
        for each in tmplist:
            tmp = each.strong.i.contents
            if len(tmp) == 1:
                prices.append(float(tmp[0]))
        prices.sort()

        return url, payload, prices

    @staticmethod
    def parse_tb(item):
        url = "https://s.taobao.com/search"
        payload = {"q":item, "s":"1", "ie":"utf8"}
        resp, _ = Tools.request_data(url, payload)
        prices = [float(x) for x in re.findall(r'"view_price":"([0-9]+\.[0-9]{2})"', resp.text, re.I)]
        prices.sort()

        return url, payload, prices

    @staticmethod
    def parse_dd(item):
        url = "http://search.dangdang.com/"
        payload = {"key":item, "act":"input"}
        resp, _ = Tools.request_data(url, payload)
        prices = [float(x[4:]) for x in re.findall(r'yen;[0-9]+\.[0-9]{2}', resp.text)]
        prices.sort()

        return url, payload, prices

    # TODO: There are still some problems needed to be solved
    @staticmethod
    def parse_tm(item):
        url = "https://list.tmall.com/search_product.htm"
        payload = {"q":item}
        resp, _ = Tools.request_data(url, payload)
        prices = [float(x) for x in re.findall(r'yen;</b>([0-9]+\.[0-9]{2})</em>', resp.text)]
        prices.sort()

        return url, payload, prices

    @staticmethod
    def parse_ymx(item):
        url = "https://www.amazon.cn/s"
        payload = {"field-keywords":item}
        _, bs = Tools.request_data(url, payload)
        prices = []
        temp = ["".join(x.contents[0].split(",")) for x in bs.find_all("span", class_="a-size-base a-color-price s-price a-text-bold")]
        for x in temp:
            for each_price in re.findall(r'[0-9]+\.[0-9]+', x):
                prices.append(float(each_price))

        prices.sort()
        return url, payload, prices