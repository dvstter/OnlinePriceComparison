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

    def item_exists(self, item):
        if not self.conn:
            return None

        return self.conn.exists("prices:"+item) and self.conn.exists("update:"+item)

    def specific_day_price_exists(self, item, month, day):
        if not self.item_exists(item):
            return None

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

    def save_file(self, filename="dump.txt"):
        file = open(filename, "wt")
        for item in self.get_all_ids():
            for price, update_time in self.get_all(item):
                file.write("{}:{}:{}\n".format(item, price, update_time))

        file.close()

    def restore(self, filename="dump.txt"):
        with open(filename, "rt") as file:
            for eachline in file.readlines():
                if ":" not in eachline:
                    pass

                item, price, update_time = eachline.strip("\n").split(":")
                month, day = update_time.split("-")
                self.add_price(item, price, month, day)
