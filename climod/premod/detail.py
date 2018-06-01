from tkinter import *

# 预览区域的详细信息展示类，尚未实现
class DetailInfo(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__details = None

        self.__create_widgets()
        self.__place_widgets()

    def __create_widgets(self):
        self.__details = Label(self, text="")

    def __place_widgets(self):
        self.__details.grid(row=0, column=0, sticky="w")