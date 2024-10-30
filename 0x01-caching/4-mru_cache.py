#!/usr/bin/python3
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.usage_order = []

    def put(self, key, item):
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.usage_order.remove(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                self._evict()
            self.cache_data[key] = item

        self.usage_order.append(key)

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None
        self.usage_order.remove(key)
        self.usage_order.append(key)
        return self.cache_data[key]

    def _evict(self):
        mru_key = self.usage_order.pop()
        print(f"DISCARD: {mru_key}")
        del self.cache_data[mru_key]
