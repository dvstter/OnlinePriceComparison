# -*- coding:utf-8 -*-

from tkinter import *
from selenium import webdriver
import requests
import json
import time

class Comments(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()

        self.__label = None
        self.__text_variable = StringVar()
        self.__data = []

        self.__create_widgets()
        self.__place_widgets()

    def add_comment(self, cmt_str):
        self.__data.append(cmt_str)
        self.__text_variable.set(self.__generate_str())
        #self.__label["text"] = self.__generate_str()

    def clear_comment(self):
        self.__label["text"] = ""

    def __deprecated__fetch_and_update_comments(self, item):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument('user-agent="Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
        client = webdriver.Chrome(chrome_options=options)
        client.get("https://item.m.jd.com/product/{}.html".format(item))
        for each in client.find_elements_by_tag_name("a"):
            if each.get_attribute("dtype") == "comment":
                each.click()
        time.sleep(5)

        for each in client.find_elements_by_class_name("cmt_cnt"):
            print(type(each.text))
            string = each.text.decode("utf-8")
            self.add_comment(string)

        client.quit()

    def fetch_and_update_comments(self, item):
        url = "http://club.jd.com/productpage/p-{}-s-0-t-3-p-0.html".format(item)
        tmp = json.loads(requests.get(url).text)
        for each in tmp["comments"]:
            #print(each["content"])
            self.add_comment(each["content"])

    def __generate_str(self):
        res = ""
        for idx in range(len(self.__data)):
            res += "{}.{}\n\n".format(idx + 1, self.__data[idx])
        return res

    def __create_widgets(self):
        self.__label = Label(self, textvariable=self.__text_variable, width=50, height=10, wraplength=300, justify="left")

    def __place_widgets(self):
        self.__label.grid(row=0, column=0, sticky="w")