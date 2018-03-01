from tkinter import *
from PIL import Image, ImageTk

class PreviewImages(Frame):
    IMG_WIDTH = 250
    IMG_HEIGHT = 250

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__img_label = None

        self.__create_widgets()
        self.__place_widgets()

    def __create_widgets(self):
        image = PhotoImage(width=type(self).IMG_WIDTH, height=type(self).IMG_HEIGHT)
        self.__img_label = Label(self, image=image)
        self.__img_label.image = image
        # TODO: delete this test code
        self.load("resource/test.jpg")

    def __place_widgets(self):
        assert self.__img_label is not None

        self.__img_label.grid(row=0, column=0)

    def load(self, filename):
        image = Image.open(filename)
        image = type(self).zoom_photo(image)
        image = ImageTk.PhotoImage(image)
        self.__img_label.configure(image=image, width=type(self).IMG_WIDTH, height=type(self).IMG_HEIGHT)
        self.__img_label.image = image

    @staticmethod
    def zoom_photo(image):
        width, height = image.size
        ratio = float(width) / height
        t_width = PreviewImages.IMG_WIDTH
        t_height = PreviewImages.IMG_HEIGHT

        if width > height:
            t_height = int(t_width / ratio)
        else:
            t_width = int(t_height * ratio)

        image = image.resize((t_width, t_height), Image.ANTIALIAS)

        return image