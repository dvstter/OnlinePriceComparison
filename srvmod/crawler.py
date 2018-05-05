# -*- coding:utf-8 -*-
import requests
import random
import time
import json
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

        self.proxy_list = None
        self.proxies = None

        self.dbs = Database()

        self.__init_proxies()

    """
    爬虫的运行函数，只需要调用这个即可更新当日的数据库
    """
    def run(self):
        caturls = []
        all_categories = self.dbs.get_all_category_names()

        if all_categories:
            for cat in all_categories:
                url = self.dbs.get_category_url(cat)
                caturls.append(url)
        else:
            categories = self.__get_categories()
            self.__update_categories_dbs(categories)
            caturls = [x[1] for x in categories]

        for url in caturls:
            self.__update_category_items_price(url)

    """
    用于单元测试
    """
    def module_test(self):
        Crawler.Verbose = True
        self.__update_category_items_price("http://list.jd.com/list.html?cat=12218,13581,13582")

    """
    从Proxy类中从网上搜集免费代理，因为没有找到好的免费代理，因此只有用自己的代理
    
    @return [(proxy_address1, proxy_port1), ...]
    """
    def __init_proxies(self):
        '''
        # the free proxy website has been baned, so disabled these code
        filename = "proxies.dat"
        if os.path.exists(filename):
            proxy_list = joblib.load(filename)
        else:
            proxy_list = Proxy.get_available_proxy()
            joblib.dump(proxy_list, filename, compress=3)

        self.proxy_list = proxy_list
        '''

        # use my own proxy
        return [("127.0.0.1", 1087)]

    """
    从self.proxy_list中随机挑选一个代理，并切换代理
    """
    def __switch_proxy(self):
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

    def __update_categories_dbs(self, categories=None):
        categories = self.__get_categories() if not categories else categories
        for cat, url in categories:
            self.dbs.add_category(cat, url)

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

