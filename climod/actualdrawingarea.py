from tkinter import *
from .searcharea import SearchArea
from .detailarea import DetailArea
from .previewarea import PreviewArea
from .retbutton import ReturnButtonFrame

class ActualDrawingArea(Frame):
    VISIBLE = 1
    HIDDEN = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__search = None
        self.__preview = None
        self.__detail = None
        self.__ret_button = None

        self.__search_panel_status = type(self).HIDDEN

        self.__create_widgets()
        self.__place_widgets()

    def start_search(self):
        item = self.__search.get_value()
        lowest_price = self.__detail.update_view(item)
        self.__preview.update_view(item, lowest_price)

        if not self.__search_panel_status == type(self).VISIBLE:
            self.__search_panel_status = type(self).VISIBLE
            self.__place_widgets()

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

        self.__search.grid_forget()
        self.__preview.grid_forget()
        self.__detail.grid_forget()
        self.__ret_button.grid_forget()

        self.__search.grid(row=0, column=0)

        if self.__search_panel_status == type(self).VISIBLE:
            self.__preview.grid(row=1, column=0)
            self.__detail.grid(row=2, column=0)
            self.__ret_button.grid(row=3, column=0)