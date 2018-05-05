import redis
import datetime

class Database:
    Pool = None
    Init = False

    def __init__(self, host="127.0.0.1", port=6379):
        if not type(self).Init:
            try:
                type(self).Pool = redis.BlockingConnectionPool(host=host, port=port)
                type(self).Init = True
            except redis.exceptions.ConnectionError as _:
                print("Exception: Cannot create connection pool, please check database address and port.")
                type(self).Init = False
        try:
            self.conn = redis.StrictRedis(connection_pool=type(self).Pool)
        except redis.exceptions.ConnectionError:
            print("Exception: Too many connection request, cannot get the connection.")
            self.conn = None

        self.day = datetime.date.today().day
        self.month = datetime.date.today().month

    def category_exists(self, category):
        if not self.conn:
            return None

        return self.conn.exists("category:" + category)

    def add_category(self, category, url):
        if not self.conn:
            return None
        try:
            self.conn.set("category:"+category, url)
            return True
        except Exception as _:
            return False

    def get_category_url(self, category):
        if not self.category_exists(category):
            return None

        return self.conn.get("category:"+category).decode("ascii")

    def get_all_category_names(self):
        if not self.conn:
            return None

        return [x.split(":")[1] for x in [x.decode("utf-8") for x in self.conn.keys("category:*")]]

    def item_exists(self, item):
        if not self.conn:
            return None

        return self.conn.exists("prices:"+item) and self.conn.exists("update:"+item)

    def specific_day_price_exists(self, item, month=None, day=None):
        if not self.item_exists(item):
            return None

        month = int(month) if month else self.month
        day = int(day) if day else self.day

        return "{}-{}".format(month, day) in self.get_update_time(item)

    def add_price(self, item, price, month=None, day=None):
        if not self.conn:
            return None

        try:
            price = float(price)
            month = int(month) if month else self.month
            day = int(day) if day else self.day

            self.conn.rpush("prices:"+item, price)
            self.conn.rpush("update:"+item, "{}-{}".format(month, day))
            return True
        except Exception as _:
            print("Exception: Database.add_price")
            return False

    """
    如果指定日期（若为None，则为当日）的价格已经存在就不再添加价格
    
    :param item: 货品id
    :param price: 价格
    :param month: 月份（若为None，则为当月）
    :param day: 日期（若为None，则为当日）
    
    :return None(连接错误等)/True(成功添加)/False(无法添加)
    """
    def add_price_another_day(self, item, price, month=None, day=None):
        # this line code can't be "if not self.specific...", because the function may return None
        if self.specific_day_price_exists(item, month, day) == False:
            return self.add_price(item, price, month, day)

    def get_all(self, item):
        if not self.item_exists(item):
            return None

        prices = self.get_prices(item)
        update_time = self.get_update_time(item)
        if len(prices) != len(update_time):
            raise Exception("Exception: Database corrupted!")
        else:
            return [(prices[idx], update_time[idx]) for idx in range(len(prices))]

    def get_prices(self, item):
        if self.conn:
            return [x.decode("ascii") for x in self.conn.lrange("prices:" + item, 0, -1)]
        else:
            return None

    def get_update_time(self, item):
        if self.conn:
            return [x.decode("ascii") for x in self.conn.lrange("update:" + item, 0, -1)]
        else:
            return None

    def get_all_ids(self):
        if not self.conn:
            return None

        return [x.split(":")[1] for x in [x.decode("ascii") for x in self.conn.keys("prices:*")]]

    def save_all(self):
        self.save_categories_file()
        self.save_items_file()

    def restore_all(self):
        self.restore_categories()
        self.restore_items()

    def save_categories_file(self, filename="categories.txt"):
        file = open(filename, "w", encoding="utf-8")
        for cat in self.get_all_category_names():
            url = self.get_category_url(cat)
            file.write("{}:{}\n".format(cat, url))

        file.close()

    def restore_categories(self, filename="categories.txt"):
        with open(filename, "r", encoding="utf-8") as file:
            for eachline in file.readlines():
                if ":" not in eachline:
                    continue

                tmp = eachline.strip("\n").split(":")
                cat = tmp[0]
                url = "".join(tmp[1:])
                self.add_category(cat, url)


    def save_items_file(self, filename="items.txt"):
        file = open(filename, "wt")
        for item in self.get_all_ids():
            for price, update_time in self.get_all(item):
                file.write("{}:{}:{}\n".format(item, price, update_time))

        file.close()

    def restore_items(self, filename="items.txt"):
        with open(filename, "rt") as file:
            for eachline in file.readlines():
                if ":" not in eachline:
                    continue

                item, price, update_time = eachline.strip("\n").split(":")
                month, day = update_time.split("-")
                self.add_price(item, price, month, day)
