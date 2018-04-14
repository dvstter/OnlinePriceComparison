from tkinter import *

# 价格曲线展示区域，尚未实现
class PriceCurve(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__image = None

        self.__create_widgets()
        self.__place_widgets()

    def __create_widgets(self):
        pass

    def __place_widgets(self):
        pass
