from tkinter import *
from climod.globalarea import GlobalArea

class Client(Tk):
    def __init__(self, master=None):
        super().__init__(master)

if __name__ == "__main__":
    client = Client()
    client.title("Price Comparison")
    area = GlobalArea(client)
    client.mainloop()