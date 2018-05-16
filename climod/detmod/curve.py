from tkinter import *
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
from random import randint
from ..premod.preimg import PreviewImages
from ..keymod.dbs import Database

# 价格曲线展示区域，尚未实现
class PriceCurve(Frame):
    PIC_WIDTH = 250
    PIC_HEIGHT = 250

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__img_label = None
        self.__dbs = Database()
        self.__filename = "resource/curve.jpg"

        self.__create_widgets()
        self.__place_widgets()

    """
    加载已经画好的折线图
    """
    def load(self, item_id, filename=None, normal_price=None):
        if filename:
            self.__filename = filename
        days = [x.split("-")[1] for x in self.__dbs.get_update_time(item_id)] # wipe off month info
        prices = [int(float(x)) for x in self.__dbs.get_prices(item_id)]
        if not len(days) == len(prices):
            print("Exception: Database corrupted.")
            return

        if len(days) == 0:
            tmp_price = normal_price
            for newest in range(6, 10):
                #print("added price {} for {} 5-{}".format(tmp_price, item_id, newest))
                self.__dbs.add_price(item_id, tmp_price, 5, newest)
                tmp_price = normal_price if randint(0, 10) < 8 else (normal_price + (normal_price * randint(5, 10)/100))

            # refetch the data
            days = [x.split("-")[1] for x in self.__dbs.get_update_time(item_id)]
            prices = [int(float(x)) for x in self.__dbs.get_prices(item_id)]
        elif len(days) < 4:
            for newest in range(int(days[-1]) + 1, 10):
                #print("added price {} for {} 5-{}".format(prices[0], item_id, newest))
                self.__dbs.add_price(item_id, prices[0], 5, newest)

            # refetch the data
            days = [x.split("-")[1] for x in self.__dbs.get_update_time(item_id)]
            prices = [int(float(x)) for x in self.__dbs.get_prices(item_id)]

        item_prices = [(days[i], prices[i]) for i in range(len(days))]
        self.draw_curve(item_prices)

        image = Image.open(self.__filename)
        image = PreviewImages.zoom_photo(image)
        image = ImageTk.PhotoImage(image)
        self.__img_label.configure(image=image, width=type(self).PIC_WIDTH, height=type(self).PIC_HEIGHT)
        self.__img_label.image = image

    """
    利用给出的价格数据，绘制图像
    
    :param item_prices: [(day1, price1), ...]
    :filename 图片的默认存储地
    """
    def draw_curve(self, item_prices):
        x = [x[0] for x in item_prices]
        y = [x[1] for x in item_prices]

        plt.close("all")
        plt.plot(x, y, linewidth=1)
        plt.xlabel("day")
        plt.ylabel("price")
        plt.savefig(self.__filename)

    def __create_widgets(self):
        image = PhotoImage(width=type(self).PIC_WIDTH, height=type(self).PIC_HEIGHT)
        self.__img_label = Label(self, image=image)
        self.__img_label.image = image

    def __place_widgets(self):
        self.__img_label.grid(row=0, column=0)
