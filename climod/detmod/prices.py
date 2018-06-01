from tkinter.ttk import *
from selenium import webdriver

# 平台价格展示区域，为一个表状
class PricesTable(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__table = None # 价格表，四列，分别为编号、电商平台名、价格区间、链接
        self.__data = []
        self.__client = None

        self.__create_widgets()
        self.__place_widgets()

    # 给定平台、价格及链接，向表中添加一项价格
    def add_price(self, platform, price, link):
        self.__data += [[platform, price, link]]

        self.__init_table()

        num_rows = len(self.__data)
        for idx in range(num_rows):
            self.__table.insert("", "end", values=(str(idx + 1), self.__data[idx][0], self.__data[idx][1], self.__data[idx][2]))
        self.__place_widgets()

    # 清空表的所有内容
    def clear_table(self):
        self.__data = []
        self.__init_table()
        self.__place_widgets()

    def __init_table(self):
        if self.__table is not None:
            self.__table.grid_forget()

        num_rows = len(self.__data)
        self.__table = Treeview(self, show="headings", columns=("a", "b", "c", "d"), height=num_rows)

        for x in ["a", "b", "c"]:
            self.__table.column(x, anchor="center")

        self.__table.column("a", width=20, stretch=False)
        self.__table.column("b", width=70, stretch=False)
        self.__table.column("c", width=140, stretch=False)

        self.__table.heading("a", text="#")
        self.__table.heading("b", text="平台")
        self.__table.heading("c", text="价格")
        self.__table.heading("d", text="链接")

        self.__table.bind("<Double-Button-1>", self.__on_click)

    def __on_click(self, event):
        item_id = event.widget.focus()
        item = event.widget.item(item_id)
        values = item['values']
        url = values[3]
        if not self.__client:
            self.__client = webdriver.Chrome()
            self.__client.get(url)
        else:
            self.__client.get(url)

    def __create_widgets(self):
        self.__init_table()

        # TODO: delete these two lines test code
        self.add_price("京东"," 500", "jd.com")
        self.add_price("淘宝", "400", "taobao.com")

    def __place_widgets(self):
        self.__table.grid(row=0, column=0, sticky="we")