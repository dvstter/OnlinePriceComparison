import requests
from bs4 import BeautifulSoup
from .tools import Tools

class ImageGetter:
    def __init__(self):
        pass

    @staticmethod
    def get_image(item):
        url = "http://image.baidu.com/search/index"
        payload = {"word":item, "ie":"utf-8"}
        resp, bs = Tools.request_data(url, payload)
        Tools.debug(resp)