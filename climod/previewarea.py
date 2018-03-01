from tkinter import *
from .premod.preimg import PreviewImages
from .premod.short import ShortInfo
from .premod.detail import DetailInfo

class PreviewArea(Frame):
    IMG_WIDTH = 30
    IMG_HEIGHT = 30

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__images = None
        self.__short_info = None
        self.__detail_info = None

        self.__create_widgets()
        self.__place_widgets()

    def load_preview_photo(self, path):
        #self.__images.load(path)
        self.__images.load("resource/test.jpg")

    def set_lowest_price(self, price):
        self.__short_info.set_lowest_price(price)

    def __create_widgets(self):
        self.__images = PreviewImages(self)
        self.__short_info = ShortInfo(self)
        self.__detail_info = DetailInfo(self)

    def __place_widgets(self):
        assert self.__images is not None
        assert self.__short_info is not None
        assert self.__detail_info is not None

        self.__images.grid(row=0, column=0, rowspan=2)
        self.__short_info.grid(row=0, column=1)
        self.__detail_info.grid(row=1, column=1)