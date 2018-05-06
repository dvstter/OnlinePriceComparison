from tkinter.ttk import *
from .detmod.prices import PricesTable
from .detmod.curve import PriceCurve
from .detmod.comments import Comments
from .keymod.getprices import PricesGetter

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

        self.__price_getter = PricesGetter()

        self.__create_widgets()
        self.__place_widgets()

    def update_view(self, item):
        # update price detail page
        self.__clear_prices()
        lowest_price = 100000
        skuids = None
        for platform, results, link in self.__price_getter.get_prices(item):
            print("platform: {}\nresults: {}\nlink: {}\n".format(platform, results, link))
            prices = [x[1] for x in results]
            skuids = [x[0] for x in results]
            print(prices)
            self.__add_price(platform, str(prices[0]) + "-" + str(prices[-1]), link)
            lowest_price = prices[0] if prices[0] < lowest_price else lowest_price

        # update curve detail page
        self.__curve.load(str(skuids[0]))

        return lowest_price

    def __add_price(self, platform, price, link):
        self.__prices.add_price(platform, price, link)

    def __clear_prices(self):
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