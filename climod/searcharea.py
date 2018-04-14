from tkinter import *

# 搜索区域类
class SearchArea(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky="we")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.__input = None # 输入框控件
        self.__confirm = None # 确定按钮
        self.__parent = master

        self.__create_widgets()
        self.__place_widgets()

    def search_item(self):
        self.__parent.start_search()

    def get_value(self):
        return self.__input.get()

    def clear_value(self):
        self.__input.delete(0, END)

    def __create_widgets(self):
        self.__input = Entry(self)
        self.__confirm = Button(self, text="Search", command=self.search_item)

    def __place_widgets(self):
        assert self.__input is not None
        assert self.__confirm is not None

        self.__input.grid(row=0, column=0, sticky="we")
        self.__confirm.grid(row=0, column=1)