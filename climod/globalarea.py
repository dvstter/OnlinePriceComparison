from tkinter import *
from .actualdrawingarea import ActualDrawingArea

# 全局区域类，并没有做任何实际的事，但是创建ActualDrawingArea进行UI绘制
# 该类的目标是为了后期的扩展做准备
class GlobalArea(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__area = None

        self.__create_widgets()
        self.__place_widgets()

    def __create_widgets(self):
        self.__area = ActualDrawingArea(self)

    def __place_widgets(self):
        assert self.__area is not None

        self.__area.grid(row=0, column=0)