from .tools import Tools

class ImageGetter:
    def __init__(self):
        pass

    @staticmethod
    def get_image(item, filename):
        url = "https://search.jd.com/search"
        payload = {"keyword": item, "enc": "utf-8"}
        resp, bs = Tools.request_data(url, payload)
        for each in bs.find_all("img", width="220", height="220"):
            try:
                img_src = each["src"]
                break
            except KeyError as _:
                pass

        img_src = img_src[2:]
        return Tools.save_image(img_src, filename)