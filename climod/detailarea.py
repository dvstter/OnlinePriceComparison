from tkinter.ttk import *
from .detmod.prices import PricesTable
from .detmod.curve import PriceCurve
from .detmod.comments import Comments

class DetailArea(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky="we")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.__note = Notebook(self)
        self.__prices = None
        self.__curve = None
        self.__comments = None

        self.__create_widgets()
        self.__place_widgets()

    def add_price(self, platform, price, link):
        self.__prices.add_price(platform, price, link)

    def clear_prices(self):
        self.__prices.clear_table()

    def __create_widgets(self):
        self.__note = Notebook(self)
        self.__prices = PricesTable(self)
        self.__note.add(self.__prices, text="Prices")

        self.__curve = PriceCurve(self)
        self.__note.add(self.__curve, text="Curve")

        self.__comments = Comments(self)
        self.__note.add(self.__comments, text="Comments")

    def __place_widgets(self):
        assert self.__note is not None
        assert self.__prices is not None
        assert self.__curve is not None
        assert self.__comments is not None

        self.__note.grid(row=0, column=0, sticky="we")