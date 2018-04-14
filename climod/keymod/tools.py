import requests
from bs4 import BeautifulSoup

# 核心组件的支持类，定义了很多类方法，用于网络数据获取和调试
class Tools:

    @staticmethod
    def debug(resp, filename=None):
        if filename is None:
            filename = "debug.txt"

        f = open(filename, "w", encoding="utf-8")

        f.write(resp.text)
        f.close()

    # 从网络上获取数据
    @staticmethod
    def request_data(url, payload):
        resp = requests.get(url, params=payload, verify=False)
        bs = BeautifulSoup(resp.text, "lxml")
        return resp, bs

    # 在指定网络连接上，获取图片，并保存到指定的位置
    @staticmethod
    def save_image(url, filename):
        filename += "." + url.split(".")[-1]
        if not url.startswith("http://"):
            url = "http://" + url

        try:
            resp = requests.get(url)
            f = open(filename, "wb")
            f.write(resp.content)
            f.close()
        except Exception as _:
            print("Exception: Tools.save_image")
            return False, None

        return True, filename