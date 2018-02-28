from tkinter import *

class DetailInfo(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__details = None

        self.__create_widgets()
        self.__place_widgets()

    def __create_widgets(self):
        self.__details = Label(self, text="Processor: i7 2.7ghz")

    def __place_widgets(self):
        self.__details.grid(row=0, column=0, sticky="w")