from tkinter import *
from .actualdrawingarea import ActualDrawingArea

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