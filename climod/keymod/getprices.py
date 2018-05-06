# coding:utf-8
import requests
import re
import time
from selenium import webdriver
from .tools import Tools

class PricesGetter:
    def __init__(self):
        requests.packages.urllib3.disable_warnings()

        #self.supported = {"jd":"京东", "tb":"淘宝", "dd":"当当", "tm":"天猫", "ymx":"亚马逊"}
        self.supported = {"jd":"京东"}

    def get_prices(self, item):
        for func, platform in self.supported.items():
            f = getattr(type(self), "parse_" + func)
            url, results = f(item)
            yield platform, results, url

    @staticmethod
    def parse_jd(item):
        url = "https://www.jd.com"

        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        client = webdriver.Chrome(chrome_options=options)

        client.get(url)
        _form_ele = client.find_element_by_class_name("form")
        _form_ele.find_element_by_tag_name("input").send_keys(item+"\n")
        time.sleep(2)
        client.refresh()
        time.sleep(2)

        url = client.current_url
        results = []
        for each in client.find_elements_by_class_name("gl-item"):
            try:
                skuid = each.get_attribute("data-sku")
                price = float(re.findall(r"(\d+\.\d{2})", each.find_element_by_class_name("p-price").find_element_by_tag_name("strong").text)[0])
                results.append((skuid, price))
            except Exception:
                continue

        client.close()
        return url, results

    def deprecated_get_prices(self, item):
        for func, platform in self.supported.items():
            f = getattr(type(self), "parse_" + func)
            url, payload, prices = f(item)
            link = url +  "?" + "&".join([x + "=" + "%20".join(payload[x].split(" ")) for x in payload.keys()])
            yield platform, prices, link

    @staticmethod
    def deprecated_parse_jd(item):
        url = "https://search.jd.com/search"
        payload = {"keyword":item, "enc":"utf-8"}
        _, bs = Tools.request_data(url, payload)
        prices = [float(x) for x in [each.strong.contents[1].contents[0] for each in bs.find_all("div", class_="p-price")]]
        prices.sort()

        return url, payload, prices

    @staticmethod
    def deprecated_parse_tb(item):
        url = "https://s.taobao.com/search"
        payload = {"q":item, "s":"1", "ie":"utf8"}
        resp, _ = Tools.request_data(url, payload)
        prices = [float(x) for x in re.findall(r'"view_price":"([^"]+)"', resp.text, re.I)]
        prices.sort()

        return url, payload, prices

    @staticmethod
    def deprecated_parse_dd(item):
        url = "http://search.dangdang.com"
        payload = {"key":item, "act":"input"}
        _, bs = Tools.request_data(url, payload)
        prices = [float(x.contents[0][1:]) for x in bs.find_all("span", class_="search_now_price")]
        prices.sort()

        return url, payload, prices

    @staticmethod
    def deprecated_parse_tm(item):
        url = "https://list.tmall.com/search_product.htm"
        payload = {"q":item}
        _, bs = Tools.request_data(url, payload)
        prices = [float(x.em["title"]) for x in bs.find_all("p", class_="productPrice")]
        prices.sort()

        return url, payload, prices

    @staticmethod
    def deprecated_parse_ymx(item):
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
