from tkinter import *
from .premod.preimg import PreviewImages
from .premod.short import ShortInfo
from .premod.detail import DetailInfo
from .keymod.getimage import ImageGetter

# 预览区域类
class PreviewArea(Frame):
    IMG_PATH = "resource/preview_temp" # 预览图片下载后将被保存的文件名

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__images = None # 预览图控件
        self.__short_info = None # 简要信息展示
        self.__detail_info = None # 详细信息展示

        self.__img_getter = ImageGetter() # 图片获取器，用于从网络上获取一张预览图

        self.__create_widgets()
        self.__place_widgets()

    # 更新区域内容，首先设置最低价格，然后获取预览图并加载预览图
    def update_view(self, item, lowest_price):
        self.__set_lowest_price(lowest_price)
        res, filename = self.__img_getter.get_image(item, type(self).IMG_PATH)
        if res:
            self.__load_preview_photo(filename)
        else:
            self.__load_preview_photo(None)

    # 类内部方法，用于加载预览图
    def __load_preview_photo(self, path):
        if path:
            self.__images.load(path)
        else:
            self.__images.load("resource/test.jpg")

    # 类内部方法，用于设置最低价格
    def __set_lowest_price(self, price):
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