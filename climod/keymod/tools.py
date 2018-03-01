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