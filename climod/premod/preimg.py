from tkinter import *
from PIL import Image, ImageTk

# 预览区域的预览图控件
class PreviewImages(Frame):
    # 预览图的大小，为类对象
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

    def __place_widgets(self):
        assert self.__img_label is not None

        self.__img_label.grid(row=0, column=0)

    # 加载一张预览图，filename为图片的存放地址
    def load(self, filename):
        image = Image.open(filename)
        image = type(self).zoom_photo(image)
        image = ImageTk.PhotoImage(image)
        self.__img_label.configure(image=image, width=type(self).IMG_WIDTH, height=type(self).IMG_HEIGHT)
        self.__img_label.image = image

    # 对图片进行等比例缩放
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