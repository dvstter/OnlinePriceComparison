from tkinter import *
from .searcharea import SearchArea
from .detailarea import DetailArea
from .previewarea import PreviewArea
from .retbutton import ReturnButtonFrame

# 实际的UI绘制类
class ActualDrawingArea(Frame):
    VISIBLE = 1
    HIDDEN = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__search = None # 搜索区域对象
        self.__preview = None # 预览区域对象
        self.__detail = None # 详细展示区域对象
        self.__ret_button = None # 返回按钮区域对象

        self.__search_panel_status = type(self).HIDDEN # 仅展示搜索区域或者全部展示，当还未开始搜索时，仅展示搜索区域

        self.__create_widgets()
        self.__place_widgets()

    # 该函数将由搜索区域的confirm控件进行调用
    def start_search(self):
        item = self.__search.get_value() # 获取搜索框的值
        lowest_price = self.__detail.update_view(item) # 先调用详细展示区域update_view函数，同时该函数会返回最低价格
        self.__preview.update_view(item, lowest_price) # 利用返回的最低价格，更新预览区域

        if not self.__search_panel_status == type(self).VISIBLE:
            self.__search_panel_status = type(self).VISIBLE
            self.__place_widgets()

    # 该区域将由返回按钮区域进行调用，用于缩回展示区域，仅展示搜索区域
    def end_search(self):
        self.__search_panel_status = type(self).HIDDEN
        self.__place_widgets()

    def __create_widgets(self):
        self.__search = SearchArea(self)
        self.__preview = PreviewArea(self)
        self.__detail = DetailArea(self)
        self.__ret_button = ReturnButtonFrame(self)

    def __place_widgets(self):
        assert self.__search is not None
        assert self.__preview is not None
        assert self.__detail is not None
        assert self.__ret_button is not None

        # 首先将所有的区域从界面上"取"下来，再重新根据状态值"安"上去
        self.__search.grid_forget()
        self.__preview.grid_forget()
        self.__detail.grid_forget()
        self.__ret_button.grid_forget()

        self.__search.grid(row=0, column=0)

        # 如果仅仅展示搜索区域，那么下面的grid()方法将得不到调用，也就无法显示
        if self.__search_panel_status == type(self).VISIBLE:
            self.__preview.grid(row=1, column=0)
            self.__detail.grid(row=2, column=0)
            self.__ret_button.grid(row=3, column=0)