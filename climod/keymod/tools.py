import requests
from bs4 import BeautifulSoup

class Tools:

    @staticmethod
    def debug(resp):
        f = open("debug.txt", "w", encoding="utf-8")
        f.write(resp.text)
        f.close()

    @staticmethod
    def request_data(url, payload):
        resp = requests.get(url, params=payload, verify=False)
        bs = BeautifulSoup(resp.text, "lxml")
        return resp, bs