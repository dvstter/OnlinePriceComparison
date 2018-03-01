from tkinter import *
from PIL import Image, ImageTk

class ReturnButtonFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky="we")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.__image_button = None
        self.__parent = master

        self.__create_widgets()
        self.__place_widgets()

    def __click(self):
        self.__parent.end_search()

    def __init_image_button(self, filename):
        image = Image.open(filename)
        image = ImageTk.PhotoImage(image)

        if self.__image_button is not None:
            self.__image_button.grid_forget()

        self.__image_button = Button(self, image=image, command=self.__click)
        self.__image_button.image = image

        self.__image_button.bind("<Enter>", self.__mouse_callback)
        self.__image_button.bind("<Leave>", self.__mouse_callback)

    def __change_button_image(self, filename):
        image = Image.open(filename)
        image = ImageTk.PhotoImage(image)
        self.__image_button.configure(image=image)
        self.__image_button.image = image

    def __mouse_callback(self, event):
        if event.type == EventType.Enter:
            self.__change_button_image("resource/retbutton2.png")
        elif event.type == EventType.Leave:
            self.__change_button_image("resource/retbutton1.png")

    def __create_widgets(self):
        self.__init_image_button("resource/retbutton1.png")

    def __place_widgets(self):
        self.__image_button.grid(row=0, column=0, sticky="we")