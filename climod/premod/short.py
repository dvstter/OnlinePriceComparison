from tkinter import *

# 预览图的简要信息展示区域，目前仅支持最低价格展示
class ShortInfo(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__price_tag = None
        self.__hot_index = None

        self.__create_widgets()
        self.__place_widgets()

    def set_lowest_price(self, price):
        self.__price_tag.configure(text="最低价格: ¥" + str(price))

    def __create_widgets(self):
        self.__price_tag = Label(self, text="最低价格: ¥3000")
        self.__hot_index = Label(self, text="搜索热度: #1")

    def __place_widgets(self):
        self.__price_tag.grid(row=0, column=0, sticky="w")
        self.__hot_index.grid(row=1, column=0, sticky="w")