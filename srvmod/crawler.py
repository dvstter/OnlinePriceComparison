# -*- coding:utf-8 -*-
import requests
import random
import time
import json
import re
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from .proxy import Proxy
from sklearn.externals import joblib
from bs4 import BeautifulSoup
from srvmod.dbs import Database
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Crawler:
    Verbose = False

    def __init__(self):
        self.headers = {
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            "accept-encoding":"gzip, deflate, sdch"
        }
        self.httplib = requests.session()
        self.httplib.keep_alive = False

        self.proxy_list = []
        self.proxies = None

        self.dbs = Database()

        self.client = None

        self.__init_selenium()
        self.__init_proxies()

    """
    爬虫的运行函数，只需要调用这个即可更新当日的数据库
    """
    def run(self):
        caturls = []
        all_categories = self.dbs.get_all_category_names()
        cat_total = 0
        cat_count = 0

        if all_categories:
            cat_total = len(all_categories)
            for cat in all_categories:
                url = self.dbs.get_category_url(cat)
                caturls.append(url)
        else:
            categories = self.__get_categories()
            cat_total = len(categories)
            self.__update_categories_dbs(categories)
            caturls = [x[1] for x in categories]

        # Todo: everything about count needed to be deleted, this is just for jump over
        count = 140
        for url in caturls:
            count -= 1
            if count > 0:
                continue

            self.__update_category_items_price_with_selenium(url)
            cat_count += 1
            if Crawler.Verbose:
                print("----------------------")
                print("Finished {} for total {}".format(cat_count, cat_total))
                print("----------------------")

    """
    用于单元测试
    """
    def module_test(self):
        Crawler.Verbose = True
        self.__update_category_items_price_with_selenium("http://list.jd.com/list.html?cat=670,671,2694")

    """
    获取代理，应该首先调用__init_proxies_online_free()获取免费的，再加入自己的代理
    """
    def __init_proxies(self):
        #self.__init_proxies_online_free()
        # use my own proxy
        self.proxy_list.append(("127.0.0.1", 1087))

    """
    利用Proxy类从网上搜集免费代理，但是目前暂时无法找到合适的代理
    
    @return [(proxy_address1, proxy_port1), ...]
    """
    def __init_proxies_online_free(self):
        filename = "proxies.dat"
        if os.path.exists(filename):
            proxy_list = joblib.load(filename)
        else:
            proxy_list = Proxy.get_available_proxy()
            joblib.dump(proxy_list, filename, compress=3)

        self.proxy_list = proxy_list

    """
    因为只有一个代理，所以调用此函数即可
    """
    def __switch_proxy(self):
        if not len(self.proxy_list) == 1:
            return

        if not self.proxies:
            host, port = self.proxy_list[0]
            self.proxies = {
                "http": "http://{}:{}".format(host, port),
                "https": "http://{}:{}".format(host, port)
            }
        else:
            self.proxies = None

    """
    从self.proxy_list中随机挑选一个代理，并切换代理
    """
    def __switch_proxy_randomly(self):
        try:
            ori_host, ori_port = self.proxies["http"].split(":")[1:]
            ori_host = ori_host[2:]
        except IndexError as _:
            ori_host = None
            ori_port = None

        i = random.randint(-10, len(self.proxy_list) - 1)
        if i < 0:
            self.proxies = None
        else:
            host = self.proxy_list[i][0]
            port = self.proxy_list[i][1]
            self.proxies = {
                "http":"http://{}:{}".format(host, port),
                "https":"http://{}:{}".format(host, port)
            }

            if Crawler.Verbose:
                print("Switching Proxy {}:{} ---> {}:{}".format(ori_host, ori_port, host, port))

    """
    获取某一页的数据，如果没有成功就切换代理，并再次尝试
    
    :param url: url
    :param retry: 最大尝试次数
    :param encoding: 返回页面内容的编码形式，默认是utf-8
    
    :return 页面的data（以encoding进行编码）
    """
    def __request(self, url, retry=5, encoding="utf-8"):
        try:
            return requests.get(url, headers=self.headers, proxies=self.proxies, timeout=3).content.decode(encoding)
        except Exception as _:
            if retry < 0:
                return None
            elif retry < int(retry/2):
                self.__switch_proxy()
                time.sleep(random.randint(2,5))
                return self.__request(url, retry=retry-1)
    """
    获取京东所有的品类及品类的url链接
    
    :return [(品类名1, url1), ...]
    """
    def __get_categories(self):
        results = []
        url = "https://www.jd.com/allSort.aspx"
        data = requests.get(url, verify=False, headers={"user-agent":self.headers["user-agent"]}).content.decode("utf-8")
        bs = BeautifulSoup(data, "lxml")
        for each in bs.find_all("a", target="_blank"):
            if "list.jd.com" in each["href"]:
                results.append((each.contents[0], "http:{}".format(each["href"])))

        return results

    """
    将获取到的品类及链接存入数据库
    
    :param categories: [(品类名1,品类url1),...]可以指定自己的数据，如果为None，调用self.__get_categories()从网上获取
    """
    def __update_categories_dbs(self, categories=None):
        categories = self.__get_categories() if not categories else categories
        for cat, url in categories:
            self.dbs.add_category(cat, url)

    """
    初始化没有窗口的Chrome客户端
    """
    def __init_selenium(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.client = webdriver.Chrome(chrome_options=options)

    """
    利用selenium更新价格，该方法不能单独调用，必须调用下面的__update_category_items_price_with_selenium
    """
    def __update_items_price_with_selenium(self):
        # Todo: Added exception support for this function, and add exception process code on the next function

        time.sleep(3) # wait for javascript load all the prices
        self.client.execute_script("es = document.getElementsByClassName('J_price');for (var i=0; i!=es.length; i++) {es[i].style.display='block';}")
        for each in self.client.find_elements_by_class_name("j-sku-item"):
            try:
                price = float(re.findall(r"\d+\.\d{2}", each.find_element_by_class_name("J_price").text)[0])
                skuid = each.get_attribute("data-sku")

                self.dbs.add_price_another_day(skuid, price)
                if Crawler.Verbose:
                    print("Added {} for price {}".format(skuid, price))
            except Exception as e:
                print("----------------------")
                print("Exception arised.")
                print(e)
                print("----------------------")

                file = open("exception.txt", "w", encoding="utf-8")
                file.write(self.client.page_source)
                file.close()
                continue
        return True

    """
    更新某一个品类的所有商品价格
    """
    def __update_category_items_price_with_selenium(self, cat_url):
        if not self.client:
            self.__init_selenium()

        url = "{}&page=1&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main".format(cat_url)
        url = url.replace("&jth=i", "")

        if Crawler.Verbose:
            print("----------------------")
            print("Started form url:{}".format(url))
            print("----------------------")

        try:
            self.client.get(url)
        except TimeoutException:
            print("Access {} timeout, change proxy.".format(url))

        if not self.__update_items_price_with_selenium():
            return

        try:
            while True:
                time.sleep(random.randint(20, 50)/10.0)
                # move to the next page and call the
                next_page_btn = self.client.find_element_by_class_name("pn-next")
                ActionChains(self.client).click(next_page_btn).perform()

                if Crawler.Verbose:
                    print("----------------------")
                    print("Moved to page {}".format(re.findall(r"page=(\d+)", self.client.current_url)[0]))
                    print("----------------------")

                if not self.__update_items_price_with_selenium():
                    return
        except NoSuchElementException:
            print("----------------------")
            print("Ended this category.")
            print("----------------------")
            return

    """
    获取某一品类某一页的所有商品和价钱并存入数据库
    
    :param cat_url: 类型的url
    :param cur_page: 当前爬取的页数
    :param pages_num: 当前品类总共的页数，第一次传入None，将会从页面中提取总页数并返回
    
    :return 总共的页数
    """
    def __update_items_price(self, cat_url, cur_page=1, pages_num=None):
        if cur_page == 1 and Crawler.Verbose == True:
            print("Get items from " + cat_url)
            print("Page -------- {} --------".format(cur_page))

        url = "{}&page={}&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main".format(cat_url, cur_page)
        url = url.replace("&jth=i", "")

        retry = 5
        while retry:
            retry -= 1
            data = self.__request(url)

            if pages_num is None:
                pages_num = data.split("<em>共<b>")[-1].split("</b>页&nbsp;&nbsp;到第</em>")[0]
                pages_num = int(pages_num)
                if Crawler.Verbose:
                    print("Total {} pages".format(pages_num))

            bs = BeautifulSoup(data, "lxml")
            skuids = []
            try:
                for each in bs.find_all("div", class_="gl-i-wrap j-sku-item"):
                    skuids.append(each["data-sku"])
                    skuids = list(set(skuids))

                for _id in skuids:
                    price = json.loads(requests.get("https://p.3.cn/prices/mgets?skuIds=J_" + _id).text)[0]["p"]
                    self.dbs.add_price_another_day(_id, price)
                    print("Added {} price {}".format(_id, price))
                    time.sleep(random.randint(2,10)/10.0)
            except IndexError as ie:
                print(ie)

        return pages_num

    """
    获取某一品类的所有商品id和价格，并存入数据库，是对__update_items_price()的更进一步的封装
    
    :param cat_url: 类型的url
    :param wait_circle: 下一次发起链接的等待时间 
    """
    def __update_category_items_price(self, cat_url, wait_circle=None):
        cur_page = 1
        pages_num = None
        while True:
            pages_num = self.__update_items_price(cat_url, cur_page, pages_num)
            cur_page += 1
            if cur_page > pages_num:
                break
            if wait_circle:
                time.sleep(wait_circle)

