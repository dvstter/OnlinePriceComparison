from tkinter.ttk import *
from .detmod.prices import PricesTable
from .detmod.curve import PriceCurve
from .detmod.comments import Comments
from .keymod.getprices import PricesGetter

# 详细展示区域类，用于展示所有平台的价格、价格变化曲线、评论
class DetailArea(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky="we")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.__note = Notebook(self) # 选项卡组件
        self.__prices = None # 平台价格区域
        self.__curve = None # 价格曲线区域
        self.__comments = None # 评论展示区域

        self.__price_getter = PricesGetter() # 价格获取器，用于获取所有平台名称、价格及链接

        self.__create_widgets()
        self.__place_widgets()

    # item为需要搜索价格的对象，通过该方法，更新平台价格区域
    def update_view(self, item):
        self.__clear_prices()
        lowest_price = 100000
        for platform, prices, link in self.__price_getter.get_prices(item):
            self.__add_price(platform, str(prices[0]) + "-" + str(prices[-1]), link)
            lowest_price = prices[0] if prices[0] < lowest_price else lowest_price

        return lowest_price

    # 类内部方法，用于向平台价格区域的表添加一项值
    def __add_price(self, platform, price, link):
        self.__prices.add_price(platform, price, link)

    # 类内部方法，清楚所有平台价格区域表的值
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