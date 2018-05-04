import requests
import random
import time
from bs4 import BeautifulSoup
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

        self.__init_proxies()

    def module_test(self):
        categories = self.__get_category()
        for name, url in categories:
            print("{}:{}".format(name, url))

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

    def __request(self, url, retry=5, encoding="utf-8", max_wait=5):
        try:
            return requests.get(url, headers=self.headers, proxies=self.proxies, timeout=3).content.decode(encoding)
        except Exception as _:
            if retry < 0:
                return None
            elif retry < int(retry/2):
                self.swith_proxy()
                time.sleep(random.randint(2,5))
                return self.proxy_requests(url, retry=retry-1)

    def __get_category(self):
        results = []
        url = "https://www.jd.com/allSort.aspx"
        data = requests.get(url, verify=False, headers={"user-agent":self.headers["user-agent"]}).content.decode("utf-8")
        bs = BeautifulSoup(data)
        for each in bs.find_all("a", target="_blank"):
            if "list.jd.com" in each["href"]:
                results.append((each.contents[0], "http:{}".format(each["href"])))

        return results

if __name__ == "__main__":
    crawler = Crawler()
    crawler.module_test()