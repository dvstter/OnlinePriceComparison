# -*- coding: utf-8 -*-
import requests
import re
import json
import urllib3
import time

urllib3.disable_warnings()

class Proxy:
    Headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            "accept-encoding": "gzip, deflate, sdch"
        }
    Gfw = {"http":"http://127.0.0.1:1087", "https":"http://127.0.0.1:1087"}
    Verbose = False

    @staticmethod
    def get_available_proxy():
        proxy_list = Proxy.__get_proxy_online_0()
        proxy_list += Proxy.__get_proxy_online_1()
        proxy_list += Proxy.__get_proxy_online_2()

        return Proxy.filter_available_proxies(list(set(proxy_list)))

    @staticmethod
    def filter_available_proxies(proxy_list):
        available_list = []
        test_url = "http://www.baidu.com/"
        for host, port in proxy_list:
            ret = False
            proxies = {
                "http":"http://{}:{}".format(host, port),
                "https":"http://{}:{}".format(host, port)
            }
            try:
                data = requests.get(test_url, timeout=2.5, proxies=proxies, verify=False).content.decode("utf-8")
                if "百度" in data:
                    ret = True
                    available_list.append((host, port))
            except Exception as _:
                ret = False

            if Proxy.Verbose:
                print("checking proxy: {}:{} ---> {}".format(host, port, ret))
        print(available_list)
        return available_list

    @staticmethod
    def __debug(filename, data):
        file = open(filename, "wt")
        file.write(data)
        file.close()

    @staticmethod
    def __get_proxy_online_0():
        proxy_list = []
        url = "http://proxy.ipcn.org/proxylist.html"
        headers = {"Connection": "keep-alive",
                   "Cache-Control": "max-age=0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36",
                   "Accept-Language": "zh-CN,zh;q=0.8"}
        data = requests.get(url, headers=headers).text
        Proxy.__debug("get_proxy_online_0.txt", data)

        data = data.replace("\n", " ")
        alist = re.findall("(\d+\.\d+\.\d+\.\d+):(\d+)", data)
        for host, port in alist:
            proxy_list.append((host, port))
        proxy_list = list(set(proxy_list))
        return proxy_list

    @staticmethod
    def __get_proxy_online_1():
        base_url = [
            "http://www.kuaidaili.com/free/inha/",
            "http://www.kuaidaili.com/free/intr/"]
        url_list = [base_url[0]+str(x) for x in range(1,200)]
        url_list += [base_url[1]+str(x) for x in range(1, 200)]
        proxy_list = []

        for url in url_list:
            if Proxy.Verbose:
                print("Fetching {}".format(url))
            try:
                data = requests.get(url, timeout=3).text
            except Exception as _:
                continue

            "".join(list(filter(lambda x: x != "\n" and x != "\r", data)))
            if "Blocked by CC firewall" in data:
                data = requests.get(url, headers=Proxy.Headers, proxies=Proxy.Gfw).content
            origin_num = len(proxy_list)
            proxy_list += re.findall("""<td data-title="IP">(.+?)</td>\s*<td data-title="PORT">(.+?)</td>""", data)
            current_num = len(proxy_list)
            if Proxy.Verbose:
                print("Proxies number increased {}".format(current_num-origin_num))
                print("Waiting for 3 secs")
            time.sleep(3)
        return list(set(proxy_list))

    @staticmethod
    def __get_proxy_online_2():
        proxy_list = []
        try:
            url = "http://www.gatherproxy.com/zh/proxylist/country/?c=China"
            data = requests.get(url, headers=Proxy.Headers, proxies=Proxy.Gfw).text
            Proxy.__debug("get_proxy_online_2.txt", data)
            data = data.replace("\n", "").replace("\r", "")
            a_list = re.findall("""gp.insertPrx\((.+?)\);""", data)

            for proxy_info in a_list:
                proxy_info = json.loads(proxy_info)
                host = proxy_info["PROXY_IP"]
                port = proxy_info["PROXY_PORT"]
                port = eval("0x{}".format(port))
                proxy_list.append((host, port))
        except Exception as _:
            print("Exception: Proxy.get_proxy_online_2 Error.")
        return proxy_list