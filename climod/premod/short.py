from tkinter import *

class ShortInfo(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__price_tag = None
        self.__hot_index = None

        self.__create_widgets()
        self.__place_widgets()

    def set_lowest_price(self, price):
        self.__price_tag.configure(text="Lowest Price: ¥" + str(price))

    def __create_widgets(self):
        self.__price_tag = Label(self, text="Lowest Price: ¥3000")
        self.__hot_index = Label(self, text="Search Hot: #1")

    def __place_widgets(self):
        self.__price_tag.grid(row=0, column=0, sticky="w")
        self.__hot_index.grid(row=1, column=0, sticky="w")