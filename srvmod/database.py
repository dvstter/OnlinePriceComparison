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

    def exists(self, item):
        if not self.conn:
            return None

        return self.conn.exists("prices:"+item)

    def add_price(self, item, price):
        if not self.conn:
            return None

        try:
            price = float(price)
            self.conn.rpush("prices:"+item, price)
            self.conn.rpush("update:"+item, "{}-{}".format(self.month, self.day))
            return True
        except Exception as _:
            print("Exception: Database.add_price")
            return False

    def get_prices(self, item):
        if not self.exists(item):
            return None

        prices = [x.decode("ascii") for x in self.conn.lrange("prices:"+item, 0, -1)]
        update_time = [x.decode("ascii") for x in self.conn.lrange("update:"+item, 0, -1)]
        if len(prices) != len(update_time):
            raise Exception("Exception: Database corrupted!")
        else:
            return [(prices[idx], update_time[idx]) for idx in range(len(prices))]