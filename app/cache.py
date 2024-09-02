import redis

class Cache:
    def __init__(self, host='localhost', port=6379):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)

    def cache_product(self, product_title: str, product_price: float):
        if self.r.exists(product_title):
            cached_price = float(self.r.get(product_title))
            if cached_price == product_price:
                return False
        self.r.set(product_title, product_price)
        return True
